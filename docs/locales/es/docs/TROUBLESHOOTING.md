# Solución de problemas

## Windows bloquea la descarga

Las compilaciones de comunidades no firmadas pueden activar Microsoft Defender SmartScreen. Comparar lo descargado
hash SHA-256 del archivo con `SHA256SUMS.txt` de la misma versión GitHub. Las autorizaciones firmadas identifican
su editor en las propiedades del archivo Windows.

## La compilación portátil no se inicia.

Extraiga el ZIP completo antes de ejecutar `MeshMill.exe`. El directorio `_internal` debe permanecer a continuación.
a ambos ejecutables. No ejecute el ejecutable desde el interior del visor ZIP.

## Se abre un gran STL como descripción general

El conjunto de trabajo estimado excede el presupuesto de memoria en Configuración. El modo de descripción general está intencionalmente
sólo lectura. Aumente el presupuesto sólo cuando la máquina tenga suficiente memoria disponible, o reduzca el
malla antes de abrirla para editarla.

## No se guardó una vista estándar

Presione el acceso directo de vista modificado con Ctrl, luego elija **Guardar** o presione Entrar en la confirmación
diálogo. Guardar una vista también actualiza su opuesta. La línea de estado informa la vista guardada.

## Los atajos de navegación no responden

Primero cierre cualquier cuadro de diálogo modal. Revise o restablezca los accesos directos en Configuración si fueron personalizados. el
Los accesos directos de vista predeterminados utilizan Insertar, Inicio, Re Pág, Eliminar, Fin y Av Pág.

## Crear un registro de diagnóstico de orientación local

El registro de diagnóstico está deshabilitado de forma predeterminada. Para registrar el enrutamiento del teclado y el estado de la cámara localmente:

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

El registro puede contener la ruta del archivo abierto. Revíselo y redactelo antes de compartirlo. La geometría de la malla no es
escrito en el registro.

## Informar un problema

Incluye la versión MeshMill, la versión Windows, el modelo GPU, recuento de triángulos de malla, acción exacta
secuencia y si se utilizó el instalador o el paquete portátil. Utilice la muestra redistribuible
malla cuando sea posible. No adjunte escaneos privados o registros de diagnóstico sin revisarlos primero.
