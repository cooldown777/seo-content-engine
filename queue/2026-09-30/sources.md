# Sources – 2026-09-30 carousel: 6 SEO fixes for category pages

Note: developers.google.com was blocked by the session's network proxy, so these pages were
verified via web search results pointing at the official Google documentation (not fetched directly).

| Claim | Source |
|---|---|
| If category pages don't link to all products, Googlebot might not find them all by crawling; link menus → categories → sub-categories → products | https://developers.google.com/search/docs/specialty/ecommerce/help-google-understand-your-ecommerce-site-structure |
| Google can only reliably discover links that are `<a>` elements with an `href` attribute | https://developers.google.com/search/docs/crawling-indexing/links-crawlable |
| Paginated pages are treated as separate pages; give each a unique URL (e.g. ?page=n); don't use page 1 as canonical for all; Google ignores URL fragments (#) | https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading |
| Faceted navigation can generate near-infinite URLs and cause overcrawling; robots.txt disallow for filters not needed in Search; return 404 for empty filter combinations; consistent filter order | https://developers.google.com/crawling/docs/faceted-navigation · https://developers.google.com/search/blog/2024/12/crawling-december-faceted-nav |
| Titles should be unique and descriptive; duplicate, vague or overly long titles can lead Google to generate alternative title links | https://developers.google.com/search/docs/appearance/title-link |
| Breadcrumb markup (BreadcrumbList) helps Google categorize page info in search results; breadcrumbs should reflect a typical user path | https://developers.google.com/search/docs/appearance/structured-data/breadcrumb |
