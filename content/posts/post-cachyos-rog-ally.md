---
title: "Le metí Linux a mi ROG Ally (y el USB no quería arrancar)"
date: 2026-07-06
draft: false
---

Tengo una ROG Ally Z1 Extreme. La compré para jugar, como cualquiera. Pero después de meterle CachyOS a mi torre y quedarme enganchado a esto de Linux, empecé a mirarla con otros ojos: ¿y si le hago lo mismo a la Ally?

Antes de lanzarme a nada, le pregunté a Claude si tenía sentido siquiera planteárselo. Porque yo sabía una cosa: en handhelds de gaming, meter Linux suele chocar con los anticheats — esos sistemas antitrampas que muchos juegos multijugador usan para evitar que hagas trampas online. Y resulta que como yo no juego a nada competitivo ni online, ese problema directamente no me afecta. Con eso ya tenía luz verde para investigar en serio.

## Lo que fuimos descubriendo antes de tocar nada

Le pedí que buscara qué opciones había, y resultó que CachyOS (la distro que ya uso en mi torre) tiene una **Handheld Edition** — una versión pensada específicamente para dispositivos como el Steam Deck, la Legion Go y la propia ROG Ally. Instalador propio, KDE Plasma, un kernel optimizado para handhelds.

Antes de instalar nada, le pedí que investigara qué problemas de hardware me iba a encontrar seguro, porque un handheld no es como un PC de sobremesa — hay mandos, botones traseros, sensores, batería... cosas que en Windows gestiona el software propio de Asus (Armoury Crate) y que en Linux, según me explicó, no vienen resueltas de fábrica:

- **TDP, ventilador y RGB**: no funcionan de fábrica, hace falta instalar herramientas de la comunidad aparte.
- **Brillo automático**: no funciona, sin arreglo limpio todavía.
- **Botones traseros (M1/M2)**: no se mapean solos.
- **Lector de huellas**: no funciona.

Ninguno de esos me pareció bloqueante para lo que quiero hacer, así que fui a por ello.

## Preparando el USB (y aprendiendo qué es Ventoy)

Nunca había usado **Ventoy** antes de esto. Me lo explicaron así: en vez de "quemar" un USB distinto cada vez que quieres probar un sistema operativo, Ventoy te deja meter varias imágenes `.iso` en el mismo pendrive, y al arrancar te aparece un menú para elegir cuál usar. Lo instalé en mi torre (`yay -S ventoy-bin`), y con `sudo ventoy -i /dev/sda` (tuve que aprender a identificar bien cuál era mi USB con `lsblk`, para no liarla y borrar el disco equivocado) preparé el pendrive. Copié ahí el ISO de CachyOS Handheld Edition, unos 2,7 GB.

## El USB que no quería arrancar

Fui a arrancar la Ally desde el pendrive. Como solo tiene un puerto USB-C, iba con un hub para poder meter el USB y cargar a la vez. Llegué al menú de Ventoy y, al intentar arrancar el ISO, me encontré esto en pantalla:

```
Failed to open (hd0,1)/cachyos-handheld-linux-260628.iso
error: Can't open file (hd0,1)/cachyos-handheld-linux-260628.iso
error: image chunk is null
ventoy not ready
chain empty failed
```

No tenía ni idea de qué significaba nada de eso. Le pasé la foto de la pantalla, y me explicó que en esta fase tan temprana del arranque (antes de que cargue cualquier sistema operativo), el firmware del ordenador usa unos drivers USB muy básicos, y que muchos hubs con varios puertos simplemente no son compatibles con ese modo tan primitivo, aunque luego funcionen perfectamente con Windows o Linux ya arrancados.

La solución fue tan simple que me dio hasta un poco de vergüenza lo mucho que le había dado vueltas al problema: **cambiar el pendrive de puerto dentro del mismo hub**. Un puerto no servía para arrancar, el otro sí. A veces el "bug complicado" es mover un cable de sitio.

## Elegir bootloader sin saber qué es un bootloader

El instalador me preguntó si quería usar **systemd-boot** o **Limine** como bootloader, y tuve que preguntar qué diferencia había, porque no tenía ni idea de qué es un bootloader más allá de "lo primero que arranca antes que Linux".

Me explicaron que Limine, al usar BTRFS como sistema de archivos, viene con **snapshots automáticos** — cada vez que instalas o actualizas algo, el sistema guarda solo una "foto" del estado anterior, accesible desde el propio menú de arranque. Como sé que voy a estar trasteando bastante (instalando cosas, rompiendo cosas, aprendiendo así), me convenció tener esa red de seguridad tan a mano. Elegí Limine.

Y de hecho ya lo he visto actuar solo, sin que yo hiciera nada especial: cada vez que instalo un paquete nuevo, veo en la terminal que hace un snapshot antes y después, sin que tenga que acordarme de nada.

## Adiós Windows

Llegó el momento sin vuelta atrás: confirmar el borrado completo del disco, sin dual-boot. Antes de darle, quise asegurarme de que tenía forma de volver a Windows si algo salía mal. Resulta que la propia Ally trae integrado en su BIOS un sistema llamado **ASUS Cloud Recovery**: entrando con una combinación de botones al encender, el propio dispositivo se descarga Windows de fábrica directamente de los servidores de Asus por WiFi. No hacía falta que yo preparara ningún USB de recuperación de antemano. Eso me quitó bastante presión a la hora de confirmar el borrado.

Unos 15 minutos después, tenía CachyOS Handheld Edition arrancando en mi Ally.

## Metiéndole a Claude Code dentro del propio sistema

Una vez instalado, quise probar algo que me parecía casi de ciencia ficción: instalar **Claude Code** directamente en la Ally — un agente de terminal que puede leer, ejecutar comandos y editar archivos del sistema, explicándote cada paso en vez de simplemente "arreglarlo él solo" sin que tú entiendas nada. Justo lo que necesito para no depender siempre de copiar comandos a ciegas.

La instalación fue un solo comando:
```
curl -fsSL https://claude.ai/install.sh | bash
```

Y ahí me encontré con mi primer tropiezo pequeño de la sesión: al terminar, escribí `claude` y la terminal me contestó `fish: Unknown command: claude`. Se había instalado bien (el propio instalador me lo confirmó), pero mi terminal (uso Fish, no Bash) no sabía dónde buscar el programa. El propio instalador me dio una solución pensada para Bash que en Fish no vale, porque tiene su propia forma de escribir las cosas. Tuve que aprender que en Fish se hace así:
```
fish_add_path ~/.local/bin
```

Con eso, `claude` empezó a funcionar. Le pedí un diagnóstico del sistema (sin tocar nada, solo mirar) y me contó algo que yo ni sabía que podía pasar: tenía dos "gestores de energía" instalados a la vez que podían pisarse entre sí si no se gestionaban con cuidado. Ese tipo de detalle es justo lo que busco: que me avise de cosas que yo solo ni habría sabido que existían.

## Moonlight, y aprendiendo a buscar paquetes yo solo

Para el streaming de juegos desde mi torre a la Ally necesitaba **Moonlight**. Aquí aproveché para aprender algo más general que el propio programa: cómo buscar un paquete en Arch cuando no sabes el nombre exacto, en vez de ir directo a Google.

```
pacman -Ss moonlight
```

Probé primero `moonlight` a secas y me dio error de "no encontrado". El nombre real del paquete es **`moonlight-qt`**. Un tropiezo tonto, pero que ahora ya sé resolver yo solo la próxima vez que me pase con cualquier otro programa.

## Jugando desde la torre, en la mano

Con todo instalado, la prueba de fuego: streaming desde mi torre a la Ally por Sunshine + Moonlight. Funcionó a la primera, cosa que no esperaba dado todo lo anterior.

Un detalle práctico que aprendí sobre la marcha: para salir de una sesión de streaming sin buscar un botón en pantalla, hay dos atajos — con teclado, `Ctrl + Alt + Shift + Q`; con el propio mando de la Ally, mantener pulsados `Select/View + Start + LB + RB` a la vez. (El gesto táctil de tres dedos que la documentación de Moonlight menciona para dispositivos sin teclado no me funcionó, porque resulta que KDE Plasma usa ese mismo gesto para cambiar de escritorio virtual, y gana el gesto del sistema antes de que le llegue a la app.)

## ¿Merece la pena?

De momento, con lo que llevo probado: para mi caso, sí, sin duda. Nada de anticheat bloqueándome, streaming funcionando, y un sistema que ya se siente más "mío" que cualquier Windows preinstalado — aunque todavía me quede mucho por entender.

Lo que queda pendiente (TDP, botones traseros, giroscopio, y un experimento de acceso remoto que no salió nada bien) te lo cuento en la siguiente entrada, porque ahí sí que me choqué con algo que no tuvo solución fácil.
