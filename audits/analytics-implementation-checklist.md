# Analytics Implementation Guide (Public Template)
**Applies to:** ORGANIZATION_NAME web properties  
**Owner:** Analytics Lead / SEO Lead  
**Last reviewed:** YYYY-MM-DD  
**Environments:** Dev → Staging/UAT → Production

> This document defines how we implement, govern, and validate analytics in privacy-sensitive environments. Replace ALL_CAPS placeholders before use.

---

## 1) Principles & Guardrails
- **Privacy-first:** No PII (personally identifiable information) is collected or transmitted. See §7.
- **Least privilege:** Access is role-based; service accounts use minimum scopes.
- **Deterministic, documented events:** Every event has a spec (name, params, data type, ownership).
- **Environment isolation:** Dev/Staging use TEST containers/properties; Production uses PROD.
- **Consent-aware:** Tracking respects consent state at page load and on change (CMP integrated).
- **Reproducible QA:** Each release follows the same validation steps and evidence capture.

---

## 2) Tracking Stack (Reference Architecture)
- **Tag Manager:** GTM (web) – TEST and PROD containers
- **Analytics:** GA4 (Web) – TEST and PROD properties
- **Server-side (optional):** GTM Server container on SERVER_HOST
- **Exports:** GA4 → BigQuery daily export (TEST and PROD projects)
- **Consent Management Platform (CMP):** CMP_VENDOR with IAB TCF v2 (or custom categories)

> Note: This template references GA4; adapt to your analytics platform as needed.

---

## 3) Environments & IDs (Placeholders)
| Layer        | Dev/Feature | Staging/UAT         | Production           |
|--------------|-------------|---------------------|----------------------|
| GTM ID       | GTM-TESTDEV | GTM-TESTUAT         | GTM-PROD             |
| GA4 Property | GA4-TEST    | GA4-UAT             | GA4-PROD             |
| BigQuery     | PROJ_TEST   | PROJ_UAT            | PROJ_PROD            |

**Rules**
- Never deploy TEST tags/IDs to Production.
- Block PROD containers in non-prod via Content Security Policy or environment gates.

---

## 4) Data Layer Spec (Minimum)
We standardize a `dataLayer` push at page view and on meaningful interactions.

### 4.1 Page View (on every route)
```js
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  event: 'page_view_data',
  page: {
    url: window.location.href,
    path: window.location.pathname,
    title: document.title,
    language: 'en-US',
    content_type: 'ARTICLE|HUB|PRODUCT|...'
  },
  user: {
    // NO PII. Only anonymous flags allowed.
    logged_in: false,
    role: 'anonymous' // or 'internal_tester' if whitelisted
  }
});
