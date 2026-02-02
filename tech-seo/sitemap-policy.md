# Sitemap Policy
- Separate sitemaps by type: `/sitemaps/sitemap-pages.xml`, `…-news.xml`, `…-images.xml`
- Max 50k URLs or 50MB per file; cascade via index
- Include only indexable 200s (no redirects, no canonicals elsewhere)
- Update frequency: nightly; priority fields optional/not trusted
- Hostnames must match target property (no cross-host)
- Ping GSC on rotate; keep 60–90 days of historical indexes
- Validate with CI before publish (well-formed XML, URL count, host check)
