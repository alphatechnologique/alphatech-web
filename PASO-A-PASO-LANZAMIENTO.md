# 🚀 Alpha Tech — Paso a paso de lanzamiento

Guía operativa para que Arturo levante el sitio + pasarela Culqi LIVE.

**Tiempo estimado total:** ~45 minutos
**Lo que NO está cubierto acá:** subir a GitHub (eso ya está hecho con el .bat)

---

## ⚙️ Antes de empezar — abrí 4 pestañas en el navegador

1. https://panel.culqi.com (logueado)
2. https://resend.com (logueado con `admin@alphatechnologique.com`)
3. https://vercel.com (logueado con GitHub)
4. https://squareup.com → panel donde tenés el dominio (Square Domains)

Tené a mano un archivo `.txt` o nota donde vas pegando las llaves que copias. Borrá la nota al final.

---

# PARTE 1 — Culqi (5 min)

## 1.1 Obtener tus llaves LIVE

1. En **panel.culqi.com → Desarrollo → Llaves API**
2. Verás:
   - **Llave pública** — `pk_live_xxxxxxxxxx` → la usás en frontend (HTML)
   - **Llave privada** — `sk_live_xxxxxxxxxx` → la usás en backend (Vercel env)
3. Copialas a tu nota temporal. **NUNCA las pegues en chat, email, ni Slack.**

⚠️ Las RSA keys NO se usan. Ignoralas.

## 1.2 Activar modo prueba (paralelo — opcional pero recomendado)

Si NO encontrás el toggle:
- Mandá email a `soporte@culqi.com` desde `admin@alphatechnologique.com`:
  > Asunto: Habilitar llaves de prueba (sandbox)
  > Hola, necesito habilitar las llaves de prueba para mi cuenta corporativa. RUC: 20615287203. Razón social: Alpha Tech Solutions S.A.C. Gracias.
- Si te llegan las TEST keys después, simplemente las swapeas en Vercel cuando quieras y volvés a LIVE cuando termines de testear.

---

# PARTE 2 — Resend (10 min)

## 2.1 Obtener tu API key

1. Dashboard → **API Keys** (menú izquierdo)
2. Click **Create API Key**
3. Nombre: `Alpha Tech Web — Production`
4. Permission: **Sending access** (no Full Access — más seguro)
5. Domain: dejar **All domains** por ahora
6. Click **Add**
7. Copiá el `re_xxxxxxxxxx` que aparece. **Solo se muestra una vez.** Pegalo en tu nota.

## 2.2 Verificar dominio alphatechnologique.com

1. Dashboard → **Domains** (menú izquierdo)
2. Click **Add Domain**
3. Domain: `alphatechnologique.com`
4. Region: **us-east-1** (default está bien)
5. Click **Add**
6. Resend te muestra **4-5 registros DNS** que tenés que agregar:
   - 1 registro **TXT** (verificación SPF + DKIM, típicamente `resend._domainkey`)
   - 1 registro **MX** (opcional pero recomendado)
   - 1 registro **TXT** (SPF: `v=spf1 include:amazonses.com ~all`)
   - 1 registro **DMARC** (TXT)
7. **DEJÁ ESTA PESTAÑA ABIERTA** — los necesitamos en la Parte 4.

---

# PARTE 3 — Vercel (10 min)

## 3.1 Importar el repo

1. Dashboard → **Add New → Project**
2. Vercel detecta tus repos de GitHub. Buscá **alphatech-web** → click **Import**
3. En "Configure Project":
   - **Framework Preset:** *Other*
   - **Root Directory:** `.` (raíz, dejar vacío)
   - **Build Command:** dejar vacío
   - **Output Directory:** dejar vacío
   - **Install Command:** dejar vacío
4. **NO hagas click en Deploy todavía.** Primero agregá las env vars.

## 3.2 Configurar variables de entorno

1. En la misma pantalla de Import, abrí **Environment Variables**
2. Agregá una por una (todas en **Production, Preview, Development**):

| Name | Value (pegar tu llave) |
|---|---|
| `CULQI_SECRET_KEY` | `sk_live_...` (pegado de tu nota) |
| `CULQI_PUBLIC_KEY` | `pk_live_...` (pegado de tu nota) |
| `RESEND_API_KEY` | `re_...` (pegado de tu nota) |
| `NOTIFY_EMAIL_OWNER` | `comercial@alphatechnologique.com` |

3. Ahora sí: **Deploy**
4. Espera 30-60 seg. Vercel publica el sitio en una URL `alphatech-web-xxx.vercel.app`
5. Abrí esa URL → debería verse igual que el sitio actual

## 3.3 Conectar tu dominio personalizado

1. En tu proyecto Vercel → **Settings → Domains**
2. Click **Add** → escribí `alphatechnologique.com` → Add
3. Vercel te dice "Invalid Configuration — Add A record" y muestra los registros DNS necesarios. Anotá:
   - **A record:** `@` → IP que te muestre Vercel (típicamente `76.76.21.21`)
   - **CNAME:** `www` → `cname.vercel-dns.com`
4. Click **Add** otra vez para agregar `www.alphatechnologique.com`
5. **DEJÁ ESTA PESTAÑA ABIERTA** — los DNS los configuramos en la Parte 4.

---

# PARTE 4 — DNS en Square Domains (10 min)

Aquí es donde combinás los registros que te dieron **Resend (Parte 2.2)** y **Vercel (Parte 3.3)**.

## 4.1 Acceder al panel DNS

1. squareup.com → tu dashboard → **Online → Domains** (o donde tengas el dominio gestionado en Square)
2. Click en `alphatechnologique.com`
3. Buscá la sección **Manage DNS** / **DNS Settings** / **Configuración DNS**

## 4.2 Backup del estado actual (precaución)

Antes de tocar nada:
1. Tomá un **screenshot** de los registros actuales
2. Guardá ese screenshot — si algo sale mal podés revertir manualmente

## 4.3 Eliminar registros conflictivos (si existen)

Si ya hay un registro **A** para `@` apuntando a otro IP (no Vercel) o un **CNAME** para `www` apuntando a GitHub Pages, hay que reemplazarlos. **No los borres todavía — solo identifícalos.**

Los registros que NO se borran:
- MX records (tu email Workspace)
- TXT con `google-site-verification`
- TXT con `v=spf1` viejo si no es de Resend
- Cualquier registro Google Workspace

## 4.4 Agregar los registros nuevos

**Para Vercel:**
- Tipo `A`, Host `@`, Valor `76.76.21.21`, TTL `3600`
- Tipo `CNAME`, Host `www`, Valor `cname.vercel-dns.com`, TTL `3600`

**Para Resend** (copiá tal cual te muestre Resend en su pestaña):
- Tipo `TXT`, Host `resend._domainkey`, Valor (la cadena larga que te dieron)
- Tipo `TXT`, Host `@`, Valor `v=spf1 include:amazonses.com ~all`
- Tipo `TXT`, Host `_dmarc`, Valor `v=DMARC1; p=none;`

## 4.5 Esperar propagación

DNS tarda **5-30 min** en propagar globalmente. Para chequear:
- https://dnschecker.org → escribí `alphatechnologique.com` → seleccioná tipo `A`
- Cuando veas el IP `76.76.21.21` en la mayoría de los servidores → DNS listo

Mientras tanto pasá a la Parte 5.

---

# PARTE 5 — Pegar la PUBLIC key en checkout.html (3 min)

1. Abrí `checkout.html` en tu editor (VS Code, Notepad++, etc.)
2. Buscá (`Ctrl+F`): `pk_test_REEMPLAZAR_AQUI`
3. Reemplazalo por tu llave pública real: `pk_live_xxxxxxxxxx`
4. Guardar
5. Ejecutá el `.bat` `SUBIR-A-GITHUB.bat` con doble click → sube el cambio
6. Vercel detecta el push y re-deploya automático (~30 seg)

---

# PARTE 6 — Volver a Vercel y Resend a confirmar

## 6.1 Vercel → verificar dominio activo

1. Vercel → tu proyecto → Settings → Domains
2. Refrescá la pestaña
3. Debería decir **alphatechnologique.com → Valid Configuration ✓** (con candado verde)
4. Abrí https://alphatechnologique.com en navegador incógnito → debería cargar el sitio nuevo

## 6.2 Resend → verificar dominio verificado

1. Resend → Domains
2. Refrescá la pestaña
3. Debería decir **alphatechnologique.com → Verified ✓** (los 3-4 registros con check verde)

Si después de 30 min algún registro no se verifica, chequeá que el valor del DNS esté **exactamente** igual al que pide Resend (sin comillas extra, sin punto al final, sin espacios).

---

# PARTE 7 — Testing en LIVE (con cuidado) (5 min)

## 7.1 Protocolo de prueba mínima

Como vamos directo a LIVE sin sandbox, hacemos esto para validar sin riesgo financiero:

1. Andá a https://alphatechnologique.com/catalogo-simulations.html
2. Agregá la **Bautismo aeronáutico (S/. 49)** al carrito — es el monto más bajo
3. Click "Finalizar compra"
4. Llená los datos (Nombre / Apellido / Email / Teléfono con TU info real)
5. Click "Pagar con tarjeta"
6. Widget Culqi se abre → pegá **tu propia tarjeta de crédito personal**
7. Cobro real de **S/. 49** se procesa

## 7.2 Validar que TODO funcionó

Verificá los 5 puntos:

- [ ] Te redirigió a `/gracias.html?orden=chr_…&monto=49.00`
- [ ] Tu carrito quedó vacío (chequear ícono badge en navbar)
- [ ] Email confirmación llegó a TU bandeja de entrada (la que pusiste en el form)
- [ ] Email alerta llegó a `comercial@alphatechnologique.com`
- [ ] En **panel.culqi.com → Cargos** aparece el cobro de S/. 49

## 7.3 Refund inmediato

Si todo OK:
1. Panel Culqi → Cargos → tu cobro → **Reembolsar**
2. Reembolsar el monto completo (S/. 49)
3. El dinero vuelve a tu tarjeta en 5-10 días hábiles

Si algo NO funciona:
1. Panel Culqi → Cargos → tu cobro → Reembolsar igual (no le cobramos a Arturo)
2. Revisar **Vercel → Deployments → último → Functions → Logs** para ver qué falló
3. Avisame qué error sale y lo resuelvo

---

# ✅ Checklist final

Después de Parte 7 OK:

- [ ] DNS `@` apunta a `76.76.21.21` (Vercel)
- [ ] DNS `www` apunta a `cname.vercel-dns.com`
- [ ] DNS Resend (3-4 TXT records) verificados
- [ ] Vercel deploy verde con dominio personalizado
- [ ] Resend domain status: Verified
- [ ] 4 env vars cargadas en Vercel
- [ ] `pk_live_…` real pegado en checkout.html
- [ ] Tu prueba LIVE de S/. 49 funcionó end-to-end
- [ ] Te reembolsaste vos mismo desde panel Culqi

🎉 **El sitio está vendiendo de verdad.**

---

# 🆘 Problemas comunes y soluciones rápidas

| Problema | Causa probable | Solución |
|---|---|---|
| Vercel: "Domain Invalid Configuration" | DNS aún no propaga | Esperá 15 min más, refrescá dnschecker.org |
| Resend: "Domain not verified" después de 30 min | TXT record mal copiado | Borrá y volvé a pegar tal cual lo muestra Resend |
| Widget Culqi no abre | `pk_live_…` mal pegado o ad-blocker activo | Chequear consola (F12) |
| Pago va a 500 error | env var mal escrita en Vercel | Vercel → Settings → Env Vars → revisar typos |
| Email no llega | Resend domain not verified, o llegó a spam | Chequeá spam + Resend → Logs |
| El sitio sigue mostrando GitHub Pages | DNS aún no propaga, o caché de navegador | Esperá + abrir en incógnito |

---

**Cuando tengas dudas en cualquier paso, mandame screenshot (sin keys visibles) y te ubico.**
