# Sitebulb Audit Brief (Public Template)
**Project:** ORGANIZATION_NAME – PROPERTY_NAME  
**Owner:** SEO Lead  
**Last reviewed:** YYYY-MM-DD  
**Environments:** Staging/UAT → Production  
**Related docs:** /audits/technical-audit-template.md • /qa/prelaunch-SEO-smoke-test.md • /governance/change-management-SOP.md

> Purpose: Define a reproducible Sitebulb crawl that is safe (privacy-first), scoped (no crawl traps), and comparable over time. Replace ALL_CAPS placeholders before use.

---

## 1) Scope & Objectives
- **Primary goals:** Indexation health, canonical consistency, redirect integrity, CWV risk indicators, structured data validity, accessibility intersections.
- **In scope:** PUBLIC_SECTIONS (e.g., `/programs/`, `/benefits/`, `/news/`)
- **Out of scope:** AUTH_PORTALS, admin paths, search endpoints, infinite calendars, file archives unless explicitly requested.

**KPIs to inform:** `/data/kpi-definitions.md` → Index Coverage Valid, Redirect Integrity, Canonical Consistency, A11y pass (SEO-relevant).

---

## 2) Target & Entry Points
- **Start URL(s):**  
  - `https://WWW.EXAMPLE.GOV/`  
  - `https://WWW.EXAMPLE.GOV/SECTION/`
- **Host allowlist:** `WWW.EXAMPLE.GOV` (add subdomains only if required)
- **Protocol:** `https` only

---

## 3) Authentication & Consent
- **Authentication:** None for public audit. If staging/UAT requires login, use **test credentials** approved by Security (do not commit credentials).
- **Consent/CMP:** Capture baseline in browser session; if Consent Mode blocks critical resources, run **two profiles** (consented vs denied) and document differences.

---

## 4) Rendering & Browser
- **JavaScript Rendering:** **Enabled** (Chromium), default device: **Desktop**  
- **User-Agent:** Sitebulb default OR custom: `SitebulbAudit/XX (+PUBLIC-CONTACT-EMAIL)`  
- **Viewport:** 1366×768 (default)  
- **Robots handling:** Respect `robots.txt` and meta robots

---

## 5) Crawl Limits & Safety
- **Max URLs:** 50,000 (adjust per property size)  
- **Max Depth:** 0 (unlimited) or set to LIMIT if needed  
- **Rate limits:** Polite crawl; throttle to avoid server impact  
- **Query parameters:** **Allowlist only** – `utm_source|utm_medium|utm_campaign|utm_content|utm_term`  
- **Disallowed patterns:**  
  - `/ADMIN_PATH/`  
  - `/INTERNAL_TOOLS/`  
  - `/?search=` or `/search?` (server-side searches)  
  - Infinite calendars: `/calendar?month=`  
  - Session/tokens: `?token=`, `?session=`

---

## 6) Sitemaps & Seeds
- **Sitemap sources:**  
  - `https://WWW.EXAMPLE.GOV/sitemap.xml`  
  - Include sitemap indexes and child sitemaps  
- **Include-only mode:** Optional for “sitemap coverage” audits—crawl only URLs from sitemaps + hub seeds to compare indexability and response codes.

---

## 7) Extraction & Custom Checks
**Custom Extraction (Examples):**
- **Canonical tag**: `<link rel="canonical" href="(.*?)">` → `canonical_url`
- **Hreflang**: `<link rel="alternate" hreflang="(.*?)" href="(.*?)">` → `hreflang`
- **Meta robots**: `<meta[^>]+name=["']robots["'][^>]+content=["'](.*?)["']` → `meta_robots`
- **Schema presence**: `"@type":"(Article|FAQPage|WebPage)"` in JSON-LD → `schema_type`

**Custom Checks (flag if):**
- Canonical ≠ final resolved URL  
- Multiple canonicals present  
- Meta robots contains `noindex` on pages expected to be indexable  
- 3XX chains > 1 hop  
- HTML size > 2 MB (render risk)  
- Title/H1 missing or duplicate within same directory

> Save your extraction templates within Sitebulb project and export config JSON to `/tooling/sitebulb/exports/` (gitignore if sensitive).

---

## 8) Performance & CWV Signals (Directional)
- **Lab signals**: Use Sitebulb’s performance hints (not a substitute for field data)  
- Flag heavy images (`>300KB` above the fold) and late-loading fonts  
- Note render-blocking resources count and transfer sizes

For field data: see CrUX/RUM processes; do not infer pass/fail solely from lab.

---

## 9) Accessibility Intersections (Quick)
- Presence of **single H1** and logical H2–H3 hierarchy  
- Link text clarity (avoid “click here”)  
- Alt attributes for meaningful images  
- Color contrast warnings (where reported)

> Full A11y testing remains with axe/Lighthouse or dedicated tooling.

---

## 10) Deliverables
- **Crawl file** (`.sitebulb`) stored outside repo; share via internal drive.  
- **Exports** (CSV):  
  - `pages-all.csv` (URL, status, depth, title, H1, canonical, meta robots)  
  - `redirects.csv` (source, hop count, final)  
  - `duplicates.csv` (near-duplicate groups)  
  - `hreflang.csv` (if extracted)  
  - `issues-summary.csv` (issue → count)

- **Audit deck or write-up** maps findings → `/audits/technical-audit-template.md` sections.  
- **Remediation CSVs** suitable for handoff:
  - `/tech-seo/redirect-map-template.csv` (proposed)
  - `/tech-seo/hreflang-mapping-template.csv` (proposed)
  - Canonical fix list (URL → recommended canonical)

---

## 11) Evidence & Reproducibility
- **Version the config**: export Sitebulb configuration JSON with date stamp to `/tooling/sitebulb/exports/CONFIG_YYYYMMDD.json` (sanitize if needed).  
- **Note environment**: staging vs prod, consent state, auth.  
- **Record seeds & limits**: include start URLs, URL cap, and param rules in the audit report.  
- **Baseline comparisons**: keep the same settings across audits to trend deltas.

---

## 12) Quality Guardrails (Pre-run)
- [ ] Confirm `robots.txt` and environment controls  
- [ ] Param allowlist active; risky params blocked  
- [ ] Start URLs resolve **200** and are indexable  
- [ ] Throttle set; off-hours run if required by IT  
- [ ] Sitemaps reachable and valid

**Post-run sanity:**
- [ ] URL count within expected range (±10%) vs previous run  
- [ ] No mass 500s or 403s (else re-run with IT)  
- [ ] Sample canonical/final URL consistency validated  
- [ ] Exported CSV row counts match Sitebulb totals

---

## 13) Hand-off & Change Management
- Convert confirmed issues → `/templates/ticket-template.md` items with owners/ETAs.  
- For redirect/canonical/robots changes, follow `/governance/change-management-SOP.md`.  
- Attach crawl exports and screenshots as **evidence** in tickets.  
- Schedule re-crawl after fixes; compare against baseline.

---

## 14) Appendix: Recommended Settings (Quick Reference)
- **Crawler:** Chrome Crawler, JS rendering **ON**  
- **Robots:** Respect robots & meta robots  
- **Speed:** Concurrent connections modest (e.g., 2–5), delay 250–500ms  
- **Limits:** Max URLs 50k (tune), Depth unlimited (or 6–10 for smoke tests)  
- **Canonicalization:** Extract canonicals; report mismatches  
- **Parameters:** Allowlist `utm_*`; block others  
- **Sitemaps:** Import and validate; include-only mode for coverage audits  
- **Exports:** CSV with UTF-8 encoding

---

## 15) Changelog
- **YYYY-MM-DD:** Initial public template created by YOUR_NAME.
