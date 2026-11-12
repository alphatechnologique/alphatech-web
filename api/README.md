# API stubs · Alpha Tech v3

Esta carpeta contiene **stubs** (placeholders) de los endpoints que se van a implementar cuando exista backend.

> ⚠️ **Fase actual:** stubs solamente. Ninguno está conectado a un servidor real.
> Cuando se contrate un BaaS (Vercel, Cloudflare Workers, Supabase Edge Functions, Railway, etc.) o un VPS, estos archivos se reescriben con la lógica real y se reemplaza el `action` de los formularios + el endpoint de los webhooks Culqi.

## Archivos

- `culqi-webhook.js` — recibe los webhooks de Culqi (`charge.succeeded`, `subscription.*`)
- `reclamaciones.js` — recibe el POST del formulario del Libro de Reclamaciones
- `contacto.js` — recibe el POST del formulario de contacto
- `cotizar.js` — recibe el POST del formulario de cotización

## Eventos Culqi a manejar (cuando se conecte el webhook real)

| Evento | Acción esperada |
|---|---|
| `charge.succeeded` | Crear deal Won en HubSpot + factura en Notion + email confirmación |
| `subscription.created` | Activar miembro en Notion "Miembros Club" + email bienvenida + código de acceso |
| `subscription.charged` | Emitir comprobante recurrente + email recibo |
| `subscription.cancelled` | Notificar al GM + email cliente + remover de "Miembros activos" |
| `subscription.failed` | Email cliente para actualizar tarjeta + reintentos Culqi automáticos |

## Por qué solo stubs

El sitio v3 está optimizado para pasar la auditoría de Culqi (legal compliance). Los endpoints reales requieren:

1. Servidor backend (no hay aún)
2. Llaves Culqi LIVE (solo se entregan post-afiliación)
3. Tokens API de HubSpot + Notion configurados en variables de entorno
4. Emisor electrónico (Nubefact, Facturador SUNAT, o plataforma propia)

Todos los formularios del sitio actual hacen fallback a `mailto:` (cliente de email del usuario) hasta que exista backend. Esto está documentado en cada formulario con un `<!-- TODO: cambiar a POST cuando exista backend -->`.
