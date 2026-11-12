# Iteración 08 — silencio, portadas y miniaturas HD

- Los tres videos enlazados por la web no tienen pista de audio. AMG y Civic exportados en H.264 sin audio a su resolución, duración y fps originales. Porsche ya era una exportación sin audio. Se añade muted al reproductor como estado inicial.
- Sin música añadida: queda pendiente una pista propia que el propietario elija.
- Miniaturas 3D regeneradas a 1920 × 1248 con Blender Cycles CPU, antialiasing, iluminación y sombreado suave con aristas preservadas. Las geometrías estáticas usan agrupación espacial de 0,0015 frente al 0,0075 del visor (cinco veces más fina). No se aumenta el peso de las mallas interactivas.
- WebP de alta calidad para la web. El case conserva la cara con relieve; Porsche conserva la transformación de la iteración 06.
- Portadas vectoriales ES/EN para AMG y Civic, con texto nítido. AMG utiliza el render HD como referencia 3D; Civic utiliza un fotograma a tamaño nativo dentro de la composición, sin ampliarlo. Porsche utiliza el render HD.
- Las portadas no añaden detalle a los videos: AMG 576 × 1024 y Civic 478 × 640. La mejora de la reproducción requeriría originales de mayor resolución.
- Favicon SVG trazado desde la silueta alfa de la chakana con A: negro en tema claro y blanco en tema oscuro mediante prefers-color-scheme. PNG de respaldo con fondo blanco para navegadores que no admitan SVG.

Validación: pistas MP4 analizadas (sin soun, con vide), duración conservada; archivos, enlaces, imágenes 1920 × 1248, SVG válidos y referencias en ambas páginas. Inspección visual de renders AMG, Volkswagen y case. Interacción de reproductores y cambio de tema del favicon pendientes de revisión en navegador.

Reconstrucción habitual: build_v4.py conserva los medios preparados y aplica build_iteration8.py al final. Para regenerar geometría estática: prepare_hd_thumbnails.py con Python/NumPy/Pillow; después render_hd_thumbnails.py con Blender 5.1 en background. Para reexportar videos sin audio: export_silent_videos.py con Blender. Los originales del usuario no se modifican.
