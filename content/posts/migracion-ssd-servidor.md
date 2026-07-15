---
title: "Le cambié el disco a mi servidor casero (y no fue ningún milagro, solo memoria)"
date: 2026-07-15T06:00:00+02:00
draft: false
description: "Cómo detecté que el disco duro de mi servidor casero estaba desgastado y lo sustituí por un SSD."
---

Este post no va de una hazaña. Va de una tarea de mantenimiento normal, del tipo que cualquier técnico de sistemas hace sin pensarlo dos veces — y de que, para hacerla, no necesité buscar ningún tutorial en YouTube. Solo recordar lo que ya sabía.

## El síntoma

Mi servidor casero (un Lenovo ThinkCentre Tiny que ya ha salido por aquí antes) lleva semanas funcionando de fondo: Docker, Tailscale, Syncthing. Nada exigente. Pero tenía curiosidad por saber cómo estaba de salud el disco duro mecánico que traía de fábrica, así que un día lancé `smartctl` sobre él, sin esperar sorpresas.

Y ahí estaba: sectores reasignados acercándose al umbral de fallo. Ese dato es literal — S.M.A.R.T. (el sistema de autodiagnóstico que llevan los discos) te avisa cuando el hardware empieza a fallar de verdad, no cuando "va lento" o "hace ruido raro". Es la diferencia entre sospechar y confirmar.

No fue una sorpresa dramática. Fue justo lo que se supone que tiene que pasar: un disco mecánico con miles de horas de uso, dando señales de que le queda cuerda, pero no infinita.

## La decisión, sin vueltas

Aquí no hubo debate largo. El disco tenía sectores dañados confirmados, el precio de un SSD SATA de 512GB decente rondaba los 120€, y la diferencia de rendimiento y fiabilidad no tenía color. Elegí un modelo con caché DRAM y buena reputación en foros, y punto.

Nada de sustituirlo por otro HDD "porque era barato". El disco viejo, con el desgaste ya confirmado, se desecha — no se reutiliza como backup. Eso también es una decisión técnica: un disco que ya ha dado señales de fallo no es un buen sitio donde confiar una copia de seguridad.

## Clonar, no reinstalar

Podría haber reinstalado Debian desde cero en el SSD. Pero eso significa reconfigurar Docker, Tailscale, usuarios, red... horas de trabajo para llegar exactamente al mismo sitio donde ya estaba. La alternativa con sentido es **clonar el disco entero, tal cual, a otro dispositivo** — mismos datos, mismas configuraciones, mismos servicios, solo que ahora corriendo sobre memoria flash en vez de un plato que gira.

Para eso usé **Clonezilla**, una herramienta de código abierto pensada exactamente para esto: copiar un disco entero (o solo particiones) de un sitio a otro, byte a byte, respetando la estructura interna. Se arranca desde un USB, así que ni siquiera toca el sistema operativo que ya tienes instalado — trabaja "desde fuera", con los dos discos apagados y quietos, evitando el riesgo de copiar algo a medio escribir.

El proceso, resumido: arrancar el USB, decirle "quiero clonar disco a disco, no una partición suelta", elegir cuál es el origen (el HDD viejo) y cuál el destino (el SSD nuevo — con cuidado, porque equivocarse aquí significa borrar el disco que no tocaba), y confirmar. El propio programa avisa en mayúsculas de que el disco destino se sobrescribe entero. Se lee, y se confirma con calma.

Quince minutos después, listo. Sin errores.

## El momento manual: cambiar el disco de verdad

Clonar es la parte "de software". Pero el disco seguía siendo un objeto físico dentro de una carcasa, y había que sacarlo de verdad. Abrí el Lenovo, desconecté el cable SATA + alimentación del HDD viejo, y lo desatornillé de su bandeja: cuatro tornillos, un cable, y el disco fuera. El SSD entra en el mismo hueco, con el mismo cable, en cinco minutos.

Encendido de prueba, con la carcasa aún abierta por si algo fallaba y había que volver a mirar dentro. Arrancó a la primera.

## Verificar antes de dar nada por hecho

Que arranque no basta. Antes de cerrar la carcasa y esconder el servidor otra vez donde no moleste, comprobé:

- Que el sistema realmente corre desde el SSD (`lsblk` con el dato de si el disco es "rotacional" o no — un SSD siempre marca que no)
- Que el espacio del disco se aprovecha entero, sin quedarse recortado por el proceso de clonado
- Un informe SMART completo del SSD nuevo, como punto de referencia "cero horas" — así, dentro de un año, podré comparar el desgaste real
- Que Docker y Tailscale seguían funcionando con normalidad
- Y, la comprobación que de verdad importa: un **reinicio completo**, no solo un encendido tras estar apagado. Muchos problemas de arranque solo se manifiestan ahí.

Todo correcto. Servidor cerrado, escondido, y mi pareja sin enterarse de que durante un rato hubo un ordenador desmontado encima de la mesa.

## Por qué cuento esto

No hay ningún giro de guion en este post, ni ningún bug misterioso que resolver a las tres de la mañana (para eso ya tengo otros posts). Lo cuento porque es la prueba pequeña y sin dramatismo de algo que sí me importa: no seguí ningún tutorial paso a paso para hacer esto. Leí la documentación de `smartctl`, recordé lo que aprendí como Técnico en Sistemas Microinformáticos y Redes, até cabos, y lo hice.

Mantenimiento de servidores es justo esto la mayoría de las veces: no dramatismo, sino saber leer una señal a tiempo y actuar con calma.
