# Items pendientes para el GM (Arturo)

> Estos items quedan abiertos porque solo Arturo puede proveerlos o decidirlos.
> Hay que resolverlos **antes de solicitar la afiliación a Culqi** o quedan documentados como "TODO" en las páginas legales.

---

## 1. Datos del negocio que necesitan reemplazar placeholders

✅ **RESUELTO 2026-06-13 — Jirón Oxapampa 243, Breña, Lima**

Dirección aplicada en las 4 páginas legales:
- `terminos.html` § 1. Identificación del prestador → `Jirón Oxapampa 243, Breña, Lima, Perú`
- `privacidad.html` § 1. Responsable del tratamiento → `Jirón Oxapampa 243, Breña, Lima, Perú`
- `privacy.html` § 1. Data controller → `Jiron Oxapampa 243, Breña, Lima, Peru`
- `terms.html` § 1. Service provider identification → `Jiron Oxapampa 243, Breña, Lima, Peru`

---

## 2. Verificaciones técnicas del dominio

✅ **CONFIRMADO POR GM 2026-06-13 — HTTPS activo en alphatechnologique.com**

| Item | Estado |
|---|---|
| Certificado SSL activo en alphatechnologique.com | ✅ Confirmado por GM |
| Redirección HTTP → HTTPS automática | ✅ Confirmado por GM |
| Dominio apunta correctamente | ✅ Confirmado por GM |

---

## 3. Datos para el footer y emails

Estos están preconfigurados con los lockeados, pero el GM debe confirmarlos:

| Dato | Valor configurado | ¿Correcto? |
|---|---|---|
| Razón Social | Alpha Tech Solutions S.A.C. | ✅ confirmado |
| RUC | 20615287203 | ✅ confirmado |
| Email contacto público | contacto@alphatechnologique.com | ✅ confirmado |
| Email admin / DPO | admin@alphatechnologique.com | ✅ confirmado |
| Email comercial | comercial@alphatechnologique.com | ✅ confirmado |
| WhatsApp Business | +51 922 877 190 | ⏸️ Confirmar — extraído del WhatsApp button existente en v2 |
| Sede | Lima, Perú | ✅ confirmado |

---

## 4. Redes sociales del footer

✅ **RESUELTOS 2026-06-13 — URLs aplicadas en las 32 páginas activas**

- ✅ Instagram: `https://www.instagram.com/alphatechsolutions.pe?igsh=YnpsbHdrMmtwbGRr`
- ✅ LinkedIn: `https://www.linkedin.com/company/alpha-tech-solutions-sac`
- [ ] URL de Facebook (si existe) — pendiente del GM
- [ ] URL de YouTube (si existe) — pendiente del GM

---

## 5. Páginas gracias.html y thanks.html sin footer

Estas dos páginas son thank-you minimalistas sin footer. **Decisión del GM:**

- [ ] Mantenerlas como están (más simples, mejor UX post-compra)
- [ ] Agregarles un footer compacto con links legales (más estricto para auditoría)

Recomendación: mantenerlas simples por ahora. Si Culqi observa en la auditoría, agregamos footer compacto en una iteración corta.

---

## 6. Pasos para solicitar afiliación a Culqi

Cuando los puntos 1-3 estén resueltos:

1. Ir a https://afiliate.culqi.com/culqionline/afiliacion
2. Completar el formulario de afiliación con:
   - RUC: 20615287203
   - Razón Social: Alpha Tech Solutions S.A.C.
   - Sitio web: https://alphatechnologique.com
   - Categoría del negocio: ingeniería técnica + e-commerce + servicios profesionales
   - Modelo de negocio: B2C (consumo final) y B2B (empresas)
   - Monto estimado de ventas mensuales (input del GM)
3. Adjuntar documentos requeridos por Culqi (DNI del representante legal, ficha RUC, etc.)
4. Esperar revisión técnica del sitio (1-3 semanas habitualmente)
5. Resolver observaciones de Culqi si las hubiera
6. Recibir las llaves API LIVE (`pk_live_*` y `sk_live_*`)

---

## 7. Fase 2 (post-aprobación Culqi) — no en este paquete

Una vez Culqi apruebe y entregue las llaves LIVE:

1. Contratar backend para los endpoints (Vercel / Cloudflare Workers / Supabase / Railway)
2. Implementar los stubs de `api/` con la lógica real
3. Conectar a HubSpot CRM, Notion Catálogo y emisor electrónico de boletas/facturas
4. Embeber Culqi Checkout en las páginas de producto reales (ya hay páginas de producto en `productos/` brief)
5. Pruebas end-to-end con tarjetas dummy → migrar a LIVE con monto chico
6. Lanzamiento comercial

Esta fase requiere un brief separado y dev específico de backend.

---

## 8. Items menores

- [ ] Actualizar la copy de OG / Twitter cards de las páginas legales (heredan las de la home, podría afinarse)
- [ ] Agregar Schema.org `Organization` con datos del negocio (mejora SEO)
- [ ] Agregar Schema.org `BreadcrumbList` en las páginas legales (mejora SEO)
- [ ] Configurar sitemap.xml incluyendo las nuevas páginas legales
- [ ] Configurar robots.txt si no existe

Ninguno bloquea la afiliación a Culqi, pero son nice-to-have para SEO.

---

*Resolver los items 1-3 es lo único bloqueante. El resto se va resolviendo en paralelo o post-aprobación.*
