---
title: "Le di memoria a Claude Code (y la comparten mis tres ordenadores)"
date: 2026-11-16T15:04:35+01:00
draft: false
description: "Cada vez que abría Claude Code tenía que explicarle todo otra vez. Cómo monté una carpeta de notas, sincronizada entre mis tres equipos, para que sepa lo que hice y en qué ordenador."
tags: ["claude-code", "syncthing", "homelab", "linux"]
---

Hay una cosa que me molestaba cada vez que abría Claude Code: **no se acordaba de nada**. Había pasado la tarde con él montando un tema de escritorio en el portátil, y al día siguiente, en la torre, tocaba contárselo todo otra vez. Qué hicimos, dónde está cada cosa, qué falló y por qué lo dejamos así.

Lo que quería era sencillo de decir: **que cualquier ordenador, y cualquier sesión, empiece sabiendo lo que ya se hizo**.

{{< captura src="cerebro-memoria.png" alt="Tres equipos, torre, servidor y portátil, con la carpeta Memoria unida por Syncthing, y debajo lo que contiene: manual, índice, proyectos, decisiones y aprendizajes" caption="La misma carpeta Memoria en los tres equipos, y lo que lleva dentro" >}}

Aviso como siempre: no lo tenía claro desde el principio. Lo fui montando con Claude Code, y una parte de este post es lo que salió mal.

## La idea: una carpeta de notas

Nada de bases de datos ni plugins. Una carpeta llamada `Memoria` con notas en texto plano (Markdown), que se pueden leer con cualquier cosa, y que Claude Code encuentra con un simple `grep`.

Dentro hay carpetas con una idea cada una:

- **`proyectos/`**: cómo está cada proyecto *hoy*. Dónde está, qué falta, quién lo tocó.
- **`decisiones/`**: *por qué* elegí algo, y qué descarté. Así no me pregunto dentro de un mes por qué instalé esto y no lo otro.
- **`aprendizajes/`**: una trampa por nota. Por ejemplo, que `pkill -f` dentro de un comando mata tu propio terminal. Me pasó una vez y no quiero que me pase dos.
- **`t14s/`, `torre/`, `servidor/`**: una carpeta por ordenador, con su estado y su bitácora.
- **`indice.md`**: el mapa de entrada.

Como son notas con enlaces entre ellas (`[[así]]`), puedo abrir la carpeta con **Obsidian** y ver el grafo: cada punto es una nota, cada línea un enlace. En el centro, el índice, de donde sale todo; alrededor, proyectos, decisiones, aprendizajes y las bitácoras de cada día.

{{< captura src="cerebro-grafo-obsidian.png" alt="Grafo de Obsidian con la carpeta Memoria: decenas de puntos de colores unidos por líneas, con la nota índice en el centro" caption="La carpeta Memoria vista como grafo en Obsidian: las telarañas del cerebro" >}}

## Cómo sabe en qué ordenador está

Aquí está el truco que más me gustó. En la carpeta hay un archivo, `LEEME-IA.md`, que es el manual de instrucciones para la IA. Y Claude Code lo carga solo, porque la primera línea de su archivo de configuración (`~/.claude/CLAUDE.md`) lo enlaza.

El manual le dice:

1. Ejecuta `hostname` y busca tu ordenador en esta tabla.
2. **Tu carpeta es la de tu ordenador. La de los otros solo la lees.**
3. Lee el índice y el resumen de la última sesión de cada equipo.

Con eso, si pregunto «¿qué es lo último que hicimos?», me contesta con lo que pasó y **en qué ordenador pasó cada cosa**. La regla de que cada equipo escribe solo en su carpeta evita que dos ordenadores se pisen las notas.

## Cómo viaja entre los tres

La carpeta se sincroniza con **Syncthing**, igual que conté en [el post anterior]({{< ref "sincronizar-proyectos-tres-equipos" >}}). Sin nube de por medio, con versionado por si borro algo sin querer. Lo que escribe la torre aparece en el portátil y en el servidor.

## Cómo se guarda

Cuando me despido («hasta luego», «buenas noches»), Claude Code repasa la sesión y guarda lo que merece la pena: sobrescribe un resumen corto de la última sesión, añade lo hecho a la bitácora del día y actualiza las notas que toquen. Y me lo cuenta en tres o cuatro líneas.

No es magia: **es una instrucción, no un automatismo**. Depende de que la IA se acuerde de seguirla. Hasta ahora lo ha hecho, pero es la parte frágil.

También hay un script que saca una foto técnica de cada ordenador (hardware, paquetes, servicios, configuración, sin contraseñas) para poder reconstruirlo si un día se rompe.

## Lo que salió mal (o se quedó viejo)

Pasadas un par de semanas le pedí a otro modelo que auditara el cerebro como había hecho con el blog. Su veredicto fue que **funciona, pero se envejece**:

- Las notas de estado se contradecían: una decía que Tailscale estaba pendiente de instalar cuando llevaba semanas funcionando.
- Casi todo se añadía y casi nada se corregía.
- La nota «qué pasó en la última sesión» se había hinchado con varias sesiones juntas, y se lee **cada vez que se abre Claude Code**. Cada línea de más cuesta gasto siempre.
- El servidor casi no existía en el cerebro.

Así que hice limpieza con un script de chequeo (`revisar.py`) que cuenta enlaces rotos, notas sin fecha, notas demasiado largas... Pasé de 13 avisos a 2. Y escribí reglas claras de qué va en cada carpeta: lo que *es* hoy en proyectos, lo que *se eligió* en decisiones, y lo que *volverá a pasar* en aprendizajes.

## Lo que me llevo

- **Texto plano y carpetas.** Funciona porque no hay nada que mantener aparte de escribir bien.
- **Una carpeta por equipo, y cada uno escribe solo en la suya.** Evita conflictos sin hacer nada más.
- **Las notas se pudren si solo las añades.** Hay que corregirlas, y hay que tener algo que te avise.
- **Lo que no quiero guardar, lo digo en las reglas:** nada de contraseñas, claves ni datos de otras personas, y tampoco de salud. Si la IA duda, no lo guarda.

Si quieres montar algo parecido, el truco no es la herramienta: es decidir qué merece la pena recordar y dónde va cada cosa.
