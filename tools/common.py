"""Shared page chrome for the static generators."""
import html
import os

e = html.escape

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)


def _read(path):
    return open(path, encoding='utf-8').read().strip()


def _assets():
    """Everything needed to paint, inlined: fonts CSS + normalize + site CSS.
    One HTML response renders the page; only the woff2 files load after."""
    fontfaces = _read(os.path.join(_HERE, 'fontfaces.css'))
    normalize = _read(os.path.join(_REPO, 'public', 'css', 'normalize.css'))
    styles = _read(os.path.join(_REPO, 'public', 'css', 'styles.css'))
    preloads = '\n'.join(
        f'  <link rel="preload" href="/fonts/{f}" as="font" type="font/woff2" crossorigin>'
        for f in ('alfa-slab-one-400-latin.woff2', 'archivo-400-latin.woff2',
                  'bricolage-grotesque-400-latin.woff2'))
    return f'''  <link rel="icon" href="/img/hurbs.svg" type="image/svg+xml">
{preloads}
  <style>
{fontfaces}
{normalize}
{styles}
  </style>'''


FONTS = _assets()
JS = '<script>' + _read(os.path.join(_REPO, 'public', 'js', 'main.js')) + '</script>'


def head(title, description, canonical=None, og_type='website', jsonld=None):
    canon = f'\n  <link rel="canonical" href="https://hurbs.io{canonical}">' if canonical else ''
    og = ''
    if canonical:
        og = (f'\n  <meta property="og:title" content="{e(title)}">'
              f'\n  <meta property="og:description" content="{e(description)}">'
              f'\n  <meta property="og:type" content="{og_type}">'
              f'\n  <meta property="og:url" content="https://hurbs.io{canonical}">'
              f'\n  <meta property="og:site_name" content="Hurbs LLC">'
              f'\n  <meta property="og:image" content="https://hurbs.io/img/og.png">'
              f'\n  <meta property="og:image:width" content="1200">'
              f'\n  <meta property="og:image:height" content="630">'
              f'\n  <meta name="twitter:card" content="summary_large_image">'
              f'\n  <meta name="twitter:title" content="{e(title)}">'
              f'\n  <meta name="twitter:description" content="{e(description)}">'
              f'\n  <meta name="twitter:image" content="https://hurbs.io/img/og.png">')
    ld = ''
    if jsonld:
        import json
        ld = f'\n  <script type="application/ld+json">{json.dumps(jsonld, separators=(",", ":"))}</script>'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">{canon}{og}{ld}
{FONTS}
</head>
<body>'''


def nav(active=None):
    def cls(name):
        return ' class="active"' if active == name else ''
    return f'''  <nav class="nav">
    <a href="/" class="nav-logo"><img src="/img/hurbs.svg" alt="Hurbs LLC"></a>
    <div class="nav-links">
      <a href="/#services"{cls('services')}>Services</a>
      <a href="/blog/"{cls('blog')}>Blog</a>
      <a href="/about"{cls('about')}>About</a>
      <a href="/contact"{cls('contact')}>Contact</a>
      <a href="mailto:mason@hurbs.io" class="nav-email">mason@hurbs.io</a>
    </div>
  </nav>'''


def cta_band(inner=True):
    mod = ' cta--inner' if inner else ''
    return f'''  <section class="cta{mod}">
    <div class="cta-kicker">NO FORMS. JUST EMAIL.</div>
    <a href="mailto:mason@hurbs.io" class="cta-email">mason@hurbs.io</a>
    <div class="cta-sub">or <a href="tel:+18324574317">(832) 457-4317</a>, LA and Houston</div>
  </section>'''


FOOTER = '''  <footer class="footer">
    <span>© 2026 Hurbs LLC</span>
    <span>Part of the <a href="https://lepida.io">Lepida</a> family</span>
  </footer>
</div>
''' + JS + '''
</body>
</html>'''


def blog_cards(slugs, posts_by_slug, lanes, heading='From the blog'):
    cards = []
    for s in slugs:
        p = posts_by_slug[s]
        color = lanes[p['lane']][1]
        cards.append(f'''      <a href="/blog/{p['slug']}" class="blog-card">
        <div class="why-sq sq-{color}"></div>
        <h3>{e(p['title'])}</h3>
        <p>{e(p['description'])}</p>
        <span class="blog-card-read">Read →</span>
      </a>''')
    cards_html = '\n'.join(cards)
    return f'''  <section class="blog-teaser">
    <div class="section-head">
      <h2>{e(heading)}</h2>
      <a href="/blog/" class="section-head-hint" style="text-decoration:none">ALL POSTS →</a>
    </div>
    <div class="blog-cards">
{cards_html}
    </div>
  </section>'''
