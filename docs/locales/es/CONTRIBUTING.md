# Contribuyendo

Las contribuciones son bienvenidas a través de issues y pull request.

## Alcance del proyecto

MeshMill hace que los archivos de malla de gran tamaño, densos o difíciles sean manejables para edición posterior y
flujos de trabajo de producción. Las contribuciones deberían mejorar la inspección de la geometría, la malla y la densidad de puntos.
gestión, optimización, selección, recorte, limpieza, validación, intercambio STL, rendimiento,
o la coordinación de dichas operaciones.

El proyecto no incluye modelado, escultura, pintura, animación, renderizado,
composición de la escena, materiales, montaje u otros sistemas de creación de contenido. Propuestas que introducen
esas características están fuera del alcance del proyecto.

Las nuevas características deberían mantener la aplicación enfocada, preservar los flujos de trabajo directos que convierten el código fuente
geometría en mallas manejables y evitar convertir los controles de soporte en una edición general
ambiente.

## Localización

El texto fuente de la interfaz de usuario en inglés se almacena en `locales/en-US.json`. Los metadatos locales se almacenan en
`locales/manifest.json`. Los catálogos de UI traducidos utilizan las mismas claves estables y el mismo nombre de archivo
`<locale>.json`. La documentación traducida utiliza el nombre de archivo raíz correspondiente en
`docs/locales/<locale>/`.

Después de cambiar etiquetas, información sobre herramientas, cuadros de diálogo u otro texto visible para el usuario, ejecute:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Revise juntos los cambios de fuente y las claves regeneradas.

## Cambios de geometría y algoritmo.

Utilice la geometría de muestra incluida al cambiar la optimización, el análisis de densidad, la selección, el recorte,
manejo de archivos grandes o comportamiento de comparación de ventanas gráficas. Contiene intencionalmente capas redundantes.
y densidad desigual, por lo que un resultado útil debería mejorar la manejabilidad sin ocultar la distorsión,
descartar límites significativos o eliminar silenciosamente la geometría que otro algoritmo conserva.

Registre la entrada, el algoritmo, la configuración, el recuento de triángulos, las dimensiones, la desviación de dimensiones, el tiempo transcurrido,
y capturas de pantalla relevantes para comparaciones. Pruebe tanto el dispositivo Git normal más pequeño como, cuando el
El cambio se refiere a geometría grande o en capas, el accesorio original Git LFS. No ajustar un algoritmo
solo a este encuentro. Agregue pequeños casos sintéticos para la invariante o regresión específica que se está
probado.

Consulte [Prueba y contribución de algoritmos](docs/ALGORITHM_TESTING.md) para ver la lista de verificación de comparación.

## Configuración de desarrollo

1. Instale Python 3.12 de 64 bits en Windows.
2. Crea y activa un entorno virtual.
3. Instale `requirements-dev.txt`.
4. Ejecute `python meshmill.py` para la GUI o `python meshmill.py --help` para uso de CLI.
5. Ejecute `python -m py_compile meshmill.py` antes de enviar un cambio.

Mantenga mallas privadas, ejecutables generados, capturas de pantalla que contengan información privada y archivos locales.
crear directorios a partir de confirmaciones. La geometría de prueba redistribuible pertenece a `samples/` con su
fuente, licencia, dimensiones y método de generación documentados. Los nuevos archivos fuente deben usar el
Identificador SPDX `GPL-3.0-or-later`.

Recorte cada captura de pantalla de la documentación al contenido de la aplicación MeshMill. No incluya el
barra de tareas, ventana cromada no relacionada, notificaciones, detalles de la cuenta, rutas privadas o fondo
contenido de escritorio.
