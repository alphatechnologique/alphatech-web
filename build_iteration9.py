"""Integrate the approved ATP covers and improve header readability."""
from pathlib import Path
import re
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parent
SITE = ROOT / 'atperformance'
ASSETS = SITE / 'assets'
SOURCE = ASSETS / 'approved-video-covers.png'

def build():
    incoming = ROOT.parent / 'portadas-atp.png'
    if incoming.exists():
        shutil.copy2(incoming, SOURCE)
    with Image.open(SOURCE) as original:
        w, h = original.size
        for i, key in enumerate(('amg', 'civic', 'porsche')):
            # Separate the approved panels without retouching their content.
            left, right = round(i*w/3), round((i+1)*w/3)
            original.crop((left, 0, right, h)).convert('RGB').save(
                ASSETS / f'{key}-cover-approved.webp', quality=95, method=6)
    for filename in ('index.html', 'en.html'):
        path = SITE / filename
        content = path.read_text(encoding='utf-8')
        def update_video(match):
            block = match.group(0)
            key = next((k for k in ('amg', 'civic', 'porsche')
                        if f'assets/{k}-' in block), None)
            if key is None:
                return block
            block = re.sub(r'poster="[^"]*"',
                           f'poster="assets/{key}-cover-approved.webp"', block)
            return block
        content = re.sub(r'<video\b[^>]*>.*?</video>', update_video,
                         content, flags=re.S)
        path.write_text(content, encoding='utf-8')
    path = SITE / 'style.css'
    css = path.read_text(encoding='utf-8')
    css = re.sub(r'/\* Iteration 09 \*/.*?/\* End iteration 09 \*/', '', css, flags=re.S)
    css += '''
/* Iteration 09 */
header nav{font-size:14px}
header .language{font-size:13px}
video[poster$="-cover-approved.webp"],.workshop-video[poster$="-cover-approved.webp"]{aspect-ratio:1/1;object-fit:contain;height:auto}
.porsche-progress video[poster$="-cover-approved.webp"]{max-width:650px;max-height:none;margin-inline:auto}
@media(max-width:650px){header nav{font-size:15px}header .language{font-size:12px}}
/* End iteration 09 */
'''
    path.write_text(css, encoding='utf-8')
    print('Iteration 09: three approved covers integrated in ES/EN; header enlarged.')

if __name__ == '__main__':
    build()
