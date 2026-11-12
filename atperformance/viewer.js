'use strict';
(() => {
 const en=document.documentElement.lang==='en';
 const dialog=document.querySelector('#model-dialog');
 const canvas=document.querySelector('#model');
 const select=document.querySelector('#model-select');
 const status=document.querySelector('#viewer-status');
 const fallback=document.querySelector('#viewer-fallback');
 const toggle=document.querySelector('#mesh-toggle');
 const layerControls=document.querySelector('#porsche-layers');
 const opacity=document.querySelector('#design-opacity');
 const projects=window.ATP_PROJECTS||[];
 const gl=canvas.getContext('webgl',{antialias:true,alpha:true});
 const loads=new Map();
 let program,buffer,count=0,active='',request=0,yaw=.18,pitch=-.12,zoom=1,mesh=false,drag=null,frame=0,opener=null,oldOverflow='';
 let locations;
 let batches=[],layerMode='both';
 function shader(type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(s));return s;}
 function setup(){
  if(!gl)return;
  const vertex=shader(gl.VERTEX_SHADER,`
   attribute vec3 aPosition; attribute vec3 aNormal; attribute vec3 aBary;
   uniform vec2 uAngle; uniform vec2 uScale;
   varying vec3 vNormal; varying vec3 vBary;
   vec3 rotate(vec3 p){float c=cos(uAngle.x),s=sin(uAngle.x);p=vec3(c*p.x+s*p.z,p.y,-s*p.x+c*p.z);c=cos(uAngle.y);s=sin(uAngle.y);return vec3(p.x,c*p.y-s*p.z,s*p.y+c*p.z);}
   void main(){vec3 p=rotate(aPosition);vNormal=rotate(aNormal);vBary=aBary;gl_Position=vec4(p.xy*uScale,-p.z*.6,1.0);}
  `);
  const fragment=shader(gl.FRAGMENT_SHADER,`
   precision mediump float; varying vec3 vNormal; varying vec3 vBary; uniform float uMesh; uniform vec3 uColor; uniform float uOpacity;
   void main(){vec3 n=normalize(vNormal);if(n.z<0.0)n=-n;
    vec3 light=normalize(vec3(-.45,.7,1.0));float key=max(dot(n,light),0.0);float fill=max(dot(n,normalize(vec3(.8,-.1,.5))),0.0);
    float spec=pow(max(dot(n,normalize(light+vec3(0.,0.,1.))),0.0),32.0);
    vec3 color=uColor*(.27+.72*key+.20*fill)+vec3(.16)*spec;
    float edge=1.0-smoothstep(.0,.024,min(vBary.x,min(vBary.y,vBary.z)));
    color=mix(color,color*.48,edge*uMesh*.72);gl_FragColor=vec4(color,uOpacity);
   }
  `);
  program=gl.createProgram();gl.attachShader(program,vertex);gl.attachShader(program,fragment);gl.linkProgram(program);
  if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw new Error(gl.getProgramInfoLog(program));
  gl.deleteShader(vertex);gl.deleteShader(fragment);buffer=gl.createBuffer();
  locations={position:gl.getAttribLocation(program,'aPosition'),normal:gl.getAttribLocation(program,'aNormal'),bary:gl.getAttribLocation(program,'aBary'),angle:gl.getUniformLocation(program,'uAngle'),scale:gl.getUniformLocation(program,'uScale'),mesh:gl.getUniformLocation(program,'uMesh')};
  locations.color=gl.getUniformLocation(program,'uColor');locations.opacity=gl.getUniformLocation(program,'uOpacity');
  gl.enable(gl.DEPTH_TEST);gl.depthFunc(gl.LEQUAL);gl.disable(gl.CULL_FACE);gl.clearColor(0,0,0,0);
 }
 let renderingError=false;
 try{setup();}catch(error){renderingError=true;console.error('3D viewer initialization failed',error);}
 function load(id){
  if(window.ATP_GEOMETRY?.[id])return Promise.resolve(window.ATP_GEOMETRY[id]);
  if(loads.has(id))return loads.get(id);
  const promise=new Promise((resolve,reject)=>{const script=document.createElement('script');script.src='assets/models/'+id+'.js';script.onload=()=>{script.remove();const model=window.ATP_GEOMETRY?.[id];model?resolve(model):reject(new Error('Model missing'));};script.onerror=()=>{script.remove();loads.delete(id);reject(new Error('Model unavailable'));};document.head.append(script);});
  loads.set(id,promise);return promise;
 }
 function uploadSingle(data){
  const positions=data.vertices,indices=data.indices;
  if(indices.length%3||positions.length%3)throw new Error('Invalid geometry');
  const array=new Float32Array(indices.length*9);
  let offset=0;
  for(let i=0;i<indices.length;i+=3){
   const a=indices[i]*3,b=indices[i+1]*3,c=indices[i+2]*3;
   const ux=positions[b]-positions[a],uy=positions[b+1]-positions[a+1],uz=positions[b+2]-positions[a+2];
   const vx=positions[c]-positions[a],vy=positions[c+1]-positions[a+1],vz=positions[c+2]-positions[a+2];
   let nx=uy*vz-uz*vy,ny=uz*vx-ux*vz,nz=ux*vy-uy*vx;const length=Math.hypot(nx,ny,nz)||1;nx/=length;ny/=length;nz/=length;
   for(let j=0;j<3;j++){const p=indices[i+j]*3;array[offset++]=positions[p];array[offset++]=positions[p+1];array[offset++]=positions[p+2];array[offset++]=nx;array[offset++]=ny;array[offset++]=nz;array[offset++]=j===0?1:0;array[offset++]=j===1?1:0;array[offset++]=j===2?1:0;}
  }
  const gpuBuffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,gpuBuffer);gl.bufferData(gl.ARRAY_BUFFER,array,gl.STATIC_DRAW);
  return {id:data.id||'surface',buffer:gpuBuffer,count:indices.length};
 }
 function upload(data){
  for(const batch of batches)gl.deleteBuffer(batch.buffer);
  batches=(data.layers||[data]).map(uploadSingle);count=batches.reduce((sum,b)=>sum+b.count,0);
 }
 function draw(){
  frame=0;if(!dialog.open||!gl||renderingError||!count)return;
  const rect=canvas.getBoundingClientRect();if(!rect.width||!rect.height)return;
  const ratio=Math.min(window.devicePixelRatio||1,2),width=Math.round(rect.width*ratio),height=Math.round(rect.height*ratio);
  if(canvas.width!==width||canvas.height!==height){canvas.width=width;canvas.height=height;}
  gl.viewport(0,0,width,height);gl.depthMask(true);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.useProgram(program);
  const aspect=rect.width/rect.height;gl.uniform2f(locations.scale,1.65*zoom/Math.max(1,aspect),1.65*zoom*Math.min(1,aspect));
  gl.uniform2f(locations.angle,yaw,pitch);gl.uniform1f(locations.mesh,mesh?1:0);
  for(const batch of batches){
   if(active==='porsche'&&layerMode!=='both'&&batch.id!==layerMode)continue;
   gl.bindBuffer(gl.ARRAY_BUFFER,batch.buffer);
   for(const [loc,offset] of [[locations.position,0],[locations.normal,12],[locations.bary,24]]){gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,3,gl.FLOAT,false,36,offset);}
   const design=batch.id==='design',alpha=design&&layerMode==='both'?Number(opacity.value)/100:1;
   gl.uniform3f(locations.color,...(design?[.85,.19,.14]:[.56,.59,.64]));gl.uniform1f(locations.opacity,alpha);
   gl.disable(gl.BLEND);gl.depthMask(true);
   if(alpha<1){
    // Depth prepass retains the nearest design surface before compositing over the scan.
    gl.colorMask(false,false,false,false);gl.drawArrays(gl.TRIANGLES,0,batch.count);gl.colorMask(true,true,true,true);
    gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.depthMask(false);
   }
   gl.drawArrays(gl.TRIANGLES,0,batch.count);gl.depthMask(true);gl.disable(gl.BLEND);
  }
 }
 function schedule(){if(!frame)frame=requestAnimationFrame(draw);}
 function reset(){const view=projects.find(p=>p.id===active)?.view||[.18,-.12];[yaw,pitch]=view;zoom=1;schedule();}
 function showFallback(message){canvas.hidden=true;fallback.hidden=false;fallback.src='assets/'+active+'-solid.webp';status.textContent=message;toggle.disabled=true;layerControls.hidden=true;}
 async function choose(id){
  const project=projects.find(p=>p.id===id);if(!project)return;
  active=id;select.value=id;document.querySelector('#viewer-title').textContent=project[en?'en':'es'];count=0;reset();const ticket=++request;
  layerControls.hidden=id!=='porsche';layerMode='both';opacity.value='75';opacity.disabled=false;
  layerControls.querySelectorAll('[data-layer]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.layer==='both')));
  fallback.hidden=true;canvas.hidden=false;toggle.disabled=false;status.textContent=en?'Loading geometry…':'Cargando geometría…';
  if(!gl||renderingError){showFallback(en?'Interactive 3D is unavailable in this browser. Showing the shaded preview.':'El 3D interactivo no está disponible en este navegador. Se muestra la vista sombreada.');return;}
  gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
  try{const data=await load(id);if(ticket!==request||!dialog.open)return;upload(data);status.textContent='';schedule();}
  catch(error){if(ticket!==request||!dialog.open)return;showFallback(en?'Unable to load 3D. Showing the shaded preview.':'No se pudo cargar el 3D. Se muestra la vista sombreada.');console.error(error);}
 }
 function open(id,button){opener=button;oldOverflow=document.body.style.overflow;dialog.showModal();document.body.style.overflow='hidden';choose(id);document.querySelector('#close-model').focus();}
 document.querySelectorAll('[data-open-model]').forEach(button=>button.addEventListener('click',()=>open(button.dataset.openModel,button)));
 document.querySelector('#close-model').addEventListener('click',()=>dialog.close());
 dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
 dialog.addEventListener('close',()=>{++request;drag=null;document.body.style.overflow=oldOverflow;if(frame){cancelAnimationFrame(frame);frame=0;}opener?.focus();});
 select.addEventListener('change',()=>choose(select.value));
 layerControls.querySelectorAll('[data-layer]').forEach(button=>button.addEventListener('click',()=>{layerMode=button.dataset.layer;layerControls.querySelectorAll('[data-layer]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));opacity.disabled=layerMode!=='both';schedule();}));
 opacity.addEventListener('input',schedule);
 toggle.addEventListener('click',()=>{mesh=!mesh;toggle.setAttribute('aria-pressed',String(mesh));toggle.textContent=en?(mesh?'Hide mesh':'Show mesh'):(mesh?'Ocultar malla':'Mostrar malla');schedule();});
 document.querySelector('#reset-model').addEventListener('click',reset);
 function changeZoom(delta){zoom=Math.min(3.5,Math.max(.5,zoom+delta));schedule();}
 document.querySelector('#zoom-in').addEventListener('click',()=>changeZoom(.15));document.querySelector('#zoom-out').addEventListener('click',()=>changeZoom(-.15));
 canvas.addEventListener('pointerdown',e=>{drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId);canvas.focus();});
 canvas.addEventListener('pointermove',e=>{if(!drag)return;yaw+=(e.clientX-drag[0])*.008;pitch+=(e.clientY-drag[1])*.008;drag=[e.clientX,e.clientY];schedule();});
 ['pointerup','pointercancel','lostpointercapture'].forEach(type=>canvas.addEventListener(type,()=>drag=null));
 canvas.addEventListener('wheel',e=>{e.preventDefault();changeZoom(e.deltaY<0?.1:-.1);},{passive:false});
 canvas.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','-','='].includes(e.key))return;e.preventDefault();if(e.key==='ArrowLeft')yaw-=.12;if(e.key==='ArrowRight')yaw+=.12;if(e.key==='ArrowUp')pitch-=.12;if(e.key==='ArrowDown')pitch+=.12;if(e.key==='+'||e.key==='=')zoom=Math.min(3.5,zoom+.1);if(e.key==='-')zoom=Math.max(.5,zoom-.1);schedule();});
 canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();renderingError=true;showFallback(en?'3D context lost. Reopen or reload to retry.':'Se perdió el contexto 3D. Recarga la página para reintentarlo.');});
 new ResizeObserver(schedule).observe(canvas);
})();
