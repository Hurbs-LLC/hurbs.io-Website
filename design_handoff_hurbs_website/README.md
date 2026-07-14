# Handoff: Hurbs LLC Website

## Overview
A full marketing website for Hurbs LLC (hurbs.io) — Mason Herbel's homegrown IT/software shop, part of the Lepida family. Rebranded from the Lepida service catalog with a warmer, 70s-retro "small shop that shows up" voice. Four pages: Home, Service detail (covers 8 services), About, Contact.

## About the Design Files
The files in this bundle are **design references created in HTML** (`.dc.html` design-component prototypes) — they show intended look and behavior, not production code to copy directly. The task is to **recreate these designs in the target codebase's environment**. The existing hurbs.io repo is plain static HTML/CSS/JS with no build system — implementing this as plain static HTML/CSS (one file per page + one page per service) is the natural fit. Alternatively, Astro (like the Lepida site) works well for the 8 service pages generated from a data file.

## Fidelity
**High-fidelity.** Colors, typography, spacing, and copy are final. Recreate pixel-perfectly.

## Design Tokens

Colors (all derived from the Hurbs logo, `assets/hurbs.svg`):
- Brick red `#C84E3F` (primary accent, CTA buttons)
- Mustard yellow `#E4DB5B` (CTA band bg, underline accents; use `#9A8F1E` for yellow *text* on cream — raw yellow is illegible)
- Avocado green `#6E945E` (kickers, accents)
- Denim blue `#516EB4` (accents, default link color)
- Cream page bg `#FAF6EC`; card bg `#FFFDF7`; hover row bg `#F3EDDD`
- Ink `#2B2620` (text, all 2px borders); body-muted `#57503F`; faint `#8A8170`
- Dark band/footer bg `#2B2620`, muted text on dark `#A89F92`, light text `#FAF6EC`
- Stat colors on dark: `#E4DB5B`, `#C87F6F`, `#8FAE7E`, `#7C93C9`
- Red button hover: `#A93D30`

Typography (Google Fonts):
- **Alfa Slab One** (400 only) — display headlines, big numbers. Hero H1: 108px/1, brick red with logo-echo text-shadow: `text-shadow: 0.05em 0 0 #E4DB5B, 0.1em 0 0 #6E945E, 0.15em 0 0 #516EB4`. Section H2: 30–34px. CTA email link: 46–58px.
- **Bricolage Grotesque** — service/row titles (700, 19–24px), card headings (700, 20px).
- **Archivo** — body (400, 15.5–21px, line-height 1.55–1.7), nav (600 15px), kickers (700 14px, letter-spacing .18–.2em, uppercase), buttons (800 17–18px).

Spacing & structure:
- Page gutter: 56px horizontal. Section padding: 64–96px vertical.
- Borders: 2px solid ink everywhere (nav bottom, section dividers, ledger rows); 4px ink under section headers.
- Buttons: pill (`border-radius: 999px`), brick red bg, cream text, padding 16-17px × 28-32px.
- Colored squares: 10–16px solid squares (no radius) as service markers.
- No rounded cards, no drop shadows on this direction — flat retro.

## Screens / Views

### 1. Home (`Hurbs Home.dc.html`)
- **Nav**: cream, 2px ink bottom border; logo (height 30px, links home) left; right: Services / About / Contact links + `mason@hurbs.io` bold with 3px yellow bottom-border. Link hover → brick red.
- **Hero**: kicker "GROWING INNOVATION — SINCE 2012" (green); H1 "HONEST IT" (Alfa Slab 108px, red + stacked shadow above); subhead 30px 600 "for businesses that would rather not think about IT."; body paragraph (max-width 600px); red pill button "Email Mason →" (mailto) + phone text.
- **Services ledger** (`#services`): header row "The services" + right-aligned label "CLICK ONE — EACH HAS ITS OWN PAGE", 4px ink bottom border. 8 clickable rows, each: number (Alfa Slab 17px, per-service color) · 12px colored square · title (Bricolage 700 24px) · short hint (15px muted) · "→". Row: 22px vertical padding, 2px ink bottom border, hover bg `#F3EDDD`. Colors rotate red/yellow/green/blue. Each row links to its service page.
- **Stats band**: dark ink bg, 4 columns centered: 2012 / 50 / 1 / 0 (Alfa Slab 52px in the four stat colors) with muted captions ("fixing & building since", "states we'll show up in", "email — and it's Mason's", "phone trees, ever").
- **CTA band**: yellow bg, 2px ink top border, centered: kicker "NO FORMS. JUST EMAIL.", `mason@hurbs.io` as Alfa Slab 54px link with 6px red bottom-border (hover → red text), then "or (832) 457-4317 — Houston, TX".
- **Footer**: dark ink, "© 2026 Hurbs LLC" left, "Part of the Lepida family" right (14px, muted).

### 2. Service detail (`Hurbs Service.dc.html`)
One template, 8 services selected by URL hash (`#it-support`, `#cloud`, `#cybersecurity`, `#software`, `#networks`, `#data-ai`, `#digital`, `#staffing`). In production: one static page per service.
- **Nav**: same as home (Services links to home `#services`).
- **Hero** (2px ink bottom border): "← ALL SERVICES" breadcrumb; number + 16px colored square; H1 (Alfa Slab 64px); blurb 21px; red pill "Ask Mason about this →" — mailto with `subject=Question about <service>`.
- **Two-column section** (flex 1.3 / 1, gap 64px, 2px ink bottom border):
  - "What's included": 5 rows, each 10px colored square + item (Bricolage 600 19px), 2px ink bottom borders.
  - "Tools we reach for": wrapping pill chips (2px ink border, `#FFFDF7` bg, 600 14px, radius 999px).
- **"Why do it with Hurbs"**: 3 columns, each 14px colored square + heading (Bricolage 700 20px) + body.
- **"Everything else we do"**: compact ledger of the other 7 services (same row anatomy, smaller: 19px titles), cross-linking.
- **CTA band + footer**: same as home (CTA email at 46px).

All 8 services' full copy (titles, blurbs, includes, tools, why-points) lives in the logic block of `Hurbs Service.dc.html` — treat it as the content source of truth.

### 3. About (`Hurbs About.dc.html`)
- Nav (About highlighted red).
- Hero: kicker "ABOUT HURBS"; H1 "Built my first computer in 2012. Never stopped." (Alfa Slab 62px); intro paragraph. 2px ink bottom border.
- Story section: left 380×440px photo placeholder (2px ink border, 45° cream stripes via `repeating-linear-gradient`, monospace label "photo: Mason / the shop" — replace with a real photo); right: three first-person paragraphs (18.5px/1.7) + red pill "Say hi →".
- "How we work": 3 columns (blue/green/red squares): "You talk to a person" / "We show up" / "Priced fair".
- CTA band + footer as home.

### 4. Contact (`Hurbs Contact.dc.html`)
- Nav (Contact highlighted). Full-height centered column (flex, `min-height:100vh`).
- Kicker "NO FORMS. NO PHONE TREES."; H1 "Tell me what's broken." (56px); paragraph; `mason@hurbs.io` as Alfa Slab 58px link with 6px red underline; below: "☎ (832) 457-4317" and "Houston, TX — on-site anywhere". Footer as home.

## Interactions & Behavior
- All primary CTAs are `mailto:mason@hurbs.io` (service pages add a subject line). No forms anywhere — intentional.
- Link/row hovers: text → `#C84E3F`; ledger rows → bg `#F3EDDD`; red buttons → `#A93D30`. No transitions specified; instant or ~150ms ease is fine.
- Service page scrolls to top on navigation between services.
- Responsive behavior not designed yet — desktop (≥1240px) is the reference; mobile needs a pass (stack ledger row hints below titles, shrink hero to ~56px, single-column grids).

## State Management
None beyond per-page static content. The prototype's hash-routing on the service page is a prototype convenience only.

## Assets
- `assets/hurbs.svg` — the Hurbs wordmark (stacked 4-color offset logo), from the existing hurbs.io repo (`img/hurbs.svg`). Used in nav on every page; also the favicon in the current site.
- Google Fonts: Alfa Slab One, Bricolage Grotesque, Archivo.
- Needed from client: a real photo of Mason / the shop for the About page placeholder.

## Files
- `Hurbs Home.dc.html` — home page
- `Hurbs Service.dc.html` — service detail template + all 8 services' copy (in the script block)
- `Hurbs About.dc.html` — about page
- `Hurbs Contact.dc.html` — contact page
- `assets/hurbs.svg` — logo
