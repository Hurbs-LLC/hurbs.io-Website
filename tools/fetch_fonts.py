"""One-time: download the Google Fonts woff2 files (latin + latin-ext subsets)
and emit tools/fontfaces.css with local /fonts/ URLs. Fonts are OFL-licensed.
Requires /tmp/gfonts.css fetched from the css2 URL with a woff2-capable UA."""
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(HERE, '..', 'public', 'fonts')
os.makedirs(FONTS_DIR, exist_ok=True)

css = open('/tmp/gfonts.css', encoding='utf-8').read()

# Blocks are preceded by a /* subset */ comment
out = []
seen = {}
for m in re.finditer(r'/\* (\S+) \*/\s*(@font-face \{[^}]+\})', css):
    subset, block = m.group(1), m.group(2)
    if subset not in ('latin', 'latin-ext'):
        continue
    url = re.search(r'url\((https://[^)]+\.woff2)\)', block).group(1)
    family = re.search(r"font-family: '([^']+)'", block).group(1)
    weight = re.search(r'font-weight: ([\d ]+);', block).group(1).replace(' ', '-')
    fname = f"{family.lower().replace(' ', '-')}-{weight}-{subset}.woff2"
    if url not in seen:
        subprocess.run(['curl', '-sf', '-o', os.path.join(FONTS_DIR, fname), url], check=True)
        seen[url] = fname
        print('downloaded', fname)
    block = block.replace(url, '/fonts/' + seen[url])
    out.append(f'/* {subset} */\n{block}')

with open(os.path.join(HERE, 'fontfaces.css'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(out) + '\n')
print(f'{len(out)} font-face rules -> tools/fontfaces.css')
