/**
 * culqi-webhook.js — STUB
 *
 * Endpoint que recibirá los webhooks de Culqi cuando se obtengan las llaves LIVE.
 * Documentación oficial: https://docs.culqi.com/es/documentacion/webhooks/conceptos-generales/
 *
 * Eventos a manejar:
 *   - charge.succeeded
 *   - charge.failed
 *   - subscription.created
 *   - subscription.charged
 *   - subscription.cancelled
 *   - subscription.failed
 *
 * Acciones por evento (cuando se conecten HubSpot, Notion, emisor electrónico):
 *
 *   charge.succeeded → crear deal Won + factura/boleta + email confirmación
 *   subscription.created → activar miembro Club + email bienvenida + código acceso
 *   subscription.charged → emitir comprobante recurrente
 *   subscription.cancelled → notificar GM + remover de miembros activos
 *
 * TODO: implementar cuando exista backend (Vercel / Workers / Supabase / Railway).
 */

/* eslint-env serverless */

export default async function handler(req, res) {
  // --- 1. Validar método ---
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // --- 2. Validar firma del webhook ---
  // Culqi firma cada webhook con HMAC-SHA256 usando tu llave secreta
  // const signature = req.headers['culqi-signature'];
  // if (!verifySignature(signature, req.rawBody, process.env.CULQI_WEBHOOK_SECRET)) {
  //   return res.status(401).json({ error: 'Invalid signature' });
  // }

  // --- 3. Parsear evento ---
  const event = req.body;
  const { type, data } = event;

  // --- 4. Dispatch por tipo de evento ---
  try {
    switch (type) {
      case 'charge.succeeded':
        await handleChargeSucceeded(data);
        break;
      case 'subscription.created':
        await handleSubscriptionCreated(data);
        break;
      case 'subscription.charged':
        await handleSubscriptionCharged(data);
        break;
      case 'subscription.cancelled':
        await handleSubscriptionCancelled(data);
        break;
      default:
        console.log(`Unhandled event: ${type}`);
    }
    return res.status(200).json({ received: true });
  } catch (err) {
    console.error('Webhook processing error:', err);
    return res.status(500).json({ error: 'Processing failed' });
  }
}

// --- Handlers (TODO: implementar cuando exista backend) ---

async function handleChargeSucceeded(data) {
  /*
   * 1. Identificar producto por data.metadata.external_id (SKU)
   * 2. Crear deal en HubSpot con stage = closedwon
   * 3. Crear registro en Notion database "Facturas" con status = Pagada
   * 4. Emitir boleta o factura electrónica vía emisor configurado
   * 5. Enviar email de confirmación al cliente
   * 6. Para productos físicos: agregar orden en Notion database "Producción"
   */
  console.log('TODO: charge.succeeded', data);
}

async function handleSubscriptionCreated(data) {
  /*
   * 1. Identificar plan por data.plan_id (CLB-MB-001/002/003)
   * 2. Generar código de acceso al simulador (3 letras + 4 dígitos)
   * 3. Crear registro en Notion database "Miembros Club"
   * 4. Enviar email de bienvenida con código + link a calendario de reservas
   * 5. Crear contact en HubSpot con tag "Miembro Club + Nivel"
   */
  console.log('TODO: subscription.created', data);
}

async function handleSubscriptionCharged(data) {
  /*
   * 1. Emitir comprobante electrónico recurrente
   * 2. Enviar email de recibo al cliente
   * 3. Actualizar fecha de "Próximo cobro" en Notion
   */
  console.log('TODO: subscription.charged', data);
}

async function handleSubscriptionCancelled(data) {
  /*
   * 1. Marcar miembro como inactive en Notion
   * 2. Enviar email de cancelación con resumen
   * 3. Notificar al GM
   * 4. Bloquear acceso al simulador (manual o vía sistema de control)
   */
  console.log('TODO: subscription.cancelled', data);
}
