from pathlib import Path
import json,re,shutil
import numpy as np
import build_iteration3 as b

def build():
 scan_path=b.BASE/'porsche 924 board/porsche 924 board nu 2.stl'
 design_path=b.BASE/'porsche 924 board/porsche dashboard 1 complet.stl'
 scan,sf=b.read_mesh(scan_path);design,df=b.read_mesh(design_path)
 # Rigid visual registration, reviewed against the 20-28 second reference.
 # Row vectors: registered_design = design @ R + t. No independent scaling.
 alignment=json.loads((b.ROOT/'PORSCHE-REGISTRATION.json').read_text())
 design=design@np.array(alignment['rotation'])+np.array(alignment['translation'])
 angle=.35
 rotation=np.array([[-1,0,0],[0,-np.sin(angle),np.cos(angle)],[0,np.cos(angle),np.sin(angle)]])
 scan=scan@rotation;design=design@rotation
 lo=np.minimum(scan.min(0),design.min(0));hi=np.maximum(scan.max(0),design.max(0))
 centre=(lo+hi)/2;scale=max(hi-lo)
 scan=(scan-centre)/scale;design=(design-centre)/scale
 scan,sf=b.simplify(scan,sf,normalized=True);design,df=b.simplify(design,df,normalized=True)
 layers=[{'id':'scan','vertices':scan.reshape(-1).tolist(),'indices':sf.reshape(-1).tolist()}, {'id':'design','vertices':design.reshape(-1).tolist(),'indices':df.reshape(-1).tolist()}]
 payload={'layers':layers}
 (b.MODELS/'porsche.js').write_text('window.ATP_GEOMETRY=window.ATP_GEOMETRY||{};window.ATP_GEOMETRY["porsche"]='+json.dumps(payload,separators=(',',':'))+';',encoding='utf-8')
 b.preview(design,df,b.ASSETS/'porsche-design-solid.webp')
 b.preview(scan,sf,b.ASSETS/'porsche-scan-solid.webp')
 shutil.copy2(b.ASSETS/'porsche-design-solid.webp',b.ASSETS/'porsche-solid.webp')
 assert (b.ASSETS/'porsche-dashboard-progress-20-28.mp4').is_file(),'Generate the trimmed video with trim_dashboard_video.py in Blender first.'
 report={'scan_source':str(scan_path),'design_source':str(design_path),'orientation':rotation.tolist(),'centre_after_rotation':centre.tolist(),'scale':float(scale),'design_registration':alignment,'registration':'Approximate rigid visual registration reviewed against video. No nonuniform scaling, no mechanical tolerance validation.'}
 (b.ROOT/'PORSCHE-COORDINATES.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 for name,en in [('index.html',False),('en.html',True)]:
  t=lambda es,english:english if en else es
  path=b.SITE/name;text=path.read_text(encoding='utf-8')
  text=re.sub(r'<section id="porsche-progress".*?</section>','',text,flags=re.S)
  section=f'''<section id="porsche-progress" class="section porsche-progress"><div class="section-heading"><div><p class="eyebrow">PORSCHE 924 / DESIGN IN PROGRESS</p><h2>{t('Del escaneo al nuevo tablero.','From scan to a new dashboard.')}</h2></div><p>{t('Animación del diseño v1: una mirada al avance del proyecto y a la geometría propuesta sobre el escaneo.','Design v1 animation: a look at project progress and the proposed geometry over the scan.')}</p></div><video controls playsinline preload="metadata" poster="assets/porsche-progress-poster.png" aria-label="{t('Animación del avance del tablero Porsche, versión 1','Porsche dashboard design progress animation, version 1')}"><source src="assets/porsche-dashboard-progress-20-28.mp4" type="video/mp4"><a href="assets/porsche-dashboard-progress-20-28.mp4">{t('Abrir video','Open video')}</a></video><div class="progress-actions"><p class="fine">{t('Diseño en desarrollo. La animación no representa una pieza terminada.','Design in development. The animation does not represent a finished part.')}</p><button class="button" data-open-model="porsche">{t('Comparar escaneo y diseño en 3D','Compare scan and design in 3D')} ↗</button></div></section>'''
  text=text.replace('<section id="scan"',section+'<section id="scan"',1)
  # Quick path from the dashboard project card to its animation.
  pattern=r'(<article class="project">.*?<h3>'+re.escape(t('Tablero Porsche 924','Porsche 924 dashboard'))+r'</h3>.*?)</article>'
  # Bound the match to a single card, avoiding earlier project articles.
  text=re.sub(r'<article class="project">.*?</article>',lambda m:m.group(0).replace('</article>',f'<a class="textlink progress-link" href="#porsche-progress">{t("Ver animación del avance","Watch progress animation")} ↗</a></article>') if ('<h3>'+t('Tablero Porsche 924','Porsche 924 dashboard')+'</h3>') in m.group(0) and 'progress-link' not in m.group(0) else m.group(0),text,flags=re.S)
  text=re.sub(r'<div id="porsche-layers".*?</div><!-- /porsche-layers -->','',text,flags=re.S)
  controls=f'''<div id="porsche-layers" class="porsche-layer-controls" hidden><div role="group" aria-label="{t('Capas del tablero Porsche','Porsche dashboard layers')}"><button data-layer="scan" aria-pressed="false">{t('Escaneo','Scan')}</button><button data-layer="design" aria-pressed="false">{t('Diseño','Design')}</button><button data-layer="both" aria-pressed="true">{t('Ambos','Both')}</button></div><label for="design-opacity">{t('Opacidad del diseño','Design opacity')} <input id="design-opacity" type="range" min="15" max="100" value="75"></label><p class="fine">{t('Gris: escaneo · Rojo: diseño. Alineación visual aproximada; escala relativa conservada. Sin validación de tolerancias de fabricación.','Grey: scan · Red: design. Approximate visual alignment; relative scale preserved. Manufacturing tolerances have not been validated.')}</p></div><!-- /porsche-layers -->'''
  text=text.replace('<div class="canvas-stage">',controls+'<div class="canvas-stage">',1)
  path.write_text(text,encoding='utf-8')
 print('Trimmed Porsche video retained; registered layers built:',len(sf),len(df),'triangles',flush=True)

if __name__=='__main__':build()
