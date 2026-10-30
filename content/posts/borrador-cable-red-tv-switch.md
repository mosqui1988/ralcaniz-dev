---
title: "Le quité la antena a la tele (y acabé diagnosticando un switch, un cable y dos gatas sospechosas)"
date: 2026-08-11T10:00:00+02:00
draft: false
slug: "cable-red-tv-switch"
aliases: ["/posts/borrador-cable-red-tv-switch/"]
tags: ["redes", "hardware", "diagnóstico", "hogar"]
description: "Quité la antena de la tele para pasar un cable de red por el mismo conducto y acabé aislando variables hasta dar con el culpable real: un switch, no el cable."
---

Todo empezó por un problema de espacio: quería pasar un cable de red hasta la tele del salón, y el conducto de la pared solo tenía sitio para un cable. Ya había uno allí dentro, el de la antena. No era la primera vez que lo intentaba: meses atrás ya había probado con una guía, y el cable se atascaba a mitad de camino sin manera de pasarlo, ni con jabón. Lo dejé aparcado.

Esta vez tomé la decisión de forma definitiva: fuera la antena, dentro el cable de red. (Convencer a mi pareja de que era buena idea ha sido, de largo, la parte más complicada de todo esto.)

Empujé el cable nuevo enganchándolo al viejo de la antena para que hiciera de guía, y esta vez salió sin apenas resistencia. Un alivio. Al tratarse de sustituir un cable por otro que ya tenía el camino abierto, no hizo falta arrastrar nada desde cero.

## Sin puertos libres en el nodo del salón

Llegué al mueble del salón a conectar el cable nuevo y me encontré con que el nodo de la red mesh (el Halo, que reparte la señal wifi por toda la casa) solo tiene tres puertos Ethernet, y los tres estaban ocupados: el router, el cable que conecta con el otro nodo de la casa, y el servidor casero. Cero puertos libres para la tele.

La solución técnica es sencilla: un switch, un pequeño concentrador que multiplica los puertos de red disponibles a partir de uno solo. Compré uno de 5 puertos (un Tenda SG105), lo conecté al puerto que antes ocupaba el servidor, y desde ahí repartí tanto el servidor como la tele.

Aproveché también para sustituir la regleta eléctrica de la zona, que ya estaba saturada de cargadores.

## Crimpar un cable RJ45 después de años sin hacerlo

El cable que había pasado hasta la tele no traía conector, así que tocaba crimparlo yo mismo: pelar la funda exterior, ordenar los ocho hilos internos según el estándar de colores T568B, insertarlos en un conector RJ45 y fijarlo con una crimpadora. Ya había hecho esto antes en algún momento de mi vida, pero hacía tanto tiempo que fui bastante más de memoria que de práctica reciente.

Terminado el cable, probé la tele: los canales vía aplicaciones de streaming y el resto de contenido normal funcionaban sin ningún problema. Cable dado por bueno.

## "Conexión inestable": el primer misterio

El problema apareció al probar streaming de juegos desde el PC de la habitación hacia la tele del salón (Moonlight, para quien conozca la herramienta). La tele mostraba de forma repetida un aviso de conexión inestable, algo que no se había insinuado en ningún momento con el uso normal de aplicaciones.

Sospeché de varias cosas antes de mirar lo evidente: la configuración de códec de vídeo, ajustes de resolución y bitrate, un posible fallo puntual del switch. Ninguna de esas pistas terminaba de explicar por completo lo que estaba pasando.

La primera pista sólida llegó con una comparativa simple: un test de velocidad de la conexión con la tele por cable, y el mismo test por wifi. El resultado por cable fue notablemente peor que por wifi, algo que no debería ocurrir nunca en una instalación correcta: un cable de red bien hecho debe rendir igual o mejor que el wifi, no la mitad.

Asumí que el cable que había crimpado no estaba bien hecho, a pesar de que a simple vista pareciera funcionar con normalidad para usos poco exigentes. Lo recrimpé con más cuidado, prestando especial atención a que los ocho hilos llegaran hasta el fondo del conector, y el resultado del test de velocidad no cambió en absoluto.

## Una hipótesis paralela: las gatas

Antes de seguir con el diagnóstico técnico, merece la pena contar un detalle que no es tan técnico. El cable estuvo un tiempo guardado en una bolsa detrás de la tele, a la espera de que me decidiera a instalarlo definitivamente. En esa misma casa conviven dos gatas con acceso libre a cualquier bolsa susceptible de contener algo mordisqueable. Al revisar el cable de cerca aparecieron marcas compatibles con mordiscos.

No tengo forma de confirmar si el origen de esas marcas fue felino o simplemente desgaste del propio cable, así que la hipótesis quedó abierta sin descartarla del todo. Spoiler: al final resultó ser irrelevante para el desenlace, pero se quedan en la lista de sospechosas por si acaso.

## Aislando la variable real: el switch, no el cable

El punto de inflexión llegó al conectar la tele directamente al nodo de red o al router, sin pasar por el switch. En ambos casos, la velocidad se acercó al máximo real esperable para ese puerto, en torno a 94-95 Mbps. El mismo cable, sin intermediarios, funcionaba perfectamente.

Para confirmar si el switch en sí tenía un problema generalizado, hice una prueba de transferencia de datos en red local (con la herramienta iperf3) entre el PC y el servidor casero, que también cuelga del mismo switch. El resultado fue el máximo real esperable en una red Gigabit, sin ninguna pérdida.

La conclusión quedó clara: el switch Tenda funcionaba correctamente con dispositivos que negocian velocidad Gigabit, pero introducía una pérdida notable de rendimiento específicamente con la tele. Investigando un poco más, resultó que muchas Smart TV, incluida la mía, incorporan de fábrica un puerto Ethernet limitado a 100 Mbps en lugar de Gigabit completo, un dato que ningún fabricante suele destacar en sus fichas comerciales ni manuales de usuario. Revisé el manual oficial completo de LG (veinte páginas) y la única mención al puerto LAN es una recomendación genérica de usar cable Cat 7, sin especificar en ningún momento la velocidad real. Escribí directamente al soporte técnico de LG para preguntarlo; a la espera de respuesta.

Esa limitación de fábrica explicaba el techo real de velocidad de la tele por cable, tanto conectada directa como a través del switch. Lo que no explicaba era la caída adicional de rendimiento específica al pasar por el switch: un switch Gigabit correctamente fabricado debería negociar sin pérdidas con un dispositivo de 100 Mbps con la misma fiabilidad con la que lo hace con uno de Gigabit completo.

## El veredicto final

Decidí devolver el switch Tenda y sustituirlo por un modelo gestionado, un NETGEAR GS305E, con la ventaja añadida de poder consultar desde su propio panel de administración la velocidad negociada de cada puerto, sin depender de tests indirectos.

El panel confirmó exactamente lo que sospechaba: el puerto de la tele negocia a 100 Mbps de forma limpia, sin errores. La diferencia con el switch anterior fue inmediata. Repetí el test de velocidad con la tele conectada al nuevo switch y el resultado subió de los 50-70 Mbps que daba con el Tenda a cerca de 84-91 Mbps, en línea con el máximo real del puerto de la tele.

La prueba definitiva llegó al volver a lanzar Moonlight. Donde antes la tele mostraba "conexión inestable" y 0 fotogramas por segundo, el panel de rendimiento mostró esta vez 59,88 FPS de red, 0,00 % de pérdida de fotogramas, una latencia de red de 4 milisegundos y tiempos de decodificación y procesamiento bajos y estables.

Conclusión completa del caso: el cable nunca fue el problema, ni el primero ni el segundo crimpado, ambos confirmados con un comprobador de continuidad. El puerto Ethernet de la tele está limitado a 100 Mbps de fábrica, algo que ningún documento oficial confirma pero que ahora tengo comprobado con datos directos del propio switch. Y el switch original tenía un problema real de negociación con ese tipo de dispositivo, resuelto por completo al sustituirlo por un modelo gestionado de mejor calidad.

Las gatas, de momento, siguen sin cargos.

## Lo que me llevo de todo esto

Más allá del switch culpable, esta ha sido una buena lección de cómo diagnosticar un problema técnico de verdad: no asumir la primera explicación que parece encajar, sino ir aislando variables una a una hasta que los datos no dejen sitio a la duda. Cambié de sospechoso varias veces (el cable, el códec, la crimpadora, el propio puerto de la tele), y cada vez que descarté uno fue gracias a una prueba concreta, no a una intuición. Ese orden es el que al final marca la diferencia entre "creo que ya funciona" y "sé por qué funciona".

También me llevo la confirmación de algo que ya sospechaba: la ficha técnica de un producto casi nunca cuenta toda la historia. Ni el fabricante de la tele ni el de mi primer switch avisan de sus propias limitaciones, y esa información solo aparece cuando la mides tú mismo, con las herramientas adecuadas.

Y, sobre todo, esto es exactamente el porqué de este blog: vengo de la carretera y la logística, con una base técnica de otra época que ahora estoy retomando, y cada uno de estos líos (el cable atascado, las pruebas fallidas, el switch que hubo que devolver) es una clase que nadie me va a dar en un curso, pero que me llevo puesta de por vida en cuanto la resuelvo con mis propias manos. Se aprende mucho más tropezando con un problema real que leyendo cómo se resuelve en la teoría.
