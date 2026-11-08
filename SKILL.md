---
name: kr-geo
description: Audit and improve Korean website content for AI-assisted search using page evidence and official sources; distinguish site readiness from observed brand mentions, recommendations, and citations. Use for Korean AEO/GEO audits and scoped fixes, including Naver context, not automatic ranking guarantees.
metadata:
  version: "0.1.0"
---
# Korean AEO/GEO

Start with the actual customer question, the site's truthful service description, and the user's intended output (audit, local fix, or measurement). Keep those separate. Use Korean unless requested otherwise.

## Audit and fix

1. Read the site's own instructions and current rendered page. Preserve source/HTML and date before changes. A raw HTML fetch alone cannot establish the rendered page or indexing state.
2. Identify whether this is an independent website, Naver blog, or Place listing. Recommend only controls available to its owner; blog authors cannot upload verification files to Naver's domain.
3. For local HTML, run `python3 scripts/inspect_html.py PAGE --url PUBLIC_URL` for a small, offline evidence inventory. It checks title, description, canonical, robots meta and JSON-LD syntax. It does NOT measure crawlers, factual quality, indexing or AI citation probability.
4. For the highest-impact findings, provide evidence, the customer question affected, a specific change and a recheck. If the page is already adequate, say so. Do not invent defects to justify a fix.
5. Ask for missing business facts rather than invent prices, cases, customers, reviews or impact numbers. Do not manufacture statistics to make content look citable. Short Korean headings and KRW are normal; do not apply English word-count formulas.
6. Implement only requested fixes, usually in a local copy first. Validate changed HTML and actual browser behavior. Local changes, deployed changes, recrawling, and observed citation changes are separate states.

## Controls and claims

Use current official documentation before recommending bot policy changes:
- Google AI features: https://developers.google.com/search/docs/appearance/ai-features
- Naver site basics: https://searchadvisor.naver.com/guide/seo-basic-intro
- OpenAI crawlers: https://developers.openai.com/api/docs/bots
- Google-Extended: https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers#google-extended

GPTBot training and OAI-SearchBot search are independent. Google-Extended has no independent HTTP user agent and does not govern Google Search inclusion. A spoofed User-Agent request is not proof an actual provider can reach the page. `llms.txt` is not a required Google AI-search file; do not penalize absence or promise uplift from it. Structured data must match visible facts. Robots blocking, noindex, and authenticated access have different meanings; avoid global statements about all AI engines.

## Observe AI answers

Preserve exact question, service/surface (web versus API), visible model/mode, date, login/personalization/search conditions, locale and trial number. Incognito does not remove IP/location or account preferences. Do not change privacy settings without authorization.

Record separately: collection succeeded, AI feature triggered, brand string mentioned, correct entity, recommendation, and actual cited URL. Search/grounding candidates are not automatically citations. Missing observations are null with reasons, not zeros. Keep branded and non-branded questions separate. Repeated trials are small observations, not a guarantee of representative rates or causal uplift.

No network calls, API billing, installation, deployment or external messages are authorized merely by invoking this skill. Respect the task's permissions. This package has no hooks, dependencies, telemetry or Inyonglab account requirement.
