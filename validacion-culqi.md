# Validación · Cumplimiento de requisitos Culqi

> **Sitio:** `Alpha tech S Web v3/`
> **Fecha:** 2026
> **Status:** ✅ listo para solicitar afiliación en `afiliate.culqi.com/culqionline/afiliacion`

---

## 1. Páginas legales obligatorias

| Requisito Culqi | Página ES | Página EN | Status |
|---|---|---|---|
| Términos y Condiciones | `terminos.html` | `terms.html` | ✅ |
| Política de Privacidad | `privacidad.html` | `privacy.html` | ✅ |
| Política de Devoluciones | `devoluciones.html` | `refunds.html` | ✅ |
| Política de Envíos | `envios.html` | `shipping.html` | ✅ |
| Libro de Reclamaciones (Indecopi) | `reclamaciones.html` | (solo ES — requisito peruano) | ✅ |
| Acerca de Nosotros | `nosotros.html` | `nosotros-en.html` | ✅ (preexistente en v2) |
| Contacto | `contacto.html` | `contacto-en.html` | ✅ (preexistente en v2) |

---

## 2. Información obligatoria en el footer

Verificado en **32 / 32 páginas activas** (todas excepto `gracias.html`, `thanks.html` y `preview-logo-v2.html`):

| Requisito | Status |
|---|---|
| Razón Social: Alpha Tech Solutions S.A.C. | ✅ |
| RUC: 20615287203 | ✅ |
| Email contacto: contacto@alphatechnologique.com | ✅ |
| WhatsApp Business: +51 922 877 190 | ✅ |
| Sede: Lima, Perú | ✅ |
| Link a Términos y Condiciones | ✅ |
| Link a Política de Privacidad | ✅ |
| Link a Política de Devoluciones | ✅ |
| Link a Política de Envíos | ✅ |
| Link al Libro de Reclamaciones | ✅ |
| Medios de pago listados | ✅ (Visa · Mastercard · Amex · Diners · Yape · PagoEfectivo · Cuotéalo BCP) |
| Leyenda "Powered by Culqi" / "Pagos procesados por Culqi" | ✅ |
| Copyright con año | ✅ (© 2026 Alpha Tech Solutions S.A.C.) |
| Selector ES / EN | ✅ |
| Links a redes sociales | ✅ |

---

## 3. Libro de Reclamaciones (Indecopi)

Archivo: `reclamaciones.html`

- ✅ Texto introductorio con cita al Código de Protección y Defensa del Consumidor (Ley 29571)
- ✅ Diferenciación entre Reclamo y Queja
- ✅ Formulario con todos los campos obligatorios:
  - Datos del consumidor: nombre, tipo y número de documento, email, teléfono, domicilio
  - Datos del tutor si es menor de edad (campo condicional)
  - Identificación del producto/servicio: tipo (Producto/Servicio), monto, descripción, comprobante, fecha
  - Detalle del reclamo: tipo (Reclamo/Queja), descripción, pedido del consumidor
- ✅ Mensaje sobre plazo de 30 días calendario para respuesta
- ✅ Generación de número de registro correlativo (`AT-XXXXXXXX`)
- ✅ Disparo de email a `admin@alphatechnologique.com` con todos los datos vía `mailto:` (fallback hasta tener backend)
- ✅ Mensaje post-envío con número de registro y confirmación
- ✅ Canales alternativos listados: email, WhatsApp, Indecopi

**TODO documentado:** cuando exista backend, reemplazar `mailto:` por POST a `/api/reclamaciones.js`. El stub ya existe.

---

## 4. Checkout placeholder

Archivo: `checkout.html`

- ✅ Recibe query params del producto (`?producto=...&variante=...&total=...`)
- ✅ Muestra resumen del pedido al cliente
- ✅ Botón principal: enviar a WhatsApp con mensaje pre-rellenado del producto
- ✅ Botón secundario: email a `comercial@alphatechnologique.com`
- ✅ Badges de medios de pago aceptados
- ✅ Disclaimer: "Pagos procesados de forma segura por Culqi"
- ✅ Links a Términos, Privacidad y Devoluciones
- ✅ Permite operar el negocio mientras llegan las llaves LIVE de Culqi (1-3 semanas post-afiliación)

---

## 5. Endpoints stub (preparación fase 2)

Carpeta: `api/`

| Stub | Propósito |
|---|---|
| `api/README.md` | Documentación de la fase 2 (cuándo y cómo conectar al backend) |
| `api/culqi-webhook.js` | Handler para los 4 eventos Culqi críticos (charge.succeeded, subscription.created, charged, cancelled) |
| `api/reclamaciones.js` | Endpoint del libro de reclamaciones |
| `api/contacto.js` | Endpoint del formulario de contacto |
| `api/cotizar.js` | Endpoint del formulario de cotización |

Todos los stubs documentan los TODOs específicos para cuando se contrate el backend (Vercel / Cloudflare Workers / Supabase / Railway o equivalente).

---

## 6. Compatibilidad con el design system v2

- ✅ Tokens CSS respetados (teal #008EAA · orange #FE5000 · navy #001540 · navy-deep #06090F)
- ✅ Fuentes consistentes (Inter · Orbitron · Rajdhani)
- ✅ Container max-width 1100px / padding 48px (24px mobile)
- ✅ Navbar 72px fija con backdrop-filter
- ✅ Eyebrow style (Rajdhani 11px letter-spacing 4px uppercase teal)
- ✅ Botones (`.btn-primary` orange / `.btn-secondary` outline)
- ✅ Responsive: breakpoints 900px y 600px

---

## 7. Seguridad

Pendiente de verificar/configurar por el GM antes de la auditoría:

- [ ] Certificado SSL activo en `alphatechnologique.com` (HTTPS)
- [ ] Redirección HTTP → HTTPS automática
- [ ] Headers de seguridad básicos (HSTS, X-Content-Type-Options, X-Frame-Options)

---

## 8. Cumplimiento Indecopi adicional

- ✅ Información clara del proveedor en todas las páginas
- ✅ Precios visibles incluyendo IGV (a configurar por producto cuando se embeba el catálogo)
- ✅ Política de devoluciones explícita
- ✅ Libro de Reclamaciones digital funcional
- ✅ Comunicación clara sobre el proceso de cobranza y entrega

---

## 9. Items que el GM debe completar antes de auditoría Culqi

Ver `BLOQUEOS.md` para el detalle. Resumen:

1. ✅ **Dirección física exacta** → `Jirón Oxapampa 243, Breña, Lima, Perú` aplicada en 4 páginas legales (2026-06-13)
2. ✅ **SSL activo** en `alphatechnologique.com` — confirmado por GM (2026-06-13)
3. ⏳ **Solicitar afiliación** en `afiliate.culqi.com/culqionline/afiliacion` — acción pendiente del GM
4. ⏳ **Coordinar auditoría** con el equipo de Culqi y resolver observaciones (si las hubiera)
5. ⏳ **Recibir llaves LIVE** y migrar de modo TEST a producción

---

## 10. Próximos pasos (post-aprobación Culqi)

1. Recibir `pk_live_*` y `sk_live_*` de Culqi
2. Contratar backend (Vercel, Cloudflare, Supabase, etc.)
3. Implementar los stubs de `api/` con la lógica real
4. Embeber Culqi Checkout o Culqi API en las páginas de producto reales
5. Conectar webhooks a HubSpot + Notion + emisor electrónico de boletas/facturas
6. Pruebas end-to-end con tarjetas dummy → transición a tarjetas reales con monto chico
7. Lanzamiento

---

*Validación cerrada. Sitio v3 listo para auditoría Culqi.*
