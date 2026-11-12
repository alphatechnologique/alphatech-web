from pathlib import Path
from html.parser import HTMLParser
from PIL import Image
import struct,re,xml.etree.ElementTree as ET
root=Path(__file__).parent;site=root/'atperformance';assets=site/'assets'
def atoms(data,start,end):
 while start+8<=end:
  size,kind=struct.unpack_from('>I4s',data,start);head=8
  if size==1:size=struct.unpack_from('>Q',data,start+8)[0];head=16
  if size==0:size=end-start
  assert size>=head and start+size<=end
  yield kind,start+head,start+size
  start+=size
def descend(data,start,end):
 for kind,a,z in atoms(data,start,end):
  yield kind,a,z
  if kind in (b'moov',b'trak',b'mdia',b'minf',b'stbl'):yield from descend(data,a,z)
for name,expected in [('amg-silent.mp4',425/30),('civic-silent.mp4',180),('porsche-dashboard-progress-20-28.mp4',8)]:
 raw=(assets/name).read_bytes();handlers=[];duration=None
 for kind,a,z in descend(raw,0,len(raw)):
  if kind==b'hdlr':handlers.append(raw[a+8:a+12])
  if kind==b'mvhd':
   version=raw[a];offset=a+(20 if version else 12)
   timescale=struct.unpack_from('>I',raw,offset)[0]
   length=struct.unpack_from('>Q' if version else '>I',raw,offset+4)[0];duration=length/timescale
 assert b'soun' not in handlers and b'vide' in handlers,(name,handlers)
 assert abs(duration-expected)<.04,(name,duration)
 print(name,'PASS: no audio track;',duration,'seconds')
for p in (assets/'hd').glob('*.webp'):assert Image.open(p).size==(1920,1248)
for file in ['index.html','en.html']:
 text=(site/file).read_text(encoding='utf-8')
 videos=re.findall(r'<video\b[^>]*>.*?</video>',text,re.S);assert len(videos)==3
 for video in videos:
  assert ' muted' in video.split('>')[0]
  poster=re.search(r'poster="([^"]+)"',video).group(1);assert (site/poster).exists()
 assert 'assets/amg-air-test.mp4' not in text and 'assets/civic-scan-pov.mp4' not in text
 assert text.count('href="assets/favicon.svg"')==1
 print(file,'PASS: silent sources, poster assets and adaptive favicon')
svg=(assets/'favicon.svg').read_text();ET.fromstring(svg);assert 'prefers-color-scheme:dark' in svg and 'fill:#111' in svg and 'fill:#fff' in svg
for p in assets.glob('*-cover-*.svg'):ET.fromstring(p.read_text(encoding='utf-8'))
print('PASS: 1920 x 1248 stills, valid SVG covers and light/dark favicon styles.')
