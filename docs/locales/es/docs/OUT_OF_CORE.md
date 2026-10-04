# Arquitectura de malla fuera del núcleo

La actual protección de archivos grandes de MeshMill estima la memoria de trabajo antes de asignar una copia completa.
malla. Los archivos que superen el presupuesto configurado se pueden abrir como descripciones generales de navegación limitadas. un
La descripción general es geometría de muestra, está visiblemente identificada como tal y no se puede editar ni exportar como
aunque era la fuente completa.

Los verdaderos detalles dependientes del zoom requieren un índice espacial persistente. El diseño siguiente define que
próxima fase de implementación.

## Formato de índice

Cada malla de origen recibe un directorio `.meshmill-index` versionado que contiene:

- `manifest.json`, con el tamaño de la fuente, el tiempo de modificación, los hashes del contenido de muestra, los límites,
  recuento de triángulos, versión de índice, precisión de coordenadas y descripciones de niveles;
- mosaicos espaciales abordados por nivel de octree y código Morton;
- una malla de visualización gruesa para cada mosaico principal ocupado;
- registros triangulares de resolución completa en mosaicos de hojas; y
- propiedad de límites y metadatos de superposición utilizados durante las operaciones y el montaje regionales.

La creación de índice lee la fuente secuencialmente en bloques acotados. Escribe ejecuciones de mosaicos temporales y
publica atómicamente el manifiesto después de que cada archivo requerido pase la validación. Una interrupción o
El índice obsoleto se detecta desde su manifiesto y se puede reanudar o reconstruir sin abrir el archivo completo.
malla en la memoria.

## Transmisión de ventana gráfica

La ventana gráfica selecciona mosaicos usando el frustum de la cámara y el error de espacio de la pantalla. Los mosaicos principales gruesos son
mostrado primero. Los mosaicos secundarios visibles los reemplazan a medida que la cámara se acerca, mientras que fuera de la pantalla y
las baldosas de bajo impacto siguen siendo ásperas. RAM y VRAM tienen presupuestos independientes y son de uso menos reciente.
cachés. Liberar detalles nunca libera la representación aproximada del objeto completo.

El programador registra estos estados de mosaico: en cola, leyendo, procesando, cargando, residente, fallido,
y cancelado. La ventana gráfica puede colorear cubos por estado y llenar cada cubo en proporción a su
progreso. La cancelación elimina resultados parciales y deja activa la última representación completa.

## Procesamiento y capacidad

Una unidad de trabajo local es una loseta más el solapamiento determinista que requiere su funcionamiento. concurrencia
está limitado por el RAM actualmente disponible, el porcentaje de memoria configurado, el recuento de procesadores lógicos y
Tamaño medido de la unidad de trabajo. La carga y visualización de GPU tienen un presupuesto VRAM independiente. Paralelo reportado
la capacidad es una estimación hasta que se hayan medido los mosaicos representativos.

Las operaciones retienen un propietario para cada elemento de límite. La asamblea valida los límites compartidos,
elimina duplicados, verifica recuentos y límites, y registra los parámetros exactos utilizados. el mismo trabajo
El formato de la unidad y del resultado se puede programar posteriormente en nodos de síntesis distribuidos.

## Reglas de seguridad

- Una muestra global está etiquetada como descripción general, no como detalle de ventana gráfica de resolución completa.
- Una descripción general no puede sobrescribirse ni exportarse como la malla de origen completa.
- Las solicitudes de carga completa que superan el presupuesto actual requieren una elección explícita.
- La generación de índices, el procesamiento de mosaicos y el ensamblaje siguen siendo cancelables y preservan el anterior
  estado completo.
- Los valores de capacidad son estimaciones e identifican si describen el motor actual o el planificado.
  Ejecución de mosaicos paralelos.
