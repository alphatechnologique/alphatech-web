from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,math

root=Path(__file__).parent
site=root/'atperformance'
expected={'amg-canards','civic','vw-wheel','porsche-wheel','porsche','case','kicks-console','kicks-center'}
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.refs=[];self.projects=[];self.cards=0;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for key in ('src','href'):
   if a.get(key):self.refs.append(a[key])
  if a.get('data-open-model'):self.projects.append(a['data-open-model'])
  if tag=='article' and a.get('class')=='project':self.cards+=1
for path in site.glob('*.html'):
 text=path.read_text(encoding='utf-8');p=Page(text)
 assert p.cards==8 and set(p.projects)==expected
 assert len(p.ids)==len(set(p.ids))
 assert 'AMG A35' in text and 'assets/models.js' not in text
 assert '\ufffd' not in text
 assert text.count('<dialog ')==1
 assert 'width="110" height="110"' in text
 for ref in p.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  if u.path:assert (path.parent/unquote(u.path)).is_file(),(path,ref)
  elif u.fragment:assert u.fragment in p.ids,(path,ref)
 print(path.name,': eight project cards, modal, assets, anchors and UTF-8 OK')
manifest=json.loads((site/'assets/projects.js').read_text(encoding='utf-8').split('=',1)[1].rstrip(';'))
assert {p['id'] for p in manifest}==expected
total=0
for key in sorted(expected):
 path=site/'assets/models'/f'{key}.js'
 raw=path.read_text(encoding='utf-8')
 data=json.loads(raw.split(']=',1)[1].rstrip(';'))
 layers=data.get('layers',[data])
 if key=='porsche':assert {layer['id'] for layer in layers}=={'scan','design'}
 face_count=0
 for layer in layers:
  v=layer['vertices'];indices=layer['indices']
  assert len(v)%3==0 and len(indices)%3==0
  assert all(math.isfinite(n) for n in v)
  assert min(indices)>=0 and max(indices)<len(v)//3
  face_count+=len(indices)//3
 assert (site/'assets'/f'{key}-solid.webp').exists()
 total+=path.stat().st_size
 print(key,':',face_count,'triangles')
assert total<25*1024*1024
print('Total geometry: %.2f MB, loaded on demand.'%(total/1024/1024))
print('PASS. GPU shader execution and browser UI validation require a browser and remain unverified in this session.')
