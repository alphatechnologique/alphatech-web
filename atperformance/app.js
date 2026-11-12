'use strict';
const menu=document.querySelector('.menu'),nav=document.querySelector('nav');
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');menu.setAttribute('aria-expanded','false')}));
document.addEventListener('keydown',e=>{if(e.key==='Escape'){nav.classList.remove('open');menu.setAttribute('aria-expanded','false')}});
let quoteReference='';
const quoteNote=document.querySelector('#quote-reference');
document.querySelectorAll('[data-service]').forEach(a=>a.addEventListener('click',()=>{
 document.querySelector('#service').value=a.dataset.service;
 quoteReference=a.dataset.reference||'';
 quoteNote.hidden=!quoteReference;
 quoteNote.textContent=(document.documentElement.lang==='en'?'Reference project: ':'Proyecto de referencia: ')+quoteReference;
}));
document.querySelector('#service').addEventListener('change',()=>{quoteReference='';quoteNote.hidden=true;quoteNote.textContent=''});
document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelectorAll('[data-category]').forEach(x=>{x.hidden=b.dataset.filter!=='all'&&x.dataset.category!==b.dataset.filter})}));
document.querySelector('#request').addEventListener('submit',e=>{e.preventDefault();const en=document.documentElement.lang==='en';const service=document.querySelector('#service');const vehicle=document.querySelector('#vehicle');if(!vehicle.value.trim()){vehicle.setCustomValidity(en?'Enter your vehicle or part.':'Indica el vehículo o pieza.');vehicle.reportValidity();return}vehicle.setCustomValidity('');const msg=(en?'Hello ATPerformance! I would like to enquire about: ':'¡Hola ATPerformance! Quisiera consultar por: ')+service.selectedOptions[0].text+(quoteReference?'\n'+(en?'Reference project: ':'Proyecto de referencia: ')+quoteReference:'')+'\n'+vehicle.value.trim()+'\n'+document.querySelector('#description').value.trim();window.open('https://wa.me/51922877190?text='+encodeURIComponent(msg),'_blank','noopener,noreferrer')});
document.querySelector('#vehicle').addEventListener('input',e=>e.target.setCustomValidity(''));
document.querySelectorAll('[data-photo]').forEach(button=>button.addEventListener('click',()=>{
 const img=document.querySelector('#mirror-photo');
 img.src='assets/civic-mirrors-'+button.dataset.photo+'.png';
 document.querySelectorAll('[data-photo]').forEach(other=>other.setAttribute('aria-pressed',String(other===button)));
}));
