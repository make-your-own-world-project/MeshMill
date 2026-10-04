# Pruebas de algoritmos y contribución.

Los algoritmos MeshMill deberían hacer que la geometría difícil sea manejable y al mismo tiempo mantener sus efectos visibles.
mensurable y reversible antes de que se aplique un resultado.

## Accesorios de referencia

Utilice ambas versiones incluidas de la geometría de muestra compuesta:

- `samples/sample-scan.stl` es el dispositivo Git normal más pequeño para desarrollo de rutina, automatizado
  comprobaciones y aprendizaje de los controles.
- `samples/original-scan.stl` es el dispositivo Git LFS completo para el comportamiento de archivos grandes, capas redundantes,
  densidad desigual, superposición y trabajo de rendimiento.

Las regiones redundantes y densas son características de prueba intencionales. Una prueba puede apuntar a ellos, pero
No debe asumir que todas las superficies superpuestas son desechables. Agregue mallas sintéticas compactas cuando
el cambio necesita un límite, curvatura, topología, densidad o invariante de superposición conocidos.

## Lista de verificación de comparación

Para un cambio de algoritmo o parámetro, registre:

- Versión o confirmación MeshMill;
- dispositivo de entrada y suma de comprobación;
- algoritmo, configuración preestablecida de calidad, objetivo y avanzada;
- recuentos de triángulos y vértices originales y resultantes;
- porcentaje de reducción, dimensiones y deriva de dimensiones;
- tiempo transcurrido y memoria máxima cuando el rendimiento es relevante;
- capturas de pantalla de las mismas vistas guardadas y modos de visualización;
- cambios visibles en límites, agujeros, autointersecciones, superposiciones o distorsiones;
- si el resultado provino de una operación de malla completa o solo de selección.

Compare con el comportamiento actual en el mismo objetivo, no solo con otro preestablecido con un
recuento de salida diferente. Inspeccione las visualizaciones sombreadas, de densidad, de estructura alámbrica y de vértices cuando corresponda.

## Guía de aceptación

Un cambio de optimización debe evitar cambios de dimensiones inesperados, inversiones de superficie obvias,
grietas entre regiones procesadas, pérdida de límites significativos y grandes regresiones de calidad a un
recuento de salida similar. Los cambios orientados a la densidad deberían demostrar que la concentración eliminada no
no lleva curvatura o topología útil.

Los resultados de rendimiento deben identificar el procesador, la capacidad de la memoria, el hardware de gráficos, el sistema operativo.
sistema, tamaño de entrada y si los datos ya estaban almacenados en caché. Validación estructural y capturas de pantalla.
respaldan la revisión, pero no reemplazan la inspección realizada por colaboradores familiarizados con la geometría de origen.

## Pruebas de regresión

Prefiere pruebas deterministas con tolerancias explícitas. Mantenga los dispositivos nuevos lo suficientemente pequeños para Git normal,
documentar su origen y licencia, y utilizar geometría sintética cuando los datos de origen reales no sean necesarios.
Las pruebas deben cubrir la cancelación y la restauración del estado cuando una operación pueda modificar la geometría.
