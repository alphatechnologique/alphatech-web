# Mapeo de cambios · v2 → v3

> **Origen:** `Alpha tech S Web v2/`
> **Destino:** `Alpha tech S Web v3/`
> **Operación:** copia completa + adición de páginas legales + actualización de footers + checkout placeholder + stubs API

---

## 1. Archivos NUEVOS (no existían en v2)

### 1.1. Páginas legales (9 archivos)

| Archivo | Idioma | Tamaño | Propósito |
|---|---|---|---|
| `terminos.html` | ES | 23 KB | Términos y Condiciones generales |
| `terms.html` | EN | 20 KB | Terms and Conditions (espejo) |
| `privacidad.html` | ES | 22 KB | Política de Privacidad (Ley 29733 Perú) |
| `privacy.html` | EN | 20 KB | Privacy Policy (espejo) |
| `devoluciones.html` | ES | 20 KB | Política de Devoluciones y Reembolsos |
| `refunds.html` | EN | 18 KB | Refund Policy (espejo) |
| `reclamaciones.html` | ES | 23 KB | **Libro de Reclamaciones digital** con formulario funcional (Indecopi) |
| `envios.html` | ES | 18 KB | Política de Envíos |
| `shipping.html` | EN | 17 KB | Shipping Policy (espejo) |

### 1.2. Checkout placeholder

| Archivo | Propósito |
|---|---|
| `checkout.html` | Página intermedia: muestra resumen de pedido + redirige al cliente a WhatsApp/email comercial mientras la integración técnica de Culqi llega (post-afiliación) |

### 1.3. Stubs de API (carpeta `api/`)

| Archivo | Propósito |
|---|---|
| `api/README.md` | Documentación de los stubs y fase 2 |
| `api/culqi-webhook.js` | Handler estructurado para los 4 eventos críticos de Culqi |
| `api/reclamaciones.js` | Stub del endpoint del libro de reclamaciones |
| `api/contacto.js` | Stub del endpoint del formulario de contacto |
| `api/cotizar.js` | Stub del endpoint del formulario de cotización |

### 1.4. Reportes (este paquete)

| Archivo | Propósito |
|---|---|
| `validacion-culqi.md` | Checklist de cumplimiento de requisitos Culqi |
| `MAPEO-DE-CAMBIOS.md` | Este archivo |
| `BLOQUEOS.md` | Items que requieren input del GM antes de la afiliación |

---

## 2. Archivos MODIFICADOS

### 2.1. Actualización del footer en todas las páginas existentes

Se reemplazó el bloque `<footer>...</footer>` en las 32 páginas activas con un footer enriquecido que cumple los requisitos de Culqi.

**Cambios en el footer:**

- ✅ Razón social completa: `Alpha Tech Solutions S.A.C.`
- ✅ RUC visible: `20615287203`
- ✅ Email contacto: `contacto@alphatechnologique.com`
- ✅ WhatsApp Business: `+51 922 877 190`
- ✅ Sede: `Lima, Perú`
- ✅ Nueva columna "Legal" con links a las 5 páginas legales
- ✅ Bloque de medios de pago aceptados (Visa · Mastercard · Amex · Diners · Yape · PagoEfectivo · Cuotéalo BCP)
- ✅ Leyenda: "Pagos procesados de forma segura por **Culqi**, empresa del grupo BCP."
- ✅ Selector ES / EN
- ✅ Links a redes sociales (LinkedIn, Instagram)
- ✅ Copyright 2026

**CSS extra inyectado:** las clases `.footer-payments`, `.footer-payments-label`, `.footer-payments-list`, `.footer-culqi` se agregaron al `<style>` de cada página.

### 2.2. Páginas modificadas (32 archivos)

```
aeronautica.html, aeronautics.html
checkout.html
contacto.html, contacto-en.html
cotizar.html, cotizar-en.html
devoluciones.html
en.html
engineering.html, engineering-en.html
envios.html
index.html
intelligence.html, intelligence-en.html
news-airshow.html, news-corpac.html, news-ivao.html
nosotros.html, nosotros-en.html
noticia-airshow.html, noticia-corpac.html, noticia-ivao.html
performance.html, performance-en.html
privacidad.html, privacy.html
reclamaciones.html
refunds.html
shipping.html
terminos.html, terms.html
```

---

## 3. Archivos NO modificados

### 3.1. Sin footer original (sin cambios)

- `gracias.html` — página thank-you minimalista, no tiene footer
- `thanks.html` — página thank-you minimalista, no tiene footer

> ⏸️ Decisión sugerida: estas páginas son simples mensajes de confirmación post-compra. Si la auditoría Culqi exige links legales también acá, se les puede añadir un footer compacto en una iteración futura.

### 3.2. Páginas de utilidad interna (no expuestas)

- `preview-logo-v2.html` — preview de logos para diseñador interno, no es parte del sitio público

### 3.3. Activos preservados sin cambios

Todos los archivos no-HTML de v2 (imágenes, videos, SVGs, fuentes, manifest) se copiaron tal cual:

- Imágenes `*.png`, `*.jpg`, `*.jpeg`, `*.webp`
- Videos `*.mp4`, `*.webm`
- SVGs (logos, favicons, iconos)
- `favicon.ico`, `apple-touch-icon.png`, `site.webmanifest`

---

## 4. Decisiones tomadas durante el desarrollo

### 4.1. Libro de Reclamaciones solo en español

El Libro de Reclamaciones digital es un requisito legal del Perú (Ley 29571 / Indecopi). No tiene equivalente en regiones angloparlantes, por eso no se creó una versión EN. El nav y footer de las páginas EN linkean a `reclamaciones.html` (en ES) como página informativa.

### 4.2. Formulario de reclamaciones con fallback mailto:

El formulario captura todos los datos requeridos por Indecopi y, al enviar, dispara el cliente de email del usuario con un mensaje pre-rellenado destinado a `admin@alphatechnologique.com`. Esto funciona sin backend.

Cuando exista backend, cambiar a POST a `/api/reclamaciones.js` (stub ya creado).

### 4.3. Checkout como página intermedia

En esta fase, comprar desde el sitio dispara `checkout.html` con query params del producto. El cliente ve el resumen y un botón claro de "Escribir por WhatsApp" pre-rellenado con el producto y el monto. Esto permite seguir vendiendo durante la transición a la integración técnica.

### 4.4. Phase 2 separada

La integración técnica de Culqi (embebida real de la pasarela en las páginas de producto + procesamiento de webhooks) se realiza en fase 2, una vez Culqi apruebe la afiliación y entregue las llaves LIVE. Los stubs de `api/` documentan exactamente qué se debe implementar en esa fase.

### 4.5. Sin frameworks nuevos

Todo el sitio v3 sigue siendo HTML/CSS/JS plano como v2. No se agregaron React, Vue, jQuery ni otras dependencias. Las páginas legales y el checkout son auto-contenidos.

---

## 5. Stats finales

- **Total archivos HTML en v3:** 35
- **Páginas legales creadas:** 9
- **Páginas con footer Culqi-compliant:** 32 / 32 (100%)
- **Páginas que mencionan Culqi:** 32 / 32 (100%)
- **Páginas con RUC visible:** 32 / 32 (100%)
- **Páginas con link al Libro de Reclamaciones:** 32 / 32 (100%)
- **Stubs API documentados:** 5 (1 webhook + 3 formularios + README)

---

*Mapeo cerrado. Listo para fase de afiliación Culqi.*
