# Deploy Alpha Tech — Culqi + Vercel + Resend

Guía paso a paso para llevar el sitio de GitHub al aire con pasarela funcional.

---

## 📋 Checklist de cuentas necesarias

- [ ] **Culqi** — TEST keys (`pk_test_…` + `sk_test_…`) → panel.culqi.com → toggle "Modo prueba"
- [ ] **Vercel** — cuenta gratis vinculada al GitHub `alphatechnologique`
- [ ] **Resend** — cuenta gratis (registrarse con `admin@alphatechnologique.com`)
- [ ] **Square Domains** — acceso al panel DNS para apuntar `alphatechnologique.com` a Vercel
- [ ] **Repo GitHub** — `alphatechnologique/alphatech-web` ya creado y subido

---

## 1️⃣ Conectar Vercel al repo GitHub

1. Entrá a https://vercel.com → **Continue with GitHub**
2. Autoriza Vercel a leer tu repo `alphatechnologique/alphatech-web`
3. Click en **Add New Project** → seleccioná `alphatech-web` → **Import**
4. En la pantalla de Configure Project:
   - **Framework Preset:** Other
   - **Root Directory:** dejar en blanco (raíz del repo)
   - **Build Command:** dejar vacío
   - **Output Directory:** dejar vacío
5. Click **Deploy**

Vercel publica el sitio en una URL tipo `alphatech-web-xxx.vercel.app` automáticamente.

---

## 2️⃣ Configurar variables de entorno en Vercel

En el panel de Vercel → tu proyecto → **Settings → Environment Variables**, agregá:

| Variable | Valor (pegar tu llave real) | Environment |
|---|---|---|
| `CULQI_SECRET_KEY` | `sk_test_xxxxxxxxxx` | Production + Preview + Development |
| `CULQI_PUBLIC_KEY` | `pk_test_xxxxxxxxxx` | Production + Preview + Development |
| `RESEND_API_KEY` | `re_xxxxxxxxxx` | Production + Preview + Development |
| `NOTIFY_EMAIL_OWNER` | `comercial@alphatechnologique.com` | Production + Preview + Development |

Después de agregarlas: **Deployments → último deploy → "Redeploy"** para que tomen las variables.

---

## 3️⃣ Pegar la PUBLIC key en checkout.html

Vercel inyecta env vars solo en server-side. Para el frontend hay que pegar la `pk_test_…` directamente en el HTML:

1. Abrí `checkout.html`
2. Buscá la línea:
   ```js
   const CULQI_PUBLIC_KEY = 'pk_test_REEMPLAZAR_AQUI';
   ```
3. Reemplazá `pk_test_REEMPLAZAR_AQUI` por tu llave pública real
4. Commit + push → Vercel re-deploya solo

⚠️ La PUBLIC key es **pública por diseño** (Culqi así lo define). No es un secreto. La SECRET key NUNCA va acá.

---

## 4️⃣ Configurar Resend

1. Crear cuenta en https://resend.com
2. Dashboard → **Domains → Add Domain** → `alphatechnologique.com`
3. Resend te muestra registros DNS (TXT, MX, CNAME). Copialos.
4. Andá al panel de **Square Domains → DNS Records** y agregá esos registros tal cual.
5. Volvé a Resend y click **Verify Domain**. Tarda 5-30 min.
6. **API Keys → Create API Key** → permisos `sending_access` → copiar y pegar en Vercel (variable `RESEND_API_KEY`).

---

## 5️⃣ Apuntar el dominio alphatechnologique.com a Vercel

En Vercel → tu proyecto → **Settings → Domains**:
1. Agregá `alphatechnologique.com` y `www.alphatechnologique.com`
2. Vercel te muestra los registros DNS que necesitás (A record o CNAME)

En Square Domains → DNS:
1. Cambiá el A record de `@` (raíz) al IP que te indique Vercel (típicamente `76.76.21.21`)
2. CNAME `www` apuntando a `cname.vercel-dns.com`

Espera 5-30 min para que propague DNS.

---

## 6️⃣ Probar el flujo end-to-end

### Tarjetas de prueba Culqi (TEST mode)

Usá estas tarjetas en el widget Culqi cuando pruebes:

| Tipo | Número | CVV | Exp |
|---|---|---|---|
| Visa exitosa | 4111 1111 1111 1111 | 123 | 09/30 |
| Mastercard exitosa | 5111 1111 1111 1118 | 123 | 09/30 |
| Visa rechazada (testing fail) | 4000 0000 0000 0002 | 123 | 09/30 |

### Test journey

1. Abrí `alphatechnologique.com/catalogo.html`
2. Agregá productos al carrito
3. Click "Finalizar compra" → llega a `/checkout.html?cart=1`
4. Llená datos + click "Pagar con tarjeta"
5. Widget Culqi se abre → ingresá tarjeta de prueba
6. Si exitoso: redirige a `/gracias.html?orden=chr_…&monto=…`
7. Verificá:
   - [ ] Email de confirmación llegó al cliente
   - [ ] Email de notificación llegó a `comercial@alphatechnologique.com`
   - [ ] En **panel.culqi.com → Cargos** aparece el cargo de prueba
   - [ ] Carrito quedó vacío al volver

---

## 7️⃣ Cambiar a LIVE

Cuando ya probaste todo en TEST y funciona:

1. En **panel Culqi → arriba derecha** desactivá "Modo prueba"
2. Copiá las llaves LIVE (`pk_live_…` + `sk_live_…`)
3. En Vercel → Settings → Environment Variables → editá `CULQI_SECRET_KEY` y `CULQI_PUBLIC_KEY` con las nuevas LIVE
4. En `checkout.html` cambiá la `CULQI_PUBLIC_KEY = 'pk_live_…'`
5. Commit + push → Vercel re-deploya
6. Hacé **un pago real con tu propia tarjeta** por S/. 1 para validar (después te lo devolvés vos mismo desde el panel Culqi)

---

## 🆘 Troubleshooting

### El widget Culqi no abre
- Chequeá la consola del navegador (F12)
- Verificá que `CULQI_PUBLIC_KEY` no diga `REEMPLAZAR_AQUI`
- Asegurate de que el script `https://js.culqi.com/checkout-js` cargue (sin bloqueos de ad-blocker)

### Culqi devuelve "Token no válido"
- La llave pública del frontend tiene que ser del MISMO entorno (TEST o LIVE) que la secreta del backend
- No mezclar `pk_test_…` con `sk_live_…`

### Email no llega
- Verificá en Resend → Logs que el envío salió
- Si dice "Domain not verified" → completar verificación DNS
- Spam folder del destinatario

### El backend devuelve 500
- Vercel → Deployments → último deploy → Functions → ver logs en tiempo real
- Causa más común: variable de entorno no configurada o mal escrita

---

## 🗂 Estructura final del repo

```
alphatech-web/
├── api/
│   └── culqi-charge.js       ← backend serverless
├── *.html                     ← páginas estáticas
├── *.png                      ← imágenes catálogo
├── cart.js                    ← lógica carrito (frontend)
├── vercel.json                ← config Vercel
├── .env.example               ← template de variables
├── .gitignore                 ← excluye .env y basura
└── DEPLOY-CULQI.md            ← este archivo
```

---

## 📞 Siguiente fase (cuando Culqi LIVE funcione)

- Integración HubSpot (crear contact + deal automático en cada venta)
- Activación de membresía: marcar "Member Since" en HubSpot al pagar membresía
- Webhook receiver para refunds y disputas
- Dashboard simple de ventas dentro del sitio (`/admin/ventas.html` protegido)
