# KPI Definitions (Public Template)
**Applies to:** ORGANIZATION_NAME web properties  
**Owner:** Analytics Lead • SEO Lead  
**Last reviewed:** YYYY-MM-DD

> This document standardizes SEO KPIs, their formulas, data sources, attribution windows, and data hygiene rules. Replace ALL_CAPS placeholders and adjust to your stack.

---

## 0) Governance & Guardrails
- **No PII**: KPIs must not rely on email, names, or raw user identifiers.
- **Environment isolation**: TEST/UAT data is excluded from production KPIs.
- **Attribution clarity**: Each KPI lists its attribution model/window.
- **Single source of truth**: Define a primary source (GA4, BigQuery, GSC, etc.).
- **Sampling**: Note where tools sample/estimate (e.g., GSC, GA4).
- **Timezone**: Report in ORG_TIMEZONE unless stated otherwise.

---

## 1) Traffic & Engagement

### 1.1 Organic Sessions
- **Definition**: Visits where default channel grouping = Organic Search.
- **Formula**: Count of sessions with `channel_group = "Organic Search"`.
- **Source**: GA4 (explorer/api) or BigQuery export.
- **Attribution**: Session-based; last non-direct click within session.
- **Notes**: Exclude internal IP ranges; exclude test hosts.

### 1.2 Organic Users
- **Definition**: Distinct users who had at least one Organic Search session.
- **Formula**: Count distinct `user_pseudo_id` (GA4 BQ) with Organic session.
- **Source**: GA4 BQ.
- **Caveats**: Device/browser resets impact deduplication.

### 1.3 Entrances from Organic (Landing Pages)
- **Definition**: Sessions that began on a given page from Organic.
- **Formula**: Count of sessions where first page path = X and channel = Organic.
- **Source**: GA4 BQ; Landing Page dimension in UI.
- **Use**: Prioritize high-impact templates and hub pages.

### 1.4 Engagement Rate (Organic)
- **Definition**: GA4 engaged sessions / total sessions (Organic only).
- **Formula**: `engaged_sessions / sessions` with channel = Organic.
- **Source**: GA4.
- **Threshold**: Org-specific baseline (e.g., ≥ 55% sitewide).

### 1.5 Organic Conversions (Proxy)
- **Definition**: Count of SEO-relevant conversion events (non-PII).
- **Formula**: Sum of events in allowlist (e.g., `form_submit_success`, `download`).
- **Source**: GA4 / BQ.
- **Attribution**: Last non-direct within `X` days (e.g., 30-day).
- **Notes**: Document event IDs in `/data/event-catalog.csv`.

---

## 2) Visibility & Coverage

### 2.1 Impressions (Search Console)
- **Definition**: SERP load events where the property’s URL was eligible.
- **Formula**: Sum `impressions` over date range.
- **Source**: GSC Performance report / API.
- **Caveats**: Aggregation & anonymization may suppress low-volume queries.

### 2.2 Clicks (Search Console)
- **Definition**: User clicks from Google SERPs to site.
- **Formula**: Sum `clicks`.
- **Source**: GSC.
- **Notes**: Discrepancies vs GA4 due to consent, blocking, and filters.

### 2.3 CTR (Search Console)
- **Definition**: Click-through rate from impressions to clicks.
- **Formula**: `clicks / impressions`.
- **Source**: GSC.
- **Usage**: Diagnose title/meta or SERP feature competition.

### 2.4 Average Position (Directional)
- **Definition**: Mean ranking position across impressions.
- **Formula**: `sum(position * impressions) / sum(impressions)`.
- **Source**: GSC.
- **Caveats**: Use directionally; blended by query/device/locale.

### 2.5 Index Coverage – Valid URLs
- **Definition**: Count of URLs with status “Valid” (Indexable & Indexed).
- **Source**: GSC Indexing / API; sitemap reconciliation.
- **Target**: ≥ 95% of sitemap URLs valid (template-level thresholds).

---

## 3) Technical Health

### 3.1 Core Web Vitals – LCP
- **Definition**: Share of pageviews passing Largest Contentful Paint threshold.
- **Formula**: `% of pageviews with LCP ≤ 2.5s (CrUX/field)`.
- **Source**: CrUX (Page-level if available), RUM, or Lighthouse CI (lab for prelaunch).
- **Target**: ≥ 75th percentile passing.

### 3.2 Core Web Vitals – INP
- **Definition**: Share with Interaction to Next Paint ≤ 200ms (or current standard).
- **Source**: CrUX / RUM.
- **Target**: ≥ 75th percentile passing.

### 3.3 Core Web Vitals – CLS
- **Definition**: Share with Cumulative Layout Shift ≤ 0.1.
- **Source**: CrUX / RUM.
- **Target**: ≥ 75th percentile passing.

### 3.4 Crawlability Errors
- **Definition**: Count/rate of 4xx/5xx on sitemap & key templates.
- **Source**: Crawler exports (Screaming Frog / Sitebulb) + server logs (redacted).
- **Threshold**: ≤ 0.5% error on sitemap; ≤ 0.1% on key templates.

### 3.5 Redirect Integrity
- **Definition**: % of mapped redirects that resolve in one hop to 200.
- **Formula**: `valid_one_hop / total_mapped`.
- **Source**: Redirect audit script; `/audits/redirect-audit-template.md`.
- **Target**: 100% for permanent migrations.

### 3.6 Canonical Consistency
- **Definition**: % of pages where declared canonical = final URL.
- **Formula**: `matches / tested`.
- **Source**: Crawler extraction and URL normalization logic.
- **Target**: ≥ 98% on canonicalized templates.

---

## 4) Content & Information Architecture

### 4.1 Content Freshness Coverage
- **Definition**: % of pages updated within policy SLA (e.g., 12 months).
- **Formula**: `pages_updated_within_SLA / total_pages_in_scope`.
- **Source**: CMS export (sanitized), sitemap `lastmod`, crawler metadata.
- **Target**: Policy-defined per section.

### 4.2 Hub Depth (Clicks to Important Content)
- **Definition**: Median internal link depth from top hubs to target pages.
- **Formula**: Graph shortest-path median.
- **Source**: Crawler link graph.
- **Target**: ≤ 3 clicks for priority pages.

### 4.3 Thin/Duplicate Content Rate
- **Definition**: % of pages flagged as thin or near-duplicate by ruleset.
- **Source**: Crawler word count thresholds, near-duplicate hashing.
- **Threshold**: ≤ X% (define per section); action plan required if exceeded.

---

## 5) Internationalization (if applicable)

### 5.1 Hreflang Validity
- **Definition**: % of URLs with valid, reciprocal hreflang clusters.
- **Formula**: `valid_clusters / total_clusters`.
- **Source**: Crawler hreflang report.
- **Target**: ≥ 98%.

### 5.2 Locale Routing Accuracy
- **Definition**: % of locale-specific sessions landing on correct locale.
- **Source**: GA4 (geo) + landing path rules; server logs (sanitized).
- **Target**: ≥ 97%.

---

## 6) Compliance & Accessibility Intersections

### 6.1 Accessibility (SEO-Relevant) Pass Rate
- **Definition**: % of sampled pages passing WCAG 2.2 AA checks that impact discoverability.
- **Source**: Axe/Lighthouse programmatic checks + manual sample.
- **Target**: ≥ 95% pass on sampled set.

### 6.2 Robots/Noindex Drift
- **Definition**: Count of unintended `noindex`/blocked URLs detected post-deploy.
- **Source**: Crawler diff vs baseline.
- **Target**: 0.

---

## 7) Governance & Delivery KPIs

### 7.1 Release QA Pass Rate
- **Definition**: % of SEO releases passing the `/qa/release-QA-checklist.md` on first attempt.
- **Formula**: `passes_first_try / total_releases`.
- **Source**: Release tickets; QA evidence.
- **Target**: ≥ 90%.

### 7.2 Incident Count (SEO-impacting)
- **Definition**: Number of Sev-1/Sev-2 incidents affecting indexability, traffic, or CWV.
- **Source**: Incident log (non-PII); change management system.
- **Target**: ≤ N per quarter.

### 7.3 SLA Compliance (Analytics)
- **Definition**: % of releases with analytics evidence attached (staging + prod).
- **Source**: Release tickets.
- **Target**: 100%.

---

## 8) KPI Table (Roll-up)

| KPI | Source of Truth | Cadence | Owner | Attribution/Window | Target/Threshold |
|---|---|---:|---|---|---|
| Organic Sessions | GA4 | Weekly/Monthly | Analytics | Session, last non-direct | ≥ Baseline + X% |
| Landing Page Entrances (Organic) | GA4 | Weekly | SEO | Session | Top N pages monitored |
| GSC Clicks/Impressions/CTR | GSC | Weekly | SEO | N/A | Directional |
| Index Coverage – Valid | GSC + Sitemap | Monthly | SEO/Dev | N/A | ≥ 95% sitemap indexed |
| CWV Pass Rate (LCP/INP/CLS) | CrUX/RUM | Monthly | Perf Eng | 75th percentile | ≥ 75% passing |
| Redirect Integrity | Audit Script | Per release | SEO/Dev | N/A | 100% one-hop |
| Canonical Consistency | Crawler | Monthly | SEO | N/A | ≥ 98% |
| Hreflang Validity | Crawler | Monthly | SEO | N/A | ≥ 98% |
| A11y Pass (SEO-relevant) | Lighthouse/Axe | Quarterly | A11y Lead | N/A | ≥ 95% |
| Release QA Pass Rate | Tickets | Monthly | SEO Lead | N/A | ≥ 90% |

---

## 9) Data Hygiene & Redaction

- **Internal traffic**: Filter by IP ranges, request headers, or cookie flags.
- **Bots/spam**: Maintain a blocklist; cross-check with server logs.
- **Param allowlist**: Keep only `utm_source|utm_medium|utm_campaign|utm_content|utm_term` in reporting URLs.
- **Host allowlist**: Only production hosts included in SEO KPIs.
- **Redaction**: Strip/hash potential PII at edge before analytics.

---

## 10) Implementation Notes (Mapping Examples)

### 10.1 GA4 → BigQuery Fields (Examples)
| KPI | GA4 UI | BigQuery (events_* fields) |
|---|---|---|
| Sessions (Organic) | Sessions (Organic) | Count distinct `session_id` where `traffic_source.medium = "organic"` |
| Users (Organic) | Users (Organic) | Count distinct `user_pseudo_id` with Organic session |
| Landing Page | Landing Page | First `page_location` per session |
| Engaged Sessions | Engaged sessions | `event_name="user_engagement"` count/session logic |

### 10.2 GSC API Fields (Examples)
| KPI | Field |
|---|---|
| Impressions | `impressions` |
| Clicks | `clicks` |
| CTR | `ctr` |
| Position | `position` |

---

## 11) Targets & Alerting (Optional)
- **Alert thresholds** (illustrative; set for your org):
  - **Index coverage valid** drops > 2% WoW → alert SEO + Dev.
  - **CWV pass rate** drops below 70% for any template → open perf ticket.
  - **4xx/5xx rate** on sitemap URLs > 0.5% daily → incident review.
  - **Redirect integrity** < 100% post-migration → block next deploy.

---

## 12) Change Log
- **YYYY-MM-DD**: Initial public template created by YOUR_NAME.
- **YYYY-MM-DD**: Added CWV INP; clarified attribution windows.

