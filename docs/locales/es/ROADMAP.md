# Hoja de ruta MeshMill

## Soporte de plataforma

Windows es la plataforma empaquetada inicial. La arquitectura de la aplicación y los formatos de malla son
multiplataforma y las versiones futuras deberían agregar paquetes nativos Linux y macOS. Trabajo de plataforma
Incluye empaquetado, integración de aplicaciones, métricas de hardware, comportamiento del sistema de archivos y automatización.
pruebas de lanzamiento mientras se conserva el mismo proyecto y los flujos de trabajo STL en todos los sistemas compatibles.

- Valide el paquete de vista previa de Linux x86-64 en todas las distribuciones, entornos de escritorio y pantalla.
  servidores y controladores de GPU antes de promocionarlo a estable.
- Valide los paquetes de vista previa de macOS Apple Silicon y x86-64 en hardware real y luego agregue Developer
  Firma de identificación y certificación notarial antes de promoverlos a estable.
- Agregue proveedores de métricas CPU, memoria y GPU nativos de la plataforma detrás de una interfaz compartida.
- Mantenga portátiles las configuraciones guardadas, las asignaciones de teclado, el comportamiento de la línea de comandos y los datos del proyecto.

Esta hoja de ruta registra el trabajo planificado. No describe las funciones de la versión actual.

## Alcance

MeshMill gestiona geometría, densidad de malla, densidad de puntos, optimización, limpieza, validación y STL
intercambie archivos de malla grandes o pesados que sigan siendo útiles en los flujos de trabajo de edición posteriores.

Modelado de uso general, escultura, pintura, animación, renderizado, composición de escenas, materiales,
rigging y otros sistemas de creación de contenido están fuera de esta hoja de ruta. Se aplica la síntesis distribuida
a las operaciones de gestión de malla de MeshMill y no expande el producto a un editor general.

## Geometría de referencia

La malla compuesta incluida es el elemento de desarrollo común para los algoritmos y la hoja de ruta actuales.
trabajo. Sus capas intencionalmente redundantes y su densidad desigual respaldan comparaciones repetibles de
calidad de reducción, análisis de densidad, manejo de superposiciones, operaciones regionales, procesamiento fuera del núcleo,
y futura síntesis. Las implementaciones de la hoja de ruta deberían informar los resultados de este evento y de los pequeños
mallas de regresión diseñadas específicamente, en lugar de optimizar el comportamiento para un solo modelo.

## Espacios de trabajo Multi-STL y síntesis estadística

Un espacio de trabajo debe aceptar múltiples entradas STL como objetos de origen separados y visibles de forma independiente.
MeshMill debe alinear esas fuentes, medir su concordancia geométrica y sintetizar una utilizable
malla sin retener superficies internas duplicadas o geometría de superposición repetida.

Comportamiento planificado:

- agregar, eliminar, ocultar, aislar, reordenar e inspeccionar múltiples fuentes STL en un espacio de trabajo;
- conservar la identidad de origen, las unidades, las transformaciones, los límites, la resolución y el historial de operaciones;
- proporcionar registro automático con controles de alineación manuales y calidad de ajuste mensurable;
- dividir las fuentes en regiones espaciales antes de la comparación para que las entradas grandes permanezcan limitadas;
- analizar la ocupación, la distancia a la superficie más cercana, la concordancia normal, la densidad local, la varianza y
  recuento de observaciones en regiones superpuestas;
- clasificar superficies coincidentes, superficies en conflicto, ruido de escaneo, espacios y geometría única;
- consolidar superficies estadísticamente coincidentes en una superficie representativa con registros
  confianza en lugar de apilar triángulos duplicados;
- eliminar la geometría cerrada, coincidente y compartida que no aporta ningún detalle de forma exterior;
- conservar la geometría de origen que no se superponga y exponer regiones ambiguas para revisión visual;
- permitir ponderación por fuente y por región cuando un escaneo sea más limpio o más detallado;
- validar la estanqueidad, los límites, las normales, las dimensiones y la topología después de la síntesis;
- registrar la procedencia de la fuente y los parámetros de síntesis para que la malla combinada sea reproducible;
- obtenga una vista previa del recuento de triángulos esperado, los límites, la superposición eliminada y la distribución de confianza antes
  cometer el resultado sintetizado.

Este flujo de trabajo debe utilizar el mismo índice espacial externo y el mismo modelo de unidad de trabajo planificado para grandes
mallas. La comparación estadística y la consolidación de superposiciones también deberían poder distribuirse entre los países locales.
o nodos remotos MeshMill.

## Síntesis distribuida

Un clúster MeshMill debe coordinar múltiples nodos que operan en paralelo en múltiples
estaciones de trabajo. Un nodo puede inspeccionar, seleccionar, reducir, validar, reparar o combinar una región asignada o
unidad de trabajo. Las contribuciones permanecen versionadas de forma independiente hasta que sean revisadas e incorporadas.
en una versión de objeto compartido.

El sistema debería soportar:

- contribuciones simultáneas de múltiples operadores y nodos automatizados;
- entradas, parámetros, dependencias y salidas deterministas de la unidad de trabajo;
- programación consciente de la capacidad basada en CPU, GPU, memoria, algoritmos y carga actual;
- partición de mallas, regiones, pases de validación y etapas de síntesis teniendo en cuenta la dependencia;
- colas duraderas con pausa, reanudación, cancelación, reintento, reasignación y recuperación de fallas;
- artefactos dirigidos al contenido y comprobaciones de integridad entre nodos;
- síntesis reproducible a partir de un conjunto grabado de versiones de contribuciones aceptadas;
- estaciones de trabajo fuera de línea o conectadas de forma intermitente que pueden sincronizarse más tarde;
- Operación local primero con control explícito sobre los nodos participantes y datos compartidos del proyecto.

## Colaboración versionada

Cada contribución debe registrar su versión del objeto principal, región o unidad de trabajo seleccionada, operación,
parámetros, identidad del nodo, marcas de tiempo, dependencias, resultados de validación y suma de comprobación de salida.

Comportamiento de colaboración planificado:

- los proyectos contienen objetos, ramas, puntos de control, contribuciones y versiones sintetizadas;
- los contribuyentes pueden trabajar desde la misma versión principal sin sobrescribirse entre sí;
- las contribuciones que no se superponen pueden fusionarse automáticamente después de la validación;
- la geometría superpuesta o las dependencias incompatibles crean un conflicto explícito;
- los conflictos proporcionan comparación visual, elección a nivel de región, rebase, repetición y resolución manual;
- los estados de revisión incluyen pendiente, aceptado, rechazado, reemplazado, en conflicto e incorporado;
- el manifiesto de síntesis final identifica cada contribución y dependencia incorporada.

## IU de coordinación

La aplicación de escritorio debe gestionar el trabajo distribuido sin necesidad de una línea de comandos independiente.
o flujo de trabajo de administración del servidor. Las vistas planificadas incluyen:

- **Proyectos:** objetos, ramas, versiones, contribuyentes y estado de síntesis.
- **Clúster:** estaciones de trabajo y nodos conectados, capacidades, estado, carga y asignación actual.
- **Cola:** unidades de trabajo pendientes, activas, en pausa, bloqueadas, fallidas y completadas.
- **Contribuciones:** autor, nodo, versión principal, región afectada, parámetros, comprobaciones y estado de revisión.
- **Comparar:** vistas 3D sincronizadas, diferencias de geometría, métricas e inspección de límites.
- **Conflictos:** regiones superpuestas, conflictos de dependencia, opciones de resolución y resultados de validación.
- **Síntesis:** gráfico de dependencia, progreso agregado, versiones de contribución seleccionadas y resultado final.
- **Historial:** gráfico de ramas, puntos de control, fusiones, versiones sintetizadas y manifiestos de reproducibilidad.

La ventana gráfica debe mostrar propiedad, regiones asignadas, trabajo completado, cambios pendientes, conflictos,
y diferencias de versión sin alterar la malla subyacente.

## Coordinación y transporte.

La primera fase de diseño debe definir los límites del protocolo antes de seleccionar un transporte. el protocolo
debe separar los metadatos de coordinación de los grandes artefactos de malla, admitir la transferencia reanudable y
permanecer utilizable en una red local sin una cuenta externa o servicio alojado.

Conceptos de coordinación necesarios:

- elección del coordinador o de un coordinador seleccionado explícitamente;
- descubrimiento de nodos e inscripción manual de nodos;
- sesiones autenticadas y autorización en el ámbito del proyecto;
- arrendamientos y latidos para la propiedad del trabajo;
- presentación idempotente del trabajo y aceptación de resultados;
- negociación de versiones entre diferentes versiones de MeshMill;
- eventos estructurados para progreso, registros, validación, fallas y reintentos;
- recuperación después de la interrupción del coordinador, la estación de trabajo, la red o el nodo.

## Fases de entrega

### Fase 0: procesamiento de malla grande fuera del núcleo

El contrato de índice, transmisión, caché, unidad de trabajo y seguridad está documentado en
[`docs/OUT_OF_CORE.md`](docs/OUT_OF_CORE.md).

- Calcule el número de triángulos y la memoria de trabajo antes de asignar la malla completa.
- Abra archivos binarios STL de gran tamaño como descripciones generales de navegación delimitadas y muestreadas uniformemente.
- Divida la geometría de resolución completa en cubos espaciales con límites de superposición deterministas.
- Lea, analice y optimice cubos independientes simultáneamente dentro de CPU y los límites de memoria.
- Implementaciones comparativas de computación GPU para etapas de reducción como evaluación de errores, candidato
  puntuación, consultas espaciales y procesamiento independiente de unidades de trabajo. Descargue una etapa sólo cuando
  proporciona un beneficio de memoria o velocidad de extremo a extremo medible sin reducir el determinismo, la malla
  calidad, garantías de topología o compatibilidad con sistemas que carecen de una GPU adecuada.
- Transmita niveles de ventana gráfica de grueso a fino en lugar de requerir la malla completa en la memoria.
- Dibuje el estado del cubo directamente en la ventana gráfica: en cola, leyendo, procesando, completado y fallido.
- Muestre el progreso por cubo llenando cada cubo y conserve una vista de alto nivel de todo el objeto.
- Ensamble cubos procesados con validación de límites, eliminación de duplicados y configuraciones reproducibles.
- Amplíe el programador de cubos local a unidades de trabajo de síntesis distribuidas en fases posteriores.

### Fase 1: fundación local versionada

- Defina formatos de objeto, operación, contribución, rama y manifiesto.
- Agregue espacios de trabajo multi-STL con visibilidad, transformaciones, metadatos y procedencia por fuente.
- Agregue métricas de calidad de registro y clasificación de superposición espacial.
- Sintetice superficies estadísticamente coincidentes mientras elimina geometría duplicada y cerrada.
- Agregue una revisión visual de conflictos, brechas, confianza y geometría exclusiva de una fuente.
- Conservar el historial local en todas las sesiones de la aplicación.
- Agregue comparaciones de regiones y mallas visuales.
- Haga que las operaciones sean deterministas y reproducibles de forma independiente.

### Fase 2: nodos locales coordinados

- Ejecute nodos trabajadores en una estación de trabajo.
- Agregue colas, informes de capacidad, asignación de trabajo y cancelación.
- Muestre el estado del nodo y la unidad de trabajo en la interfaz de usuario MeshMill.
- Valide la partición y el ensamblaje de resultados localmente.

### Fase 3: síntesis de múltiples estaciones de trabajo

- Agregue descubrimiento e inscripción de LAN autenticados.
- Transfiera aportes y resultados de trabajo relacionados con el contenido con soporte para currículums.
- Coordine el trabajo simultáneo en múltiples estaciones de trabajo.
- Recuperar asignaciones después de una falla de nodo o red.

### Fase 4: versionado colaborativo

- Agregue contribuyentes, sucursales, estados de revisión y permisos.
- Fusionar contribuciones que no se superpongan.
- Detectar y resolver conflictos de superposición o dependencia.
- Sintetizar contribuciones seleccionadas en una versión de objeto reproducible.

### Fase 5: endurecimiento de la producción

- Agregue pruebas de compatibilidad de protocolos y manejo de versiones mixtas.
- Agregue pruebas de auditoría, integridad, corrupción, interrupción y recuperación.
- Comparar el rendimiento de programación, partición, transferencia, fusión y síntesis.
- Implementación de documentos, respaldo, migración y recuperación de incidentes.
