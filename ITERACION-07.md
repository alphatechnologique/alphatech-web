# Iteración 07 — medios reales y catálogo por aplicación

- AMG: modelo del visor y miniaturas sustituidos por `canard v5 w front.stl`, conservando el conjunto canard/frontal. Fuente indicada por el propietario.
- Video AMG original incorporado sin recorte: 425 fotogramas, 30 fps, 576 × 1024, aproximadamente 14,17 segundos. Prueba visual de flujo con humo sobre el prototipo instalado; no se presenta como medición de carga.
- Civic: `scan pov.mp4`, completo, 5400 fotogramas, 30 fps, 478 × 640, 3 minutos. Espacio propio para el escaneo de la zona inferior del parachoques trasero; separado del proyecto terminado de skinning.
- Ambos videos usan controles, reproducción manual, poster y preload="none". Archivos originales conservados byte a byte, con su audio original.
- `Volante fibra.jpeg` incorporado en la ficha de volante Porsche, el desarrollo del interior Porsche y la categoría de interiores. Identificado como render, no fotografía de pieza terminada. El visor de volante sigue mostrando el escaneo de referencia.
- Catálogo separado en motos, aerodinámica e interiores. Para motos: carenados laterales, quillas, colines y tapas, propuestos bajo evaluación/cotización por modelo; no stock ni trabajos presentados como terminados.
- Cubreespejos movidos al espacio Acabados en carbono / Skinning, con sus fotografías y cotización contextual. Diferencia explícita entre revestir una pieza base y fabricar una nueva.
- Formulario incorpora la categoría de carenados/piezas para moto.
- Español e inglés, ocho modelos, alineación Porsche y orientación del case conservadas.

Validación: archivos, enlaces, categorías, videos y posters; correspondencia del modelo AMG con la nueva fuente; conservación de medios por SHA-256; geometrías válidas; reconstrucción repetida. Interacción real de video/WebGL y diseño responsive en navegador aún pendientes.

Para reconstruir: build_v4.py. Los posters ya están incluidos; se tomaron de fotogramas de los videos originales. build_iteration7.py conserva los posters si no se dispone de la carpeta temporal de revisión.
