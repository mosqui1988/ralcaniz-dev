---
title: "Me he montado mi propio servidor de streaming: ahora puedo jugar en mi PC de casa desde cualquier sitio"
date: 2026-07-07T19:00:00
draft: false
description: "Cómo terminé de cerrar el círculo del proyecto del servidor casero: no solo encender el PC en remoto, sino también jugar en él desde una red completamente distinta a la de casa, usando el mando de mi ROG Ally."
---

Hay historias que empiezan con un objetivo modesto y terminan en un sitio que ni te habías planteado al arrancar. Esta es una de ellas.

Todo empezó con una idea sencilla: quería poder encender mi PC principal (la "Torre") estando fuera de casa, y poder entrar por terminal a hacer lo que necesitara. Ese objetivo ya quedó cumplido y contado en el post anterior. Pero mientras montaba esa pieza, se me quedó rondando una pregunta más ambiciosa: si ya puedo encenderlo desde cualquier sitio... ¿podría también jugar en él desde cualquier sitio?

La respuesta corta es sí. La respuesta larga tiene su recorrido, así que vamos con ella.

## El plan, en una frase

Quería poder llevarme mi ROG Ally (un handheld de gaming con forma de Nintendo Switch grande, con Linux instalado en vez del Windows de fábrica) a casa de un amigo, o a cualquier sitio con WiFi, y desde ahí encender mi Torre y jugar a mis juegos de PC como si estuviera sentado delante de ella, usando el propio streaming de vídeo hacia la pantalla de la Ally.

Esto de "jugar en un ordenador que está en otro sitio, viendo la imagen en tu pantalla en tiempo real" se llama **streaming de juegos**, y llevaba tiempo funcionando ya dentro de mi propia casa: mi Torre corre un programa llamado **Sunshine**, que capta lo que pasa en la pantalla y lo manda por la red a otro dispositivo, donde otro programa llamado **Moonlight** lo recibe y lo muestra. Es la misma tecnología, en esencia, que usan servicios como Xbox Cloud Gaming o GeForce Now, solo que aquí el "servidor en la nube" soy yo mismo, desde mi salón.

El problema era que, hasta ahora, esto solo funcionaba si la Ally estaba conectada a la misma red WiFi de casa que la Torre. En cuanto salías de casa, se acababa la magia.

## La pieza que faltaba: meter la Ally en mi red privada

Ya tenía montada, desde hace tiempo, una **VPN** (red privada virtual) con **Tailscale** — una tecnología que conecta todos mis dispositivos entre sí de forma segura, sin importar en qué red física esté cada uno conectado en cada momento. Es un poco como tener un cable invisible que une mi móvil, mi Torre y mi servidor casero, aunque estén en puntos distintos del planeta.

El Lenovo que monté como servidor puente ya estaba en esa red. La Torre, también. Pero la ROG Ally, la pieza que faltaba para poder jugar en remoto, todavía no formaba parte de esa red privada — así que aunque pudiera encender la Torre desde fuera, la Ally no tenía forma de "verla" para iniciar el streaming.

Instalar Tailscale en la Ally fue, comparado con otros líos que he tenido en este proyecto, un trámite tranquilo: un comando de instalación, activar el servicio, autenticarme desde el navegador, y listo. La Ally pasó a tener su propia dirección dentro de mi red privada, igual que el resto de mis dispositivos.

## Un asunto pendiente que casi lío por las prisas

Antes de meterme de lleno en la prueba de streaming, tenía un pendiente suelto de cuando instalé Linux en la Ally: decidir entre dos programas distintos para controlar cosas específicas del hardware (la velocidad del ventilador, el consumo del procesador, y el giroscopio del mando, que es clave para mí porque juego a juegos de disparos y apuntar con el giroscopio, además del stick, mejora mucho la precisión).

Al principio pensé que tendría que cambiar de programa para conseguir esa función del giroscopio. Investigando con Claude sobre el estado real de mi sistema (no solo en teoría, sino mirando qué tenía instalado y funcionando de verdad en ese momento), resultó que el programa que ya traía instalado de fábrica el propio sistema de la Ally ya cubría el giroscopio sin ningún problema. Así que, en vez de complicarme cambiando de programa y arriesgándome a romper algo que ya funcionaba bien, decidí dejarlo tal cual estaba. A veces la mejor decisión técnica es no tocar lo que ya funciona.

## La prueba de fuego, sin salir de casa

Aquí venía el reto real: ¿cómo pruebo "estar en otra casa" sin desplazarme de verdad? La solución fue más sencilla de lo que esperaba: usé el **punto de acceso** (o "hotspot") de mi propio móvil, que convierte los datos móviles del operador en una señal WiFi que otros dispositivos pueden usar. Desconecté la Ally de mi WiFi de casa y la conecté a ese hotspot en su lugar.

Con eso, la Ally quedó en una red completamente distinta a la de mi Torre, exactamente la misma situación que si estuviera en casa de otra persona.

El proceso completo, paso a paso:

1. Con la Torre apagada, me conecté por **SSH** (una forma segura de controlar otro ordenador a distancia escribiendo comandos) al servidor puente que ya tengo montado en casa.
2. Ejecuté el comando que envía la orden de encendido remoto a la Torre.
3. Esperé a que arrancara del todo. Como tengo Sunshine configurado para arrancar solo en cuanto enciende el sistema, no tuve que hacer nada más en ese lado.
4. Desde la Ally, abrí Moonlight y añadí la Torre usando su dirección dentro de la red privada de Tailscale, en vez de la dirección de la red local de casa (que desde el hotspot del móvil no tendría ningún sentido, porque son redes distintas).
5. Le di a conectar.

Y funcionó. De verdad. La imagen de mi Torre apareció en la pantalla de la Ally, con mando en mano, exactamente igual que si hubiera estado sentado en mi salón.

## Lo que esto significa, en la práctica

Con esto, el objetivo que me planteé al principio del proyecto (encender el PC y controlarlo por terminal desde cualquier sitio) se ha quedado corto de lo que finalmente he conseguido. Ahora tengo, en la práctica, mi propio servidor de streaming de juegos personal: puedo llevarme la Ally a cualquier sitio con WiFi, encender mi Torre en remoto, y jugar a mis juegos de PC como si no me hubiera movido de casa.

Hay un matiz honesto que quiero dejar anotado, porque este blog cuenta las cosas tal como son: la calidad de ese streaming, jugando desde fuera de casa, depende de la velocidad de subida de mi conexión de casa y de la velocidad de bajada de donde esté conectado en cada momento. Jugando dentro de mi propia WiFi la experiencia es prácticamente perfecta; jugando a través de internet de verdad, es razonable esperar algo más de retardo (lo que se conoce como latencia) que estando en la misma habitación. Para partidas tranquilas, sin problema. Para algo muy competitivo online, seguramente se note. Por suerte, como no juego a nada competitivo por internet, esa limitación no me afecta en la práctica.

## Cómo he llegado hasta aquí

Todo este recorrido lo he hecho con Claude al lado en cada paso, no como quien hace el trabajo por mí, sino como quien me va explicando el porqué de cada pieza: qué es una VPN, por qué el streaming necesita que ambos extremos se encuentren en la misma red privada, por qué convenía o no cambiar de programa para el giroscopio. Las decisiones han sido mías, pero entender el fundamento de cada una es lo que hace que esto se sienta como aprendizaje real, y no como seguir una receta sin saber qué se está cocinando.

De reparto, a root, a jugar en mi propio PC desde donde me dé la gana. Quién me lo iba a decir hace un año.
