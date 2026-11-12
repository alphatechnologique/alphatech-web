# Versión actual: iteración 09

Consultar ITERACION-09.md para las portadas ATP aprobadas y el aumento del tamaño de la navegación.

# Iteración 08

Consultar ITERACION-08.md para videos sin audio, miniaturas HD, portadas y favicon adaptativo.

# Versión actual: iteración 07

Consultar ITERACION-07.md para el AMG con frontal y prueba de aire, el POV del Civic, el render del volante y el catálogo separado de acabados.

# Versión actual: iteración 06

Consultar ITERACION-06.md para las fichas AMG/Porsche/Civic, cotizaciones por categoría, orientación del case y ajuste de consola.

# Versión actual: iteración 05

Consultar ITERACION-05.md para la cabecera plata/rojo, el video recortado y la alineación visual del Porsche. Las notas anteriores se conservan como historial.

# Versión actual: iteración 04

Consultar ITERACION-04.md para el video Porsche y la comparación entre escaneo y diseño.

# Versión actual: iteración 03

Consultar ITERACION-03.md para las siete fichas y el nuevo visor sombreado. Las notas siguientes describen la base inicial y han sido sustituidas en esos puntos.

# Alpha tech S Web v4 — iteración 01

Fecha: 11 de noviembre de 2026. Prototipo local, sin publicación.

## Abrir

Abre `index.html` para la web corporativa y entra a Performance.
También puedes abrir directamente `atperformance/index.html` (ES) o `atperformance/en.html` (EN).
No requiere instalación, servidor, conexión a una CDN ni proceso de compilación para Performance.
WhatsApp, Instagram y correo requieren sus aplicaciones/conexión correspondientes.

## Cambios

- Copia independiente de la v3. La v3 original no se modifica.
- Performance tiene navegación propia, negro carbono, plata, rojo y enlace de regreso a la matriz.
- Propuesta de cabecera: emblema existente + nombre ATPerformance en texto inclinado.
- Proyectos Mercedes-AMG A35 y Porsche 924 identificados como desarrollos en curso.
- Visor de geometrías derivadas de STL locales, simplificadas por agrupación espacial de vértices. Rotación con ratón o flechas; zoom con botones y teclado; reinicio de vista.
- Catálogo filtrable por aerodinámica, carbono y diseño. Trabajos desde S/ 400 como referencia general, sin asignar ese precio a todas las piezas.
- Formulario que prepara una consulta en WhatsApp. El visitante debe enviarla; no reserva automáticamente una cita.
- Español e inglés. Estilos adaptables a móvil y controles de teclado.
- Las rutas `performance.html` y `performance-en.html` llevan al espacio ATP. El resto de la copia corporativa conserva su código anterior.

## Materiales y límites

Los visuales de catálogo y portada proceden de la antigua carpeta web ATP. Se identifican como ilustrativos/conceptuales, no como fotos de proyectos terminados.
Las vistas de los proyectos proceden de `AMG A35/front amg.stl` y `porsche 924 board/porsche 924 board nu 2.stl`. Son referencias simplificadas, no archivos dimensionales de fabricación. No se incluyen los STL originales.
No se han utilizado fotografías con matrículas; no se realizó retoque fotográfico.
No hay resultados aerodinámicos, fechas de entrega ni proyectos terminados inventados.

## Migración futura a atperformance.pe

La carpeta `atperformance` contiene todos los recursos propios de ATP. Para alojarla como web independiente:
1. Copiar su contenido a la raíz del alojamiento ATP.
2. Sustituir los enlaces `../index.html` y `../en.html` por las URLs definitivas de la web corporativa.
3. Añadir canonical, hreflang, sitemap y metadatos sociales del dominio confirmado.
4. Retirar `noindex,nofollow` y la mención a prototipo solo al publicar.
5. Confirmar alcance/precios, condiciones comerciales y aviso de privacidad; revisar fotografías reales y disponibilidad de citas.
6. Validar escritorio, móvil, visor y formulario en navegador antes del despliegue.

No se ha cambiado ningún dominio, DNS ni alojamiento. El correo sigue siendo contacto@alphatechnologique.com.

## Ubicación

Esta sesión solo puede escribir en su carpeta de trabajo. Por eso la v4 está dentro de `Documents/ChatGPT/Alpha tech`, no junto a la v3 en `Alpha Tech - Web Maintenance`. Puede trasladarse completa sin cambiar sus enlaces relativos.

## Verificación

Se comprueban enlaces/recursos locales de las páginas nuevas, IDs de anclas, estructura de geometrías y diferencias respecto de la copia v3.
La revisión visual y funcional en navegador quedó bloqueada por el acceso a la conexión local. No debe interpretarse la validación estática como una prueba de interacción en escritorio o móvil.
