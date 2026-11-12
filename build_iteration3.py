"""Build local portfolio from real STL/PLY files; no network dependencies."""
from pathlib import Path
import json, re, struct, shutil, html
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).parent
SITE=ROOT/'atperformance'
ASSETS=SITE/'assets'
BASE=Path(r'C:\Users\MS1\Documents\Alpha tech Proyectos')
MODELS=ASSETS/'models'
MODELS.mkdir(exist_ok=True)
PROJECTS=[
 dict(id='amg-canards',es='AMG A35 · Canards v5',en='AMG A35 · Canards v5',source=r'D:\Dynabook doc\Alpha Tech Solutions\Proyectos\AMG 35\canard\Canard v5\canard v5 w front.stl',description_es='Desarrollo aerodinámico específico para el AMG A35. Diseño y cálculo orientados al rendimiento; geometría v5 en desarrollo.',description_en='A dedicated aerodynamic development for the AMG A35. Performance-oriented design and calculation; v5 geometry in development.'),
 dict(id='civic',es='Espejos Honda Civic Type R',en='Honda Civic Type R mirrors',source='Honda civic Type R/honda civic type r espejos.stl',done=True,description_es='Cubreespejos revestidos en fibra de carbono. Proyecto de skinning terminado; explora la geometría de referencia.',description_en='Carbon fibre mirror-cover skinning. Completed project; explore the reference geometry.'),
 dict(id='vw-wheel',es='Volante Volkswagen',en='Volkswagen steering wheel',source='porsche 924 board/Volante VW scan.stl',description_es='Escaneo disponible del volante Volkswagen como base para el desarrollo a medida.',description_en='Volkswagen steering-wheel scan available as a reference for bespoke development.'),
 dict(id='porsche-wheel',es='Volante Porsche',en='Porsche steering wheel',source='porsche 924 board/volante porsche simpl.stl',description_es='Geometría del volante Porsche. Escaneo disponible y proyecto en desarrollo.',description_en='Porsche steering-wheel geometry. Scan available; project in development.'),
 dict(id='porsche',es='Tablero Porsche 924',en='Porsche 924 dashboard',source='porsche 924 board/pSGC3_tyR7_7htk_I2XC/result/Mesh.ply',description_es='Escaneo del tablero, diseño y planos en proceso para un interior con identidad propia.',description_en='Dashboard scan, design and drawings in progress for an interior with its own identity.'),
 dict(id='case',es='Case para fibra',en='Composite case',source='case para fibra/case para fibra.stl',description_es='Geometría de referencia para el desarrollo de un case en fibra. Proyecto en proceso.',description_en='Reference geometry for a composite case. Project in development.'),
 dict(id='kicks-console',es='Consola Nissan Kicks',en='Nissan Kicks console',source='consola kicks/sVsOq9H_a0Q73X_s3ceL4_QoxvJh/result/Fused.ply',description_es='Escaneo de la consola Nissan Kicks. Referencia para estudiar formas, ajustes y acabados.',description_en='Nissan Kicks console scan. A reference for studying shapes, fit and finishes.'),
 dict(id='kicks-center',es='Consola central Nissan Kicks',en='Nissan Kicks centre console',source='consola central/pgKn4_9rtk_ofe7_oonK/result/Mesh.ply',description_es='Malla de la consola central Nissan Kicks. Escaneo disponible para el desarrollo del proyecto.',description_en='Nissan Kicks centre-console mesh. Scan available for project development.')
]

def read_mesh(path):
 if path.suffix.lower()=='.stl':
  raw=path.read_bytes(); n=struct.unpack_from('<I',raw,80)[0]
  if len(raw)==84+n*50:
   records=np.frombuffer(raw,dtype=np.dtype([('normal','<f4',3),('vertices','<f4',(3,3)),('attr','<u2')]),offset=84)
   v=records['vertices'].reshape(-1,3).astype(np.float64)
  else:
   v=np.array(re.findall(rb'vertex\s+([-+\deE.]+)\s+([-+\deE.]+)\s+([-+\deE.]+)',raw),dtype=np.float64)
  assert len(v)%3==0 and len(v)>0
  return v,np.arange(len(v),dtype=np.int32).reshape(-1,3)
 with path.open('rb') as f:
  lines=[]
  while True:
   line=f.readline().decode('ascii').strip();lines.append(line)
   if line=='end_header':break
  offset=f.tell()
 assert 'format binary_little_endian 1.0' in lines
 nv=int(next(s.split()[-1] for s in lines if s.startswith('element vertex')))
 nf=int(next(s.split()[-1] for s in lines if s.startswith('element face')))
 props=[]; section=None
 types={'float':'<f4','double':'<f8','uchar':'u1','uint8':'u1','int':'<i4'}
 for line in lines:
  if line.startswith('element '):section=line.split()[1]
  if line.startswith('property ') and section=='vertex':
   _,typ,name=line.split();props.append((name,types[typ]))
 dtype=np.dtype(props)
 vertices=np.memmap(path,dtype=dtype,mode='r',offset=offset,shape=(nv,))
 v=np.column_stack([vertices[c] for c in 'xyz']).astype(np.float64)
 fdtype=np.dtype([('count','u1'),('indices','<i4',3)])
 faces=np.memmap(path,dtype=fdtype,mode='r',offset=offset+nv*dtype.itemsize,shape=(nf,))
 assert np.all(faces['count']==3),'Non-triangular PLY'
 return v,faces['indices'].copy()

def simplify(v,faces,normalized=False):
 assert np.isfinite(v).all()
 if not normalized:
  v-=v.mean(axis=0)
  _,basis=np.linalg.eigh(np.cov(v[::max(1,len(v)//40000)].T))
  # Principal plane faces the camera: longest dimension horizontal.
  v=v@basis[:,[2,1,0]]
  v-=(v.min(axis=0)+v.max(axis=0))/2
  v/=np.ptp(v,axis=0).max()
 cells=np.round(v/.0075).astype(np.int32)
 _,inverse=np.unique(cells,axis=0,return_inverse=True)
 counts=np.bincount(inverse)
 verts=np.column_stack([np.bincount(inverse,weights=v[:,a])/counts for a in range(3)])
 indices=inverse[faces]
 indices=indices[(indices[:,0]!=indices[:,1])&(indices[:,1]!=indices[:,2])&(indices[:,0]!=indices[:,2])]
 _,keep=np.unique(np.sort(indices,axis=1),axis=0,return_index=True)
 indices=indices[keep]
 tri=verts[indices]
 area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)
 indices=indices[area>1e-10]
 return np.round(verts,5),indices

def preview(v,faces,path,yaw=.18,pitch=-.12):
 # Painter projection for static thumbnails. Interactive viewer uses GPU depth buffering.
 ry=np.array([[np.cos(yaw),0,np.sin(yaw)],[0,1,0],[-np.sin(yaw),0,np.cos(yaw)]])
 rx=np.array([[1,0,0],[0,np.cos(pitch),-np.sin(pitch)],[0,np.sin(pitch),np.cos(pitch)]])
 transformed=v@ry.T@rx.T
 tri=transformed[faces]
 norms=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norms/=np.maximum(np.linalg.norm(norms,axis=1)[:,None],1e-12)
 norms[norms[:,2]<0]*=-1
 light=np.array([-.4,.65,1]);light/=np.linalg.norm(light)
 shade=.25+.65*np.maximum(0,norms@light)+.1*np.maximum(0,norms@np.array([.8,.1,.6]))
 # Preserve proportions and centre all geometries in the frame.
 span=np.ptp(transformed[:,:2],axis=0);scale=min(850/max(span[0],.01),510/max(span[1],.01))
 xy=np.stack([500+transformed[:,0]*scale,325-transformed[:,1]*scale],axis=1)
 im=Image.new('RGB',(1000,650),(18,20,24));d=ImageDraw.Draw(im)
 for idx in np.argsort(tri[:,:,2].mean(axis=1)):
  c=int(np.clip(shade[idx]*220,45,235));d.polygon([tuple(x) for x in xy[faces[idx]]],fill=(int(c*.93),int(c*.97),c))
 im.save(path,quality=88)

def build_geometry():
 manifest=[]
 for project in PROJECTS:
  source=BASE/project['source'];target=MODELS/(project['id']+'.js')
  cached=MODELS/(project['id']+'.meta.json')
  signature={'source':str(source),'mtime_ns':source.stat().st_mtime_ns,'version':4}
  if target.exists() and cached.exists() and json.loads(cached.read_text()).get('signature')==signature:
   print('Cached',project['id'],flush=True);continue
  v,f=read_mesh(source);nv,nf=len(v),len(f)
  v,f=simplify(v,f)
  payload={'vertices':v.reshape(-1).tolist(),'indices':f.reshape(-1).tolist()}
  target.write_text('window.ATP_GEOMETRY=window.ATP_GEOMETRY||{};window.ATP_GEOMETRY['+json.dumps(project['id'])+']='+json.dumps(payload,separators=(',',':'))+';',encoding='utf-8')
  angles={'case':[3.79,-.35],'civic':[3.32,-.15]}.get(project['id'],[.18,-.12])
  preview(v,f,ASSETS/(project['id']+'-solid.webp'),*angles)
  record={'signature':signature,'original_vertices':nv,'original_faces':nf,'web_vertices':len(v),'web_faces':len(f)}
  cached.write_text(json.dumps(record,indent=2),encoding='utf-8')
  print(project['id'],nf,'->',len(f),'faces',flush=True)
 public=[{**{k:p[k] for k in ['id','es','en']},'view':{'case':[3.79,-.35],'civic':[3.32,-.15]}.get(p['id'],[.18,-.12])} for p in PROJECTS]
 (ASSETS/'projects.js').write_text('window.ATP_PROJECTS='+json.dumps(public,ensure_ascii=False)+';',encoding='utf-8')

def build_pages():
 for filename,en in [('index.html',False),('en.html',True)]:
  t=lambda es,eng:eng if en else es
  path=SITE/filename;text=path.read_text(encoding='utf-8')
  text=text.replace('<script defer src="assets/models.js"></script>','<script defer src="assets/projects.js"></script>')
  if 'src="viewer.js"' not in text:text=text.replace('<script defer src="app.js"></script>','<script defer src="app.js"></script><script defer src="viewer.js"></script>')
  text=re.sub(r'<img src="assets/emblem.png"[^>]*>','<img src="assets/emblem.png" alt="ATPerformance" width="110" height="110">',text,count=1)
  cards=[]
  for i,p in enumerate(PROJECTS,1):
   title=p['en' if en else 'es'];description=p['description_en' if en else 'description_es']
   img='civic-mirrors-white.png' if p['id']=='civic' else p['id']+'-solid.webp'
   status=t('TERMINADO · SKINNING','COMPLETED · SKINNING') if p.get('done') else t('ESCANEO DISPONIBLE · EN DESARROLLO','SCAN AVAILABLE · IN DEVELOPMENT')
   cards.append(f'''<article class="project"><button type="button" class="project-image" data-open-model="{p['id']}" aria-label="{t('Explorar','Explore')} {title} {t('en 3D','in 3D')}"><img src="assets/{img}" alt="{title}" loading="lazy"><span class="badge">{status}</span><span class="image-action">{t('Abrir modelo 3D','Open 3D model')} ↗</span></button><p class="eyebrow">{i:02d} / {t('DEL ESCANEO AL PROYECTO','FROM SCAN TO BUILD')}</p><h3>{title}</h3><p>{description}</p><button type="button" class="textlink model-link" data-open-model="{p['id']}">{t('Explorar en ventana ampliada','Explore in expanded view')} ↗</button></article>''')
  text=re.sub(r'<div class="project-grid">.*?</div></section>',lambda _:'<div class="project-grid">'+''.join(cards)+'</div></section>',text,count=1,flags=re.S)
  viewer=f'''<div class="viewer scan-preview"><img src="assets/vw-wheel-solid.webp" alt="{t('Vista sombreada del escaneo del volante Volkswagen','Shaded Volkswagen steering-wheel scan')}" loading="lazy"><div class="scan-preview-caption"><p class="eyebrow">3D / {t('SUPERFICIE E ILUMINACIÓN','SURFACE & LIGHTING')}</p><h3>{t('La forma, con claridad.','See the shape clearly.')}</h3><p>{t('Gira, acerca y activa la malla sobre una superficie sólida.','Rotate, zoom and reveal the mesh over a solid surface.')}</p><button class="button red" data-open-model="vw-wheel">{t('Explorar los siete modelos','Explore all seven models')} ↗</button></div></div>'''
  text=re.sub(r'<div class="viewer-layout">.*?<div class="scan-copy">',lambda _:'<div class="viewer-layout">'+viewer+'<div class="scan-copy">',text,count=1,flags=re.S)
  text=re.sub(r'<dialog id="model-dialog".*?</dialog>','',text,flags=re.S)
  options=''.join(f'<option value="{p["id"]}">{html.escape(p["en" if en else "es"])}</option>' for p in PROJECTS)
  dialog=f'''<dialog id="model-dialog" aria-labelledby="viewer-title"><div class="modal-header"><div><p class="eyebrow">ATPERFORMANCE / DIGITAL WORKSHOP</p><h2 id="viewer-title">{t('Explorar proyecto','Explore project')}</h2></div><button id="close-model" class="close-model" aria-label="{t('Cerrar visor','Close viewer')}">✕</button></div><div class="viewer-toolbar"><label for="model-select">{t('Proyecto','Project')}</label><select id="model-select">{options}</select><button id="mesh-toggle" aria-pressed="false">{t('Mostrar malla','Show mesh')}</button><button id="reset-model">{t('Restablecer','Reset view')}</button><button id="zoom-out" aria-label="{t('Alejar','Zoom out')}">−</button><button id="zoom-in" aria-label="{t('Acercar','Zoom in')}">+</button></div><div class="canvas-stage"><canvas id="model" tabindex="0" aria-label="{t('Modelo 3D. Arrastra para girar, usa las flechas o los controles de zoom.','3D model. Drag to rotate, use arrow keys or zoom controls.')}"></canvas><img id="viewer-fallback" alt="{t('Vista estática del proyecto','Static project view')}" hidden><p id="viewer-status" role="status" aria-live="polite"></p></div><div class="modal-footer"><span>{t('Arrastra para girar · Rueda o + / − para zoom · Esc para cerrar','Drag to rotate · Wheel or + / − to zoom · Esc to close')}</span><span>{t('Geometría simplificada de referencia','Simplified reference geometry')}</span></div></dialog>'''
  text=text.replace('</body>',dialog+'</body>')
  text=text.replace('<small>ENGINEERED. BUILT. DRIVEN.</small>','<small class="brand-tagline"><span>ENGINEERED.</span> <span class="tagline-red">BUILT.</span> <span>DRIVEN.</span></small>')
  path.write_text(text,encoding='utf-8')

if __name__=='__main__':
 build_geometry()
 shutil.copy2(Path(r'D:\Dynabook doc\Documents\Alpha Tech Performance\06-ATP-Marketing\02-Logos\04-Versiones-Mono\ATP-Emblema-Blanco_512px.png'),ASSETS/'emblem.png')
 build_pages()
 print('Iteration 03 built.',flush=True)
