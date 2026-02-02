# Canonicalization Matrix
**Goal:** One canonical URL per content entity; predictable rules.

| Pattern | Example | Canonical To | Rules |
|---|---|---|---|
| Trailing slash variants | /news vs /news/ | Preferred site-wide (decide) | Enforce via 301 + consistent links |
| Case variants | /News vs /news | /news | 301 lowercase; ensure internal links lowercase |
| Params (sorting) | /news?sort=asc | /news | `rel=canonical` to clean URL; optionally disallow crawl |
| Tracking params | ?utm_*, ?fbclid | canonical to clean | Strip at edge; never index |
| Pagination | /page/2 | self | No canonical to page 1; unique titles |
| Facets/filters | /shop?color=red | Depends | Either canonicalize to clean or allow only approved combos |
| Mobile/print | /m/, ?print=1 | desktop canonical | Mobile uses responsive; print pages `noindex,follow` |

**Enforcement:** redirects at edge/app, canonical tags, internal link hygiene.
