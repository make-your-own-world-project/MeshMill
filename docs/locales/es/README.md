<p align="center">
  <img src="assets/meshmill-logo.svg" width="620" alt="MeshMill: Dirty geometry? Clean it up!">
</p>

MeshMill es una aplicación de escritorio especializada en gestionar geometrías de malla
de gran tamaño, alta densidad o difícil manejo. Ofrece funciones de inspección rápida, análisis de densidad, selección por regiones, recorte, eliminación
y reducción controlada de mallas, sin necesidad de crear una cuenta ni de cargar la geometría en la nube.

El renderizado OpenGL acelerado por GPU mantiene la navegación por ventanas gráficas, la selección de hardware y la visualización de densidad.
e inspección interactiva responsiva. La reducción de malla actualmente se ejecuta en trabajadores de CPU nativos separados.
manteniendo largos cálculos de geometría alejados de la interfaz.

MeshMill trabaja con mallas provenientes de escáneres 3D, exportaciones de CAD y modelado, procesos de reconstrucción,
geometría generada y otras fuentes compatibles con STL. Prepara la geometría para editores posteriores,
herramientas de fabricación y otros flujos de trabajo con mallas. El modelado de propósito general, la escultura, la animación,
la creación de materiales y el diseño de escenas quedan fuera de su ámbito.

## Descarga

Descarga uno de estos archivos desde [Lanzamientos de GitHub](../../releases):

- `MeshMill-<version>-windows-x64-setup.exe`: instalador por usuario con acceso directo en el menú Inicio y
  accesos directos opcionales en el escritorio.
- `MeshMill-<version>-windows-x64-portable.zip`: aplicación portátil. Extrae todo el contenido del archivo comprimido,
  y luego ejecuta `MeshMill.exe`.

Ambos paquetes incluyen el entorno de ejecución de la aplicación. Los usuarios finales no instalan Python, Node.js ni
dependencias. La versión estable es compatible con Windows 10 y Windows 11 en hardware x64.

Los paquetes de vista previa de Linux x86-64 y macOS Intel/Apple Silicon sin firmar también pueden aparecer en las versiones.
Se basan en ejecutores nativos alojados en GitHub y pasan pruebas de humo de malla de muestra y CLI empaquetadas.
pero aún es necesario realizar pruebas en hardware real. Consulte [Pruebas de vista previa de Linux y macOS](../../PLATFORM_TESTING.md)
antes de instalar o informar los resultados.

Las compilaciones de comunidades no firmadas pueden mostrar una advertencia de Windows SmartScreen o macOS Gatekeeper. Lanzamiento
Las sumas de verificación se enumeran al lado de cada versión.

## Inicio rápido

1. Abra un STL.
2. Examínelo en el modo de visualización Sombreado, Densidad, Estructura alámbrica o Vértices.
3. Elija un nivel de calidad, un algoritmo y un recuento de triángulos objetivo.
4. Seleccione **Optimizar** para calcular un resultado.
5. Compare las mallas original y optimizada y, a continuación, seleccione **Aplicar** para confirmar la operación.
6. Seleccione **Guardar estado actual** o pulse `Ctrl+S`.

MeshMill nunca inicia la optimización simplemente porque haya cambiado un archivo o una configuración.

## Capacidades

- Entrada STL en formato binario y ASCII, salida STL en formato binario
- Reducción Fast QEM que preserva la densidad, la forma y la topología
- Ventana gráfica OpenGL acelerada por GPU, selección de hardware y visualización de densidad
- Trabajadores nativos de geometría de fondo para reducción de malla
- Modos de visualización: sombreado, densidad, estructura alámbrica y vértices
- Objetivos automáticos derivados de la geometría en lugar de un límite fijo de triángulos
- Selección de polígonos con selección aditiva de múltiples regiones
- Recortar, eliminar u optimizar solo la región seleccionada
- Comparación en caché de la malla original, la anterior y la actual
- Deshacer y rehacer cambios de geometría aplicados
- Desviación dimensional, porcentaje de reducción y tamaño de salida estimado
- Unidades de visualización: milímetros, centímetros, metros, pulgadas y pies
- Métricas de CPU, memoria, GPU y actividad geométrica
- Carga de vista general limitada cuando un archivo STL binario supera el presupuesto de memoria configurado
- Aplicaciones con interfaz gráfica (GUI) y de línea de comandos
- Procesamiento local sin dependencia de cuentas, telemetría, carga de archivos o nube

## Inspeccionar la geometría antes de reducirla.

La pantalla Sombreada proporciona una vista limpia de la superficie y la silueta. Es útil para comparar
preservación de la forma antes de aplicar una pasada de optimización.

![Vista sombreada de MeshMill que muestra la malla de muestra incluida](../../images/meshmill-shaded.png)

La visualización de Vértices expone la distribución de puntos real. Regiones de escaneo densas, áreas escasas y
Los cambios abruptos en el muestreo son visibles sin cambiar la geometría. El panel de métricas ampliado
rastrea la CPU, la memoria, la GPU y la actividad de procesamiento de geometría mientras trabaja con la malla.

![Visualización de MeshMill Vertices con métricas de rendimiento ampliadas](../../images/meshmill-vertices.png)

La pantalla Wireframe muestra la estructura triangular directamente. Ayuda a identificar densidad innecesaria,
triangulación irregular y regiones donde la simplificación puede eliminar una geometría sustancial.

![Visualización de estructura alámbrica de MeshMill que muestra la variación en la densidad del triángulo](../../images/meshmill-wireframe.png)

## Analizar la densidad de la malla.

La visualización Densidad mapea la densidad local relativa en todo el modelo. Las regiones dispersas permanecen frías mientras
Las regiones cada vez más densas se mueven a través de colores más brillantes, lo que hace que el muestreo desigual sea visible a simple vista.

![Visualización de densidad de MeshMill que muestra la densidad de malla relativa](../../images/meshmill-density.png)

La densidad permanece disponible mientras se evalúa una optimización provisional. La caja de herramientas informa la
algoritmo, objetivo, recuento de vértices y triángulos resultantes, porcentaje de reducción, dimensiones y
tamaño de salida estimado antes de aplicar el pase.

![Pantalla de densidad de MeshMill que muestra una optimización provisional](../../images/meshmill-density-overview.png)

Mantenga presionado el botón derecho del mouse para inspeccionar una región a través de la lupa circular. La vista ampliada
permanece centrado en el puntero y revela la densidad local sin cambiar la posición de la cámara principal.

![Visualización de densidad de MeshMill con la lupa de la ventana gráfica](../../images/meshmill-density-zoom.png)

## Controles de visualización

| Entrada | Acción |
| --- | --- |
| Arrastrar con el botón central | Orbitar |
| Mayús + arrastrar con el botón central | Desplazar (panorámica) |
| Rueda del ratón | Zoom hacia el puntero |
| Ctrl + rueda del ratón | Girar en sentido horario o antihorario |
| Teclas de flecha | Orbitar alrededor del centro de la vista |
| Ctrl + teclas de flecha | Desplazar (panorámica) |
| Ctrl + Mayús + Arriba/Abajo | Zoom |
| Ctrl + Mayús + Izquierda/Derecha | Rollo |
| `F1` / `F2` / `F3` / `F4` | Sombreado / Densidad / Estructura alámbrica / Vértices |
| Mantenga pulsado el botón derecho del ratón | Lupa |
| Mayús + clic izquierdo | Agregar o quitar puntos de regla |
| Ctrl + arrastrar hacia la izquierda | Dibujar un polígono de selección |
| `Ctrl+C` | Agregue el polígono a la selección guardada |
| `Ctrl+X` | Recortar a la selección |
| `Ctrl+Space` | Optimizar la selección |
| `Delete` | Eliminar la selección |
| `Escape` | Borrar la selección o regla activa |
| `Ctrl+Z` / `Ctrl+Y` | Deshacer/rehacer |
| `Ctrl+S` | Guardar el estado actual de la malla |

Las teclas de vista estándar siguen el bloque de navegación de seis teclas:

| Clave | Ver | Ctrl + tecla |
| --- | --- | --- |
| `Insert` | Izquierda | Establecer la orientación actual como Izquierda |
| `Home` | Frente | Establecer la orientación actual como Frente |
| `Page Up` | Derecha | Establecer la orientación actual como Derecha |
| `Delete` | Arriba cuando no existe ninguna selección | Establecer la orientación actual como Superior |
| `End` | Atrás | Establecer la orientación actual como Atrás |
| `Page Down` | Abajo | Establecer la orientación actual como Inferior |

Al guardar una vista, también se actualiza la vista opuesta. Izquierda y derecha, adelante y atrás, y arriba y abajo
permanecer emparejado. En el cuadro de diálogo de confirmación, **Guardar** es la acción predeterminada, por lo que Enter guarda el
orientación. El frente aparece en la parte superior de las vistas Superior e Inferior.

Los atajos se pueden cambiar o restablecer en Configuración.

## Flujo de trabajo de selección

Mantenga presionada la tecla Ctrl y arrastre hacia la izquierda para dibujar un polígono. Arrastre las esquinas para darle nueva forma, haga clic izquierdo en un borde para agregar un
punto, o haga clic derecho en un borde para eliminar uno. Agregue más regiones con `Ctrl+C`. Al mover la cámara se esconde
el polígono del espacio de la pantalla conservando la geometría seleccionada.

La optimización con una selección activa afecta únicamente a esa selección. El resultado sigue siendo provisional.
hasta que se seleccione **Aplicar**. **Cancelar** descarta el resultado provisional y conserva la selección para
Se puede probar otra configuración. Las operaciones de recortar y eliminar se convierten en ediciones de malla normales que se pueden deshacer.

El panel de selección informa los vértices, triángulos, participación de malla y cálculos acumulados seleccionados.
tamaño y dimensiones. Sus acciones recortan, agregan, optimizan, eliminan, retroceden o borran lo retenido.
selección sin ocultar la geometría circundante.

![MeshMill muestra una selección regional retenida y sus estadísticas de geometría](../../images/meshmill-crop-selection.png)

## Mallas grandes

Antes de asignar un STL binario, MeshMill compara su memoria de trabajo estimada con la configurada.
presupuesto de memoria. Un archivo encima del presupuesto se abre como una descripción general limitada de solo lectura. Los informes generales
el recuento completo de triángulos de origen, pero desactiva la edición y exportación porque es una muestra, no la versión completa.
objeto. El procesamiento fuera del núcleo indexado y dependiente del zoom está planificado en
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## línea de comando

`MeshMillCLI.exe` está incluido en ambos paquetes de versión:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Ejecute `.\MeshMillCLI.exe --help` para todas las opciones. MeshMill se niega a sobrescribir su archivo de entrada.

## Geometría de muestra

Hay dos versiones del ejemplo de desarrollo disponibles. La muestra es una malla compuesta con
capas intencionales de geometría redundante y densidad variada. Ofrece a las personas sin escáner una
accesorio realista para comparar algoritmos, inspeccionar la densidad, ejercer operaciones regionales,
y desarrollar funciones de hoja de ruta. MeshMill no requiere entrada escaneada.

| Archivo | Triángulos | Tamaño | Entrega | Lo mejor para |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249.999 | 11,9 MB | Git normal | Evaluación rápida, CI y aprendizaje de los controles |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4.126.315 | 196,8 MB | Git LFS | Prueba de geometría de fuente densa y rendimiento de malla grande |

La muestra más pequeña se descarga con cada clon normal. El original intacto es opcional y
administrado a través de Git LFS para que no infle el historial del repositorio ordinario. El escritorio GitHub incluye
Git LFS. Los usuarios de la línea de comandos pueden instalar Git LFS y ejecutar:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

Las versiones etiquetadas también publican el STL original como descarga directa para personas que no usan Git.
Consulte [`samples/README.md`](../../../samples/README.md) para conocer la procedencia, las dimensiones y las sumas de verificación.

Los contribuyentes de algoritmos también deben leer el
[guía de prueba de algoritmos](docs/ALGORITHM_TESTING.md) antes de comparar o cambiar la reducción
comportamiento.

## Unidades STL

STL no codifica una unidad. Cambiar las unidades del modelo cambia etiquetas y medidas sin escalar
las coordenadas guardadas. Seleccione la unidad que describe la geometría de origen.

## Privacidad

MeshMill lee y escribe archivos locales. No contiene cuentas, telemetría, carga, publicidad ni
función de procesamiento en la nube. La implementación actual de métricas GPU utiliza el rendimiento local Windows.
contadores. Se planean proveedores de métricas nativas equivalentes para Linux y macOS.

Para la resolución de problemas de diagnóstico, los desarrolladores pueden iniciar la GUI con
`--diagnostic-log <local-file.jsonl>`. El registro registra el enrutamiento de entrada y el estado de la cámara localmente y se
desactivado durante el uso normal.

## Desarrollo y lanzamiento

El texto y la documentación de la interfaz de usuario localizados se producen inicialmente con traducción automática externa.
servicios y se comprueba automáticamente si hay daños estructurales. La traducción automática todavía puede ser
antinatural o incorrecto. Se anima a los hablantes nativos a revisar y corregir las traducciones a través de
el proceso de contribución.

- [Contribuyendo](CONTRIBUTING.md)
- [Proceso de liberación](RELEASING.md)
- [Hoja de ruta](ROADMAP.md)
- [Solución de problemas](docs/TROUBLESHOOTING.md)
- [Avisos de terceros](THIRD_PARTY_NOTICES.md)

## Soporte MeshMill

MeshMill se desarrolla y mantiene de forma independiente. leer
[por qué es importante apoyar este trabajo](SUPPORT.md), o apoyar el desarrollo continuo a través de
[Cómprame un café](https://buymeacoffee.com/tednv).

MeshMill tiene la licencia pública general GNU, versión 3 o posterior. Ver
[`LICENSE`](../../../LICENSE).
