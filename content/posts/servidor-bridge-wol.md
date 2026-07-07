---
title: "Le di vida a un PC de hace once años para poder encender el otro desde el sofá (o desde el fin del mundo)"
date: 2026-07-07T03:00:00
draft: false
description: "Cómo fui, paso a paso, montando un pequeño servidor casero para poder encender mi PC principal estando fuera de casa. Con tropiezos, un experimento que no salió, y bastante vocabulario nuevo explicado sobre la marcha."
---

Anoche, pasada la medianoche, estaba tumbado en el sofá con el móvil en la mano. Había apagado el WiFi a propósito y activado los datos móviles, porque quería hacer la prueba de verdad, no una versión facilona con trampa. Escribí un comando, pulsé Enter, y esperé.

Al otro lado de la casa, mi PC principal —al que llamo cariñosamente "la Torre"— se encendió solo. Sin que yo lo tocara. Sin estar conectado a la misma red WiFi de casa. Solo un mensaje que viajó desde mi móvil, salió a internet, encontró el camino de vuelta hasta mi casa, y despertó al ordenador como si le hubiera dado al botón físico yo mismo.

Ese momento es la meta de todo lo que os voy a contar en este post. Pero para llegar hasta ahí hicieron falta varios días de trabajo, un cacharro comprado de segunda mano por 45 euros, y algún que otro tropiezo que casi me hace tirar la toalla.

## ¿Por qué quería esto?

La idea de partida era sencilla de explicar, aunque no tanto de conseguir: yo tengo mi PC principal en casa, apagado la mayoría del tiempo para no gastar luz de más. El problema es que a veces, estando fuera de casa, me acuerdo de que necesito algo que solo tengo en ese ordenador, o simplemente me apetece trabajar en él desde otro sitio. Y claro, si está apagado, no hay manera.

La solución existe y tiene nombre: **Wake-on-LAN** (a veces abreviado como WoL). Es una función que llevan casi todas las tarjetas de red desde hace años, y que permite encender un ordenador apagado mandándole un mensaje especial por la red, llamado "paquete mágico". El propio ordenador, aunque esté apagado del todo, deja un poquito de energía reservada solo para escuchar si llega ese mensaje concreto — y si llega, se enciende él solo.

El problema es que ese "paquete mágico" solo puede viajar dentro de tu propia red de casa. No sirve de nada mandarlo desde el móvil con datos si estás en la calle, porque el mensaje simplemente no sabe cómo llegar hasta tu router desde fuera. Necesitaba algo intermedio: un segundo ordenador, siempre encendido, que viviera dentro de mi red de casa, y al que yo sí pudiera acceder desde cualquier sitio del mundo. Ese ordenador recibiría mi orden desde fuera, y él, que sí está dentro de la red local, se encargaría de mandar el paquete mágico a la Torre.

A ese segundo ordenador, en mi cabeza, empecé a llamarlo "el server" — que hace de puente entre mi móvil, fuera de casa, y mi PC principal, dentro de casa.

## Buscando el cacharro adecuado

Antes de nada necesitaba un ordenador barato, pequeño, y que pudiera estar encendido todo el día sin gastar mucha luz — porque su único trabajo iba a ser estar ahí, esperando. Le pregunté a Claude qué opciones tenía sentido valorar, y estuvimos días descartando cosas: una Raspberry Pi (un ordenador diminuto muy popular para estos proyectos) se quedaba corta de memoria y precios por las nubes, varios mini PCs de tiendas raras olían a estafa, un móvil viejo que tengo con la pantalla rota no daba para tanto...

Al final encontré, de segunda mano y en persona (nada de comprar a ciegas por internet), un **Lenovo ThinkCentre**: un mini PC de oficina de hace once años, con un procesador Intel i5 de una generación ya antigua pero perfectamente capaz para esta tarea, 4 GB de memoria RAM y un disco duro mecánico de 500 GB. Precio: 45 euros. Encendió delante de mí antes de pagarlo, así que sin sorpresas.

## Instalando el sistema operativo: primeros tropiezos

Le pregunté a Claude qué sistema operativo instalar en este mini PC, y me recomendó **Debian**, una de las distribuciones (versiones) de Linux más estables y usadas para servidores, precisamente por ser sencilla y fiable.

Aquí viene el primer concepto nuevo importante: iba a instalarlo en modo **headless**, que significa "sin cabeza" en inglés, y en la práctica quiere decir sin interfaz gráfica — nada de escritorio con iconos y ventanas, solo una pantalla negra con texto (una terminal). Suena intimidante, pero tiene su lógica: este ordenador va a vivir escondido junto al router, sin monitor ni teclado conectados casi nunca, así que no tiene sentido gastar recursos en algo bonito que nadie va a ver.

Durante la instalación me encontré varias cosas raras que Claude me fue explicando sobre la marcha:

**Los pitidos de la BIOS.** La BIOS es un programita muy básico que vive dentro de la placa base del ordenador y se encarga de arrancar todo antes incluso de que empiece a cargar el sistema operativo. Al encender el Lenovo por primera vez en su sitio definitivo, escuché dos pitidos raros y me temí lo peor — en algunas placas, dos pitidos indican un fallo de la memoria RAM. Al final resultó ser una falsa alarma: solo era el cable de red, que no había hecho bien contacto al cambiar el ordenador de sitio.


**Las zonas horarias de Estados Unidos.** En un momento del instalador, sin darme cuenta, elegí sin querer una configuración que asumía que vivo en Estados Unidos, y de repente me tocaba elegir entre zonas horarias de ciudades americanas. Aprendí que el instalador separa "idioma" (qué idioma habla el sistema) de "región/locale" (de qué país eres, para cosas como la zona horaria o el formato de fecha), y que hay que prestar atención a las dos por separado, no solo a la primera pantalla.

**`sudo: command not found`.** Este me hizo reír una vez resuelto. `sudo` es un comando muy famoso en Linux que te permite ejecutar acciones como si fueras el administrador del sistema (llamado "root", el usuario con permiso para todo) sin tener que iniciar sesión directamente como él. Pues resulta que, al elegir la instalación más mínima posible, ni siquiera `sudo` viene instalado por defecto. Tuve que iniciar sesión directamente como `root` para poder instalar las cosas básicas — algo que hay que hacer con cuidado, porque como root puedes romper cualquier cosa del sistema sin que nadie te pregunte "¿estás seguro?".

## El problema del internet que no encontraba nombres

Una vez instalado, configuré la dirección de red del servidor para que fuera siempre la misma (una **IP fija**, en vez de una que cambia cada vez que se reinicia, que es lo normal por defecto). También configuré qué servidores debía usar para resolver nombres de dominio — esto se llama **DNS**, y es básicamente la libreta de contactos de internet: tú escribes "google.com" y el DNS te dice la dirección numérica real de ese servidor, para que tu ordenador sepa a dónde conectarse.

El problema: el ping a una dirección numérica directa funcionaba perfecto, pero en cuanto intentaba resolver un nombre de dominio normal, nada. Silencio total.

Claude me ayudó a diagnosticarlo mirando un archivo del sistema donde se guarda la configuración de DNS real, y estaba completamente vacío, a pesar de que yo lo había configurado bien en otro sitio. La explicación: Debian, con el sistema de redes que usa por defecto, necesita un paquete adicional (llamado `resolvconf`) para que la configuración que escribes en un lado llegue de verdad al archivo que el sistema consulta de verdad. Sin ese paquete, es como escribir una carta y no echarla al buzón — se queda ahí, sin que nadie la reciba. Lo arreglamos escribiendo el archivo a mano directamente, mientras dejábamos anotado instalar ese paquete para que no vuelva a pasar en el futuro.

## Metiendo el servidor en mi red privada

Con el servidor limpio, actualizado, y con internet funcionando de verdad, tocaba el siguiente paso: meterlo en mi **Tailscale**. Esto ya lo tenía montado desde hace tiempo para otras cosas (acceder a mi PC principal desde el móvil, hacer streaming de juegos), así que aquí no hubo sorpresas.

Tailscale es lo que se llama una **VPN** (red privada virtual): crea una especie de red invisible entre todos mis dispositivos (el móvil, la Torre, y ahora también este nuevo servidor), sin importar en qué red física esté cada uno conectado en cada momento. Es como si todos mis aparatos estuvieran siempre en la misma habitación, aunque en realidad uno esté en casa y otro en la calle con datos móviles. Y lo mejor: nadie de fuera puede ver ni tocar esa red, solo mis propios dispositivos autorizados.

Instalar Tailscale en el nuevo servidor fue, comparado con todo lo anterior, un trámite rápido: un comando, autenticarme desde el navegador del móvil, y listo. El servidor pasó a tener su propia dirección dentro de mi red privada, accesible desde cualquier parte del mundo.

## El experimento que probé, y que decidí aparcar

Aquí toca ser sincero, porque este blog cuenta lo que pasa de verdad, no solo lo que sale bien a la primera.

Antes de centrarme solo en el Wake-on-LAN, quise aprovechar este servidor para algo más: instalar **Pi-hole**, un programa que bloquea anuncios y rastreadores para toda mi red de casa a la vez, actuando también como ese "DNS" del que hablaba antes, pero uno que filtra la publicidad antes de que llegue a cualquier dispositivo.

Para instalarlo usé **Docker**, que es una herramienta que permite meter un programa entero, con todo lo que necesita para funcionar, dentro de una especie de "caja" aislada (llamada contenedor), sin que interfiera con el resto del sistema. Claude me fue explicando cada parte del comando de instalación: qué puertos abrir, para qué servía cada opción.

Costó un poco arrancarlo bien (Pi-hole tiene una protección de seguridad que al principio rechazaba las consultas de mi propia red, hasta que descubrimos que había que cambiar el modo de red del contenedor), pero al final funcionó de verdad: probé a preguntarle por un dominio conocido de publicidad, y en vez de darme la dirección real, me devolvió una dirección "nula", señal de que lo estaba bloqueando correctamente.

El problema llegó cuando configuré Pi-hole para que repartiera las direcciones de red de toda la casa (algo llamado **DHCP**, el sistema que le asigna automáticamente una dirección a cada móvil, tablet u ordenador que se conecta a tu WiFi). Mi pareja, desde la habitación de al lado, notó que las páginas con mucha publicidad le cargaban más lentas de lo normal.

Investigando con Claude, la explicación tuvo sentido: el disco duro de este mini PC es mecánico (con piezas físicas que giran), no de los modernos sin partes móviles. Cada vez que alguien navega, Pi-hole tiene que anotar esa consulta en una base de datos, y eso implica escribir en el disco. Con un solo dispositivo (el mío) no se nota nada. Con dos o tres a la vez, ese disco de once años empieza a notarse.

Decidí desinstalarlo sin darle más vueltas. No era la solución adecuada para *este* disco duro concreto, aunque técnicamente funcionara. Dejé la configuración guardada por si algún día cambio el disco mecánico por uno de estado sólido (mucho más rápido), y seguí adelante. A veces la opción más completa no es la correcta para el momento, y está bien reconocerlo sin sentir que el tiempo invertido se ha perdido — al final aprendí cómo funciona Docker, qué es un DNS filtrador, y por qué el hardware antiguo importa más de lo que parece a simple vista.

## Por fin, el Wake-on-LAN de verdad

Con el servidor limpio otra vez, solo quedaba instalar una pequeña herramienta (llamada `wakeonlan`) que sabe construir y enviar ese "paquete mágico" del que hablaba al principio. Necesitaba solo un dato: la **dirección MAC** de mi PC principal, que es como el número de identificación único y de fábrica de la tarjeta de red de cualquier ordenador (a diferencia de la IP, que puede cambiar, la MAC es siempre la misma).

Primera prueba, dentro de casa, con la Torre apagada: funcionó a la primera. Segunda prueba, la de verdad: WiFi del móvil apagado, datos móviles activados, conexión por **SSH** (una forma segura y cifrada de controlar otro ordenador a distancia, escribiendo comandos como si estuvieras sentado delante de él) hacia mi nuevo servidor a través de Tailscale, y un solo comando.

La Torre se encendió. Ese es el momento que os contaba al principio del post.

## Lo que viene después

De momento me quedo aquí: poder encender el PC y controlarlo por SSH desde cualquier sitio. No es el final del camino — es solo el primer escalón de algo más grande que quiero ir construyendo poco a poco, con más tropiezos que contar seguramente, que es al final como de verdad se aprende todo esto.

Todo este proceso lo he hecho apoyándome en Claude en cada paso: no para que hiciera el trabajo por mí, sino para que me explicara qué era cada cosa la primera vez que me la encontraba, por qué fallaba algo, y qué alternativas tenía antes de decidir. Las decisiones —qué comprar, cuándo parar con Pi-hole, qué construir después— siguen siendo mías. Pero tener a alguien al lado que te traduce el "por qué" detrás de cada error, en vez de darte solo la solución sin más, es la diferencia entre copiar comandos a ciegas y entender de verdad lo que estás construyendo.

De reparto, a root, a un pequeño servidor que ahora vive junto al router de casa, esperando pacientemente la próxima orden que le mande desde donde sea.
