# Operational notes (for the next agent/session)

State as of 2026-07-14. CLAUDE.md has structure and brand rules; this file has
everything you can't infer from the code.

## Deploy & environment

- Workers Builds auto-deploys on push to `main` (build: `npm run build`,
  deploy: `npx wrangler deploy`). Just commit and push.
- Custom domains `hurbs.io` + `www.hurbs.io` are declared in `wrangler.jsonc`
  (routes with `custom_domain: true`); Cloudflare attaches them on deploy.
- LOCAL GOTCHA: proxy env vars on Mason's machine break Node fetch (wrangler)
  and Python urllib SSL. Prefix commands with
  `env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy` for anything
  that hits the Cloudflare API. Plain `curl` works fine either way.
- Wrangler is OAuth-logged-in as mason-herbel@comcast.net. The newer `cf` CLI
  (`npx cf`) has a separate login that was never completed; `cf dns dnssec`
  is the intended tool for the DNSSEC task below.

## DNS / domain

- DNS hosted on Cloudflare (kai/rose nameservers). Registrar is NAMECHEAP.
- DNSSEC is UNSIGNED. Plan agreed with Mason: enable signing on the zone
  (`cf dns dnssec edit` after `cf auth login`), then Mason pastes the DS
  record into Namecheap (Advanced DNS → DNSSEC). Parked by Mason ("later").
- Domain transfer to Cloudflare Registrar discussed as optional cleanup.

## Cloudflare dashboard settings (Mason drives; verify before assuming)

- AI Crawl Control: all AI crawlers should be set to Allow (site is
  deliberately fully open: robots.txt Content-Signal all "yes").
- Bot Fight Mode: should be OFF.
- "Markdown for Agents" toggle: recommended ON (serves markdown on
  Accept: text/markdown). Status unconfirmed.
- Google Search Console + Bing Webmaster: walkthrough given 2026-07-14;
  verification TXT records + sitemap submission may or may not be done yet.

## Deliberate decisions (don't "fix" these)

- Fully open to AI: llms.txt + llms-full.txt + Content-Signal ai-train=yes.
  Mason's explicit choice for LLM discoverability.
- No hidden-text SEO. JSON-LD + llms.txt are the honest equivalents; keep it.
- Footer year "© 2026" is static. Post dates are static "July 2026".
- No contact forms, ever. Every CTA is mailto (service/blog pages add subject).
- Blog index intro deliberately does NOT state a post count.
- 3 chips intentionally unlinked (no matching post): TeamViewer,
  On-site visits, Ongoing maintenance.
- Buttons: chunky square + hard ink offset shadow (Mason overrode the
  handoff's pill buttons). Chips/filter pills stay round.
- Mason is based in LA ~300 days/yr; HQ + phone stay Houston. Copy uses
  dual-city framing; JSON-LD PostalAddress stays Houston.
- design_handoff_hurbs_website/ is historical reference only; live site has
  diverged (voice pass, buttons, blog) and the handoff should not be
  re-applied over current copy.

## Pending / known gaps

- About page still has the striped photo placeholder; Mason owes a real photo.
- DNSSEC (above), parked.
- TODO.md: blog AI search via Cloudflare AI Search + AI Gateway (+ MCP server
  card and agent-skills index once that endpoint exists).
- Blog guide posts were written by parallel agents against a strict accuracy
  spec but commands were never executed end-to-end; a spot-check pass on the
  technical guides would be worthwhile.
- Visual browser QA of the blog filter UI (search/pills/collapse) was done by
  markup inspection only; one human click-through recommended.

## Content system crib sheet

- Add/edit a post: entry in `tools/blog_data.py` + fragment in `tools/posts/`,
  then `npm run build`. Chips on service pages auto-link via `CHIP_TO_SLUG`;
  chips double as the blog's tag/filter vocabulary and llms.txt regenerates.
- Edit index/about/contact/404 in `tools/pages/` (never `public/`).
- CSS lives in `public/css/styles.css` but is INLINED into every page at
  build; editing CSS without rebuilding changes nothing user-visible.
- Voice rules are non-negotiable and enforced by grep during reviews:
  no em dashes, we-voice, no MSP-speak. Full list in CLAUDE.md.
