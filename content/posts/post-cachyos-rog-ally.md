---
title: "Le metí Linux a mi ROG Ally (y el USB no quería arrancar)"
date: 2026-07-06
draft: false
---

Tengo una ROG Ally Z1 Extreme. La compré para jugar, como cualquiera. Pero después de meterle CachyOS a mi torre y quedarme enganchado, empecé a mirarla con otros ojos: ¿y si le hago lo mismo a la Ally?

Aquí va la trampa que me hizo plantearlo en serio: no juego a nada competitivo ni online. Ni Valorant, ni battle royales, nada de eso. Y resulta que el mayor problema de meter Linux en un handheld de juegos es el anticheat — esos sistemas antitrampas que muchos juegos multijugador usan, y que casi nunca funcionan bien en Linux porque los desarrolladores tienen que activarlos explícitamente para esa plataforma, y muchos no lo hacen. Como yo no toco esos juegos, ese problema simplemente no existe para mí.

Así que investigué. Y bien.

## Lo que encontré antes de tocar nada

CachyOS (la distro que ya uso en mi torre) tiene una **Handheld Edition** — una versión pensada específicamente para dispositivos como el Steam Deck, la Legion Go y la propia ROG Ally. No es un hack ni un apaño: instalador propio, KDE Plasma, un kernel optimizado para handhelds y un "Game Mode" al estilo SteamOS.

Antes de lanzarme, investigué qué problemas de hardware me iba a encontrar seguro, porque en un handheld no es como en un PC de sobremesa — hay mandos, botones traseros, sensores, control de batería... cosas que en Windows gestiona el software propio de Asus (Armoury Crate) y que en Linux no vienen solas:

- **TDP, ventilador y RGB**: no funcionan de fábrica. Se arreglan con `asusctl` + `rog-control-center`, dos paquetes de la comunidad.
- **Brillo automático**: no funciona, y no tiene arreglo limpio todavía (está pensado solo para Steam Deck).
- **Botones traseros (M1/M2)**: no se mapean solos, hace falta una herramienta aparte.
- **Lector de huellas**: no funciona, sin visos de arreglo próximo.

Con eso ya sabía a qué me enfrentaba. Nada bloqueante para mi caso.

## El USB que no quería arrancar

Preparé un pendrive con **Ventoy** — una herramienta que te permite meter varias imágenes `.iso` en un mismo USB y elegir cuál arrancar desde un menú, en vez de tener que "quemar" un USB distinto para cada sistema operativo que quieras probar. Copié ahí el ISO de CachyOS Handheld Edition (2,7 GB) y fui a arrancar la Ally desde él.

Primer obstáculo: la Ally solo tiene un puerto USB-C, así que iba con un hub para poder meter el pendrive y cargar a la vez. Al llegar al menú de Ventoy, esto es lo que me encontré:

```
Failed to open (hd0,1)/cachyos-handheld-linux-260628.iso
error: Can't open file (hd0,1)/cachyos-handheld-linux-260628.iso
error: image chunk is null
ventoy not ready
chain empty failed
```

Nada arrancaba. El pendrive estaba bien, el ISO estaba bien copiado... pero Ventoy no conseguía leerlo en el momento crítico. La explicación tiene su lógica una vez la entiendes: en esta fase tan temprana del arranque, el firmware UEFI usa drivers USB muy básicos y limitados, y muchos hubs multipuerto (los que llevan su propio chip controlador dentro) simplemente no son compatibles con ese modo tan primitivo — aunque luego, con el sistema operativo ya cargado y con drivers completos, funcionen sin problema.

La solución fue tan tonta como efectiva: **cambiar el pendrive de puerto dentro del propio hub**. Un puerto no funcionaba para el arranque, el otro sí. A veces la solución a un problema que suena a "controlador incompatible complejo" es literalmente mover un cable.

## Elegir bootloader: por qué Limine y no systemd-boot

Antes de particionar, el instalador me preguntó qué **bootloader** quería usar — el programa que arranca antes que el propio Linux, y que hace de puente entre el firmware del hardware y el sistema operativo ya cargado.

Tenía dos opciones: **systemd-boot** (el clásico, minimalista, el que llevo usando en mi torre) o **Limine** (más moderno, y el que CachyOS ha elegido como predeterminado para la Handheld Edition). Me decidí por Limine por un motivo muy concreto para mi situación: viene integrado con **snapshots automáticos** cuando usas BTRFS como sistema de archivos. Es decir, cada vez que instalo o actualizo algo, el sistema guarda automáticamente una "foto" del estado anterior, accesible directamente desde el propio menú de arranque.

Como voy a estar trasteando bastante con este sistema (instalando cosas, tocando configuraciones, aprendiendo a base de romper cosas), tener una red de seguridad tan directa — arrancar, elegir el snapshot de ayer, listo, sin USB de rescate — me pareció el argumento decisivo. Y de hecho, ya lo he visto actuar solo, sin buscarlo, cada vez que instalo un paquete nuevo: el propio instalador de paquetes hace su snapshot antes y después, sin que yo tenga que acordarme de nada.

## Adiós Windows (con red de seguridad)

Aquí viene la parte sin vuelta atrás: el instalador me mostró el resumen final, y confirmé borrar el disco entero. Nada de dual-boot, todo para CachyOS.

Antes de darle al botón, ya tenía claro cómo volver a Windows si algo salía mal: la Ally trae integrado en su propia BIOS un sistema llamado **ASUS Cloud Recovery**. Se entra manteniendo el botón de bajar volumen mientras enciendes, y desde ahí el propio dispositivo se descarga Windows de fábrica directamente de los servidores de Asus por WiFi — sin que yo tuviera que preparar ningún USB de recuperación de antemano. Saber que ese "botón de pánico" ya existe en el propio hardware me quitó bastante presión a la hora de confirmar el borrado.

Instalación completa, unos 15 minutos, y ya tenía CachyOS Handheld Edition arrancando en mi Ally.

## Metiéndole un asistente de IA al propio sistema

Ya con el sistema instalado, quise probar algo: meter **Claude Code** — un agente de terminal que puede leer, ejecutar comandos y editar archivos directamente en tu sistema — para que me ayudara a diagnosticar y configurar cosas específicas del hardware de la Ally, explicándome cada paso en vez de simplemente "arreglarlo él solo" sin que yo entienda nada.

La instalación fue de un solo comando:
```
curl -fsSL https://claude.ai/install.sh | bash
```

Y ahí me encontré con mi primer tropiezo pequeño: al terminar, escribí `claude` y la terminal me contestó `fish: Unknown command: claude`. El programa sí se había instalado, pero mi terminal (uso Fish, no Bash) no sabía dónde buscarlo — el instalador me dio una solución pensada para Bash, que en Fish simplemente no vale porque tiene su propia sintaxis. La solución real fue:
```
fish_add_path ~/.local/bin
```
Una función propia de Fish para añadir carpetas a la lista de sitios donde busca comandos. Al momento, `claude` funcionó.

Le pedí a Claude Code un diagnóstico inicial del sistema (sin tocar nada, solo mirar) y me devolvió algo que ni yo sabía: tenía dos "gestores de energía" instalados a la vez (`power-profiles-daemon` de CachyOS y el futuro `asusd` de asusctl) que podían pisarse entre sí si no se gestionaban con cuidado. Es el tipo de detalle que un simple "instala y ya" nunca te habría avisado.

## Moonlight, y una lección de cómo buscar paquetes en Arch

Para el streaming de juegos desde mi torre a la Ally, necesitaba **Moonlight** — el cliente que recibe la imagen desde un PC que tenga Sunshine corriendo (lo monté hace tiempo para jugar desde el móvil, así que ya tenía el lado servidor listo).

Aquí aproveché para aprender algo más general y útil que el propio Moonlight: **cómo buscar un paquete cuando no sabes el nombre exacto**. En vez de ir directo a la web del proyecto, el método correcto en Arch es:
```
pacman -Ss moonlight
```
Primero intenté instalar `moonlight` a secas y me dio error de "paquete no encontrado" — el nombre real es **`moonlight-qt`** (el sufijo viene del framework gráfico que usa). Ese tipo de pequeño tropiezo por un nombre no exacto es de lo más común en Linux, y ahora sé cómo resolverlo yo solo la próxima vez.

Curiosidad extra: el paquete aparece duplicado en dos repositorios — el genérico `extra` de Arch, y uno propio de CachyOS llamado `cachyos-extra-znver4`, recompilado específicamente para procesadores con arquitectura Zen 4 (justo la que lleva el Z1 Extreme de la Ally). Es una de las señas de identidad de CachyOS: recompilar software popular optimizado para tu CPU concreta, sacando algo más de rendimiento que la versión genérica.

## Jugando desde la torre, en la mano

Con todo instalado, la prueba de fuego: streaming desde mi torre a la Ally por Sunshine + Moonlight. Funcionó a la primera.

Un detalle práctico que merece la pena anotar: para salir de una sesión de streaming sin tener que buscar un botón en pantalla, hay dos atajos:
- Con teclado conectado: `Ctrl + Alt + Shift + Q`
- Con el propio mando de la Ally: mantener pulsados a la vez `Select/View + Start + LB + RB`

(El gesto táctil de "tres dedos hacia abajo" que documenta Moonlight para dispositivos sin teclado no me funcionó — resulta que KDE Plasma usa ese mismo gesto para cambiar de escritorio virtual, y gana el gesto del sistema operativo antes de que le llegue a la app de streaming. Cosas de tener dos capas de software queriendo interpretar el mismo gesto.)

## ¿Merece la pena?

De momento, con lo que llevo probado: sí, sin duda, para mi caso concreto. Nada de anticheat que me bloquee, streaming funcionando de fábrica, y un sistema que ya se siente más "mío" que cualquier Windows preinstalado.

Lo que queda pendiente — configurar bien el TDP y los botones traseros, el giroscopio, y algún que otro experimento de acceso remoto que no salió como esperaba — te lo cuento en la siguiente entrada, porque ahí sí que me choqué con algo que no tuvo solución tan fácil.
