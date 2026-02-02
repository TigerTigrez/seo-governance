# Redirect Audit – Template
**Property:** EXAMPLE.GOV  
**Date:** YYYY-MM-DD  
**Owner:** YOUR_NAME  
**Environments:** Staging/UAT → Production  
**Related Docs:** /tech-seo/redirect-map-template.csv • /governance/change-management-SOP.md • /qa/release-QA-checklist.md

> Purpose: verify that all redirects are necessary, correct, performant, privacy-safe, and aligned with canonicalization and analytics policies. Replace ALL_CAPS placeholders.

---

## 1) Scope & Objectives
- **Scope:** Legacy → new URL migrations, domain/platform moves, canonical/normalization rules (HTTP→HTTPS, slash, case), temporary campaigns, and deprecations.
- **Objectives:**
  - Ensure **one-hop** redirects (no chains/loops).
  - Use correct status codes (**301** permanent, **302/307** temporary).
  - Preserve query parameters **only when required** by policy; otherwise strip/normalize.
  - Confirm destination returns **200**, is **indexable**, and matches canonical rules.
  - Validate analytics and consent behavior are unaffected.

---

## 2) Inputs
- **Redirect map** (authoritative): `/tech-seo/redirect-map-template.csv`  
  Columns: `source_url,target_url,redirect_type,justification,ticket_id`
- **Inventory sources:** legacy sitemaps, top landing pages, logs (anonymized), internal link exports.
- **Normalization policy:** `/tech-seo/canonicalization-matrix.md`

---

## 3) Acceptance Criteria
- No redirect **chains** (>1 hop) or **loops**.
- Redirect type matches justification (perm vs temp).
- Destinations resolve **200** within **<500ms TTFB** (staging target; prod may vary).
- **UTM allowlist** only; all other params dropped (see analytics guide §12).
- **Case** and **trailing slash** behavior consistent with policy.
- **Internationalization:** hreflang/alt-lang variants resolve to correct locale rules.
- **Robots/noindex:** redirects do **not** land on non-indexable pages (unless by design).
- **Security:** No open-redirect patterns; no leakage of tokens.

---

## 4) Methodology

### 4.1 Sample Design
Create test sets:
- **Top traffic legacy URLs** (N=500–5,000 depending on size)
- **All mapped redirects** from CSV (authoritative list)
- **Normalization cases:** uppercase, trailing slash, mixed params, fragment `#`, etc.
- **Edge cases:** 404s, non-ASCII paths, long URLs, query param permutations.

### 4.2 Test Execution
Use any combination of:
- **Bash (portable)**
```bash
# Check status & location for each source (expects CSV w/header)
tail -n +2 tech-seo/redirect-map-template.csv | while IFS=, read -r src dst type just ticket; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -I "$src")
  loc=$(curl -s -I "$src" | awk -F': ' '/^Location:/ {print $2}' | tr -d '\r')
  echo "$src,$code,$loc"
done
```
### 4.3 Powershell (Windows-friendly)
```powershell
Import-Csv "tech-seo/redirect-map-template.csv" | ForEach-Object {
  try {
    $resp = Invoke-WebRequest -Uri $_.source_url -MaximumRedirection 0 -ErrorAction Stop
    "$($_.source_url),$($resp.StatusCode),"
  } catch {
    $r = $_.Exception.Response
    if ($r) { "$($_.source_url),$($r.StatusCode.value__),$($r.Headers['Location'])" }
    else { "$($_.source_url),ERROR,$($_.Exception.Message)" }
  }
}
```
### 4.4 Chain Detection
```bash
curl -sILk "$URL" | awk '/^HTTP/{print $2} /^Location:/{print "->",$2}'
