---
title: "Mi propio Google Fotos en casa (y un botón de Guardar que no vi)"
date: 2026-10-02T20:52:02+02:00
draft: false
description: "Ya tenía las fotos del móvil copiándose solas al servidor, pero verlas era como mirar una carpeta de archivos. Instalé Immich para tener una galería de verdad, sin reconocimiento facial y sin poder borrar nada por accidente. Por el camino: un navegador que se negaba a entrar, el miedo a las fotos duplicadas y unos ajustes que no se guardaban."
---

Hace unos meses monté el [backup de fotos con Syncthing](/posts/backup-fotos-syncthing/): el móvil manda las fotos al servidor de casa y ahí se quedan guardadas. Funciona de maravilla, pero tiene un problema. Para ver una foto tenía que meterme en una carpeta llena de archivos con nombres tipo `PXL_20260712_171902.jpg`. Eso es un backup, no una galería.

Así que me pregunté: ¿puedo tener algo tipo Google Fotos, pero en mi servidor, usando las fotos que ya tengo ahí?

## Lo que quería conseguir

1. Ver mis fotos como en cualquier galería: línea de tiempo, álbumes, mapa, vídeos.
2. **No duplicar nada.** Las fotos ya están en el servidor y no quería una segunda copia ocupando otros 8 GB.
3. **Que la galería no pudiera borrar nada.** Si borro una foto desde la galería y Syncthing se lo cuenta al móvil, adiós foto. No quería ni la posibilidad.
4. Que solo se pudiera entrar desde mis aparatos, como el resto de cosas del servidor.

## Elegir la herramienta

Miré varias opciones. Había galerías ligeras (PiGallery2, Photoview) que gastan muy poca memoria, pero se quedan cortas. Al final elegí **Immich**, que es lo más parecido a Google Fotos que se puede montar en casa: tiene línea de tiempo, mapa, álbumes, usuarios separados (uno para mí y otro para mi pareja) y app para Android.

La pega es que mi servidor no es precisamente un monstruo: tiene **3,7 GB de RAM**. Immich trae una parte de "inteligencia artificial" (machine learning) que reconoce caras y te deja buscar "perro en la playa". Está muy bien, pero esa parte sola se come más de 1 GB de memoria. Decidí quitarla: prefiero un servidor que no vaya ahogado a que me encuentre las fotos del perro.

## Cómo lo monté

Immich se instala con Docker, igual que Vaultwarden y Syncthing. Cada programa va en su propia cajita y no se pisan unos a otros. La instalación oficial es un fichero `docker-compose.yml` (la "receta" que dice qué cajitas arrancar y cómo), y le hice cuatro cambios:

- **Fuera el contenedor de machine learning.** Así quitamos de golpe ese gigabyte de RAM.
- **Solo accesible por Tailscale.** Por defecto Immich escucha en todas las "puertas" de red del servidor. Lo limité a la IP de Tailscale del servidor, así que solo se puede entrar desde mis aparatos conectados a mi red privada. Desde el wifi de casa sin Tailscale, ni lo ve.
- **La carpeta de fotos en solo lectura.** Este es el truco importante. Le doy a Immich acceso al disco donde Syncthing guarda las fotos, pero con un `:ro` al final (de *read only*, solo lectura). Immich puede mirar, pero no tocar.
- **Contraseña de la base de datos aleatoria**, de 32 caracteres, guardada en un fichero que solo puede leer mi usuario.

Así quedó la cosa:

```
  📱 Móvil  ──Syncthing──>  🖥️ Servidor: /mnt/backup-fotos/ruben
                                   │
                                   │  (solo lectura 👀, no puede borrar)
                                   ▼
                              📸 Immich  ──Tailscale──>  📱 App / 💻 Navegador
                              (miniaturas y base de datos
                               en el disco interno)
```

Las fotos originales se quedan donde estaban. Immich solo guarda en el disco interno sus miniaturas y su base de datos (qué foto es de qué fecha, en qué álbum está, etc.). Con todo arrancado, Immich gasta unos **1,2 GB de RAM** y quedan unos 1,5 GB libres para lo demás.

## Primer tropiezo: el navegador que no quería entrar

Abro Brave en el móvil, escribo la dirección y… `Failed to fetch dynamically imported module`. Muy bonito todo.

Comprobamos desde el servidor que el fichero que decía que faltaba existía y se descargaba sin problemas. O sea, el servidor estaba bien. Era el navegador: había abierto la página justo mientras el contenedor se reiniciaba, y Brave se guardó en caché una versión a medio cargar. Una recarga forzada y listo.

Bueno, listo no. Después llegó el "conexión rechazada". Aquí había dos sospechosos:

- **La pestaña privada con Tor.** Brave tiene dos pestañas privadas: la normal y la "con Tor". La de Tor manda el tráfico por la red Tor, que no tiene ni idea de qué es mi IP de Tailscale. Con la pestaña privada normal sí funciona.
- **El cambio automático a HTTPS.** Brave intenta pasar todas las webs a `https://` y mi Immich habla `http://`. Si la mejora a HTTPS está en modo estricto, se estrella. Se arregla quitando los escudos de Brave para ese sitio o poniendo la mejora a HTTPS en modo "Estándar".

Al final entré, creé mi usuario de administrador y… galería vacía, claro. Faltaba decirle dónde estaban las fotos.

## Enseñarle a Immich dónde están las fotos

Immich tiene una cosa llamada **biblioteca externa**: le dices "en esta carpeta hay fotos, míralas pero no son tuyas". Justo lo que quería. En el panel de administración creé una biblioteca con la ruta `/mnt/backup-fotos/ruben`, le di a escanear y en un rato tenía todo dentro.

Instalé también la app de Immich en el móvil. Y aquí me entró la duda.

## El miedo a las fotos duplicadas

La app de Immich tiene su propia "copia de seguridad": sube sola las fotos del móvil al servidor. Pero eso ya lo hace Syncthing. Si activo las dos, cada foto llega dos veces, una por cada camino, y la galería se llena de gemelas.

```
  📱 ──Syncthing──> /mnt/backup-fotos ──> Immich   ✅ (este ya lo tengo)
  📱 ──App Immich──> ~/immich/library ──> Immich   ❌ (este no, duplicaría todo)
```

Así que la copia de seguridad de la app se queda **apagada**. La app solo sirve para ver.

Para quedarme tranquilo, lo comprobamos desde el servidor, preguntándole directamente a la base de datos de Immich cuántas fotos tenía y de dónde venían:

- **454** fotos y vídeos en Immich, y los 454 venían de la biblioteca externa.
- **0** subidos desde la app.
- **454** archivos en la carpeta de Syncthing.

Cuadra todo: ni una duplicada, ni una perdida.

## Segundo tropiezo: los ajustes que no se guardaban

Me quedaban dos ajustes:

1. **Apagar el machine learning en la configuración.** El contenedor ya no existía, pero Immich no lo sabía y seguía intentando mandarle fotos para buscar caras y leer texto. Cada intento era un error en los registros.
2. **Activar "vigilar el sistema de archivos"** en la biblioteca externa. Por defecto, Immich revisa la carpeta una vez al día, así que una foto que Syncthing trajera hoy no aparecería hasta mañana. Con la vigilancia activada, la ve en cuanto llega.

Entro, toco los dos interruptores, salgo. Hecho.

Pues no. Lo comprobamos en el servidor y la configuración de Immich estaba **vacía**: no se había guardado nada. En los registros seguían saliendo los errores del machine learning.

El motivo era una tontería, pero de las que te pueden tener una tarde entera dando vueltas. En Immich, cada sección de la configuración tiene **su propio botón de Guardar**, abajo del todo. Si cambias un interruptor y te vas sin pulsarlo, el cambio desaparece sin avisar.

Segundo intento: machine learning apagado y Guardar. Comprobamos y ya aparecía guardado, pero la vigilancia seguía igual. Tercer intento: interruptor de vigilancia y su Guardar, el de esa sección. Y en los registros apareció por fin la línea que quería ver:

```
Starting to watch library ... with import path(s) /mnt/backup-fotos/ruben
```

"Empiezo a vigilar la biblioteca." Eso es.

## Cómo quedó todo

- Una galería tipo Google Fotos, en mi casa, accesible desde el móvil y el PC solo a través de Tailscale.
- Sin reconocimiento facial, y sin que el servidor vaya justo de memoria.
- Las fotos originales intactas: Immich no puede borrarlas aunque quiera.
- Cero duplicados: Syncthing trae las fotos, Immich solo las enseña.
- Las fotos nuevas aparecen solas en cuanto llegan.

## Lo que me llevo

Que "lo he cambiado" y "está guardado" no son lo mismo, y que lo más fiable es comprobarlo en el sitio donde se guarda de verdad. Si no hubiera mirado la base de datos, me habría quedado tan tranquilo pensando que todo estaba activado.

Y la otra lección, que ya me salió con Syncthing: antes de activar cualquier cosa que "sube fotos", hay que dibujar el camino que hace cada foto. Si sale más de una flecha hacia el mismo sitio, algo va a acabar duplicado.

Queda pendiente crearle su usuario a mi pareja en cuanto su móvil empiece a sincronizar. Y, de paso, ponerle a Immich una dirección más fácil de recordar que una IP con un puerto. Pero eso ya será otra entrada.
