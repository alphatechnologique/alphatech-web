# Iteración 05 — plata, rojo y avance Porsche

- Cabecera ATPerformance: texto plata y rojo. ENGINEERED. BUILT. DRIVEN. pasa a 12 px y peso 700 en escritorio; 9 px en móvil. BUILT. destacado en rojo. Chakana conservada a 110 px / 72 px.
- Cambios aplicados en español e inglés.
- Video Porsche recortado al intervalo [20, 28) segundos: 240 fotogramas, 30 fps, 1324 × 842. Sin pista de audio en esta exportación de presentación. Original intacto.
- Poster tomado del segundo 27 del original. Controles de reproducción y sin autoplay.
- Superposición del diseño corregida con transformación rígida aproximada, revisada contra el video y proyecciones de ambas geometrías. Escala relativa conservada; ninguna pieza se estira para hacerla coincidir.
- Transformación reproducible en PORSCHE-REGISTRATION.json; orientación y normalización común en PORSCHE-COORDINATES.json. Unidades del STL conservadas. No se certifica encaje mecánico ni tolerancias.
- Visor mantiene Escaneo / Diseño / Ambos y opacidad ajustable.

Validación: enlaces y archivos locales, siete fichas, índices y datos de geometría, idiomas y duración/resolución del video comprobados. Se inspeccionaron el primer y último fotograma del recorte. Interacción WebGL y disposición responsive en navegador pendientes de comprobación visual.

Reconstrucción: ejecutar build_v4.py con Python + NumPy + Pillow. Para regenerar el recorte, ejecutar trim_dashboard_video.py desde Blender 5.1 en modo background. El constructor conserva el recorte y no vuelve a copiar la película completa.
