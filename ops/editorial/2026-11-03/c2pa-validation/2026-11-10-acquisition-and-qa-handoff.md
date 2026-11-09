# C2PA 2.5 article cluster — acquisition, distribution, QA and decision record
Date: 2026-11-10 KST · Sian · DRAFT / NO LIVE GO

## What changed
- Continued existing Draft PR #48 instead of creating a duplicate topic.
- Eight independently written locale-specific HTML explainers at `{locale}/articles/what-valid-content-credentials-mean/index.html`: EN, KO, JA, zh-Hans, es-419, pt-BR, FR, DE.
- Eight localized Article Index cards and eight sitemap URLs with reciprocal 9-entry hreflang sets.
- Each page includes SEO title/description, canonical, OG, Article JSON-LD, two existing related articles with `article-next-click`, a visible SIGNA CTA, and a Google Play link with `google-play-click` and UTM.
- C2PA technical factual source: https://spec.c2pa.org/specifications/specifications/2.5/specs/C2PA_Specification.html §§13.3, 14.
- Google hreflang reference: https://developers.google.com/search/docs/specialty/international/localized-versions

## Reader intent / content angle
Question: What do valid/trusted Content Credentials actually verify? Answer: C2PA manifest status and the asset-content binding are distinct technical statements; neither certifies the factual truth of a depicted event. Missing credentials are not proof of AI generation. SIGNA does not cryptographically validate C2PA signatures.

Locale-specific entry examples: EN breaking-news caption, KO family group chat, JA second-hand product listing, zh-Hans forwarded chat image, es-419 local flooding post, pt-BR marketplace product photo, FR exhibition attribution, DE insurance damage photo. Locales share only the factual backbone.

## Bounded distribution brief for Daon (NOT SENT / NOT PUBLISHED)
Do not post until Cy approves live publication and the destination URLs actually resolve. Do not imply that SIGNA validates C2PA signatures or proves authenticity. No unsolicited community promotion.

1. **Reels/Shorts (25–35 s), educational:** Opening: "A valid digital signature can coexist with a false photo caption." Show two separate labels: "file record checked" and "event not independently checked". Explain C2PA's limited scope. Close with the published locale article URL only after GO.
2. **Instagram carousel (5 cards):** 1) "Valid vs Trusted"; 2) "Manifest vs current file"; 3) "Missing credential ≠ AI"; 4) "Screenshot creates a new file"; 5) "Read the assertions and compare earlier sources". Source note C2PA 2.5 §13.3 and §14. No fake verified badge.
3. **Community / Naver educational draft:** A scenario-first post: "Why a verified photo can still carry a wrong caption." Distinguish technical provenance from real-world context. Provide primary specification link, not sales copy. Naver actual publishing remains Cy's responsibility.

## Acquisition / measurement (requires actual account access)
- Google Search Console: query impressions, clicks, CTR, indexed/canonical state by the eight exact URLs and nonbranded locale queries. Do not infer rankings from anonymous SERP samples.
- Umami: visitors/visits/views, landing path, source/referrer/channel, country/device/language, article-next-click with placement and locale, google-play-click with UTM and Android segmentation.
- Google Play Console: store listing visitors and acquisitions by country/source only when authenticated. Do not infer installs from website clicks.
- Exclude 2026-09-07 manual QA visitors=2, visits=2, views=4, Play-click=1 from external acquisition.
- Baseline must be captured **after** the merged publication, not from the draft branch. Compare equivalent seven-day windows and retain small-sample caution.

## QA / gates
Static readback performed on 2026-11-10: 8/8 article pages have canonical=1, hreflang=9, related event links=2, Play event CTA=1, meta description, HTML ending; 8/8 indexes have the new card and 15 cards total; sitemap now 136 URLs (previously 128). All are **branch-only**.
NOT TESTED: real browser/mobile layout, keyboard and screen-reader navigation, structured-data validation, actual destination response after deployment, Umami event ingestion, Google indexing, Play installs, native editorial peer review, Production device verification. These remain required before claiming publication-ready.
Cy approval required for merge/live publish. No app code, build, release, Play Console metadata or main branch modified.

## Public Play listing observation, separate from this PR
2026-11-10 opened US-English Play page: title "SIGNA: Photo Watermark", updated Nov 5, 2026, description includes "You can also combine a visible watermark with an invisible SIGNA signal when you want both" and 12 visible / 9 invisible batch limits. Earlier user-visible reports called it "SIGNA: Watermark & Analysis". The precise rename time and impact on nonbrand discovery are NOT established. Track as ASO WATCH; do not change Play listing without GO.
