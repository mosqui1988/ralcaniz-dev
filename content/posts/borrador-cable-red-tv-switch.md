---
title: "Le quite la antena a la tele (y acabe diagnosticando un switch, un cable y dos gatas sospechosas)"
date: 2026-08-11T10:00:00+02:00
draft: false
---

Todo empezo por un problema de espacio: queria pasar un cable de red hasta la tele del salon, y el conducto de la pared solo tenia sitio para un cable. Ya habia uno alli dentro, el de la antena. No era la primera vez que lo intentaba: meses atras ya habia probado con una guia, y el cable se atascaba a mitad de camino sin manera de pasarlo, ni con jabon. Lo deje aparcado.

Esta vez tome la decision de forma definitiva: fuera la antena, dentro el cable de red. (Convencer a mi pareja de que era buena idea ha sido, de largo, la parte mas complicada de todo esto.)

Empuje el cable nuevo enganchandolo al viejo de la antena para que hiciera de guia, y esta vez salio sin apenas resistencia. Un alivio, porque tengo los antebrazos bastante castigados ultimamente y cualquier tarea que implique forzar se nota enseguida. Al tratarse de sustituir un cable por otro que ya tenia el camino abierto, no hizo falta arrastrar nada desde cero.

## Sin puertos libres en el nodo del salon

Llegue al mueble del salon a conectar el cable nuevo y me encontre con que el nodo de la red mesh (el Halo, que reparte la señal wifi por toda la casa) solo tiene tres puertos Ethernet, y los tres estaban ocupados: el router, el cable que conecta con el otro nodo de la casa, y el servidor casero. Cero puertos libres para la tele.

La solucion tecnica es sencilla: un switch, un pequeño concentrador que multiplica los puertos de red disponibles a partir de uno solo. Compre uno de 5 puertos (un Tenda SG105), lo conecte al puerto que antes ocupaba el servidor, y desde ahi reparti tanto el servidor como la tele.

Aproveche tambien para sustituir la regleta electrica de la zona, que ya estaba saturada de cargadores.

## Crimpar un cable RJ45 despues de años sin hacerlo

El cable que habia pasado hasta la tele no traia conector, asi que tocaba crimparlo yo mismo: pelar la funda exterior, ordenar los ocho hilos internos segun el estandar de colores T568B, insertarlos en un conector RJ45 y fijarlo con una crimpadora. Ya habia hecho esto antes en algun momento de mi vida, pero hacia tanto tiempo que fui bastante mas de memoria que de practica reciente.

Terminado el cable, probe la tele: los canales via aplicaciones de streaming y el resto de contenido normal funcionaban sin ningun problema. Cable dado por bueno.

## "Conexion inestable": el primer misterio

El problema aparecio al probar streaming de juegos desde el PC de la habitacion hacia la tele del salon (Moonlight, para quien conozca la herramienta). La tele mostraba de forma repetida un aviso de conexion inestable, algo que no se habia insinuado en ningun momento con el uso normal de aplicaciones.

Sospeche de varias cosas antes de mirar lo evidente: la configuracion de codec de video, ajustes de resolucion y bitrate, un posible fallo puntual del switch. Ninguna de esas pistas terminaba de explicar por completo lo que estaba pasando.

La primera pista solida llego con una comparativa simple: un test de velocidad de la conexion con la tele por cable, y el mismo test por wifi. El resultado por cable fue notablemente peor que por wifi, algo que no deberia ocurrir nunca en una instalacion correcta: un cable de red bien hecho debe rendir igual o mejor que el wifi, no la mitad.

Asumi que el cable que habia crimpado no estaba bien hecho, a pesar de que a simple vista pareciera funcionar con normalidad para usos poco exigentes. Lo recrimpe con mas cuidado, prestando especial atencion a que los ocho hilos llegaran hasta el fondo del conector, y el resultado del test de velocidad no cambio en absoluto.

## Una hipotesis paralela: las gatas

Antes de seguir con el diagnostico tecnico, merece la pena contar un detalle que no es tan tecnico. El cable estuvo un tiempo guardado en una bolsa detras de la tele, a la espera de que me decidiera a instalarlo definitivamente. En esa misma casa conviven dos gatas con acceso libre a cualquier bolsa susceptible de contener algo mordisqueable. Al revisar el cable de cerca aparecieron marcas compatibles con mordiscos.

No tengo forma de confirmar si el origen de esas marcas fue felino o simplemente desgaste del propio cable, asi que la hipotesis quedo abierta sin descartarla del todo. Spoiler: al final resulto ser irrelevante para el desenlace, pero se quedan en la lista de sospechosas por si acaso.

## Aislando la variable real: el switch, no el cable

El punto de inflexion llego al conectar la tele directamente al nodo de red o al router, sin pasar por el switch. En ambos casos, la velocidad se acerco al maximo real esperable para ese puerto, en torno a 94-95 Mbps. El mismo cable, sin intermediarios, funcionaba perfectamente.

Para confirmar si el switch en si tenia un problema generalizado, hice una prueba de transferencia de datos en red local (con la herramienta iperf3) entre el PC y el servidor casero, que tambien cuelga del mismo switch. El resultado fue el maximo real esperable en una red Gigabit, sin ninguna perdida.

La conclusion quedo clara: el switch Tenda funcionaba correctamente con dispositivos que negocian velocidad Gigabit, pero introducia una perdida notable de rendimiento especificamente con la tele. Investigando un poco mas, resulto que muchas Smart TV, incluida la mia, incorporan de fabrica un puerto Ethernet limitado a 100 Mbps en lugar de Gigabit completo, un dato que ningun fabricante suele destacar en sus fichas comerciales ni manuales de usuario. Revise el manual oficial completo de LG (veinte paginas) y la unica mencion al puerto LAN es una recomendacion generica de usar cable Cat 7, sin especificar en ningun momento la velocidad real. Escribi directamente al soporte tecnico de LG para preguntarlo; a la espera de respuesta.

Esa limitacion de fabrica explicaba el techo real de velocidad de la tele por cable, tanto conectada directa como a traves del switch. Lo que no explicaba era la caida adicional de rendimiento especifica al pasar por el switch: un switch Gigabit correctamente fabricado deberia negociar sin perdidas con un dispositivo de 100 Mbps con la misma fiabilidad con la que lo hace con uno de Gigabit completo.

## El veredicto final

Decidi devolver el switch Tenda y sustituirlo por un modelo gestionado, un NETGEAR GS305E, con la ventaja añadida de poder consultar desde su propio panel de administracion la velocidad negociada de cada puerto, sin depender de tests indirectos.

El panel confirmo exactamente lo que sospechaba: el puerto de la tele negocia a 100 Mbps de forma limpia, sin errores. La diferencia con el switch anterior fue inmediata. Repeti el test de velocidad con la tele conectada al nuevo switch y el resultado subio de los 50-70 Mbps que daba con el Tenda a cerca de 84-91 Mbps, en linea con el maximo real del puerto de la tele.

La prueba definitiva llego al volver a lanzar Moonlight. Donde antes la tele mostraba "conexion inestable" y 0 fotogramas por segundo, el panel de rendimiento mostro esta vez 59,88 FPS de red, 0,00% de perdida de fotogramas, una latencia de red de 4 milisegundos y tiempos de decodificacion y procesamiento bajos y estables.

Conclusion completa del caso: el cable nunca fue el problema, ni el primero ni el segundo crimpado, ambos confirmados con un comprobador de continuidad. El puerto Ethernet de la tele esta limitado a 100 Mbps de fabrica, algo que ningun documento oficial confirma pero que ahora tengo comprobado con datos directos del propio switch. Y el switch original tenia un problema real de negociacion con ese tipo de dispositivo, resuelto por completo al sustituirlo por un modelo gestionado de mejor calidad.

Las gatas, de momento, siguen sin cargos.

## Lo que me llevo de todo esto

Mas alla del switch culpable, esta ha sido una buena leccion de como diagnosticar un problema tecnico de verdad: no asumir la primera explicacion que parece encajar, sino ir aislando variables una a una hasta que los datos no dejen sitio a la duda. Cambie de sospechoso varias veces, el cable, el codec, la crimpadora, el propio puerto de la tele, y cada vez que descarte uno fue gracias a una prueba concreta, no a una intuicion. Ese orden es el que al final marca la diferencia entre "creo que ya funciona" y "se por que funciona".

Tambien me llevo la confirmacion de algo que ya sospechaba: la ficha tecnica de un producto casi nunca cuenta toda la historia. Ni el fabricante de la tele ni el de mi primer switch avisan de sus propias limitaciones, y esa informacion solo aparece cuando la mides tu mismo, con las herramientas adecuadas.

Y, sobre todo, esto es exactamente el porque de este blog: no vengo de la informatica, vengo de la carretera, y cada uno de estos lios, el cable atascado, las pruebas fallidas, el switch que hubo que devolver, es una clase que nadie me va a dar en un curso, pero que me llevo puesta de por vida en cuanto la resuelvo con mis propias manos. Se aprende mucho mas tropezando con un problema real que leyendo como se resuelve en la teoria.
