# Brief — Actualización de datos finales del sitio v3 (post-bloqueos)

> **Audiencia:** ejecutor Claude Sonnet con acceso al filesystem.
> **Versión:** 1.0 · 2026
> **Carpeta de trabajo:** `/Alpha Tech - Web Maintenance/Alpha tech S Web v3/`
> **Lectura previa obligatoria:**
> 1. `_CONTEXTO-DE-TRABAJO.md` en `/AlphaTech-Marketing/`
> 2. `BLOQUEOS.md` (este directorio)
> 3. `MAPEO-DE-CAMBIOS.md` (este directorio)
> 4. `validacion-culqi.md` (este directorio)

---

## 1. Contexto

El sitio v3 está prácticamente listo para la auditoría de Culqi. Faltan 3 cambios menores con datos que el GM acaba de proveer. Tu trabajo: aplicar esos cambios, actualizar `BLOQUEOS.md` para marcarlos como resueltos, y entregar un reporte de cierre.

**No modifiques nada más** del sitio. Estos son cambios quirúrgicos sobre datos puntuales.

---

## 2. Datos lockeados por el GM (aplicar exactamente como aparece)

### 2.1. Dirección física registrada en SUNAT

```
Jirón Oxapampa 243, Breña, Lima
```

Para texto inglés (cuando aplique):

```
Jiron Oxapampa 243, Breña, Lima, Peru
```

### 2.2. HTTPS / SSL

✅ **Activo en `alphatechnologique.com`.** No requiere ninguna acción técnica del sitio. Solo registrarlo como resuelto en `BLOQUEOS.md`.

### 2.3. URL Instagram

```
https://www.instagram.com/alphatechsolutions.pe?igsh=YnpsbHdrMmtwbGRr
```

### 2.4. URL LinkedIn

```
https://www.linkedin.com/company/alpha-tech-solutions-sac
```

---

## 3. Cambios a aplicar

### 3.1. Reemplazar placeholder de dirección en páginas legales

**Operación:** find-and-replace global en 4 archivos.

**Buscar (placeholder ES):**
```
[Dirección registrada en SUNAT — pendiente], Lima, Perú
```

**Reemplazar con (ES):**
```
Jirón Oxapampa 243, Breña, Lima, Perú
```

**Buscar (placeholder EN):**
```
[SUNAT-registered address — pending], Lima, Peru
```

**Reemplazar con (EN):**
```
Jiron Oxapampa 243, Breña, Lima, Peru
```

**Archivos afectados:**
- `terminos.html` (ES) — sección "1. Identificación del prestador"
- `privacidad.html` (ES) — sección "1. Responsable del tratamiento"
- `terms.html` (EN) — section "1. Service provider identification"
- `privacy.html` (EN) — section "1. Data controller"

Verificar después del replace que ninguna otra página contenga el placeholder (puede haberse colado en algún sitio que no se documentó).

### 3.2. Actualizar links de redes sociales en el footer (todas las 32 páginas)

**Buscar el bloque Instagram (aparece dos veces por footer — ES y EN footers comparten estructura):**

```html
<a href="#" class="footer-social-link" aria-label="Instagram" target="_blank" rel="noopener">
```

**Reemplazar con:**

```html
<a href="https://www.instagram.com/alphatechsolutions.pe?igsh=YnpsbHdrMmtwbGRr" class="footer-social-link" aria-label="Instagram" target="_blank" rel="noopener">
```

**Buscar el bloque LinkedIn:**

```html
<a href="#" class="footer-social-link" aria-label="LinkedIn" target="_blank" rel="noopener">
```

**Reemplazar con:**

```html
<a href="https://www.linkedin.com/company/alpha-tech-solutions-sac" class="footer-social-link" aria-label="LinkedIn" target="_blank" rel="noopener">
```

**Aplicar a las 32 páginas activas (todas excepto `gracias.html`, `thanks.html` y `preview-logo-v2.html`).**

Si los `href="#"` aparecen en otras partes del sitio (por ejemplo en navbars con links rotos), **NO los toqués** salvo que estén marcados como social-link.

### 3.3. Actualizar BLOQUEOS.md

Marcar los 3 items como ✅ resueltos en el archivo `BLOQUEOS.md`:

- §1 Dirección física → **✅ Resuelto: Jirón Oxapampa 243, Breña, Lima**
- §2 HTTPS activo → **✅ Confirmado por GM**
- §4 URLs de redes sociales → **✅ Resueltos** con los enlaces de §2.3 y §2.4

Mantené los items 5 (gracias.html sin footer), 6 (proceso de afiliación), 7 (fase 2) y 8 (items menores SEO) como están — esos siguen pendientes.

### 3.4. Actualizar validacion-culqi.md

En la sección §9 "Items que el GM debe completar antes de auditoría Culqi", marcá items 1 y 2 como resueltos. Item 3 (solicitar afiliación), 4 (auditoría) y 5 (llaves LIVE) siguen pendientes — esos son acciones que solo Arturo puede ejecutar.

---

## 4. Cómo ejecutar (sugerencia técnica)

La forma más eficiente es un script Python o un grupo de comandos `sed`. Hacelo como prefieras.

**Estructura sugerida del script:**

```python
import re
from pathlib import Path

BASE = Path("/sessions/kind-magical-bardeen/mnt/Documents/Alpha Tech - Web Maintenance/Alpha tech S Web v3")

# Replacements globales
replacements = [
    # Dirección ES
    (
        r"\[Dirección registrada en SUNAT — pendiente\], Lima, Perú",
        "Jirón Oxapampa 243, Breña, Lima, Perú",
    ),
    # Dirección EN
    (
        r"\[SUNAT-registered address — pending\], Lima, Peru",
        "Jiron Oxapampa 243, Breña, Lima, Peru",
    ),
    # Instagram
    (
        r'<a href="#" class="footer-social-link" aria-label="Instagram"',
        '<a href="https://www.instagram.com/alphatechsolutions.pe?igsh=YnpsbHdrMmtwbGRr" class="footer-social-link" aria-label="Instagram"',
    ),
    # LinkedIn
    (
        r'<a href="#" class="footer-social-link" aria-label="LinkedIn"',
        '<a href="https://www.linkedin.com/company/alpha-tech-solutions-sac" class="footer-social-link" aria-label="LinkedIn"',
    ),
]

for html_file in sorted(BASE.glob("*.html")):
    txt = html_file.read_text(encoding="utf-8")
    original = txt
    for pat, rep in replacements:
        txt = re.sub(pat, rep, txt)
    if txt != original:
        html_file.write_text(txt, encoding="utf-8")
        print(f"✓ {html_file.name}")
```

Guardalo en `/sessions/kind-magical-bardeen/apply-final-data.py` o donde te sea cómodo.

---

## 5. Validación post-cambios

Después de ejecutar:

1. **Conteo de placeholders restantes:** `grep -r "pendiente" *.html` no debe encontrar el placeholder de dirección. Si aparece, investigá y resolvé.
2. **Conteo de social links rotos:** `grep -c 'href="#" class="footer-social-link"' *.html` debe dar `0`.
3. **Apertura visual:** abrí `terminos.html` y `privacidad.html` en el navegador y verificá que la dirección aparece correctamente.
4. **Apertura de footer:** abrí `index.html` y `en.html`, hover sobre los iconos de LinkedIn e Instagram — los hrefs deben mostrar las URLs reales en el status bar.
5. **Verificación de la versión EN:** abrí `terms.html` y `privacy.html` y verificá que aparece "Jiron Oxapampa 243, Breña, Lima, Peru" (sin tilde en "Jiron", manteniendo "Breña" con eñe).

---

## 6. Entrega final

Producí un mensaje al GM con este formato:

```
✅ Datos finales aplicados al sitio v3:

1. Dirección física actualizada en 4 páginas legales
   (terminos, terms, privacidad, privacy)
2. URLs de Instagram y LinkedIn actualizadas en 32 páginas
3. BLOQUEOS.md actualizado con items resueltos
4. validacion-culqi.md actualizado

Próximo paso (acción del GM):
→ Solicitar afiliación en afiliate.culqi.com/culqionline/afiliacion
   con los datos del negocio (RUC 20615287203, dominio
   alphatechnologique.com, Razón Social Alpha Tech Solutions S.A.C.)
→ Esperar auditoría de Culqi (1-3 semanas)
→ Recibir llaves LIVE y arrancar fase 2 (integración técnica real)

Items aún pendientes (no bloquean Culqi):
- Decisión sobre footer en gracias.html / thanks.html
- SEO menores (sitemap, robots.txt, Schema.org)
- Fase 2: contratar backend + implementar stubs api/
```

---

## 7. Reglas no negociables

- Respetá `_CONTEXTO-DE-TRABAJO.md`: voz híbrido técnico-directo, paleta navy/orange/teal, política agresiva
- Solo aplicá los cambios documentados en este brief
- No agregues, quites ni renombrés archivos
- Si encontrás algo raro (otro placeholder no documentado, un href roto que no sea de social), documentalo en un `ASUMIDOS.md` y seguí
- No toqués `gracias.html` ni `thanks.html` (las thank-you pages se discuten en otro hilo con el GM)

---

## 8. Open items que NO se resuelven en este paquete

Estos siguen abiertos:

- Decisión sobre agregarles footer a `gracias.html` / `thanks.html`
- Schema.org Organization / BreadcrumbList (SEO)
- sitemap.xml / robots.txt
- Fase 2 completa de integración técnica Culqi

---

*Cerrá este paquete y reportá al GM. Una vez ejecutado, el sitio v3 está 100% listo para que el GM solicite afiliación a Culqi.*
