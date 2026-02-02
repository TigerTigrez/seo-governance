# Content Governance Policy (Public Template)
**Applies to:** ORGANIZATION_NAME web properties  
**Owner:** Content Governance Council (CGC) – SEO Lead, Content Lead, Accessibility Lead, Legal Rep, Security Rep  
**Last reviewed:** YYYY-MM-DD  
**Version:** 1.0

> This policy defines how content is proposed, created, reviewed, published, maintained, and retired across ORGANIZATION_NAME properties. Replace ALL_CAPS placeholders before use.

---

## 1) Principles
- **Accuracy & Safety:** Content must be factually correct, non-misleading, and compliant with legal/regulatory obligations.
- **Accessibility-first:** Conform to **WCAG 2.2 AA** at minimum; accessibility is not traded for speed or aesthetics.
- **Privacy-by-design:** No PII (personally identifiable information) in public artifacts; redact per PII SOP.
- **Findability:** Content must be structured for search (internal + external): semantic HTML, metadata, and crawl hygiene.
- **Single Source of Truth (SSOT):** Each page has an authoritative owner, canonical URL, and version history.
- **Change Control:** SEO-impacting or user-critical changes follow the Change Management SOP.

---

## 2) Roles & Responsibilities
| Role | Primary Duties |
|---|---|
| **Content Owner** | Maintains page accuracy; initiates updates; ensures review cadence. |
| **Content Author** | Drafts content to spec; applies style, metadata, and taxonomy. |
| **SEO Lead** | Reviews for search intent, information architecture, structured data, canonical/URL strategy. |
| **Accessibility Lead** | Audits for WCAG; verifies headings, alt text, focus order, contrast, forms. |
| **Legal/Policy** | Reviews compliance (claims, disclaimers, required language). |
| **Security/Privacy** | Validates no PII or sensitive info; checks links/embeds for risk. |
| **Publisher** | Final checks (QA) and push to Production. |
| **Analytics** | Ensures events/measurements align to KPI definitions. |

> A single person may fill multiple roles on smaller teams, but **no one self-approves** across all gates for high-risk content.

---

## 3) Content Types & Taxonomy
Define and maintain an official content model.

### 3.1 Content Types (examples)
- **Hub / Section Landing**
- **Article / Guide**
- **Program / Benefit Page**
- **FAQ**
- **News / Advisory**
- **Form / Transaction Page**
- **Resource Download**

### 3.2 Required Metadata (front matter example)
```yaml
---
title: "PAGE_TITLE"
description: "1–2 sentence summary for SERP/snippets."
content_type: "ARTICLE|HUB|FAQ|PROGRAM"
owner: "TEAM_OR_PERSON"
review_cycle: "6 months"   # 3/6/12 months typical
last_reviewed: "YYYY-MM-DD"
canonical_url: "https://WWW.EXAMPLE.GOV/SECTION/PATH/"
robots: "index,follow"
language: "en-US"
tags: ["TOPIC_ONE","TOPIC_TWO"]
audience: ["general public"]
schema_type: "Article|FAQPage|WebPage"
---
