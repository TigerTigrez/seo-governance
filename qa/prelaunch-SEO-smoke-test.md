# Pre-Launch SEO Smoke Test
- 200 status on critical pages
- Canonicals self-referential or correct
- Noindex / nofollow correct on test environments
- Robots.txt present & sane
- Sitemap(s) present, valid, and discoverable
- Hreflang present and consistent (if used)
- Title/meta patterns rendering as expected

# Pre-Launch SEO Smoke Test
**Scope:** Final check in staging/UAT before go-live.  
**Owner:** SEO Lead • **Timebox:** 30–45 min

## 1) HTTP & Indexability
- [ ] Critical templates (Home, Hub, Article, Product, Search, 404) return **200**
- [ ] Nonexistent URLs return **404** with HTML body
- [ ] Environment is **blocked** via robots/meta on non-prod; **unblocked** for prod
- [ ] Canonicals: self-referential on canonical pages; point to preferred on variants
- [ ] No accidental `noindex`/`nofollow` on production templates

## 2) Robots & Sitemaps
- [ ] `robots.txt` reachable and environment-appropriate
- [ ] XML sitemaps reachable, valid, contain only indexable 200 URLs
- [ ] `<loc>` URLs are absolute and use the **production** host

## 3) Rendering & Content
- [ ] Title/H1 present, unique, non-truncated patterns render
- [ ] Meta description present where required
- [ ] Main content renders without JS errors; images lazy-load below the fold

## 4) Links & Navigation
- [ ] Primary nav and footer links resolve (no 4xx/5xx)
- [ ] Pagination uses rel=“prev/next” if applicable or modern pattern
- [ ] Facets/filters disallow crawl traps per spec

## 5) Performance & CWV (spot check)
- [ ] LCP element exists; server response < 600ms on cached pages
- [ ] No CLS from late-loading fonts/ads on critical templates

## 6) Analytics & GSC
- [ ] GA4 tag present on prod only; test IDs stripped
- [ ] Consent behavior matches policy
- [ ] GSC property verified and sitemaps ready to submit

## 7) Accessibility (quick)
- [ ] One H1 per page, logical headings
- [ ] Alt text for key images; decorative images marked properly
- [ ] Visible focus; sufficient color contrast

**Sign-off:** SEO ✔  Dev ✔  PM ✔

