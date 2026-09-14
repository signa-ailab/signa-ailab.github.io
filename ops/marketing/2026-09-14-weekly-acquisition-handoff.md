# SIGNA Weekly Acquisition Handoff — 2026-09-14

Status: REVIEW-ONLY. No publish/merge without Cy approval.

## Funnel diagnosis

The current public website is crawlable and surfaced by web search for branded SIGNA queries, but fresh verification did not establish non-brand Google/Play discovery for `watermark`, `photo watermark`, `image watermark`, or `invisible watermark`. Do not report an absolute rank without direct Play/SERP evidence.

The clearest competitive message pressure is local processing. Markly currently leads with “Your photos never leave your device” and Easy Watermark also emphasizes offline/local processing. SIGNA should therefore pair non-brand watermark intent with its broader differentiation: visible watermark + invisible SIGNA signal + image analysis, while stating plainly that core photo processing is performed on-device rather than uploaded to SIGNA servers.

## Highest-value website action

Target existing Korean article:
`/ko/articles/what-happens-when-you-share-a-photo/`

Search-intent cluster:
- 카톡 사진 화질 저하
- 카카오톡 사진 메타데이터
- SNS 사진 압축
- 사진 공유 메타데이터
- 워터마크 SNS 공유
- 보이지 않는 워터마크 압축

Recommended title:
`카톡·SNS로 사진 보내면 화질·메타데이터·워터마크는 어떻게 바뀔까? | SIGNA`

Recommended meta description:
`카카오톡이나 SNS로 사진을 보내면 재압축·리사이즈·메타데이터·보이지 않는 워터마크가 어떻게 달라질 수 있을까요? 사진 공유 뒤 파일에 생기는 변화를 기술적으로 설명합니다.`

Recommended first-screen CTA after the dek/meta:
`사진을 공유하기 전에 워터마크를 넣거나, 공유 후 이미지 상태를 확인하고 싶다면 SIGNA에서 기기 안에서 처리할 수 있습니다.`
CTA label: `SIGNA 기능 보기 →`
Destination: `/ko/#watermark` if a stable section anchor exists; otherwise `/ko/`.

Reason: this preserves the article as informational search content while creating a direct Article → Product path for users already expressing photo-sharing intent.

## Naver search-content next asset

Working title:
`카톡으로 사진 보내면 화질만 떨어질까? 메타데이터와 워터마크도 달라질 수 있습니다`

Opening hook:
`카톡으로 사진을 보낸 뒤 다시 저장했는데 화면으로는 똑같아 보인 적이 있나요? 같은 사진처럼 보여도 파일 안에서는 압축, 크기, 메타데이터, 보이지 않는 신호가 서로 다르게 바뀔 수 있습니다.`

Structure:
1. 카톡/SNS 공유에서 실제로 바뀔 수 있는 것
2. 화질과 파일이 “같다”는 말의 차이
3. EXIF/메타데이터는 왜 남기도 하고 사라지기도 하는가
4. 보이지 않는 워터마크는 압축·리사이즈 영향을 어떻게 받는가
5. 스크린샷은 왜 별도의 새 이미지인가
6. 더 깊게 보기 → SIGNA Article
7. 공유 전 준비/공유 후 확인 → SIGNA product page

Article UTM:
`https://signa-ailab.github.io/ko/articles/what-happens-when-you-share-a-photo/?utm_source=naver_blog&utm_medium=referral&utm_campaign=photo_share_changes`

Product UTM:
`https://signa-ailab.github.io/ko/?utm_source=naver_blog&utm_medium=referral&utm_campaign=photo_share_changes`

## Daon distribution brief

Primary problem: “사진을 카톡/SNS로 보내면 실제 파일에 무엇이 바뀌나?”
Audience: Android photo sharers, creators, small sellers, photographers, users concerned about metadata/privacy or reposting.

Priority channels:
1. Instagram/Reels/TikTok — educational short-form, not product-first promotion.
2. Verified public questions/threads where users are already asking about photo compression, metadata loss, watermark survival, or screenshot behavior. Only engage where self-promotion is allowed or a SIGNA mention is genuinely responsive to the question.

Hook A: `카톡으로 보낸 사진, 눈에는 같아도 파일은 같지 않을 수 있습니다.`
Hook B: `사진을 SNS에 올리면 EXIF만 사라지는 걸까요? 압축·크기·픽셀 신호는 따로 봐야 합니다.`
Hook C: `스크린샷은 원본 복사가 아니라 새 이미지입니다.`

Educational CTA: `공유 뒤 사진에서 무엇이 달라질 수 있는지 정리했습니다.` → localized Article URL with `utm_source`, `utm_medium`, and `utm_campaign=photo_share_changes`.

Product CTA only after relevance is established: `공유 전 워터마크 준비와 공유 후 이미지 확인을 한 흐름에서 하고 싶다면 SIGNA를 확인해보세요.`

Do not claim ownership proof, guaranteed SNS survival, guaranteed detection, AI/non-AI certification, platform verification, or C2PA/SynthID replacement.

## Measurement for next weekly review

Separate Cy QA traffic from external performance. Record:
- non-QA Visitors / Visits / Views
- `/ko/articles/what-happens-when-you-share-a-photo/` entries
- Naver/referral visits and `utm_campaign=photo_share_changes`
- Article → `/ko/` navigation
- `google-play-click`
- verified Play install/rating/review changes if available
- any verified non-brand Google/Play discovery; do not infer absolute rank

Decision rule: impressions/no visits → rewrite title/meta/snippet; visits/no Play click → strengthen product bridge/CTA; Naver or social UTM creates visits → increase that distribution channel next cycle.