---
title: "Me hice un escritorio KDE de Japón antiguo en pixel art (y su fondo sigue al sol)"
date: 2026-11-01T17:00:00+01:00
draft: false
description: "Un tema completo para KDE Plasma 6: paisaje pixel art animado que cambia con la hora de tu ciudad, iconos y cursor pixel, y un panel de datos que se adapta al tamaño de tu pantalla. Lo construí paso a paso con Claude Code. Sin dependencias, en un paquete de 1 MB."
tags: ["kde", "plasma", "linux", "cachyos", "pixel-art", "python", "personalizacion", "claude-code"]
ShowToc: true
TocOpen: false
cover:
  image: "escritorio-dia.png"
  alt: "Escritorio KDE con un paisaje japonés en pixel art de día y un panel de datos a la derecha"
  relative: true
  hiddenInSingle: true
---

Quería un escritorio que fuera bonito de mirar **y** útil. Lo primero es subjetivo; lo segundo, una lista: ver de un vistazo qué puertos tengo abiertos, si la VPN está levantada, cómo va la batería, qué servicio se ha caído. Acabé haciendo un tema entero para KDE Plasma 6, con un paisaje japonés dibujado píxel a píxel como fondo y un panel de datos encima, y me ha salido algo que me da pena no compartir.

Se llama **PixelZen**, lo puedes descargar al final y ocupa un megabyte.

Un aviso de entrada, para que nadie imagine que escribí «hazme un tema bonito» y salió esto: lo fui construyendo **paso a paso con Claude Code**, pieza a pieza, revisando el resultado en pantalla, corrigiendo y pidiendo más detalle en cada ronda. Al final del artículo cuento cómo fue ese proceso, con sus fallos incluidos.

{{< captura wide="true" src="escritorio-dia.png" alt="Escritorio KDE con un paisaje japonés en pixel art de día y un panel de datos a la derecha" caption="PixelZen de día (clic en cualquier captura para verla a tamaño completo)" >}}

## Qué es

Un tema de escritorio para **KDE Plasma 6** (lo uso en mi T14s con CachyOS) con estas piezas:

- **Un fondo animado** con pagoda, torii, lago, una montaña nevada y un cerezo en flor, todo en pixel art.
- **Un panel de datos** (le llamo HUD) en la columna libre de la derecha, que **se escala con la altura de tu pantalla**: ocupa lo mismo en un portátil de 1200 px que en un monitor de 1440.
- **Iconos, cursor, ventanas y terminal** a juego.
- **Una barra superior mínima**, porque los datos ya viven en el HUD.

Y todo se genera con **Python puro**. Ni Inkscape, ni ImageMagick, ni librerías: lo que dibuja los píxeles son unos bucles y un par de matrices.

## El fondo sigue al sol

La parte que más me gusta, y la que me costó más. El fondo no es una imagen: es una escena que cambia con **la hora real de tu ciudad**.

{{< captura wide="true" src="escritorio-amanecer.png" alt="El mismo paisaje al amanecer, con el cielo violeta y rosa" caption="Amanecer (clic para ver a tamaño completo)" >}}

- El sol sale por el este, cruza el cielo y se pone por el oeste según la fecha y tu latitud. El cálculo (con fórmulas astronómicas estándar) lo hace el propio widget, así que **no gasta nada** mientras lo usas.
- El paisaje existe en **tres iluminaciones** (noche, hora dorada y día) que se mezclan poco a poco según la altura del sol.
- De noche salen la luna, las estrellas, las luces de la pagoda y las luciérnagas. De día desaparecen.
- El camino de luz sobre el lago sigue al sol o a la luna.
- Todo se mueve a 8 fotogramas por segundo: nubes, farolillos que titilan, pétalos, grullas y alguna estrella fugaz.

{{< captura wide="true" src="escritorio-noche.png" alt="De noche, con luna llena, estrellas y la pagoda iluminada" caption="Noche: luna, estrellas y la pagoda iluminada" >}}

**No manda nada a ningún sitio.** La ubicación sale de tu zona horaria (o de una ciudad que fijes tú), y el sol se calcula en local. Pensé en añadir el tiempo real (nubes, lluvia), pero eso implica enviar tus coordenadas a un tercero, y no me compensaba.

Y es interactivo, que era mi capricho:

```bash
hora.sh 21:30   # congela esa hora
hora.sh demo    # 24 horas en 90 segundos, para ver cómo anochece
hora.sh real    # vuelve a la hora del reloj
```

El mismo fondo, animado, se ve en la pantalla de bloqueo:

{{< captura wide="true" src="bloqueo.png" alt="La pantalla de bloqueo con el mismo paisaje" caption="La pantalla de bloqueo, con el mismo fondo animado" >}}

### ¿Cómo sabe dónde está el sol?

Es la pregunta que más me han hecho. Mi primera idea fue una tabla con las horas de amanecer y anochecer de cada ciudad, pero no hace falta: el sol sigue unas reglas conocidas, y con la fecha y el lugar se puede **calcular** dónde está en cada momento.

> **Para entenderlo rápido**
>
> Piensa en un columpio: cuando subes ves el cielo y cuando bajas ves el suelo. La Tierra gira sobre sí misma y por eso el sol parece subir por la mañana y bajar por la tarde.
>
> PixelZen calcula lo alto que está el sol con tres cosas: **qué día es** (en verano sube más que en invierno), **qué hora es** (cuánto ha girado la Tierra) y **dónde estás** (en España el sol no sale igual que en Japón).
>
> Con eso sale un número: número bajo, noche con estrellas y luna 🌙; número medio, cielo naranja de amanecer o atardecer 🌅; número alto, día ☀️.

**Los pasos, a grandes rasgos:**

1. **Qué día es de verdad.** Se cuentan los días desde el año 2000 en hora universal (UTC), que es la misma en todo el mundo. Por eso la zona horaria apenas interviene.
2. **Dónde está el sol en su órbita.** La órbita de la Tierra no es un círculo perfecto y su eje está inclinado. Dos pequeñas correcciones dan la *declinación*: lo alto o bajo que pasa el sol según la época del año.
3. **Cuánto ha girado la Tierra.** Sale del *tiempo sidéreo*, que mide el giro del planeta respecto a las estrellas.
4. **Dónde estás tú.** La **latitud y la longitud** convierten ese giro en el *ángulo horario*: cuánto ha avanzado el sol desde su punto más alto.
5. **Altura del sol.** Declinación, ángulo horario y latitud dan un único número: los grados que el sol está por encima (o por debajo) del horizonte.

Esa altura lo controla todo. Por debajo de unos −14° es noche cerrada, entre −14° y 0° el cielo se tiñe de dorado, y a partir de unos 16° es pleno día. Las estrellas aparecen cuando el sol baja de unos −6°, y entre un tramo y otro la transición se suaviza con una curva (*smoothstep*) para que no haya saltos.

**¿Y las zonas horarias?** Como el cálculo parte de la hora UTC y de tu latitud y longitud, solo hace falta saber dónde estás. Eso sale de la zona horaria del equipo (buscando su punto en `zone1970.tab`, sin red) o de una ciudad fija que configures. Si viajas y cambias la zona, el paisaje se ajusta solo. Si tuviera que hacerlo para un entorno con muchas zonas, haría lo mismo: guardar todo en UTC y convertir a hora local solo al mostrar.

**Una pega:** la luna **no** se calcula así. Es un arco decorativo de este a oeste que se reparte según lo que dura la noche en tu ciudad. Queda natural, pero no es su posición real ni sus fases.

## Cómo está hecho

### Un paisaje en capas

Para que el sol pase *por detrás* de las montañas tuve que separar el cielo de la escena. El generador dibuja cada fase dos veces, una sobre fondo negro y otra sobre blanco, y saca la transparencia por la diferencia entre las dos (*difference matting*). Así la niebla y los tramados quedan semitransparentes de verdad. Cielo, escena y nubes son PNG de 640×400 que el widget amplía ×3 **sin suavizar**, para que los píxeles sigan nítidos.

Los degradados no son suaves: usan una matriz de Bayer 4×4 (tramado ordenado), como los juegos de los noventa. Las montañas salen de ruido fractal, con nieve, estratos y luz de luna en el filo.

### El HUD

Es un plasmoide en QML con un motor de datos en Python que **solo lee** (`/proc`, `sysfs`, `ss`, `ip`, `git`). Sin red y sin `sudo`. Tiene:

- **Tiempo:** reloj, calendario japonés (令和八年) y fase lunar en píxeles.
- **Sistema:** CPU, RAM, temperatura y batería con barras segmentadas.
- **Red:** Wi-Fi, IP, VPN, velocidad y **puertos en escucha**, con los expuestos a toda la red marcados en ámbar. Me sirve para saber, sin abrir una terminal, qué está escuchando mi máquina.
- **Dev:** estado de mis repos, versiones de Python/Node/Go/Rust, servicios fallidos y errores de la última hora.
- **Herramientas:** botones que abren una terminal con `btop`, `ss`, `dig`, `ping`… y detecta qué tengo instalado. El de `nmap` me propone instalarlo, sin ejecutar nada.
- **Haiku:** un verso de Bashō, Buson o Chiyo-ni que rota con fundido.

### Iconos y cursor

El tema de iconos traduce unos **3000 nombres de icono de KDE** a glifos de [Pixelarticons](https://github.com/halfmage/pixelarticons) (licencia MIT), y dibuja por su cuenta los azulejos de las apps, las carpetas y las hojas de cada tipo de archivo. Lo que no cubre cae a Breeze, así que nada se rompe.

{{< captura src="iconos.png" alt="Muestras del tema de iconos: apps, carpetas, tipos de archivo, acciones y estado" caption="Iconos: apps, carpetas, tipos de archivo, acciones y estado" >}}

El cursor lo escribí a mano en formato **Xcursor** (es un binario sencillo): flecha con la punta roja de un torii, mano, lupa, "prohibido" y una espera animada.

### La tipografía: un error que corregí

Mi primera elección fue una fuente pixel muy decorativa, y me costaba leerla. Probé **ocho fuentes** con el mismo texto y ganó **Departure Mono**: distingue `0` de `O`, `I` de `l` de `1`, y la `~` no parece una N. Moraleja pixelera: *bonito* y *legible* no siempre van juntos.

{{< captura src="terminal.png" alt="La terminal con el prompt a juego" caption="La terminal, con el prompt a juego" >}}

## Cómo lo hice (y por qué lo cuento)

PixelZen lo construí **conversando con Claude Code, paso a paso**, igual que el rediseño del blog. No fue una petición y un resultado: fueron muchas rondas cortas, y en cada una yo decidía qué quería, miraba el resultado en mi pantalla y pedía que se corrigiera o se detallara. El reparto fue más o menos este: **yo ponía la idea, el criterio y el ojo; Claude Code escribía el código** y lo probaba conmigo delante.

El orden, a grandes rasgos:

1. **El paisaje.** Primero un fondo estático en pixel art, con la pagoda, el torii, el lago y el cerezo, que fuimos detallando en varias versiones.
2. **El HUD.** Una tarjeta cada vez: reloj, sistema, red, dev, herramientas y haiku. Cada una pasó por mi revisión antes de pasar a la siguiente.
3. **Tipografía, iconos y cursor.** Aquí rectifiqué yo mismo la primera elección de fuente, como cuento arriba.
4. **El fondo animado y el ciclo día/noche.** La parte más larga. Del fondo fijo pasamos a capas, sol y luna, y a las tres iluminaciones.
5. **Pantalla de bloqueo, barra superior mínima y modo demo.**
6. **El paquete instalable**, probado en un usuario vacío antes de darlo por bueno.

Lo que más me ayudó fue **iterar con capturas reales del escritorio** en cada paso. Casi todos los fallos se vieron mirando el resultado, no leyendo código. Algunos ejemplos reales:

- Un reloj que pisaba la fecha y un widget que se salía de su caja.
- Una fuente bonita pero ilegible (la sustituí por Departure Mono).
- **Los nombres de los iconos del escritorio no se leían** sobre las flores claras del cerezo, sobre todo de día. Plasma los pinta en blanco fijo y no se puede cambiar, así que la solución fue oscurecer con un velo muy suave esa esquina del fondo.
- **El panel se veía diminuto** en mi monitor de sobremesa (2560×1440), porque lo había diseñado en el portátil. Ahora se escala con la altura de la pantalla: en el monitor lo comprobé con capturas, y en el portátil, donde se diseñó, el factor sale 1,0 y queda como estaba.

Dos detalles de método. Para que las capturas no enseñaran mis ventanas, creé un escritorio virtual vacío, saqué la foto ahí y lo borré. Y para el artículo añadí un **modo demo** que sustituye mi red, mis IP y mi VPN por datos ficticios: las capturas que ves llevan eso.

Mi conclusión: una IA acelera mucho el trabajo, pero el gusto, las decisiones y la comprobación siguen siendo tuyos. Sin ellos, el resultado se nota.

## Lo que no hace

- La luna sale siempre llena, con un arco decorativo; no usa la fase real.
- Solo lo he probado en **Plasma 6.8 con Wayland**, en dos pantallas: **1920×1200 al 125 %** y **2560×1440 al 100 %**. El fondo se recorta para llenar cualquier proporción y el HUD se escala con la altura, pero en pantallas muy pequeñas o ultraanchas no lo he probado.
- Las aplicaciones externas de la bandeja del sistema no las controla el tema.
- Es un proyecto personal: úsalo, rómpelo y mejóralo.

## Instalarlo

Necesitas **KDE Plasma 6** (el fondo animado y el panel de datos son componentes de Plasma) y tener `python3`, `qdbus6` y `kwriteconfig6` (si falta algo, el instalador te lo dice).

**Dos clics:** descarga el paquete, descomprímelo, haz **doble clic en «Instalar PixelZen»** y pulsa *Instalar*. Se encarga de todo y te avisa al terminar.

{{< captura src="instalar.gif" alt="Animación en cinco pasos: descargar el paquete, extraerlo, doble clic en Instalar PixelZen, pulsar Instalar y ver el escritorio recargado" caption="Instalación en cinco pasos (esquema ilustrativo; los textos de tu sistema pueden variar un poco)" >}}

**O desde la terminal:**

```bash
tar xzf pixelzen-1.0.tar.gz && cd pixelzen-1.0
./instalar.sh                                  # usa tu zona horaria para calcular el sol
./instalar.sh --casa=39.5,-0.4,"Mi ciudad"     # o fija tu ubicación
```

Solo toca tu usuario (**nada de `sudo`**) y antes de cambiar nada guarda una copia de tus ajustes. Si no detecta Plasma 6, te lo dice y no toca nada. Para volver atrás: `~/.local/share/pixelzen/revertir.sh`. Para quitarlo del todo: `desinstalar.sh`.

### Desinstalarlo

Desinstalar sí se hace desde una terminal, con un solo comando:

```bash
~/.local/share/pixelzen/desinstalar.sh          # vuelve a tus ajustes de antes y borra los temas instalados
~/.local/share/pixelzen/desinstalar.sh --todo   # además borra la carpeta de PixelZen y su configuración
```

{{< captura src="desinstalar.gif" alt="Animación en tres pasos: abrir una terminal, ejecutar desinstalar.sh y ver el escritorio restaurado" caption="Desinstalación en tres pasos (esquema ilustrativo)" >}}

Si solo quieres volver a tus ajustes sin borrar nada, usa `revertir.sh` en lugar de `desinstalar.sh`.

### ¿Y si no uso Plasma?

El tema completo no funcionará, pero algunas piezas son estándar. Con `./instalar.sh --portable` se instalan solo los **iconos, el cursor y las fuentes**, y luego los eliges en los ajustes de tu escritorio. Es experimental: no lo he probado fuera de Plasma.

## Descarga y licencia

**[pixelzen-1.0.tar.gz](https://github.com/mosqui1988/pixelzen/releases/download/v1.0/pixelzen-1.0.tar.gz)** (1 MB)

Código fuente, README con capturas y el sitio para abrir *issues*: **[github.com/mosqui1988/pixelzen](https://github.com/mosqui1988/pixelzen)**

SHA-256: `d11705d136cf5e91ca4bc23061971ad66b7fe0ab895d3a112123022c729d89ba`

Código y arte: GPL-3.0-or-later. Fuentes (Departure Mono, Pixelify Sans, DotGothic16, VT323): SIL OFL 1.1. Glifos de iconos: Pixelarticons, MIT. Los textos de las licencias van dentro del paquete.

Si lo pruebas y algo se rompe, cuéntamelo (lo más cómodo es abrir un *issue* en el repositorio).
