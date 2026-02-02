# Ticket: SEO / Web Change Request

**Title:** SHORT_SUMMARY_OF_CHANGE  
**Type:** Technical SEO | Content | Navigation | Analytics | Accessibility | Other  
**Priority:** P1 | P2 | P3  
**Owner:** NAME/TEAM  
**Ticket ID(s):** JIRA-#### (and related)  
**Date Opened:** YYYY-MM-DD  
**Target Release Window:** YYYY-MM-DD (change window if applicable)

---

## 1) Summary
One-paragraph description of the change and why it’s needed (business/user value).

**Goal / Hypothesis**  
If we DO_THIS, THEN KPI_X will improve by Y% within N weeks for AUDIENCE/SECTION.

**Scope (in/out)**
- In: WHAT’S CHANGING (templates, rules, components)
- Out: WHAT’S NOT CHANGING (explicitly list to avoid scope creep)

---

## 2) Impacted Surface
- **URLs / Templates:** LIST (attach CSV if large)
- **Systems / Files:** robots.txt, sitemap(s), canonical rules, redirects, head tags, nav, CMS component, etc.
- **Environments:** Dev → Staging/UAT → Production

---

## 3) Requirements (Acceptance Criteria)
- [ ] Functional behavior described (what user/Google should see)
- [ ] HTTP **200** on destinations; no unintended **4xx/5xx**
- [ ] **Canonical** tags align with `/tech-seo/canonicalization-matrix.md`
- [ ] **Redirects**: one hop; correct 301/302 per justification
- [ ] **Robots/meta** directives correct for environment
- [ ] **Schema.org** valid (if in scope)
- [ ] **Analytics**: events fire once; no PII; mapped per `/analytics-implementation.md`
- [ ] **Accessibility**: WCAG 2.2 AA critical checks pass
- [ ] **Performance**: no regressions on key templates (CWV risk noted)

---

## 4) Non-Goals / Constraints
- What this work intentionally does **not** cover.
- Tech, legal, branding, or scheduling constraints.

---

## 5) Dependencies
- Teams: Dev, SEO, A11y, Legal, Security, Analytics, Content
- Tickets/PRs this depends on:
- Feature flags / config gates:
- Edge/CDN rules (if any):

---

## 6) Risk & Mitigation
| Risk | Likelihood | Impact | Mitigation / Rollback |
|---|---|---:|---|
| Example: redirect chain | Low | Medium | Validate with audit; keep rollback rule ready |
| Example: noindex drift | Low | High | Smoke test on staging; monitor post-deploy |

---

## 7) Test Plan (Staging/UAT)
**Test Data / URLs:** link to test set(s)  
**Steps:**  
1. …  
2. …  
3. …

**Evidence to Attach:**  
- Screenshots of page/head tags, dataLayer, DebugView  
- Crawler extracts (small sample)  
- `curl -I` or script output for redirects  
- Lighthouse/axe results (if applicable)

Use checklists:
- `/qa/prelaunch-SEO-smoke-test.md`
- `/qa/release-QA-checklist.md`

---

## 8) Rollout Plan (Production)
- **Change window:** DATE/TIME + timezone
- **Steps:** deploy order, cache purge, feature flag toggles
- **Rollback plan:** exact steps + artifacts to restore
- **Comms:** who is notified before/after

---

## 9) Monitoring (24–72h Post-Deploy)
- **Technical:** 3xx/4xx/5xx rates, error logs, console errors
- **SEO:** index coverage anomalies, sitemap status, redirect errors in GSC
- **Analytics:** realtime sanity, event counts, duplicates, BigQuery export rows
- **CWV/Perf:** watch LCP/INP/CLS on affected templates

---

## 10) Approvals
- SEO Lead: NAME / DATE  
- Dev Lead: NAME / DATE  
- Accessibility Lead: NAME / DATE  
- Legal/Security (if required): NAME / DATE  
- Product/PM: NAME / DATE

---

## 11) Artifacts & Links
- PR(s): URL
- Branch/Commit: HASH
- Crawler export (sanitized): PATH
- Redirect map (if applicable): `/tech-seo/redirect-map-template.csv`
- Hreflang map (if applicable): `/tech-seo/hreflang-mapping-template.csv`
- Related docs: `/governance/change-management-SOP.md`, `/analytics-implementation.md`, `/data/kpi-definitions.md`

---

## 12) Changelog (Ticket)
- **YYYY-MM-DD:** Created.
- **YYYY-MM-DD:** Updated scope to include X; added mitigation Y.
- **YYYY-MM-DD:** Approved for release window.
