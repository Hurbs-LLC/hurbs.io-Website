"""Shared page chrome for the static generators."""
import html

e = html.escape

FONTS = '''  <link rel="icon" href="/img/hurbs.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/css/normalize.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
  <link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Archivo:wght@400;500;600;700;800&family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/styles.css">'''


def head(title, description, canonical=None):
    canon = f'\n  <link rel="canonical" href="https://hurbs.io{canonical}">' if canonical else ''
    og = ''
    if canonical:
        og = (f'\n  <meta property="og:title" content="{e(title)}">'
              f'\n  <meta property="og:description" content="{e(description)}">'
              f'\n  <meta property="og:type" content="article">'
              f'\n  <meta property="og:url" content="https://hurbs.io{canonical}">')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">{canon}{og}
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
    <div class="cta-sub">or (832) 457-4317, Houston, TX</div>
  </section>'''


FOOTER = '''  <footer class="footer">
    <span>© 2026 Hurbs LLC</span>
    <span>Part of the Lepida family</span>
  </footer>
</div>
<script src="/js/main.js"></script>
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
