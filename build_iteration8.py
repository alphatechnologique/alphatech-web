"""HD stills, video-only assets and adaptive favicon."""
from pathlib import Path
import base64,json,re,shutil
import numpy as np
from PIL import Image,ImageDraw
import build_iteration3 as b

def build():
 hd=b.ASSETS/'hd'
 for p in b.PROJECTS:
  key=p['id'];png=hd/f'{key}.png';webp=hd/f'{key}.webp'
  if png.exists():Image.open(png).convert('RGB').save(webp,quality=95,method=6)
  assert webp.exists(),f'Render HD thumbnails first: {key}'
  shutil.copy2(webp,b.ASSETS/f'{key}-solid.webp')
 shutil.copy2(hd/'porsche.webp',b.ASSETS/'porsche-design-solid.webp')
 for key in ['amg','civic']:assert (b.ASSETS/f'{key}-silent.mp4').exists()
 # SVG preserves sharp lettering; photographs are never enlarged beyond source resolution.
 native=Image.open(b.ASSETS/'civic-poster-native.png').convert('RGB');native.save(b.ASSETS/'civic-poster-native.webp',quality=95)
 for en in [False,True]:
  suffix='en' if en else 'es'
  for key,w,h in [('amg',1080,1920),('civic',1080,1440)]:
   picture=hd/'amg-canards.webp' if key=='amg' else b.ASSETS/'civic-poster-native.webp'
   data=base64.b64encode(picture.read_bytes()).decode()
   if key=='amg':
    title='AMG A35';subtitle='AIRFLOW TEST' if en else 'PRUEBA DE AIRE';x,y,iw,ih=40,580,1000,650
    caption='3D reference / on-vehicle test' if en else 'Referencia 3D / prueba en el vehículo'
   else:
    title='CIVIC TYPE R';subtitle='3D SCANNING / POV' if en else 'ESCANEO 3D / POV';iw,ih=native.size;x=(w-iw)//2;y=410
    caption='Rear bumper / scanning process' if en else 'Parachoques trasero / proceso de escaneo'
   svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="#111318"/><path d="M80 150H260" stroke="#ed2924" stroke-width="8"/><g fill="#cbd0d7" font-family="Arial, sans-serif"><text x="80" y="110" font-size="28" letter-spacing="5">ATPERFORMANCE</text><text x="80" y="260" font-size="76" font-weight="700">{title}</text><text x="80" y="330" font-size="34" letter-spacing="3">{subtitle}</text></g><image href="data:image/webp;base64,{data}" x="{x}" y="{y}" width="{iw}" height="{ih}"/><text x="80" y="{h-200}" fill="#cbd0d7" font-family="Arial,sans-serif" font-size="29">{caption}</text><circle cx="130" cy="{h-110}" r="40" fill="#ed2924"/><path d="M120 {h-130}L150 {h-110}L120 {h-90}Z" fill="white"/><text x="200" y="{h-100}" fill="white" font-family="Arial,sans-serif" font-size="32">{'WATCH VIDEO' if en else 'VER VIDEO'}</text></svg>'''
   (b.ASSETS/f'{key}-cover-{suffix}.svg').write_text(svg,encoding='utf-8')
 # Trace the existing emblem alpha silhouette, retaining the Chakana and A.
 im=Image.open(b.ASSETS/'emblem.png').convert('RGBA');alpha=np.array(im.getchannel('A'))>127
 paths=[]
 for y,row in enumerate(alpha):
  edges=np.flatnonzero(np.diff(np.r_[False,row,False].astype(np.int8)))
  for start,end in edges.reshape(-1,2):paths.append(f'M{start} {y+65}h{end-start}v1h-{end-start}z')
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><style>path{fill:#111}@media(prefers-color-scheme:dark){path{fill:#fff}}</style><path d="'+''.join(paths)+'"/></svg>'
 (b.ASSETS/'favicon.svg').write_text(svg,encoding='utf-8')
 fallback=Image.new('RGBA',(512,512),(255,255,255,255));black=Image.new('RGBA',im.size,(0,0,0,255));black.putalpha(im.getchannel('A'));fallback.alpha_composite(black,(0,65));fallback.resize((64,64),Image.Resampling.LANCZOS).save(b.ASSETS/'favicon-fallback.png')
 for file,en in [('index.html',False),('en.html',True)]:
  p=b.SITE/file;s=p.read_text(encoding='utf-8');suffix='en' if en else 'es'
  s=re.sub(r'<link rel="icon"[^>]*>','',s)
  s=s.replace('</head>','<link rel="icon" href="assets/favicon-fallback.png" type="image/png" sizes="64x64"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml" sizes="any"></head>')
  s=s.replace('assets/amg-air-test.mp4','assets/amg-silent.mp4').replace('assets/civic-scan-pov.mp4','assets/civic-silent.mp4')
  s=s.replace('poster="assets/amg-video-poster.webp"',f'poster="assets/amg-cover-{suffix}.svg"').replace('poster="assets/civic-video-poster.webp"',f'poster="assets/civic-cover-{suffix}.svg"')
  s=s.replace('poster="assets/porsche-progress-poster.png"','poster="assets/hd/porsche.webp"')
  s=re.sub(r'<video\b([^>]*)>',lambda m:'<video'+m.group(1)+(' muted' if not re.search(r'\bmuted\b',m.group(1)) else '')+'>',s)
  # Keep a stable, native video shape while the branded cover is visible.
  s=re.sub(r'<video\b[^>]*>.*?</video>',lambda m:m.group(0).replace('class="workshop-video"','class="workshop-video portrait-amg"') if 'amg-silent.mp4' in m.group(0) else m.group(0).replace('class="workshop-video"','class="workshop-video portrait-civic"') if 'civic-silent.mp4' in m.group(0) else m.group(0),s,flags=re.S)
  p.write_text(s,encoding='utf-8')
 print('Iteration 08: HD stills, silent videos, vector covers and adaptive favicon.')

if __name__=='__main__':build()
