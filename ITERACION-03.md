# Iteración 03 — 11 de noviembre de 2026

## Resultado

Siete fichas: espejos Civic Type R, volante Volkswagen, volante Porsche, tablero Porsche 924, case para fibra, consola Nissan Kicks y consola central Nissan Kicks. El AMG A35 deja de figurar en el portafolio y selector actuales.

Solo los espejos se presentan como terminados. El resto figura como escaneo disponible y proyecto en desarrollo.

La chakana blanca completa del kit sustituye al archivo anterior, que contenía márgenes grandes y una figura recortada. Tamaño de la caja: 110 px en escritorio y 72 px en móvil; el emblema conserva su relación de aspecto.

## Visor

- Ventana ampliada nativa con cierre por botón y Escape, devolución del foco y bloqueo del scroll de fondo.
- Superficie gris titanio iluminada, caras triangulares rellenas y profundidad WebGL. Las caras ocultas dejan de superponerse como líneas.
- Malla opcional superpuesta, rotación por arrastre/flechas, zoom con rueda/botones/teclado y reinicio.
- Selector de los siete proyectos dentro de la misma ventana.
- Modelos cargados solo al abrirlos, sin dependencias CDN ni necesidad de descargar los STL originales.
- Vista estática sombreada como alternativa cuando WebGL o la carga fallan.

## Fuentes

| Proyecto | Archivo original relativo a Alpha tech Proyectos |
| --- | --- |
| Espejos Civic | Honda civic Type R/honda civic type r espejos.stl |
| Volante Volkswagen | porsche 924 board/Volante VW scan.stl |
| Volante Porsche | porsche 924 board/volante porsche simpl.stl |
| Tablero Porsche | porsche 924 board/pSGC3_tyR7_7htk_I2XC/result/Mesh.ply |
| Case | case para fibra/case para fibra.stl |
| Consola Kicks | consola kicks/sVsOq9H_a0Q73X_s3ceL4_QoxvJh/result/Fused.ply |
| Consola central Kicks | consola central/pgKn4_9rtk_ofe7_oonK/result/Mesh.ply |

El tablero usa la malla de proyecto PLY, con mejor orientación inicial que el STL de la iteración anterior. Las imperfecciones y zonas incompletas propias del escaneo permanecen: el sombreado no equivale a reparar la geometría ni a validar su fabricación.

## Construcción y comprobaciones

Ejecutar `build_v4.py` para actualizar las páginas y geometrías de esta iteración; llama a `build_iteration3.py`. Requiere Python, numpy y Pillow y las rutas originales indicadas. Las páginas ya generadas no necesitan Python.

Ejecutar `validate_v4.py` para validar páginas, recursos y los siete modelos. Se ha comprobado también la sintaxis JavaScript y se han inspeccionado las siete vistas sombreadas estáticas.

La ejecución del visor GPU y las interacciones en navegador siguen pendientes: el navegador de esta sesión no permite abrir archivos file:// y la conexión localhost falló en la revisión anterior. No se afirma una prueba visual de escritorio/móvil completa.

Abrir `atperformance/index.html` (ES) o `atperformance/en.html` (EN) desde el navegador del usuario. Se continúa en la copia autorizada de Documents/ChatGPT/Alpha tech/Alpha tech S Web v4; no se modifica Web Maintenance.
