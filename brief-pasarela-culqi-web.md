# Brief — Adaptación de la web para integración con Culqi Online

> **Audiencia:** ejecutor Claude Sonnet con acceso al filesystem y a Claude Chrome.
> **Versión:** 1.0 · 2026
> **Carpeta destino del trabajo:** `/Alpha Tech - Web Maintenance/Alpha tech S Web v3/`
> **Carpeta base de la que se copia:** `/Alpha Tech - Web Maintenance/Alpha tech S Web v2/`
> **Lectura previa obligatoria:** `_CONTEXTO-DE-TRABAJO.md`, `productos/brief-master.md`, `productos/brief-culqi.md`

---

## 1. Objetivo

Adaptar el sitio web actual (`Alpha tech S Web v2`) para cumplir con los **requisitos legales y operativos de Culqi Online** y poder afiliarse a la pasarela de pagos. Una vez la web cumpla, se solicita la afiliación en `afiliate.culqi.com/culqionline/afiliacion`, Culqi audita el sitio, y al aprobar se obtienen las llaves API LIVE para empezar a cobrar real.

Esta fase es **independiente y previa** a la embebida del checkout en sí — primero la web tiene que pasar la auditoría legal de Culqi, después se embebe la pasarela técnica.

---

## 2. Requisitos de Culqi (auditados antes de aprobar la afiliación)

Culqi exige que el sitio del comercio cumpla con todo lo siguiente. Cualquier omisión puede demorar o rechazar la afiliación:

### 2.1. Páginas legales obligatorias

| Página | URL sugerida | Obligatoria por | Estado actual en v2 |
|---|---|---|---|
| Términos y Condiciones | `/terminos.html` y `/terms-en.html` | Culqi + Ley peruana | ❌ No existe |
| Política de Privacidad | `/privacidad.html` y `/privacy-en.html` | Culqi + Ley 29733 Protección de Datos Personales | ❌ No existe |
| Política de Devoluciones y Reembolsos | `/devoluciones.html` y `/refunds-en.html` | Culqi + Indecopi | ❌ No existe |
| Libro de Reclamaciones digital | `/reclamaciones.html` | Indecopi (obligatorio para todo e-commerce en Perú) | ❌ No existe |
| Política de Envíos | `/envios.html` y `/shipping-en.html` | Culqi (si vendés productos físicos) | ❌ No existe |
| Acerca de Nosotros | `/nosotros.html` y `/about-en.html` | Culqi (verificación del negocio) | 🟡 Parcial — falta versión dedicada |

### 2.2. Información obligatoria visible en el footer

- **Razón Social completa:** `Alpha Tech Solutions S.A.C.`
- **RUC:** `20615287203`
- **Dirección física registrada en SUNAT:** [PENDIENTE — el GM debe entregar]
- **Email de contacto:** `contacto@alphatechnologique.com`
- **Teléfono / WhatsApp Business:** [PENDIENTE — el GM debe entregar]
- **Links a las 5 páginas legales** del §2.1
- **Logos de medios de pago aceptados** (Visa, Mastercard, Amex, Diners, Yape, PagoEfectivo, Cuotéalo BCP)
- **Sello de "Powered by Culqi"** o leyenda *"Pagos procesados por Culqi · BCP"*

### 2.3. Información del producto

Cada página de producto debe tener visible:
- Nombre del producto
- Descripción clara
- Precio con IGV incluido (en S/.)
- Fotos reales del producto (no placeholders genéricos)
- Tiempo de entrega
- Política de devolución específica (linkeada desde la página)
- Botón de compra claro
- Información de stock o disponibilidad

### 2.4. Información de contacto accesible

- Página `/contacto.html` ya existe (revisar contenido para que cumpla)
- Email visible en footer
- WhatsApp visible o flotante (ya existe en v2)
- Horario de atención al cliente

### 2.5. Seguridad

- **Certificado SSL activo** (HTTPS) — verificar con el GM
- Iconos de seguridad visibles en el checkout (PCI Compliant, Verified by Visa, Mastercard SecureCode)

---

## 3. Página por página — qué hacer

### 3.1. Crear las 6 páginas legales nuevas

#### a) `/terminos.html` + `/terms-en.html`

Términos y Condiciones generales del servicio. Cubrir:

1. Identificación del prestador: razón social, RUC, dirección, contacto
2. Aceptación del usuario: el uso del sitio implica aceptación
3. Productos y servicios ofrecidos: descripción del catálogo (referenciar al catálogo de Notion)
4. Precios: incluyen IGV, en moneda peruana (S/.), pueden cambiar sin previo aviso
5. Proceso de compra: añadir al carrito, checkout, pago vía Culqi
6. Medios de pago aceptados: tarjetas, Yape, PagoEfectivo, Cuotéalo BCP
7. Entrega: condiciones, tiempos, costos (linkear a `/envios.html`)
8. Devoluciones y reembolsos: linkear a `/devoluciones.html`
9. Propiedad intelectual: el contenido del sitio es propiedad de Alpha Tech Solutions S.A.C.
10. Limitación de responsabilidad
11. Modificaciones de los términos
12. Ley aplicable: peruana, jurisdicción de Lima
13. Última actualización: marzo 2026 (o fecha real de publicación)

Tono: **formal pero claro**, no legalista impenetrable. Estructura con headings H2/H3 numerados.

#### b) `/privacidad.html` + `/privacy-en.html`

Política de Privacidad alineada con la **Ley 29733 (Protección de Datos Personales del Perú)**. Cubrir:

1. Responsable del tratamiento: Alpha Tech Solutions S.A.C. + RUC + dirección + email
2. Datos personales que se recopilan: nombre, email, teléfono, dirección de envío, RUC/DNI para facturación
3. Finalidad del tratamiento: procesar compras, emitir comprobantes, atención al cliente, marketing (con opt-in)
4. Base legal del tratamiento: consentimiento del usuario al aceptar términos
5. Compartir datos con terceros: Culqi (procesador de pagos), Olva/Shalom (couriers), HubSpot (CRM), Google (analytics)
6. Plazo de conservación: 10 años después de terminada la relación contractual (alineado con norma peruana)
7. Derechos del titular (ARCO): acceso, rectificación, cancelación, oposición — cómo ejercerlos vía email a `admin@alphatechnologique.com`
8. Cookies y tecnologías similares
9. Seguridad: medidas técnicas para proteger los datos
10. Contacto del DPO (Data Protection Officer): puede ser el mismo `admin@alphatechnologique.com`
11. Última actualización: marzo 2026

#### c) `/devoluciones.html` + `/refunds-en.html`

Política de devoluciones y reembolsos. Cubrir:

**Productos físicos** (HOTAS, modelos 3D, porta strips, llaveros):
- Devolución dentro de **7 días calendario** desde la recepción
- Producto sin usar, embalaje original
- Cliente cubre envío de devolución (excepto si fue error de Alpha Tech)
- Reembolso en 5-7 días hábiles vía Culqi (mismo medio de pago)
- Garantía 30 días contra defectos de fabricación

**Servicios** (consultoría, escaneo, diagnóstico):
- Cancelación hasta 24h antes del inicio con reembolso 100%
- Una vez iniciado, no hay reembolso
- Si Alpha Tech cancela, reembolso 100% + reprogramación sin costo

**Cursos:**
- Cancelación hasta 7 días antes del cohort: reembolso 80%
- Una vez iniciado: no hay reembolso, sí reprogramación a próximo cohort

**Sesiones simulador / experiencias:**
- Cancelación hasta 24h antes: reprogramación sin costo
- No-show: se cobra
- Fuerza mayor documentada: reembolso

**Membresías Club Aeronáutico:**
- Cancelable mes a mes
- Sin reembolso del mes en curso
- Pausa por viaje/enfermedad: 1 vez al año hasta 30 días, sin costo

#### d) `/reclamaciones.html`

**Libro de Reclamaciones digital** — obligatorio para todo e-commerce en Perú según Indecopi.

Debe contener:
1. Mensaje claro: *"Conforme a lo establecido en el Código de Protección y Defensa del Consumidor, este establecimiento cuenta con un Libro de Reclamaciones a tu disposición."*
2. Formulario con campos:
   - Tipo: ¿Reclamo o Queja? (radio)
   - Nombre completo
   - Documento (DNI/CE/RUC)
   - Domicilio
   - Email
   - Teléfono
   - Si es menor de edad: datos del padre/madre/tutor
   - Producto/servicio reclamado
   - Tipo de bien: ¿Producto o Servicio? (radio)
   - Monto reclamado (S/.)
   - Descripción del reclamo (textarea)
   - Pedido del consumidor (textarea)
3. Indicación clara: *"El proveedor tendrá un plazo de 30 días calendarios para responder a tu reclamo."*
4. Botón "Enviar" que dispara email a `admin@alphatechnologique.com` con todos los datos del formulario + asigna número correlativo
5. Mensaje post-envío: *"Tu reclamo ha sido registrado con el número [XXXX]. Recibirás respuesta en tu email dentro de 30 días calendarios."*

**El formulario debe ser funcional desde el día 1** (no maqueta) — Indecopi puede sancionar si el libro no funciona.

#### e) `/envios.html` + `/shipping-en.html`

Política de envíos. Cubrir:

1. **Cobertura geográfica:**
   - Lima Metropolitana: delivery gratis (absorbido en precio)
   - Provincias: vía Olva Courier o Shalom Express
   - Internacional: no disponible por ahora

2. **Tiempos de entrega:**
   - Tabla con tiempo de producción + tiempo de envío por tipo de producto

3. **Costos:**
   - Lima Metropolitana: S/. 0 (incluido en precio)
   - Provincias: S/. 25-50 según destino (asume el cliente)
   - Internacional: no aplica

4. **Recojo en local:** disponible en dirección física (referenciar)

5. **Seguimiento:** se envía código de tracking al email del cliente cuando el producto se despacha

6. **Recepción:** firma o verificación de identidad al recibir; si la dirección está vacía, courier hace 2 reintentos y luego devuelve a Alpha Tech (cliente paga reenvío)

#### f) `/nosotros.html` + `/about-en.html`

Página "Acerca de" sólida. Usar el texto emocional ya redactado (que está en el contexto de marketing). Debe incluir:

- Historia del proyecto (texto manifiesto que aprobó el GM)
- Misión y visión
- Equipo (al menos foto + nombre + rol del GM + opcional otros)
- Datos del negocio: razón social, RUC, fecha de fundación, sede
- Foto de la oficina/sede si es posible

Esta página le da credibilidad al sitio frente al auditor de Culqi y al cliente final.

### 3.2. Modificar el footer (todas las páginas)

El footer actual de v2 hay que ampliarlo para incluir todo lo de §2.2. Estructura sugerida:

```
┌──────────────────────────────────────────────────────────────────┐
│ ALPHA TECH SOLUTIONS S.A.C.                                       │
│ RUC: 20615287203 · [Dirección Lima, Perú]                         │
│                                                                    │
│ ┌─────────────┬─────────────┬─────────────┬─────────────┐         │
│ │ NAVEGACIÓN  │ EMPRESA     │ LEGAL       │ CONTACTO    │         │
│ │ Inicio      │ Solutions   │ Términos    │ Email       │         │
│ │ Performance │ Simulations │ Privacidad  │ WhatsApp    │         │
│ │ Engineering │ Nosotros    │ Devoluciones│ Horario     │         │
│ │ Intelligence│             │ Envíos      │             │         │
│ │ Simulations │             │ Reclamaciones│            │         │
│ │ Contacto    │             │             │             │         │
│ └─────────────┴─────────────┴─────────────┴─────────────┘         │
│                                                                    │
│ MEDIOS DE PAGO ACEPTADOS                                          │
│ [Visa] [Mastercard] [Amex] [Diners] [Yape] [PagoEfectivo] [BCP]   │
│                                                                    │
│ ┌────────────────────────────┐  Pagos procesados de forma segura │
│ │ Powered by [Logo Culqi]    │  por Culqi, empresa del grupo BCP │
│ └────────────────────────────┘                                    │
│                                                                    │
│ © 2026 Alpha Tech Solutions S.A.C. · Todos los derechos reservados│
└──────────────────────────────────────────────────────────────────┘
```

### 3.3. Modificar páginas de producto (para fase de embebida real)

**En esta fase NO se embebe Culqi aún** (eso requiere las llaves LIVE post-afiliación). Pero las páginas de producto deben tener:

- Botón visible "Comprar ahora" (que por ahora redirige a un placeholder, ej. `/checkout-placeholder.html`)
- Precio con leyenda "Incluye IGV"
- Linkear desde la página del producto a `/devoluciones.html` y `/envios.html`
- Mostrar tiempo de entrega y stock/disponibilidad

### 3.4. Modificar `/contacto.html`

Verificar que tenga:
- Email visible: `contacto@alphatechnologique.com`
- WhatsApp Business linkeable
- Dirección física
- Horario de atención
- Formulario funcional que dispara email a `contacto@alphatechnologique.com`
- Mapa de Google embebido (opcional pero suma para auditoría)

---

## 4. Preparativos técnicos para la embebida posterior

Aunque la integración técnica de Culqi viene en una fase posterior (cuando se tengan las llaves LIVE), se debe **preparar el terreno** ahora:

### 4.1. Crear página de checkout placeholder

`/checkout.html` — página que por ahora muestra:
- Resumen del producto que el cliente quería comprar
- Mensaje: *"Estamos finalizando la implementación de la pasarela. Para completar tu compra, escríbenos por WhatsApp al [número] o email a `comercial@alphatechnologique.com` y te asistimos personalmente."*
- Link de WhatsApp con mensaje pre-rellenado: *"Hola, quiero comprar [PRODUCTO]"*

Esto permite que el sitio sea funcional para vender mientras llega la aprobación de Culqi (puede tardar 1-3 semanas).

### 4.2. Crear página `/gracias.html` mejorada

Actualmente existe `gracias.html` en v2 — verificar que tenga:
- Mensaje de agradecimiento
- Resumen de la compra (placeholder dinámico)
- Próximos pasos: cuándo llega tu producto / cuándo recibís el código de membresía / cuándo coordinás la sesión
- CTA: "Seguinos en LinkedIn / Instagram" + "Conocé más productos"

### 4.3. Endpoints stub para futura integración

En la carpeta `/api/` (a crear si no existe), dejar archivos placeholder con comentarios:

```javascript
// /api/culqi-webhook.js (placeholder)
// Acá llegará el webhook de Culqi cuando se aprueben las llaves LIVE
// Eventos a manejar: charge.succeeded, subscription.created, subscription.charged, subscription.cancelled
// Acción esperada: crear deal en HubSpot + factura en Notion + email de confirmación
```

Esto le indica a Sonnet (o al próximo dev) dónde implementar la lógica cuando llegue el momento.

---

## 5. Plan de trabajo de Sonnet

### Día 1 — Setup y páginas legales

1. Copiar todo el contenido de `/Alpha tech S Web v2/` a `/Alpha tech S Web v3/` como base
2. Producir las 6 páginas nuevas del §3.1 (4 en español + 4 en inglés = 12 archivos HTML)
3. Verificar que respeten el brand kit (paleta navy/orange/teal, tipografía Inter, voz híbrido técnico-directo)

### Día 2 — Footer + páginas de producto

4. Modificar el footer en TODAS las páginas existentes (es repetitivo, considerar usar un componente compartido si la arquitectura lo permite)
5. Modificar páginas de producto para que tengan precio con IGV + botón comprar + links a legales
6. Crear `/checkout.html` placeholder

### Día 3 — Validación

7. Crear checklist `validacion-culqi.md` con cada uno de los 30+ requisitos verificados ✓
8. Tomar screenshots de cada página para evidencia
9. Hacer un test de UX: navegar el sitio como cliente y validar que todo fluye
10. Generar reporte para el GM con: páginas creadas, items legales cumplidos, items pendientes (info que el GM debe proveer)

### Día 4 — Handoff al GM

11. El GM revisa
12. GM completa los datos pendientes (dirección física exacta, teléfono, etc.)
13. GM solicita afiliación en `afiliate.culqi.com/culqionline/afiliacion`
14. Culqi audita el sitio
15. Cuando Culqi aprueba: empieza la siguiente fase (embebida técnica del checkout con llaves LIVE)

---

## 6. Open items (lo que solo el GM puede proveer)

Antes de que Sonnet pueda terminar, el GM debe entregar:

1. **Dirección física exacta** registrada en SUNAT (para footer + páginas legales)
2. **Número de teléfono / WhatsApp Business** definitivo (para contacto)
3. **Horario de atención al cliente** definitivo
4. **Foto/avatar del GM** para `/nosotros.html` (puede ser corporativa)
5. **Foto de la oficina/sede** si existe (opcional pero recomendable)
6. **Confirmar si el sitio actual ya tiene SSL activo** (HTTPS) — si no, hay que activarlo antes de la auditoría Culqi
7. **Confirmar los datos completos del banco BBVA** (n° de cuenta + CCI) para incluir en las facturas/boletas
8. **Aprobar el copy de las páginas legales** antes de publicar — son documentos sensibles legalmente

---

## 7. Reglas no negociables (respeta las del proyecto)

- Brand kit: paleta navy/orange/teal/white, tipografía Inter + Russo One + JetBrains Mono
- Voz: híbrido técnico-directo (incluso en páginas legales — claras, no impenetrables)
- Emails corporativos únicamente (los 6 lockeados)
- Política agresiva: ante duda, optar por lo más punzante/claro/directo
- No mencionar Catia V5 ni nada eliminado
- Versiones bilingües (ES + EN) en todas las páginas nuevas
- Sin frameworks pesados ni dependencias nuevas — HTML/CSS/JS plano como el resto del sitio

---

## 8. Success criteria

✅ Carpeta `Alpha tech S Web v3/` creada con todo el contenido de v2 + las nuevas páginas
✅ 6 páginas legales nuevas (12 archivos contando inglés)
✅ Footer actualizado en TODAS las páginas existentes
✅ Páginas de producto modificadas con precio + IGV + links legales
✅ Página `/checkout.html` placeholder funcional
✅ Carpeta `/api/` con stub para webhooks futuro
✅ Reporte `validacion-culqi.md` con checklist verificado
✅ Screenshots de evidencia
✅ Lista de open items pendientes para el GM claramente identificada
✅ Sitio sigue navegable sin errores (testeado por el ejecutor antes de entregar)

---

## 9. Entrega final

Sonnet entrega:

1. La carpeta `Alpha tech S Web v3/` lista
2. `validacion-culqi.md` con el checklist auditado
3. `MAPEO-DE-CAMBIOS.md` listando cada archivo creado/modificado y el porqué
4. `BLOQUEOS.md` con cualquier item bloqueado por falta de info del GM
5. Mensaje resumen al GM con: ✅ qué quedó listo, ⏸️ qué requiere su input, próximo paso

---

*Fin del brief. Cuando el sitio v3 cumpla con todo, el GM solicita afiliación a Culqi y la auditoría arranca.*
