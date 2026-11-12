/**
 * /api/culqi-charge.js — Vercel Serverless Function
 *
 * Recibe el token de Culqi.js (frontend) + datos del pedido
 * Llama a Culqi API server-to-server para crear el cargo real
 * Notifica por email (cliente + vendedor) vía Resend
 * Devuelve resultado al frontend
 *
 * Variables de entorno requeridas en Vercel (Settings → Environment Variables):
 *   CULQI_SECRET_KEY          → sk_test_... o sk_live_... (NUNCA en frontend)
 *   RESEND_API_KEY            → re_... (envío de emails)
 *   NOTIFY_EMAIL_OWNER        → comercial@alphatechnologique.com
 *   HUBSPOT_API_KEY           → (opcional, Fase 2)
 */

export default async function handler(req, res) {
  // CORS — permitir desde el dominio público
  res.setHeader('Access-Control-Allow-Origin', 'https://alphatechnologique.com');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { token, amount, currency, email, description, items, customer } = req.body || {};

    // ── Validación básica ──────────────────────────────────────
    if (!token || !amount || !email) {
      return res.status(400).json({
        error: 'Faltan campos requeridos: token, amount, email',
      });
    }
    if (typeof amount !== 'number' || amount < 100) {
      return res.status(400).json({ error: 'Monto inválido (mínimo S/. 1.00 = 100)' });
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return res.status(400).json({ error: 'Email inválido' });
    }

    const CULQI_SECRET = process.env.CULQI_SECRET_KEY;
    if (!CULQI_SECRET) {
      console.error('CULQI_SECRET_KEY no configurada en env');
      return res.status(500).json({ error: 'Pasarela mal configurada — contactá soporte' });
    }

    // ── Llamar Culqi API: crear el cargo ───────────────────────
    const culqiBody = {
      amount: Math.round(amount),              // en céntimos (1 sol = 100)
      currency_code: currency || 'PEN',
      email: email,
      source_id: token,
      description: (description || 'Compra Alpha Tech').slice(0, 80),
      antifraud_details: customer ? {
        first_name: customer.firstName || '',
        last_name: customer.lastName || '',
        phone: customer.phone || '',
        country_code: 'PE',
      } : undefined,
      metadata: {
        // útiles para conciliar en panel Culqi y en HubSpot después
        items_count: String((items || []).length),
        items_summary: (items || []).map(i => `${i.qty}x ${i.sku}`).join(' | ').slice(0, 200),
      },
    };

    const culqiResp = await fetch('https://api.culqi.com/v2/charges', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${CULQI_SECRET}`,
      },
      body: JSON.stringify(culqiBody),
    });

    const culqiData = await culqiResp.json();

    if (!culqiResp.ok) {
      console.error('Culqi rechazó el cargo:', culqiData);
      return res.status(culqiResp.status).json({
        error: culqiData.user_message || culqiData.merchant_message || 'Pago rechazado',
        code: culqiData.error_code,
      });
    }

    // ── Cargo exitoso ──────────────────────────────────────────
    const orderId = culqiData.id || `ORD-${Date.now()}`;
    const amountSoles = (amount / 100).toFixed(2);

    // ── Notificar (no bloqueante) ──────────────────────────────
    await Promise.allSettled([
      sendCustomerEmail({ email, orderId, amountSoles, items, customer }),
      sendOwnerEmail({ orderId, amountSoles, email, items, customer }),
      // Fase 2: HubSpot integration
      // createHubspotDeal({ email, orderId, amountSoles, items, customer }),
    ]);

    return res.status(200).json({
      success: true,
      orderId,
      culqi_id: culqiData.id,
      amount: amountSoles,
      currency: 'PEN',
      receipt_url: culqiData.outcome?.code ? `https://panel.culqi.com/charges/${culqiData.id}` : null,
    });

  } catch (err) {
    console.error('Error procesando /api/culqi-charge:', err);
    return res.status(500).json({ error: 'Error interno — intentá de nuevo o contactanos por WhatsApp' });
  }
}

// ─────────────────────────────────────────────────────────────────
// Helpers de email vía Resend (https://resend.com)
// ─────────────────────────────────────────────────────────────────

async function sendEmail({ to, subject, html }) {
  const KEY = process.env.RESEND_API_KEY;
  if (!KEY) {
    console.warn('RESEND_API_KEY no configurada — email omitido');
    return null;
  }
  try {
    const resp = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Alpha Tech <comercial@alphatechnologique.com>',
        to: Array.isArray(to) ? to : [to],
        subject,
        html,
      }),
    });
    return await resp.json();
  } catch (err) {
    console.error('Resend error:', err);
    return null;
  }
}

function itemsTableHtml(items) {
  if (!items || !items.length) return '';
  const rows = items.map(i => `
    <tr>
      <td style="padding:8px;border-bottom:1px solid #eee">${escape(i.nombre || i.sku)}</td>
      <td style="padding:8px;border-bottom:1px solid #eee;text-align:center">${i.qty}</td>
      <td style="padding:8px;border-bottom:1px solid #eee;text-align:right">S/. ${(i.precio * i.qty).toFixed(2)}</td>
    </tr>
  `).join('');
  return `
    <table style="width:100%;border-collapse:collapse;margin:18px 0;font-family:Arial,sans-serif;font-size:14px">
      <thead>
        <tr style="background:#001540;color:#fff">
          <th style="padding:10px;text-align:left">Producto</th>
          <th style="padding:10px;text-align:center">Cant.</th>
          <th style="padding:10px;text-align:right">Subtotal</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

function escape(s) {
  return String(s || '').replace(/[<>&"]/g, c => ({ '<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;' }[c]));
}

async function sendCustomerEmail({ email, orderId, amountSoles, items, customer }) {
  const name = customer?.firstName || 'Hola';
  const html = `
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#0F1B33;line-height:1.6">
      <div style="background:#001540;color:#fff;padding:32px 24px;text-align:center">
        <h1 style="margin:0;font-size:24px">¡Gracias por tu compra, ${escape(name)}!</h1>
        <p style="margin:8px 0 0;opacity:.8">Alpha Tech Solutions</p>
      </div>
      <div style="padding:24px">
        <p>Tu pago fue procesado correctamente. Aquí está el resumen:</p>
        <p><strong>Orden:</strong> <code>${escape(orderId)}</code></p>
        <p><strong>Total:</strong> S/. ${amountSoles}</p>
        ${itemsTableHtml(items)}
        <p>Te vamos a contactar en las próximas 24 h para coordinar la entrega o el agendamiento de tu sesión.</p>
        <p style="margin-top:32px;font-size:13px;color:#666">
          Cualquier consulta: respondé este email o escribinos a
          <a href="https://wa.me/51922877190" style="color:#008EAA">WhatsApp +51 922 877 190</a>.
        </p>
      </div>
      <div style="background:#f5f5f5;padding:16px;text-align:center;font-size:12px;color:#666">
        Alpha Tech Solutions S.A.C. · RUC 20615287203 · Lima, Perú
      </div>
    </div>
  `;
  return sendEmail({ to: email, subject: `Confirmación de tu compra — ${orderId}`, html });
}

async function sendOwnerEmail({ orderId, amountSoles, email, items, customer }) {
  const owner = process.env.NOTIFY_EMAIL_OWNER || 'comercial@alphatechnologique.com';
  const html = `
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#0F1B33">
      <h2 style="color:#FE5000">🎉 Nueva venta — ${orderId}</h2>
      <p><strong>Total:</strong> S/. ${amountSoles}</p>
      <p><strong>Cliente:</strong> ${escape(customer?.firstName || '')} ${escape(customer?.lastName || '')}<br>
         <strong>Email:</strong> <a href="mailto:${escape(email)}">${escape(email)}</a><br>
         <strong>Tel:</strong> ${escape(customer?.phone || '—')}</p>
      ${itemsTableHtml(items)}
      <p><a href="https://panel.culqi.com/charges/${escape(orderId)}" style="background:#008EAA;color:#fff;padding:10px 18px;text-decoration:none;border-radius:6px;display:inline-block">Ver en panel Culqi →</a></p>
    </div>
  `;
  return sendEmail({ to: owner, subject: `💰 Venta nueva: S/. ${amountSoles} — ${orderId}`, html });
}
