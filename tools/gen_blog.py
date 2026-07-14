"""Assemble public/blog/ from tools/posts/*.html fragments + blog_data.py.
Also writes sitemap.xml and robots.txt. Posts missing a fragment are skipped
(chips for them stay plain spans on the next gen_services.py run)."""
import os
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_data import POSTS, LANES, DATE
from common import head, nav, cta_band, FOOTER, e

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(REPO, 'tools', 'posts')
OUT = os.path.join(REPO, 'public', 'blog')

TYPE_LABEL = {'concept': 'EXPLAINER', 'guide': 'STEP-BY-STEP GUIDE'}


def fragment_path(slug):
    return os.path.join(POSTS_DIR, slug + '.html')


def post_page(p, live_slugs):
    num, color, lane_title = LANES[p['lane']]
    body = open(fragment_path(p['slug']), encoding='utf-8').read().strip()
    mailto = 'mailto:mason@hurbs.io?subject=' + quote('Question about ' + lane_title)

    related = [q for q in POSTS if q['lane'] == p['lane'] and q['slug'] != p['slug']
               and q['slug'] in live_slugs][:3]
    related_html = '\n'.join(
        f'''    <a href="/blog/{q['slug']}" class="other-row">
      <div class="ledger-sq sq-{color}"></div>
      <span class="other-title">{e(q['title'])}</span>
      <span class="other-arrow">→</span>
    </a>''' for q in related)
    related_section = f'''  <section class="others">
    <div class="others-head"><span>RELATED READING</span></div>
{related_html}
  </section>
''' if related else ''

    return head(f"{p['title']} | Hurbs LLC", p['description'],
                canonical=f"/blog/{p['slug']}") + f'''
<div class="page">
{nav('blog')}

  <header class="post-hero">
    <a href="/blog/" class="svc-breadcrumb">← ALL POSTS</a>
    <div class="post-lane">
      <div class="svc-sq sq-{color}"></div>
      <a href="/services/{p['lane']}" class="post-lane-link">{e(lane_title.upper())}</a>
      <span class="post-type">{TYPE_LABEL[p['type']]}</span>
    </div>
    <h1>{e(p['title'])}</h1>
    <div class="post-meta">{DATE} · by the Hurbs crew</div>
  </header>

  <article class="post">
{body}
    <div class="post-cta">
      <p>Stuck on this, or want it done for you? That's the job.</p>
      <a href="{mailto}" class="btn btn--sm">Email us →</a>
    </div>
  </article>

{related_section}{cta_band()}

{FOOTER}
'''


def index_page(live_slugs):
    sections = []
    for lane, (num, color, lane_title) in LANES.items():
        posts = [p for p in POSTS if p['lane'] == lane and p['slug'] in live_slugs]
        if not posts:
            continue
        rows = '\n'.join(
            f'''    <a href="/blog/{p['slug']}" class="ledger-row ledger-row--blog">
      <div class="ledger-sq sq-{color}"></div>
      <span class="ledger-title ledger-title--blog">{e(p['title'])}</span>
      <span class="ledger-hint">{TYPE_LABEL[p['type']].title()}</span>
      <span class="ledger-arrow">→</span>
    </a>''' for p in posts)
        sections.append(f'''  <section class="blog-lane">
    <div class="section-head">
      <h2>{e(lane_title)}</h2>
      <a href="/services/{lane}" class="section-head-hint" style="text-decoration:none">THE SERVICE →</a>
    </div>
{rows}
  </section>''')
    sections_html = '\n\n'.join(sections)
    count = len(live_slugs)

    return head('Blog | Hurbs LLC',
                'Plain-English explainers and step-by-step guides on IT, cloud, security, software, networks, and data. Written by the people who do the work.',
                canonical='/blog/') + f'''
<div class="page">
{nav('blog')}

  <header class="about-hero">
    <div class="kicker">THE BLOG</div>
    <h1>Notes from the shop.</h1>
    <p class="about-intro">{count} posts: plain-English explainers for owners, step-by-step guides for doers. No fluff, no gate, no popup asking for your email.</p>
  </header>

{sections_html}

{cta_band()}

{FOOTER}
'''


def sitemap(live_slugs):
    urls = ['/', '/about', '/contact', '/blog/']
    urls += [f'/services/{lane}' for lane in LANES]
    urls += [f'/blog/{s}' for s in sorted(live_slugs)]
    entries = '\n'.join(f'  <url><loc>https://hurbs.io{u}</loc></url>' for u in urls)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
'''


def main():
    os.makedirs(OUT, exist_ok=True)
    live_slugs = {p['slug'] for p in POSTS if os.path.exists(fragment_path(p['slug']))}
    missing = [p['slug'] for p in POSTS if p['slug'] not in live_slugs]

    for p in POSTS:
        if p['slug'] not in live_slugs:
            continue
        with open(os.path.join(OUT, p['slug'] + '.html'), 'w', encoding='utf-8') as f:
            f.write(post_page(p, live_slugs))

    with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_page(live_slugs))
    with open(os.path.join(REPO, 'public', 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap(live_slugs))
    with open(os.path.join(REPO, 'public', 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write('User-agent: *\nAllow: /\n\nSitemap: https://hurbs.io/sitemap.xml\n')

    print(f'built {len(live_slugs)} posts; missing fragments: {len(missing)}')
    if missing:
        print('  ' + ', '.join(missing))


if __name__ == '__main__':
    main()
