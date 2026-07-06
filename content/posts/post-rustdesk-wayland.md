---
title: "Quería un Chrome Remote Desktop para Linux (y me topé con un bug real)"
date: 2026-07-06
draft: false
---

Con CachyOS ya instalado y funcionando en la Ally ([como conté en el post anterior](/posts/post-cachyos-rog-ally/)), quería poder controlar tanto la Ally como mi torre desde el móvil, cómodamente, como cuando usas Chrome Remote Desktop. Me parecía lo más sencillo del mundo. No lo fue, pero el camino hasta rendirme (y lo que aprendí por el camino) merece contarse.

## Intento 1: VNC con Krfb y Krdc

Mi primera idea fue usar lo que ya traía KDE Plasma incorporado: activar **Krfb** (el servidor de escritorio remoto) en la Ally, y conectarme desde mi torre con **Krdc** (su cliente). Activé Krfb, me dio una dirección y una contraseña generada automáticamente, y probé a conectar.

Primer tropiezo:
```
La dirección usada no puede ser utilizada.
```

Ni idea de qué estaba haciendo mal. Probé con el prefijo `vnc://` delante, sin prefijo, con el puerto explícito, sin puerto... Cuatro intentos, cuatro variantes del mismo error de formato ("URL inútil", "La dirección introducida no tiene la forma requerida"...). Nunca llegamos a averiguar si el fallo estaba en la interfaz de Krdc o en algo de red más de fondo. En vez de seguir dándome cabezazos contra la misma pared, decidimos probar otra vía.

## Intento 2: RustDesk

Cambiamos de estrategia hacia **RustDesk** — de código abierto, gratis, con apps para móvil, y pensado para funcionar con un simple ID + contraseña, sin líos de direcciones IP ni puertos.

Lo instalé en la torre y en la Ally desde el AUR (`paru -S rustdesk-bin` — bueno, en realidad la primera vez escribí `rustdesk.bin` con un punto en vez de guion, y pacman ni lo encontró; cosas de ir aprendiendo la sintaxis). Conecté desde el móvil, y esta vez sí conectó... pero lo que vi no fue el escritorio real: **un fondo de pantalla genérico**, y solo era capaz de mover el ratón, nada de ver lo que de verdad había en pantalla.

## Aprendiendo a leer logs en vez de seguir probando a ciegas

Aquí me enseñaron algo que no sabía hacer: en vez de seguir cambiando ajustes al azar esperando que algo funcionara, se puede ir directo a los registros (logs) del propio programa para ver qué está pasando por dentro de verdad:

```
grep -iE "capturer|portal|screencast|error|fail" ~/.local/share/logs/RustDesk/server/rustdesk_rCURRENT.log
```

Entre líneas que no entendía nada, había una que llamaba la atención:
```
Response from DBus: response: 0, results: {"streams": ..., "size": [1920, 1080] ...}
```

Pregunté qué significaba eso de "response: 0", porque para mí eran solo números sueltos. Me explicaron que un `0` ahí es señal de **éxito** — el sistema de permisos de KDE (algo llamado "portal", que en Wayland —el protocolo gráfico moderno de Linux— hace de intermediario entre las apps y tu pantalla para que ninguna pueda "espiarte" sin permiso) sí había aceptado compartir la pantalla, incluso había acordado bien la resolución. El problema no estaba en el permiso. Estaba en un paso posterior: RustDesk no conseguía leer de verdad los fotogramas de ese vídeo que el sistema le había entregado.

Buscando un poco más sobre ese error concreto, resultó ser un **bug conocido y documentado** de RustDesk, específico de KDE Plasma sobre Wayland. Otros usuarios en GitHub reportaban exactamente el mismo síntoma, y hasta un desarrollador del propio proyecto había confirmado que ya sabían la causa, pero que todavía no había una corrección publicada.

Fue un alivio, la verdad — llevaba un rato pensando que estaba haciendo algo mal yo, y resultó ser un agujero real del software, no mío.

## Desinstalar en vez de forzar

Probamos alguna cosa más (forzar que el sistema usara el "portal" de KDE en vez de uno de GNOME que convivía activo a la vez), sin suerte. Llegados a ese punto, tomé una decisión que no siempre se cuenta en estos posts: **desinstalar limpio en vez de dejarlo a medias**.

```
sudo pacman -Rns rustdesk-bin
```

No tenía sentido dejar instalado algo que no funciona "por si algún día se arregla solo". Si hace falta, se reinstala en dos minutos cuando haya una corrección de verdad.

## Lo que de verdad necesitaba: SSH

Parándome a pensar qué era lo que realmente quería hacer con ese acceso remoto, me di cuenta de que casi siempre era simplemente **escribir comandos en la terminal de la Ally sin sacar un teclado externo cada vez** (la Ally no trae uno propio, solo pantalla táctil). No necesitaba ver el escritorio entero — necesitaba teclear cómodo.

Y para eso, **SSH** ya lo resolvía de sobra, sin ningún bug de por medio:

```
ssh ruben@192.168.1.150
```

Sin fondos de pantalla en blanco, sin depender de que alguien arregle un bug en algún momento futuro. Escribo en el teclado completo de mi torre y los comandos llegan directos a la Ally.

## La lección de este post

No todos los experimentos terminan en "y funcionó, fin". A veces la respuesta honesta es "esto no funciona todavía, aquí está la prueba, y esto otro cubre lo que necesitaba de verdad sin tanto lío". Perseguir el escritorio remoto "bonito" me habría hecho perder mucho más tiempo del que merecía la pena para algo que SSH ya resolvía sin dramas.

Si tienes CachyOS con KDE Plasma en Wayland y te encuentras el mismo síntoma con RustDesk (fondo genérico, ratón sí, pantalla no), al menos ya sabes que no eres tú: es un bug conocido, y de momento la alternativa más fiable parece ser cambiar la sesión a X11, o plantearte, como yo, si en realidad lo que necesitas es más simple de lo que parece.
