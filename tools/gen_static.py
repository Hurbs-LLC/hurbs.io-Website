"""Build public/{index,about,contact,404}.html from tools/pages/ templates,
substituting the inlined asset block and JS from common.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import FONTS, JS

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

for name in ('index', 'about', 'contact', '404'):
    src = open(os.path.join(HERE, 'pages', name + '.html'), encoding='utf-8').read()
    out = src.replace('{{ASSETS}}', FONTS).replace('{{JS}}', JS)
    with open(os.path.join(REPO, 'public', name + '.html'), 'w', encoding='utf-8') as f:
        f.write(out)
    print('wrote public/' + name + '.html')
