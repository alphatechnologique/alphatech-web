"""Project stories and contextual quote entry points; runs after base + Porsche."""
from pathlib import Path
import re,json,html
import numpy as np
import build_iteration3 as b

def build():
 # Refresh case thumbnail even when its geometry is cached.
 raw=(b.MODELS/'case.js').read_text(encoding='utf-8')
 data=json.loads(raw.split(']=',1)[1].rstrip(';'))
 b.preview(np.array(data['vertices']).reshape(-1,3),np.array(data['indices']).reshape(-1,3),b.ASSETS/'case-solid.webp',3.79,-.35)
 left=Path(r'D:\Dynabook doc\Alpha Tech Solutions\Proyectos\AMG 35\canard\Canard v5\STL\canard v5 izquierdo corr.stl')
 v,f=b.read_mesh(left);v,f=b.simplify(v,f);b.preview(v,f,b.ASSETS/'amg-canards-left.webp')
 types={'amg-canards':'aero','civic':'carbon','vw-wheel':'wheel','porsche-wheel':'wheel','porsche':'dashboard','case':'case','kicks-console':'console','kicks-center':'console'}
 for file,en in [('index.html',False),('en.html',True)]:
  t=lambda es,eng:eng if en else es
  path=b.SITE/file;s=path.read_text(encoding='utf-8')
  def quote(service,reference,label):
   return f'<a class="button quote-project" href="#contact" data-service="{service}" data-reference="{html.escape(reference,quote=True)}">{label} ↗</a>'
  def card(m):
   text=m.group(0);key=re.search(r'data-open-model="([^"]+)"',text).group(1)
   title=re.search(r'<h3>(.*?)</h3>',text).group(1)
   text=re.sub(r'<a class="button quote-project".*?</a>','',text)
   if key=='amg-canards':text=re.sub(r'<span class="badge">.*?</span>',f'<span class="badge">{t("DESARROLLO AERODINÁMICO · V5","AERODYNAMIC DEVELOPMENT · V5")}</span>',text,count=1)
   text=text.replace('</article>',quote(types[key],title,t('Cotizar un proyecto similar','Quote a similar project'))+'</article>')
   return text
  s=re.sub(r'<article class="project">.*?</article>',card,s,flags=re.S)
  s=re.sub(r'<section id="featured-builds".*?</section>','',s,flags=re.S)
  s=re.sub(r'<section id="amg-development".*?</section>','',s,flags=re.S)
  s=re.sub(r'<section id="civic-story".*?</section>','',s,flags=re.S)
  features=f'''<section id="featured-builds" class="section featured-builds"><p class="eyebrow">ATPERFORMANCE / ENGINEERING STORIES</p><h2>{t('Dos retos. Ingeniería propia.','Two challenges. Our own engineering.')}</h2><div class="story-grid">
<article class="story-card"><a href="#amg-development" class="story-image"><img src="assets/amg-canards-solid.webp" alt="{t('Geometría real del canard v5 para AMG A35','Actual AMG A35 v5 canard geometry')}" loading="lazy"></a><div class="story-body"><p class="eyebrow">AMG A35 / AERODYNAMICS</p><h3>{t('Diseñado para este AMG.','Designed for this AMG.')}</h3><p>{t('Un desarrollo específico de canards, con diseño y cálculo orientados al rendimiento aerodinámico del A35.','A dedicated canard development, with design and calculation focused on A35 aerodynamic performance.')}</p><a class="textlink" href="#amg-development">{t('Conocer el desarrollo v5','Explore the v5 development')} →</a></div></article>
<article class="story-card"><a href="#porsche-progress" class="story-image"><img src="assets/porsche-progress-poster.png" alt="{t('Diseño del tablero Porsche sobre el escaneo','Porsche dashboard design over the scan')}" loading="lazy"></a><div class="story-body"><p class="eyebrow">PORSCHE 924 / BESPOKE INTERIOR</p><h3>{t('Un interior con identidad propia.','An interior with its own identity.')}</h3><p>{t('Del escaneo del habitáculo al diseño de un tablero y consola propios. Sigue la evolución y compara las geometrías.','From cockpit scan to a bespoke dashboard and console. Follow the progress and compare the geometries.')}</p><a class="textlink" href="#porsche-progress">{t('Ver la evolución del Porsche','Follow the Porsche development')} →</a></div></article></div></section>'''
  s=s.replace('<section id="projects"',features+'<section id="projects"',1)
  amg=f'''<section id="amg-development" class="section engineering-story"><div class="section-heading"><div><p class="eyebrow">AMG A35 / CANARDS V5</p><h2>{t('La forma responde a un objetivo.','Shape follows a purpose.')}</h2></div><p>{t('Proyecto de ingeniería aerodinámica propio, desarrollado específicamente para el Mercedes-AMG A35. Diseño y cálculo para orientar la geometría hacia el rendimiento del vehículo.','Our own aerodynamic engineering project, developed specifically for the Mercedes-AMG A35. Design and calculation guide the geometry towards vehicle performance.')}</p></div><div class="canard-pair"><figure><img src="assets/amg-canards-solid.webp" alt="{t('Canard derecho v5 corregido','Corrected v5 right canard')}" loading="lazy"><figcaption>{t('Derecho · geometría v5 corregida','Right · corrected v5 geometry')}</figcaption></figure><figure><img src="assets/amg-canards-left.webp" alt="{t('Canard izquierdo v5 corregido','Corrected v5 left canard')}" loading="lazy"><figcaption>{t('Izquierdo · geometría v5 corregida','Left · corrected v5 geometry')}</figcaption></figure></div><div class="story-facts"><div><strong>01 / {t('APLICACIÓN','APPLICATION')}</strong><p>Mercedes-AMG A35</p></div><div><strong>02 / {t('DESARROLLO','DEVELOPMENT')}</strong><p>{t('Diseño propio y cálculo aerodinámico','Original design and aerodynamic calculation')}</p></div><div><strong>03 / {t('AVANCE MOSTRADO','CURRENT PREVIEW')}</strong><p>{t('Geometrías CAD v5 · proyecto en desarrollo','V5 CAD geometries · project in development')}</p></div></div><div class="actions"><button class="button" data-open-model="amg-canards">{t('Explorar canard derecho en 3D','Explore the right canard in 3D')}</button>{quote('aero','AMG A35 · Canards v5',t('Cotizar desarrollo aerodinámico','Request an aerodynamic development quote'))}</div><p class="fine">{t('Visualización del diseño. No representa una pieza terminada ni una medición de rendimiento en pista.','Design preview. It does not represent a finished part or track-measured performance.')}</p></section>'''
  civic=f'''<section id="civic-story" class="section civic-story"><div class="civic-layout"><img src="assets/civic-mirrors-white.png" alt="{t('Cubreespejos Honda Civic Type R terminados, sobre fondo blanco','Completed Honda Civic Type R mirror covers on white background')}" loading="lazy"><div><p class="eyebrow">HONDA CIVIC TYPE R / {t('TERMINADO','COMPLETED')}</p><h2>{t('Un acabado terminado. Un resultado real.','A finished piece. A real result.')}</h2><p>{t('Cubreespejos terminados mediante skinning: revestimiento en fibra de carbono sobre la pieza base. Un proyecto de acabado, con la geometría original como punto de partida.','Completed mirror covers made using skinning: a carbon-fibre covering over the base part. A finish-focused project using the original geometry as its starting point.')}</p><div class="story-facts"><div><strong>{t('PROCESO','PROCESS')}</strong><p>Skinning</p></div><div><strong>{t('ESTADO','STATUS')}</strong><p>{t('Terminado','Completed')}</p></div></div>{quote('carbon','Honda Civic Type R · Skinning',t('Cotizar skinning para mi vehículo','Quote skinning for my vehicle'))}</div></div></section>'''
  s=s.replace('<section id="porsche-progress"',amg+civic+'<section id="porsche-progress"',1)
  s=re.sub(r'<div class="porsche-milestones">.*?</div><!-- milestones -->','',s,flags=re.S)
  milestones=f'''<div class="porsche-milestones"><ol class="milestones"><li><strong>01 / {t('Escaneo','Scan')}</strong><span>{t('Referencia del habitáculo','Cockpit reference')}</span></li><li class="current"><strong>02 / {t('Diseño','Design')}</strong><span>{t('Tablero y consola · en desarrollo','Dashboard and console · in development')}</span></li><li><strong>03 / {t('Fabricación','Manufacture')}</strong><span>{t('Próxima etapa','Next stage')}</span></li><li><strong>04 / {t('Acabado','Finish')}</strong><span>{t('Por definir','To be defined')}</span></li></ol>{quote('dashboard','Porsche 924 · Dashboard',t('Cotizar un tablero a medida','Quote a bespoke dashboard'))}</div><!-- milestones -->'''
  s=re.sub(r'<section id="porsche-progress".*?</section>',lambda m:m.group(0).replace('<video controls',milestones+'<video controls',1),s,flags=re.S)
  s=s.replace('Explorar los siete modelos','Explorar los ocho modelos').replace('Explore all seven models','Explore all eight models')
  options=[('scan','Reservar un escaneo 3D','Book a 3D scan'),('wheel','Proyecto de volante','Steering-wheel project'),('console','Consola / consola central','Console / centre console'),('dashboard','Tablero / dashboard a medida','Bespoke dashboard'),('aero','Desarrollo aerodinámico / canards','Aerodynamic development / canards'),('carbon','Skinning / trabajo en carbono','Skinning / carbon-fibre work'),('case','Case / carcasa en fibra','Composite case / housing'),('design','Otro diseño a medida','Other bespoke design')]
  s=re.sub(r'(<select id="service"[^>]*>).*?</select>',lambda m:m.group(1)+''.join(f'<option value="{v}">{t(es,eng)}</option>' for v,es,eng in options)+'</select>',s,flags=re.S)
  s=re.sub(r'<p id="quote-reference".*?</p>','',s,flags=re.S)
  s=s.replace('<form id="request">','<form id="request"><p id="quote-reference" class="quote-reference" aria-live="polite" hidden></p>')
  path.write_text(s,encoding='utf-8')
 print('Iteration 06: project stories, eight models, contextual quotations, case relief.')

if __name__=='__main__':build()
