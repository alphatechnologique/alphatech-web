# Iteración 09 — portadas ATP y navegación

- Integrada la imagen aprobada de Mercedes-AMG A35, escaneo del Civic y diseño de dashboard Porsche 924. Los tres paneles se separan sin retoques y se exportan a WebP de calidad 95.
- Portadas aplicadas en ES y EN. El texto de las imágenes aprobadas permanece en español en ambas versiones.
- Reproductores cuadrados con object-fit: contain para conservar todo el diseño y reproducir los videos sin recortarlos. Porsche limitado a 650 px y centrado.
- Navegación del header: 12 → 14 px; selector de idioma: 11 → 13 px. En móvil: menú 15 px e idioma 12 px.
- build_v4.py ejecuta build_iteration9.py al final para conservar los cambios al reconstruir.
- Comprobadas las seis referencias a portadas, archivos de video y atributos muted; inspeccionado el panel Civic exportado. No se verificó la interacción en navegador.
