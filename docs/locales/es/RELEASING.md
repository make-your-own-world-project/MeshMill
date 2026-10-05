# Liberando MeshMill

La canalización de versiones estables crea artefactos de Windows en ejecutores de Windows alojados en GitHub. un separado
El flujo de trabajo manual crea vistas previas de Linux x86-64 y macOS Intel/Apple Silicon sin firmar en formato nativo.
Corredores alojados en GitHub. Los usuarios finales no instalan Python, Node.js ni dependencias.

Antes de crear, actualice y valide los catálogos de fuentes de localización:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## Antes del primer lanzamiento público

1. Finalizar y validar las traducciones planificadas de solicitudes y documentación.
2. Revise la GPL y los avisos de terceros.
3. Pruebe la instalación, el lanzamiento, la carga, optimización, exportación y desinstalación de STL en un entorno limpio.
   Cuenta Windows o máquina virtual.
4. Ejecute CI contra `samples/sample-scan.stl`. Inspeccione cada captura de pantalla de la documentación y recórtela
   la barra de tareas, ventana chrome que no forma parte de MeshMill, notificaciones, rutas privadas, cuenta
   detalles y contenido de escritorio no relacionado antes de publicarlo.
5. Configure el autor de Git local del repositorio con la dirección de no respuesta GitHub de la cuenta antes del
   primer compromiso. Confírmelo con `git config --local --get user.email`.
6. Configure secretos de firma de Authenticode opcionales:
   - `WINDOWS_CERTIFICATE_BASE64`: Certificado PFX codificado en Base64.
   - `WINDOWS_CERTIFICATE_PASSWORD`: Contraseña PFX.

Sin un certificado de firma, los archivos generados aún funcionan, pero es posible que se muestre Windows SmartScreen
una advertencia de editor no reconocido. No describa las compilaciones sin firmar como firmadas o confiables.

## Escaneo original y Git LFS

`samples/original-scan.stl` se rastrea a través de Git LFS porque excede los 100 MiB normales de GitHub
límite de archivos. Antes de la primera confirmación, verifique:

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

El filtro debe ser `lfs` y el ID del objeto puntero debe coincidir con `samples/SHA256SUMS.txt`. la liberación
El flujo de trabajo verifica el contenido de LFS y publica el STL original como un activo de lanzamiento separado. usos de CI
la muestra de Git normal más pequeña y no descarga el objeto LFS.

## Probar una versión de lanzamiento sin publicar

Abra **Acciones**, seleccione **Liberar**, elija **Ejecutar flujo de trabajo** e ingrese una versión numérica como
`0.1.0`. Una ejecución manual carga artefactos de flujo de trabajo para realizar pruebas, pero no crea un GitHub público.
Liberación.

## Publicar un comunicado

Desde una sucursal `main` limpia y revisada:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

La etiqueta inicia el flujo de trabajo de lanzamiento. Eso:

1. instala las dependencias de compilación ancladas;
2. genera metadatos de la versión Windows coincidente;
3. construye los ejecutables GUI y CLI autónomos;
4. firma los ejecutables cuando se configuran los secretos de firma;
5. construye el instalador Inno Setup por usuario;
6. firma el instalador cuando está configurado;
7. crea el archivo de suma de comprobación ZIP y SHA-256 portátil;
8. carga artefactos de flujo de trabajo;
9. crea la versión GitHub para la etiqueta enviada.

Verifique el instalador y el archivo portátil en un sistema Windows limpio antes de anunciar el lanzamiento.
Mantenga la fuente correspondiente a cada binario distribuido disponible bajo la misma etiqueta de versión.
Confirme que el botón GitHub apunte a la URL final del repositorio público antes de etiquetar el primero.
liberación.

## Cree vistas previas de Linux y macOS

Abra **Acciones**, seleccione **Compilaciones de vista previa de plataforma** y elija **Ejecutar flujo de trabajo**. Introduzca una vista previa
versión como `0.2.0-preview.1`.

Deje **Publicar una versión preliminar pública de GitHub** desactivado para la primera ejecución. El flujo de trabajo crea y prueba:

- Linux x86-64 en Ubuntu 22.04;
- macOS x86-64 en un ejecutor Intel;
- macOS arm64 en un eje de silicona de Apple.

Descargue los artefactos del flujo de trabajo e inspeccione sus sumas de verificación y registros. Ejecute el flujo de trabajo nuevamente con
La publicación se habilita solo después de que pasa cada trabajo de compilación. Las vistas previas publicadas de macOS están firmadas ad hoc,
no certificado por Apple. Descríbalos como versiones preliminares y vincule a los probadores a
`docs/PLATFORM_TESTING.md` y el formulario de problema **Prueba de vista previa de plataforma**.
