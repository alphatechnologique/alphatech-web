# Iteración 04 — avance del tablero Porsche

- Video original `porsche 924 board/videos/Dashboard v1.mp4`, copiado sin modificar a `atperformance/assets/porsche-dashboard-progress.mp4`.
- Duración indicada por el contenedor: 28,07 s. Pistas identificadas AVC/H.264 y MP4A. Reproducción con controles, sin autoplay, y carga de metadatos.
- Sección de avance del diseño y acceso desde la ficha del tablero, en español e inglés.
- STL de diseño confirmado: `porsche dashboard 1 complet.stl`.
- Vistas 3D Escaneo / Diseño / Ambos. Escaneo gris y diseño rojo, con control de opacidad del diseño cuando ambos están visibles.
- Para la comparación se usa `porsche 924 board nu 2.stl` como escaneo de referencia. El PLY usado anteriormente tiene otra orientación. No se ha realizado registro automático ni se afirma un ajuste dimensional validado.
- Las dos geometrías comparten exactamente una rotación, un centro y una escala de visualización. No se centran ni escalan por separado. Parámetros guardados en PORSCHE-COORDINATES.json.
- El diseño se simplifica para navegación web; la pieza original no se modifica.
- El video incorporado es idéntico al original por comparación SHA-256. Recursos, geometrías y sintaxis comprobados. Reproducción del MP4 e interacción GPU en navegador pendientes por las restricciones ya documentadas.

La versión actual se abre en `atperformance/index.html` o `atperformance/en.html`. `build_v4.py` reconstruye la base y aplica esta actualización de Porsche.
