# Iteración 06 — proyectos y cotización contextual

- Fichas destacadas para AMG A35 y Porsche 924, con secciones propias dentro de ATPerformance.
- AMG A35: geometrías reales v5 corregidas, derecha e izquierda, de la carpeta indicada. Visor interactivo para el canard derecho. Desarrollo de diseño y cálculo aerodinámico descrito según la información del propietario; no se publican cifras de carga ni promesas de rendimiento sin documentación.
- Porsche: etapas de escaneo, diseño, fabricación y acabado. Video 20–28 s conservado. Se elimina la rotación ICP de la iteración anterior. Traslación del diseño [175, -131, -124] en unidades fuente, con ejes originales y escala relativa intacta. Referencia de abertura [0,115,-220] llevada a [175,-16,-344], situada sobre el eje de la palanca. Vista superior inspeccionada para comprobar que el eje queda dentro de la abertura; altura y resto del ajuste siguen siendo visuales, no metrológicos.
- Civic: ficha de proyecto terminado de skinning con fotografía de fondo blanco.
- Case: miniatura y orientación inicial del visor giradas hacia la cara con relieve.
- Cada ficha permite cotizar su tipo de proyecto. Categorías: escaneo, volante, consola, dashboard, aerodinámica, carbono, case y diseño a medida.
- El formulario conserva el proyecto como referencia sin cambiar el vehículo escrito por el visitante. Cambiar manualmente la categoría limpia la referencia anterior.
- Español e inglés actualizados. Ocho modelos interactivos.

Comprobaciones: archivos y enlaces, ocho fichas y modelos, índices geométricos, referencias de cotización y correspondencia entre categorías y opciones del formulario. Prueba JS aislada de selección y composición del mensaje, sin envío. Vista superior de la consola e imágenes de los canards y del case inspeccionadas. La interacción WebGL y el diseño responsive aún requieren revisión en navegador.

Reconstrucción: build_v4.py ejecuta la base, la actualización Porsche y build_iteration6.py en ese orden. Los archivos CAD/STL originales permanecen intactos.
