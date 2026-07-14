# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Static multi-page website for Hurbs LLC (hurbs.io) — Mason Herbel's IT shop, part of the Lepida family. Plain HTML/CSS/vanilla JS served as Cloudflare Workers static assets — no build step, no framework. Keep it that way.

## Development & deploy

```bash
npm install        # once (wrangler)
npm run dev        # local dev at http://localhost:8787
npm run deploy     # deploy to Cloudflare Workers
```

`wrangler.jsonc` serves `./public` as static assets with `not_found_handling: "404-page"` (serves `/404.html`) and `html_handling: "auto-trailing-slash"` (clean URLs: `/about`, `/services/cloud`). Internal links use the clean-URL form, not `.html` — keep it that way to avoid 307 redirects. Asset links are root-relative (`/css/styles.css`), so `file://` opening breaks.

## Structure

- `public/` — everything deployed:
  - `index.html` — home: "HONEST IT" hero, 8-row services ledger, stats band, yellow CTA band.
  - `about.html`, `contact.html`, `404.html` — secondary pages.
  - `services/*.html` — 8 static service pages (it-support, cloud, cybersecurity, software, networks, data-ai, digital, staffing). All share one template shape; copy comes from the design handoff.
  - `css/styles.css` — the single stylesheet: design tokens as CSS custom properties in `:root`, component classes, mobile pass at ≤860px.
  - `css/normalize.css` — local normalize, linked from every page.
  - `js/main.js` — logo load-failure fallback only.
  - `img/hurbs.svg` — logo, also used as favicon.
  - `blog/` — generated blog: `index.html` + one page per post. Never edit these by hand.
  - `sitemap.xml`, `robots.txt` — generated.
- `tools/` — committed generators (Python, stdlib only):
  - `blog_data.py` — post registry (slug, title, lane, type, description, chips it covers) + `LANES`, `CHIP_TO_SLUG`, `FEATURED` card picks.
  - `posts/<slug>.html` — post body fragments (article HTML only, no h1/head; template adds chrome and CTA).
  - `gen_blog.py` — builds `public/blog/`, sitemap, robots. Skips registry entries with no fragment.
  - `gen_services.py` — builds `public/services/`; links chips to posts via `CHIP_TO_SLUG`, adds "From the blog" cards.
  - `common.py` — shared head/nav/CTA/footer/card templates.
  - To add a post: add a registry entry, write the fragment, run both generators from the repo root: `python3 tools/gen_blog.py && python3 tools/gen_services.py`.
- `wrangler.jsonc`, `package.json` — Cloudflare Workers config; wrangler is the only dependency.
- `design_handoff_hurbs_website/` — design source of truth (four `.dc.html` high-fidelity references + README). Not production code; never deployed.

## Brand rules (non-negotiable)

- Palette: brick `#C84E3F`, mustard `#E4DB5B`, avocado `#6E945E`, denim `#516EB4`, cream `#FAF6EC`, ink `#2B2620`. Yellow is NEVER text — use `#9A8F1E` on cream instead.
- Fonts: Alfa Slab One (display), Bricolage Grotesque (headings/rows), Archivo (body) — Google Fonts.
- Flat retro: 2px solid ink borders (4px under section headers), solid un-rounded squares as markers, pill buttons (radius 999px). NO drop shadows, NO rounded cards, NO gradients.
- Voice: write as Mason Herbel's company ("we," not "I"). Direct, casual, specific; short sentences, plain words. NO em dashes anywhere in copy (use periods, commas, or "to"). No MSP-brochure words ("solutions," "leverage," "seamless," "trusted partner," "peace of mind") and no AI-isms ("In today's fast-paced world," rule-of-three sentences, rhetorical-question transitions). Concrete over abstract: name tools, services, outcomes. CTAs are plain ("Email us"), never begging. Every CTA is `mailto:mason@hurbs.io` (service pages add a subject line). NO contact forms, ever. This is intentional.
- Company structure: Hurbs = hands-on IT services under Lepida (holding company); Rubber Duck = sibling consultancy that owns strategy/advisory copy. Hurbs copy never sells strategy. If structure needs a mention: "Hurbs is a Lepida company," one sentence max.
- Footer on every page: "© 2026 Hurbs LLC" + "Part of the Lepida family". Year is static by design.
