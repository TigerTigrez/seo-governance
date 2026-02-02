# Release QA Checklist
**When:** Every code/content release affecting URLs, head tags, nav, templates.

## Pre-deploy
- [ ] Jira/PR links and scope reviewed
- [ ] Change type tagged: Technical / Content / Navigation / Analytics
- [ ] Rollback plan documented

## Deploy validation (prod)
- [ ] Sample of changed URLs returns 200
- [ ] Canonicals as designed
- [ ] New/changed redirects verified (301/302 as spec)
- [ ] Robots/meta directives correct
- [ ] Structured data validates (if in scope)
- [ ] Caching/CDN rules applied

## Post-deploy monitoring (24–72h)
- [ ] Error rates (4xx/5xx) stable
- [ ] Index coverage deltas reviewed
- [ ] CWV regressions checked
- [ ] Sitemaps re-submitted if structure changed
