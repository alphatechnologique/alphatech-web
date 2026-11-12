/**
 * reclamaciones.js — STUB
 *
 * Endpoint que recibirá el POST del formulario de reclamaciones cuando exista backend.
 * Por ahora, el formulario hace fallback a mailto: en el frontend.
 *
 * TODO: implementar cuando exista backend.
 */

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { body } = req;

  // TODO:
  //  1. Validar campos requeridos
  //  2. Generar número de registro (formato AT-XXXXXXXX)
  //  3. Persistir en base de datos o Notion
  //  4. Enviar email a admin@alphatechnologique.com con todos los datos
  //  5. Enviar email de confirmación al remitente
  //  6. Responder con número de registro

  console.log('TODO: reclamaciones submission', body);
  return res.status(200).json({ received: true });
}
