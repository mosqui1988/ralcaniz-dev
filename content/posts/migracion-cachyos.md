+++
date = '2026-07-01T07:28:45+02:00'
draft = false
title = 'De Windows a CachyOS: mi salto al vacío'
description = 'Cómo pasé de no saber qué era una terminal a instalar Arch Linux en mi PC de juegos, y por qué no volvería atrás.'
tags = ['linux', 'cachyos', 'arch', 'windows', 'principiantes']
+++

Hay momentos en la vida en los que el universo toma decisiones por ti.

El mío fue un martes cualquiera, con Starfield a medio instalar, un reinicio forzado y una pantalla negra que no volvió a encenderse como antes. El SSD había decidido jubilarse anticipadamente. No por viejo, que tenía apenas un 1% de desgaste y poco más de dos mil horas de uso. No. Se fue por defecto de fabricación. La BIOS llevaba semanas avisando con un mensaje SMART que yo, como buen usuario de Windows, ignoré olímpicamente.

Ese día, sin quererlo, me convertí en usuario de Linux.

## Quién soy y de dónde vengo

Para entender por qué esto tiene gracia, hay que conocer un poco de contexto.

Me llamo Rubén, tengo el FP de Sistemas Microinformáticos y Redes desde 2013, que en la práctica significó trabajar una temporada en la tienda de informática y patines de Javi, el informático del barrio. Lo de los patines no tiene nada que ver con la informática, pero así era el negocio. Siempre le estaré agradecido por dejarme hacer las prácticas allí y quedarse conmigo una temporada después, cuando no tenía trabajo suficiente para los dos.

De ahí pasé a una cristalería. Y de la cristalería, al camión repartiendo cristales. Que es donde he estado los últimos años: cargando y descargando vidrio, haciendo fuerza donde no debía, hasta que mis brazos dijeron basta. El diagnóstico fue Epicondilitis lateral bilateral, que en cristiano significa que los tendones de ambos codos estaban hasta las narices y necesitaban descanso. Descanso obligatorio, indefinido y posiblemente crónico.

Así que de repente tenía tiempo. Mucho tiempo. Y un PC con Linux a medias que llevaba meses sin tocar en serio.

## La transición gradual (y la muerte del SSD)

Lo de Linux no fue una decisión heroica. Fue curiosidad con red de seguridad.

Llevaba tiempo leyendo por internet que el salto a Linux ya no era el sacrificio que era antes, que los juegos funcionaban, que la gente lo usaba en su PC principal sin dramas. Así que hice lo que hace cualquier persona sensata que no quiere perder sus juegos ni sus cosas: particioné el disco. La mitad para Windows, la mitad para CachyOS. Un pie en cada mundo.

Durante meses entré a CachyOS de vez en cuando, a trastear, a probar, a romper cosas y arreglarlas. Sin prisa. Sin compromiso. Windows seguía ahí por si acaso.

Hasta que dejó de estar.

Un día cualquiera, instalando Starfield, el sistema se congeló. Reinicio forzado. Pantalla negra. Windows no arrancaba. Lo que parecía un susto resultó ser algo más serio: el SSD tenía un defecto de fabricación en la memoria NAND. No había muerto de viejo, tenía apenas un 1% de desgaste y unas 2.100 horas de uso. Pero había quemado el 81% de sus bloques de reserva en pocos meses, acumulando 112 errores de integridad de datos. Cuando el controlador no pudo garantizar más escrituras fiables, corrompió el arranque de Windows y se acabó la historia. La BIOS llevaba semanas avisando con un mensaje SMART. Yo lo ignoré.

Moraleja: leed los avisos de la BIOS.

El caso es que de un día para otro, CachyOS dejó de ser "el sistema de pruebas" y pasó a ser el único sistema. Sin red de seguridad. Y aquí estoy.

## Qué es CachyOS y por qué esta distro

Antes de seguir, aclaremos algo para los que estén igual que yo hace unos meses.

Cuando la gente dice "me pasé a Linux" no está diciendo que instaló un programa. Linux es un sistema operativo, como Windows, pero con una diferencia importante: existe en miles de versiones distintas hechas por comunidades de todo el mundo. A cada versión se le llama distribución, o distro. Algunas están pensadas para servidores, otras para científicos, otras para gente que quiere jugar, y otras para gente que simplemente quiere que su ordenador haga lo que le mandan sin rechistar.

Hay una en concreto que tiene cierta fama: Arch Linux. Arch es la distro para los que disfrutan configurando cosas. Su instalación es completamente por terminal, sin botones, sin asistente, sin nadie que te lleve de la mano. Puro texto negro y comandos. Suena aterrador porque lo es un poco.

CachyOS es básicamente Arch, pero con un instalador gráfico que no te hace llorar. Trae todo lo necesario para funcionar desde el primer día, está optimizada para sacar el máximo rendimiento al hardware, y funciona especialmente bien para gaming. Me dio lo mejor de Arch sin tener que ser experto para instalarlo.

¿Por qué no Ubuntu o Linux Mint, que son las que todo el mundo recomienda para empezar? Pues mira, tampoco soy quién para decir que son malas opciones. Pero yo quería algo que me dejara trastear, aprender y no quedarse anticuado. CachyOS se actualiza constantemente, consume muy pocos recursos comparado con Windows, y me deja personalizarlo a mi gusto. Además los juegos funcionan. Starfield, Crimson Desert, Gothic Remake. Sin dramas, sin excusas.

El que diga que Linux no es para jugar está desactualizado.

## El choque con la terminal

Y entonces llegó ella. La ventana negra.

Cualquiera que haya usado Windows toda su vida sabe de lo que hablo. La terminal. Ese rectángulo oscuro lleno de texto que en las películas usan los hackers para hacer cosas incomprensibles a velocidad de vértigo. Yo la llamaba así: la ventana negra. Y le tenía un respeto considerable.

Lo curioso es que algo sabía. El FP de 2013 me había dado unas nociones básicas, pero entre aquello y hoy habían pasado más de diez años de Windows, ratón y doble clic. Volver a la terminal fue como encontrarte con un idioma que estudiaste en el colegio y nunca más usaste. Las bases están en algún sitio ahí dentro, pero hay que desenterrarlas.

Al principio todo cuesta. ¿Cómo instalo un programa? Por terminal. ¿Cómo muevo un archivo? Por terminal. ¿Cómo sé qué versión tengo de algo? Terminal. Es un cambio de mentalidad más que de habilidad. Windows te da botones para todo. Linux te da el control total, pero tienes que ganártelo.

Poco a poco fui viendo el otro lado. La terminal es rápida. Es precisa. Cuando entiendes lo que estás haciendo, es mucho más eficiente que andar buscando opciones enterradas en menús. Y hay algo satisfactorio en escribir un comando y que el sistema haga exactamente lo que le pediste, sin preguntas, sin ventanas de confirmación, sin "¿estás seguro?".

Bueno, a veces pregunta. Cuando le das permisos de administrador. Ahí sí conviene leer lo que estás haciendo.

## Dónde estoy ahora

Han pasado unos meses desde aquella pantalla negra de Starfield.

Hoy uso CachyOS como único sistema. Juego sin problemas, trabajo desde la terminal con más soltura cada día, y este blog que estás leyendo ahora mismo está construido, configurado y escrito desde ella. No del todo, no voy a mentir, pero más de lo que habría imaginado hace un año.

Tengo pensado cursar el CFGS de Desarrollo de Aplicaciones Multiplataforma, aunque de momento estoy intentando conseguir plaza. No sé si me la darán. Lo que sí sé es que mientras tanto no voy a quedarme parado.

¿Sé mucho de Linux? No. ¿Sé más que hace seis meses? Muchísimo. Y esa es la única métrica que me importa ahora mismo.

Este blog, "De Reparto a Root", es la bitácora de ese camino. Sin filtros, sin postureo técnico. Un repartidor de cristales aprendiendo a programar desde cero, contando lo que aprende para que a otros les cueste un poco menos.

Bienvenido.
