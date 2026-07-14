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


_STOP = set('a an and are as at be but by for from how in is it like of on or that the '
            'to we what when where which who why with without you your '
            'business businesses small need needs actually real right guide step '
            'most every one two three every explained plain english'.split())


def _tokens(p):
    import re
    text = ' '.join([p['title'], p['description']] + p['chips']).lower()
    return {w for w in re.findall(r'[a-z0-9]+', text) if w not in _STOP and len(w) > 2}


def related_posts(p, live_slugs, count=5):
    """Top posts by shared vocabulary across title/description/chips.
    Same-lane gets a small nudge; cross-lane links happen naturally when
    content overlaps (docker <-> hosting, backups <-> ransomware)."""
    mine = _tokens(p)
    scored = []
    for q in POSTS:
        if q['slug'] == p['slug'] or q['slug'] not in live_slugs:
            continue
        score = len(mine & _tokens(q)) + (1.5 if q['lane'] == p['lane'] else 0)
        scored.append((-score, q['slug'], q))
    scored.sort()
    return [q for _, _, q in scored[:count]]


def post_page(p, live_slugs):
    num, color, lane_title = LANES[p['lane']]
    body = open(fragment_path(p['slug']), encoding='utf-8').read().strip()
    mailto = 'mailto:mason@hurbs.io?subject=' + quote('Question about ' + lane_title)

    related = related_posts(p, live_slugs)
    related_html = '\n'.join(
        f'''    <a href="/blog/{q['slug']}" class="other-row">
      <div class="ledger-sq sq-{LANES[q['lane']][1]}"></div>
      <span class="other-title">{e(q['title'])}</span>
      <span class="ledger-hint">{TYPE_LABEL[q['type']].title()}</span>
      <span class="other-arrow">→</span>
    </a>''' for q in related)
    related_section = f'''  <section class="others">
    <div class="others-head"><span>RELATED READING</span></div>
{related_html}
  </section>
''' if related else ''

    jsonld = {
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        'headline': p['title'],
        'description': p['description'],
        'datePublished': '2026-07',
        'url': f"https://hurbs.io/blog/{p['slug']}",
        'image': 'https://hurbs.io/img/og.png',
        'articleSection': lane_title,
        'author': {'@type': 'Organization', 'name': 'Hurbs LLC', 'url': 'https://hurbs.io'},
        'publisher': {'@type': 'Organization', 'name': 'Hurbs LLC', 'url': 'https://hurbs.io',
                      'logo': {'@type': 'ImageObject', 'url': 'https://hurbs.io/img/hurbs.svg'}},
    }
    return head(f"{p['title']} | Hurbs LLC", p['description'],
                canonical=f"/blog/{p['slug']}", og_type='article', jsonld=jsonld) + f'''
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

    return head('Blog | Hurbs LLC',
                'Plain-English explainers and step-by-step guides on IT, cloud, security, software, networks, and data. Written by the people who do the work.',
                canonical='/blog/') + f'''
<div class="page">
{nav('blog')}

  <header class="about-hero">
    <div class="kicker">THE BLOG</div>
    <h1>Notes from the shop.</h1>
    <p class="about-intro">Plain-English explainers for owners, step-by-step guides for doers. No fluff, no gate, no popup asking for your email.</p>
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


def strip_html(fragment):
    import re
    text = re.sub(r'<pre><code>(.*?)</code></pre>', lambda m: '\n```\n' + m.group(1) + '\n```\n', fragment, flags=re.S)
    text = re.sub(r'<h2>(.*?)</h2>', r'\n## \1\n', text)
    text = re.sub(r'<h3>(.*?)</h3>', r'\n### \1\n', text)
    text = re.sub(r'<li>', '- ', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&#x27;', "'").replace('&quot;', '"')
    return re.sub(r'\n{3,}', '\n\n', text).strip()


SITE_BLURB = ('Hurbs LLC (hurbs.io) is Mason Herbel\'s hands-on IT shop in Houston, TX, '
              'serving businesses nationwide (on-site anywhere in the US). Services: IT support '
              '& managed services, cloud setup & migration, cybersecurity, custom software, '
              'networks & infrastructure, data & AI analytics, digital transformation, and IT '
              'staffing & recruiting. No contact forms: email mason@hurbs.io or call (832) 457-4317. '
              'Hurbs is part of the Lepida family (Lepida is the holding company).')


def llms_txt(live_slugs):
    lines = ['# Hurbs LLC', '', f'> {SITE_BLURB}', '',
             '## Pages', '',
             '- [Home](https://hurbs.io/): services overview and contact',
             '- [About](https://hurbs.io/about): who Hurbs is, how we work',
             '- [Contact](https://hurbs.io/contact): email mason@hurbs.io, (832) 457-4317',
             '']
    for lane, (num, color, lane_title) in LANES.items():
        lines += [f'## {lane_title}', '',
                  f'- [Service page](https://hurbs.io/services/{lane})']
        for p in POSTS:
            if p['lane'] == lane and p['slug'] in live_slugs:
                lines.append(f"- [{p['title']}](https://hurbs.io/blog/{p['slug']}): {p['description']}")
        lines.append('')
    lines += ['## Full content', '',
              '- [llms-full.txt](https://hurbs.io/llms-full.txt): every blog post in full, as plain text', '']
    return '\n'.join(lines)


def llms_full_txt(live_slugs):
    parts = ['# Hurbs LLC: full blog content', '', f'> {SITE_BLURB}', '']
    for p in POSTS:
        if p['slug'] not in live_slugs:
            continue
        lane_title = LANES[p['lane']][2]
        body = strip_html(open(fragment_path(p['slug']), encoding='utf-8').read())
        parts += [f"# {p['title']}", '',
                  f"URL: https://hurbs.io/blog/{p['slug']}",
                  f"Service: {lane_title} (https://hurbs.io/services/{p['lane']})",
                  f"Summary: {p['description']}", '',
                  body, '', '---', '']
    return '\n'.join(parts)


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
        f.write('User-agent: *\n'
                'Allow: /\n'
                '# Content Signals (contentsignals.org): welcome AI search, answers, and training\n'
                'Content-Signal: search=yes, ai-input=yes, ai-train=yes\n\n'
                'Sitemap: https://hurbs.io/sitemap.xml\n\n'
                '# Machine-readable site guide for LLMs and AI crawlers\n'
                '# https://hurbs.io/llms.txt\n')
    with open(os.path.join(REPO, 'public', 'llms.txt'), 'w', encoding='utf-8') as f:
        f.write(llms_txt(live_slugs))
    with open(os.path.join(REPO, 'public', 'llms-full.txt'), 'w', encoding='utf-8') as f:
        f.write(llms_full_txt(live_slugs))

    print(f'built {len(live_slugs)} posts; missing fragments: {len(missing)}')
    if missing:
        print('  ' + ', '.join(missing))


if __name__ == '__main__':
    main()
