---
title: "Casi mando a RMA una CPU sana (y las culpables eran mis gatas)"
date: 2026-07-26T18:14:00+02:00
draft: false
---

Ayer apagué la Torre normal. Hoy la he encendido y no arrancaba. Así de tonto empieza esto.

## El síntoma raro

Ventiladores girando sin parar, luces encendidas sin parar, pantalla negra. Ni logo, ni BIOS, nada. El botón de encendido parpadeaba a ciclos de 4-5 segundos, y durante un buen rato creí que era la propia torre la que estaba reiniciándose sola en bucle. No era así: ventiladores y luces se mantenían continuos todo el rato, sin interrumpirse ni un segundo. El único que parpadeaba era el LED del botón. Un matiz que me despistó bastante y que merece la pena aclarar, porque cambia el diagnóstico.

Como llevaba unos días pensando en ampliar RAM, mi primera sospecha fue de libro: "algo le pasa a la memoria". Así que quité un módulo, a ver si arrancaba con uno solo.

Y arrancó. Con un único módulo de 16GB en su ranura, el PC iba. Pensando que ya estaba resuelto, volví a montar el segundo módulo — y ahí es donde todo se torció de verdad: dejó de arrancar por completo, y ya no volvió a hacerlo ni con uno ni con el otro, en ninguna ranura. Ese fue el punto en el que decidí abrirlo todo: quitar piezas, limpiar, soplar el polvo, ir aislando variables una por una. Lo raro, y sigue siéndolo ahora que ya sé que todo funciona: ¿por qué un solo módulo sí arrancaba al principio, y después ni ese mismo módulo solo conseguía arrancar?

## Lo que fui descartando (por orden, y con bastante sudor)

Un detalle importante para todo lo que viene: no tengo ni un solo repuesto en casa. Ni otro módulo de RAM que no sea de este PC, ni otra placa, ni pasta térmica de sobra. Cada prueba tocaba hacerla con las piezas que ya tenía puestas, sin nada externo con lo que comparar. Eso limita mucho el diagnóstico casero, y es la razón por la que he acabado pidiendo pasta térmica nueva para mañana: ni siquiera tenía eso a mano cuando hizo falta desmontar el disipador.

**Reset de BIOS (Load Optimized Defaults).** Por si algún ajuste de la memoria estuviera dando problemas — en concreto el XMP, el perfil que hace que la RAM vaya a su velocidad "buena" de fábrica en vez de a la mínima garantizada. Nada.

**Clear CMOS.** El equivalente a "apaga y enciende" pero para la placa base entera: borra toda la configuración guardada y la deja de fábrica. Tuve que buscar el jumper `CLRTC` a tientas entre cables, con el móvil en modo macro, porque en mi placa la pila queda debajo de la gráfica y sacarla para esto habría sido un lío innecesario. Tampoco arrancó.

**La gráfica.** La saqué entera de la torre. Mismo comportamiento: luces y ventiladores continuos, sin imagen.

**El conector de alimentación de la CPU (EPS, 8 pines).** Lo desmonté y lo volví a montar por si se había aflojado al meter la mano cerca durante todo el trasteo. Nada.

Y aquí es donde el diagnóstico se puso realmente cuesta arriba: el comportamiento era idéntico con RAM puesta que sin ninguna RAM en absoluto. Mismo parpadeo del botón, misma falta de imagen, sin diferencia visible entre un escenario y otro. Eso, en su momento, no me daba ninguna pista clara sobre dónde estaba el fallo — podía ser tanto la memoria como cualquier otra cosa previa a que la placa llegara siquiera a comprobar si había RAM instalada.

## La sospecha que casi me hace tirar la CPU a la basura (mentalmente)

El controlador que gestiona la memoria no vive en la placa: vive dentro del propio procesador. Y resulta que los Intel de 13ª y 14ª generación —el mío es un i7-14700KF, comprado nuevo pero ya montado por un chico en Wallapop que hacía equipos a buen precio, sin caja ni factura del procesador en sí— tienen un problema real y reconocido de degradación por voltaje inestable. Uno de los síntomas descritos: empieza a fallar justo la inicialización de memoria.

Encajaba de forma casi sospechosa. Ya estaba mirando precios de CPUs nuevas y planteándome si merecía la pena pasarme a una plataforma DDR4 para ahorrar en RAM (spoiler: no, la DDR4 también está por las nubes por la crisis de suministro que hay ahora mismo por la demanda de memoria para IA).

Pero antes de gastar nada, algo no me cuadraba: **al principio de todo, con un módulo en la primera ranura, sí había arrancado.** Un controlador de memoria realmente muerto no deja arrancar nunca, ni una vez. Así que la CPU quedó en el banquillo de sospechosos, pero ya no como principal.

## Desmontar la CPU (sin perder los nervios)

Saqué el procesador del socket para mirar si tenía algún pin doblado. No vi nada raro. Lo volví a montar, con cuidado de que el marco de retención cerrara bien.

Y aquí viene el giro: probé un módulo en una ranura del **canal B** que no había tocado en todo el día.

Arrancó.

## `dmidecode` no miente

Con el sistema ya arrancado, comprobé qué veía Linux exactamente:

```
free -h
sudo dmidecode -t memory | grep -E "Locator|Size|Speed"
```

Los dos módulos, uno en cada canal, reconocidos y en dual channel. 31 GiB disponibles. El PC funcionando otra vez, varias horas después de la primera pantalla negra.

## Entonces, ¿qué falló de verdad?

Aquí tengo que ser honesto: no lo sé con certeza al cien por cien. Pero el candidato más probable no es tan técnico como toda la investigación de RMAs y garantías de Intel que hice por el camino.

Tengo dos gatas, y suelen usar la torre como escalón habitual para subir a una balda de la habitación — de hecho tuve que reforzar esa balda hace poco porque ya se la estaban cargando de tanto uso. Es decir, ya tenía pruebas de que estas dos hacían ejercicio de escalada sobre mi hardware y aun así no até cabos hasta la tarde. No fue nada que pasara mientras la torre estaba abierta hoy: es una rutina suya de siempre, con la torre cerrada, ajenas por completo al drama que estaban gestando ahí dentro.

Y aquí va lo mejor: mientras yo perdía la tarde leyendo sobre voltajes inestables, controladores de memoria y garantías extendidas de Intel, las presuntas culpables estaban durmiendo la siesta a dos metros de la torre, con esa cara de absoluta inocencia que solo un gato sabe poner cuando ha hecho algo. Es bastante probable que, de tanto salto acumulado a lo largo de meses, un módulo de RAM se desplazara lo justo para dejar de hacer contacto perfecto — sin que nadie lo notara hasta que la placa no consiguió completar el arranque. Ningún fallo de fábrica, ningún chip degradado: cuatro patas y un salto mal calculado.

Sobre la duda de por qué un módulo que sí había arrancado solo, dejó de hacerlo después de volver a montar el segundo: mi mejor hipótesis es que al manipular el segundo módulo — sacarlo, guardarlo, volver a meterlo — también rocé o desplacé algo del primero, que hasta ese momento estaba bien asentado por pura suerte. No es una explicación cerrada del todo, pero encaja con que el fallo apareciera justo en ese momento y no antes.

## El aprendizaje real de hoy

Antes de sospechar de la pieza más cara y menos accesible (la CPU), toca agotar primero lo barato y lo físico: reasentar, comprobar ranuras que no habías probado todavía, y no dar una pieza por "descartada" solo porque falló una vez en una posición concreta. Y sin herramientas ni repuestos en casa, cada paso cuesta más tiempo del que debería — hoy me ha faltado hasta pasta térmica cuando ha tocado desmontar el disipador.

Aproveché para hacer una prueba de temperatura con carga completa antes de cambiar esa pasta, que me llega mañana:

```
stress-ng --cpu 0 --timeout 600s
watch -n 1 sensors
```

Resultado de hoy, sin pasta nueva: **~80-81°C sostenidos**, ventiladores llegando a saturarse. Mañana repito la misma prueba tras cambiar la pasta, para comparar cifra contra cifra y ver si de verdad estaba perdiendo grados por ahí.

## Lo que me llevo

- Un PC funcionando en dual channel, que es mejor de lo que tenía a media mañana cuando solo conseguía arrancar con un módulo suelto.
- La confirmación de que el i7-14700KF sigue sano.
- Una lista de tareas para cuando llegue la pasta térmica nueva: limpiar bien el radiador (con dos gatas, hay más pelo del que parece), aplicar pasta fresca, y volver a comprobar temperaturas.
- Un pequeño kit básico de herramientas y repuestos pendiente de montar, para no volver a diagnosticar a ciegas la próxima vez.
- Y la certeza, dolorosamente adquirida, de que en esta casa el departamento de control de calidad tiene bigotes y no responde ante nadie.

Mañana toca pasta térmica y, si todo va bien, unos días de estabilidad antes de reactivar XMP y recuperar la velocidad completa de la RAM.
