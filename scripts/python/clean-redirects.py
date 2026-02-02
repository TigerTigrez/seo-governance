#!/usr/bin/env python3
"""
clean-redirects.py
------------------
Utility to sanitize and normalize a redirect map CSV before deploying rules.

INPUT CSV (header required):
    source_url,target_url,redirect_type,justification,ticket_id

FEATURES
- Validates and normalizes URLs (lowercase host, strip fragments, param allowlist).
- Optional trailing-slash enforcement (add|remove|keep).
- Optional lowercase-path enforcement.
- Drops self-redirects (source == target after normalization).
- Dedupe by source_url (keeps the last occurrence or first, configurable).
- Verifies redirect_type ∈ {301,302,307} (configurable allowlist).
- Writes a cleaned CSV and a summary report to stdout.
- (Optional) Live status check (HEAD, no follow) if --check-status is set and 'requests' is installed.

USAGE
    python scripts/python/clean-redirects.py \
        --in tech-seo/redirect-map-template.csv \
        --out tech-seo/redirect-map-clean.csv \
        --param-allowlist utm_source utm_medium utm_campaign utm_content utm_term \
        --enforce-trailing-slash keep \
        --lowercase-host \
        --lowercase-path \
        --dedupe-strategy last

    # With a stricter policy:
    python scripts/python/clean-redirects.py --in redirects.csv --out redirects.clean.csv \
        --param-allowlist utm_source utm_medium utm_campaign \
        --enforce-trailing-slash add --lowercase-host --lowercase-path

    # (Optional) spot-check HTTP codes (slow; requires 'requests')
    python scripts/python/clean-redirects.py --in redirects.csv --out redirects.clean.csv --check-status --check-sample 50

NOTES
- This script does NOT make network calls unless --check-status is provided.
- Keep real hosts/paths out of public repos if they’re sensitive.
"""

from __future__ import annotations

import argparse
import csv
import sys
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

# -----------------------------
# Utilities
# -----------------------------

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

@dataclass
class NormPolicy:
    param_allowlist: List[str] = field(default_factory=list)
    enforce_trailing_slash: str = "keep"  # add|remove|keep
    lowercase_host: bool = True
    lowercase_path: bool = False
    allowed_redirect_types: Tuple[str, ...] = ("301", "302", "307")

def normalize_url(raw: str, policy: NormPolicy) -> Tuple[Optional[str], List[str]]:
    """
    Normalize a URL per policy. Returns (normalized_url, issues[])
    On parse/validation failure, returns (None, issues)
    """
    issues: List[str] = []
    raw = (raw or "").strip()
    if not raw:
        issues.append("empty")
        return None, issues

    try:
        p = urlparse(raw)
    except Exception as ex:
        issues.append(f"unparseable:{ex}")
        return None, issues

    if not p.scheme or not p.netloc:
        issues.append("missing_scheme_or_host")
        return None, issues

    scheme = p.scheme.lower()
    host = p.netloc
    if policy.lowercase_host:
        host = host.lower()

    # Normalize path
    path = p.path or "/"
    if policy.lowercase_path:
        path = path.lower()

    # Trailing slash handling
    if policy.enforce_trailing_slash == "add":
        if not path.endswith("/"):
            path = path + "/"
    elif policy.enforce_trailing_slash == "remove":
        if path != "/" and path.endswith("/"):
            path = path.rstrip("/")
            if path == "":
                path = "/"
    # else keep

    # Strip fragment
    fragment = ""

    # Query param allowlist
    query_items = parse_qsl(p.query, keep_blank_values=False)
    if policy.param_allowlist:
        allow = set(policy.param_allowlist)
        filtered = [(k, v) for (k, v) in query_items if k in allow]
        if len(filtered) != len(query_items):
            issues.append("dropped_params")
        query_items = filtered

    # Ensure deterministic param order
    query_items.sort(key=lambda kv: kv[0])
    query = urlencode(query_items, doseq=True)

    normalized = urlunparse((scheme, host, path, "", query, fragment))
    return normalized, issues

@dataclass
class Row:
    source_url: str
    target_url: str
    redirect_type: str
    justification: str
    ticket_id: str
    # bookkeeping
    source_issues: List[str] = field(default_factory=list)
    target_issues: List[str] = field(default_factory=list)
    row_issues: List[str] = field(default_factory=list)

    @classmethod
    def from_csv(cls, row: Dict[str, str]) -> "Row":
        return cls(
            source_url=row.get("source_url", "").strip(),
            target_url=row.get("target_url", "").strip(),
            redirect_type=row.get("redirect_type", "").strip(),
            justification=row.get("justification", "").strip(),
            ticket_id=row.get("ticket_id", "").strip(),
        )

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Clean/normalize a redirect map CSV.")
    ap.add_argument("--in", dest="inp", required=True, help="Input CSV path.")
    ap.add_argument("--out", dest="outp", required=True, help="Output cleaned CSV path.")
    ap.add_argument("--param-allowlist", nargs="*", default=["utm_source","utm_medium","utm_campaign","utm_content","utm_term"],
                    help="Allowed query parameters to keep. Others are dropped.")
    ap.add_argument("--enforce-trailing-slash", choices=["add", "remove", "keep"], default="keep",
                    help="How to normalize trailing slashes.")
    ap.add_argument("--lowercase-host", action="store_true", default=True, help="Lowercase host (default on).")
    ap.add_argument("--no-lowercase-host", dest="lowercase_host", action="store_false")
    ap.add_argument("--lowercase-path", action="store_true", default=False, help="Lowercase path.")
    ap.add_argument("--dedupe-strategy", choices=["first", "last"], default="last",
                    help="If multiple rows share the same normalized source_url, keep the first or last occurrence.")
    ap.add_argument("--allow-redirect-types", nargs="*", default=["301","302","307"],
                    help="Allowed redirect types.")
    ap.add_argument("--check-status", action="store_true",
                    help="(Optional) HEAD-check sources to capture HTTP status and Location (no follow). Requires 'requests'.")
    ap.add_argument("--check-sample", type=int, default=0,
                    help="If --check-status is set, limit to N sampled rows (0 = all).")
    return ap.parse_args(argv)

def try_status_check(url: str) -> Tuple[Optional[int], Optional[str], Optional[str]]:
    """
    Optional network check using requests (if available).
    Returns (status_code, location_header, error_message)
    """
    try:
        import requests  # type: ignore
    except Exception:
        return None, None, "requests_not_installed"

    try:
        resp = requests.head(url, allow_redirects=False, timeout=6)
        loc = resp.headers.get("Location")
        return resp.status_code, loc, None
    except Exception as ex:
        return None, None, f"req_error:{ex}"

def main():
    args = parse_args()

    policy = NormPolicy(
        param_allowlist=args.param_allowlist,
        enforce_trailing_slash=args.enforce_trailing_slash,
        lowercase_host=args.lowercase_host,
        lowercase_path=args.lowercase_path,
        allowed_redirect_types=tuple(args.allow_redirect_types),
    )

    required_headers = ["source_url","target_url","redirect_type","justification","ticket_id"]

    rows: List[Row] = []
    with open(args.inp, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        headers = [h.strip() for h in rdr.fieldnames or []]
        missing = [h for h in required_headers if h not in headers]
        if missing:
            eprint(f"[ERROR] Missing required columns: {', '.join(missing)}")
            sys.exit(2)
        for raw in rdr:
            rows.append(Row.from_csv(raw))

    cleaned: Dict[str, Row] = {}  # key by normalized source
    stats = {
        "total_input": len(rows),
        "invalid_source": 0,
        "invalid_target": 0,
        "self_redirects": 0,
        "bad_type": 0,
        "deduped": 0,
        "kept": 0,
        "dropped_empty": 0,
        "dropped_other": 0,
    }

    for idx, r in enumerate(rows, start=1):
        src_norm, src_issues = normalize_url(r.source_url, policy)
        tgt_norm, tgt_issues = normalize_url(r.target_url, policy)

        if src_norm is None:
            r.row_issues.append("drop:invalid_source")
            stats["invalid_source"] += 1
            continue
        if tgt_norm is None:
            r.row_issues.append("drop:invalid_target")
            stats["invalid_target"] += 1
            continue

        r.source_issues = src_issues
        r.target_issues = tgt_issues

        # Validate redirect_type
        if r.redirect_type not in policy.allowed_redirect_types:
            r.row_issues.append(f"fix:redirect_type:{r.redirect_type}")
            stats["bad_type"] += 1
            # Default fix: coerce anything unknown to 301
            r.redirect_type = "301"

        # Drop self-redirects
        if src_norm == tgt_norm:
            r.row_issues.append("drop:self_redirect")
            stats["self_redirects"] += 1
            continue

        # Reassign normalized URLs back
        r.source_url = src_norm
        r.target_url = tgt_norm

        key = src_norm
        if key in cleaned:
            stats["deduped"] += 1
            if args.dedupe_strategy == "last":
                cleaned[key] = r
            # if "first", keep existing; do nothing
        else:
            cleaned[key] = r

    # Optional status check
    if args.check_status:
        to_check = list(cleaned.values())
        if args.check_sample and args.check_sample > 0:
            to_check = to_check[: args.check_sample]

        eprint(f"[INFO] Performing HEAD checks on {len(to_check)} source URLs (no follow)...")
        for r in to_check:
            code, loc, err = try_status_check(r.source_url)
            if err:
                r.row_issues.append(err)
            else:
                # Attach a hint; no mutation to target
                r.row_issues.append(f"head:{code}")
                if loc:
                    r.row_issues.append(f"location:{loc}")

    # Write cleaned CSV
    out_headers = required_headers + ["notes"]
    with open(args.outp, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(out_headers)
        for r in cleaned.values():
            notes = []
            if r.source_issues:
                notes.append("src:" + "|".join(r.source_issues))
            if r.target_issues:
                notes.append("tgt:" + "|".join(r.target_issues))
            if r.row_issues:
                notes.append("row:" + "|".join(r.row_issues))
            w.writerow([r.source_url, r.target_url, r.redirect_type, r.justification, r.ticket_id, "; ".join(notes)])
            stats["kept"] += 1

    # Report
    print("\n=== clean-redirects.py report ===")
    print(f"Input rows        : {stats['total_input']}")
    print(f"Kept (cleaned)    : {stats['kept']}")
    print(f"Deduped           : {stats['deduped']}  (strategy: {args.dedupe_strategy})")
    print(f"Dropped invalid src : {stats['invalid_source']}")
    print(f"Dropped invalid tgt : {stats['invalid_target']}")
    print(f"Dropped self-redirects: {stats['self_redirects']}")
    print(f"Coerced redirect type : {stats['bad_type']} → defaulted to 301")
    print(f"Param allowlist   : {', '.join(policy.param_allowlist) if policy.param_allowlist else 'NONE'}")
    print(f"Trailing slash    : {policy.enforce_trailing_slash}")
    print(f"Lowercase host    : {policy.lowercase_host}")
    print(f"Lowercase path    : {policy.lowercase_path}")
    if args.check_status:
        print(f"HEAD check sample : {args.check_sample or 'all kept rows'} (see 'row:head:CODE' notes in output CSV)")
    print(f"Output CSV        : {args.outp}")
    print("================================\n")

if __name__ == "__main__":
    main()
