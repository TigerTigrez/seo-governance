# Search Console – Export Fields (Public Template)
**Applies to:** ORGANIZATION_NAME web properties  
**Owner:** SEO Lead / Analytics Lead  
**Last reviewed:** YYYY-MM-DD

> This document standardizes which **fields/dimensions** to export from Search Console (GSC), how to structure CSVs, and guardrails for privacy and data quality. Replace ALL_CAPS placeholders.

---

## 1) Purpose
- Provide **consistent, mergeable** exports across teams/tools.
- Enable repeatable analysis (queries, pages, devices, countries, appearance).
- Prepare data for blending with **sitemaps**, **redirect maps**, and GA4.

---

## 2) Data Sources & Cadence
- **GSC Performance** (required): `searchType=web` (or `news`, `image`, `video` if applicable).
- **GSC Indexing** (optional): Coverage summaries to reconcile with sitemaps.
- **Cadence:** Weekly for tactical, Monthly for executive; keep **rolling 16 months** (GSC limit).

---

## 3) Privacy & Scope Guardrails
- **No PII** in exports. Queries may contain potentially sensitive strings—store in **public-safe folders only if sanitized** (see §10).
- Export **property-scoped** data that matches your reporting host(s) (e.g., `https://WWW.EXAMPLE.GOV/`).
- Use **production host only**; exclude test/stage hosts.

---

## 4) Standard Export Schemas (CSV)
Create one CSV per pivot. Recommended filenames:
- `gsc_performance_query_YYYYMM.csv`
- `gsc_performance_page_YYYYMM.csv`
- `gsc_performance_device_YYYYMM.csv`
- `gsc_performance_country_YYYYMM.csv`
- `gsc_performance_appearance_YYYYMM.csv`

### 4.1 Queries (by Date)
**File:** `gsc_performance_query_YYYYMM.csv`

### 4.2 date,query,clicks,impressions,ctr,position,site_section
- `date` (YYYY-MM-DD)
- `query` (lowercased as-is from GSC; sanitize per §10 if publishing)
- `clicks` (integer)
- `impressions` (integer)
- `ctr` (decimal, 0–1 or 0–100% — pick one and be consistent)
- `position` (decimal; average)
- `site_section` (optional; derived from page path lookup if you run a join later)

### 4.3 Pages (Landing URLs by Date)
**File:** `gsc_performance_page_YYYYMM.csv`

### 4.4 date,page,clicks,impressions,ctr,position,canonical_group,template
- `page` (absolute URL)
- `canonical_group` (optional; normalized cluster key)
- `template` (optional; e.g., HOME|HUB|ARTICLE|PRODUCT)

### 4.5 Devices (by Date)
**File:** `gsc_performance_device_YYYYMM.csv`

### 4.6 date,device,clicks,impressions,ctr,position
- `device` ∈ {desktop|mobile|tablet}

### 4.7 Countries (by Date)
**File:** `gsc_performance_country_YYYYMM.csv`

### 4.8 date,country,clicks,impressions,ctr,position
- `country` (ISO-3166 alpha-2; e.g., US, CA)

### 4.9 Search Appearance (by Date)
**File:** `gsc_performance_appearance_YYYYMM.csv`

### 5.0 date,search_appearance,clicks,impressions,ctr,position
- `search_appearance` (e.g., webLightResult, richResults, etc.; varies)

> Tip: If you need a **multi-dimension** pivot (e.g., page+query+date), export it separately:
> `gsc_performance_page_query_YYYYMM.csv` with headers:
> `date,page,query,clicks,impressions,ctr,position`.

---

## 5) Recommended API Dimension Sets
To keep row counts sane and avoid hitting caps:

- **By Query + Date:** `dimensions=[date,query]`
- **By Page + Date:** `dimensions=[date,page]`
- **By Device + Date:** `dimensions=[date,device]`
- **By Country + Date:** `dimensions=[date,country]`
- **By Appearance + Date:** `dimensions=[date,searchAppearance]`
- **Optional granular:** `dimensions=[date,page,query]` (use filters to limit to top pages)

**Common filters**
- `searchType=web`
- `dimensionFilterGroups`:
  - `page` startsWith `https://WWW.EXAMPLE.GOV/SECTION/`
  - `query` contains `KEYWORD` (for deep dives)

---

## 6) Row Limits & Pagination
- GSC API defaults to `rowLimit=1000`. Use pagination (`startRow`) to fetch all rows.
- For month exports, loop **per day** to reduce sampling/aggregation quirks:
  - Iterate `date` from first → last day; fetch all rows for that day; append.

---

## 7) Normalization Rules (so files merge cleanly)
- **Lowercase host**; keep **path case** as-is.
- Normalize trailing slash **site-wide** (match canonical policy).
- Strip URL fragments (`#...`) and **unknown params** from `page` (param allowlist: `utm_source|utm_medium|utm_campaign|utm_content|utm_term`).
- Keep `ctr` as **decimal** (e.g., 0.1234) or as **percentage** consistently; document choice in README.
- Dates in **ISO `YYYY-MM-DD`**.

---

## 8) Joining With Other Artifacts
- **Sitemaps:** Join `page` on sitemap lists to compute coverage and URL health.
- **Redirect map:** Resolve legacy → new; attribute clicks/impressions to destination where policy requires.
- **Sections/Templates:** Derive `site_section` or `template` via regex on `page` path (document in `/tech-seo/canonicalization-matrix.md`).

---

## 9) Quality Checks (each export)
- **Row count** matches API totals for the date range.
- **No NULL/blank dates**; no future dates.
- **Host check:** All URLs on approved hosts.
- **Param hygiene:** Only allowlisted params present.
- **Outliers:** Negative or >100% CTR → re-pull day; investigate.

---

## 10) Sanitization Policy (Public Repos)
- Queries can contain names/IDs. For any export stored publicly:
  - **Option A:** Hash `query` with a stable salt (documented privately).
  - **Option B:** Replace with `REDACTED` and keep aggregates only.
- Do not publish raw **page** URLs if sensitive; replace host with `https://WWW.EXAMPLE.GOV` and keep paths that are already public, or use placeholders (`/SECTION/PATH`).
- Store raw exports in `data/private/` (gitignored); publish only sanitized versions in `data/public/`.

---

## 11) Example API Body (pseudo-JSON)
```json
{
  "startDate": "YYYY-MM-01",
  "endDate": "YYYY-MM-31",
  "searchType": "web",
  "dimensions": ["date", "page"],
  "rowLimit": 25000,
  "startRow": 0,
  "dimensionFilterGroups": [{
    "filters": [{
      "dimension": "page",
      "operator": "contains",
      "expression": "/SECTION/"
    }]
  }]
}
