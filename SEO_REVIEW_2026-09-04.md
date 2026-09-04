# SIGNA Website SEO Review — 2026-09-04

Status: review branch only; not live until Cy approval and merge.

## Confirmed current baseline
- robots.txt allows crawling and points to sitemap.xml.
- sitemap includes the eight locale homepages plus the first Image Metadata article cluster.
- homepage has canonical, hreflang, WebSite/Organization structured data, and Google Play CTA.
- first Article cluster has canonical, locale alternates, Article schema, and localized pages.

## Review findings to implement before merge
1. Normalize the Latin America Spanish hreflang from `es` to `es-419` on homepage locale relationships, matching the Article cluster convention.
2. Expand sitemap locale relationships so each Article-cluster URL is represented with the full alternate-language set, not only as independent URLs.
3. Add a bounded `SoftwareApplication` structured-data node for SIGNA on the official homepage, linking the product entity to SIGNA AI Lab and the Google Play listing. This is entity clarification only; no ranking guarantee is implied.
4. Continue Article publication as native-original 8-locale clusters. Next proposed search topic: invisible image watermarking, its practical limits, and the distinction between visible marks and invisible signals.

## Claim-safety lock
No ownership/originality/legal proof, AI-generated/not-AI verdict, guaranteed detection or platform survival, platform/server verification, C2PA/SynthID replacement, or tamper-proof claim.
