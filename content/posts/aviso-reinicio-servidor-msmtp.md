---
title: "Cuando se va la luz: un correo que avisa de cuándo ha vuelto"
date: 2026-08-25T20:00:00+02:00
draft: false
description: "Quería que el servidor de casa avisara solo cuando se reiniciara, con la hora exacta. Parecía cosa de dos líneas, pero por el camino hubo una sesión SSH cortada a media tarea, un sudo que se negó a colaborar y una pregunta de AppArmor que no esperaba."
---

Hay proyectos que parecen sencillos hasta que te metes dentro. Este era uno de esos: "que me llegue un correo cuando el servidor se reinicie, con la hora exacta". En la teoría, dos líneas de nada. En la práctica: una sesión de SSH que se cortó a media tarea, un `sudo` que se negó a hablar conmigo, una ruta tan larga que se rompía al copiarla, y una ventanita de AppArmor preguntándome cosas que no esperaba.

No hace falta memorizar ni un solo comando de los que aparecen aquí abajo. Lo que importa es entender qué problema resuelve cada pieza, porque las piezas se repiten en cualquier proyecto de este estilo.

## El problema: enterarme tarde de un corte de luz

El servidor de casa (un ThinkCentre con Debian 13) lleva varios servicios que me importan: Vaultwarden, Syncthing, alguna cosa más. Cuando se va la luz, el servidor se apaga y vuelve a arrancar solo en cuanto vuelve la corriente, pero yo no me entero hasta que por casualidad intento entrar y algo no responde. Quería que el propio servidor me avisara: "oye, me he reiniciado, y ha sido a esta hora".

## La idea: una nota pegada a la puerta en cuanto alguien entra

La forma más sencilla de pensarlo es como una nota que alguien deja pegada a la puerta nada más entrar en casa: "he vuelto a las 14:32". Eso es literalmente lo que hace el script que escribimos, `notify-boot.sh`: en cuanto el sistema arranca, mira la hora de arranque (con `uptime -s`) y manda un correo con ese dato a mi propio Gmail.

## msmtp: el cartero que solo sabe llevar un sobre

Para mandar el correo hace falta algo que hable el idioma de un servidor de correo (SMTP). Ahí entra `msmtp`: un programa minúsculo que no hace nada más que coger un mensaje y entregarlo en el buzón de Gmail. No es un cliente de correo, no tiene bandeja de entrada ni nada parecido, es solo el cartero.

Para que Gmail confíe en ese cartero hace falta una "contraseña de aplicación": no la contraseña real de la cuenta, sino una clave aparte, generada solo para este uso, que se puede revocar sin tocar la cuenta principal. Esa clave se queda guardada en `/etc/msmtprc`, un fichero que solo puede leer el usuario root del sistema.

## systemd: quién avisa a quién y en qué momento

El script por sí solo no se ejecuta nunca; hace falta decirle al sistema cuándo debe lanzarlo. Para eso está `boot-notify.service`, una unidad de systemd que dice, en esencia: "en cuanto haya red disponible tras el arranque, ejecuta este script una vez y ya está". Al dejar esa unidad "enabled", systemd se encarga de dispararla en todos los arranques futuros, sin que yo tenga que acordarme de nada.

## Tropiezos por el camino

A media instalación se cortó la conexión SSH y perdí la sesión con la que estaba trabajando. Al reconectar, lo que ya habíamos preparado —el script, la plantilla de configuración y la unidad de systemd— seguía esperando en una carpeta temporal, así que pudimos retomarlo justo donde lo habíamos dejado, sin repetir nada.

El primer tropiezo serio fue con `sudo`. Intenté instalar todo directamente desde el propio chat, y `sudo` se negó en redondo: "necesito una terminal de verdad para pedirte la contraseña". Tiene sentido —es una medida de seguridad, no un capricho—: `sudo` no quiere que nadie le pueda colar una contraseña por un canal que no sea una terminal interactiva real. La solución fue abrir una ventana de terminal aparte, completamente separada del chat, y ejecutar ahí la instalación.

El segundo tropiezo fue más tonto: la ruta del script era tan larga (metida varios niveles dentro de una carpeta temporal con un identificador larguísimo) que, al copiarla y pegarla, la terminal la partía por la mitad y el comando fallaba buscando un fichero que "no existía", cuando en realidad sí existía, solo que con otro nombre roto a medias. Se arregló copiando todo a una ruta corta y sin sorpresas.

Y por último, al instalar `msmtp` con `apt` apareció una pregunta sobre AppArmor, el sistema que puede restringir lo que un programa tiene permiso para hacer. El propio texto de la pregunta avisaba de que activarlo para `msmtp` da a veces errores de permisos difíciles de entender, así que elegimos que no: para un script tan simple, no compensaba el riesgo de quedarme media hora buscando por qué un envío de correo "no tenía permiso" para algo tan tonto.

## La prueba

Con todo instalado —`msmtp`, el script en `/usr/local/bin`, la configuración en `/etc/msmtprc` y la unidad de systemd activada— tocaba comprobarlo. Se lanzó el script a mano, y llegó el correo de prueba a mi Gmail. Desde ahora, cada arranque del servidor manda ese mismo aviso solo, sin que nadie tenga que acordarse de nada.

## Lo que me llevo de esta sesión

Que un reinicio, o un corte de luz, no tiene por qué ser invisible: basta con pedirle al sistema que deje constancia y avise. Que una unidad de systemd es, en el fondo, un contrato muy simple entre un "cuándo" y un "qué". Y que `sudo` pidiendo una terminal real, o AppArmor preguntando antes de restringir un programa, no son obstáculos porque sí: son el sistema protegiéndose de que alguien —incluido yo mismo, sin darme cuenta— le cuele algo por la puerta de atrás.

El siguiente paso, si algún día pongo un SAI en el server, será distinguir un corte de luz real de un reinicio cualquiera. Por ahora, con saber a qué hora ha vuelto, tengo suficiente.
