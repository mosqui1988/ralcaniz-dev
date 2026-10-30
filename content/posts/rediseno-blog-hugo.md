---
title: "Rediseñé mi propio blog con Claude Code (y el CSS me dio tres lecciones de humildad)"
date: 2026-10-30T20:25:15+01:00
draft: false
slug: "rediseno-blog-hugo"
tags: ["web", "hugo", "css", "seo", "claude"]
description: "Cómo rediseñé mi blog paso a paso con Claude Code: de un PaperMod casi de serie a una web con identidad propia, tres errores de CSS que me hicieron perder el tiempo y qué añadí para que también la entienda una IA."
---

Mi blog funcionaba, pero lo miraba y me parecía soso. Tema casi de serie, fondo plano, tarjetas sin personalidad. Y como me estoy metiendo en esto de la informática en serio, quería que la web lo contara sola, sin tener que explicarlo.

Así se veía antes y así se ve ahora:

{{< gallery >}}
{{< foto wide="true" src="/img/blog/rediseno-antes.jpg" alt="Portada del blog antes del rediseño: tema casi de serie, fondo plano y tarjetas sin decoración" caption="Antes: PaperMod casi de serie" >}}
{{< foto wide="true" src="/img/blog/rediseno-despues.jpg" alt="Portada del blog después del rediseño: prompt en el logo, fondo con cuadrícula, tarjetas tipo ventana de terminal y etiquetas" caption="Ahora: prompt, cuadrícula, tarjetas-ventana, etiquetas y presentación" >}}
{{< /gallery >}}

Aviso de siempre: no me sé el CSS de memoria. Esta vez lo hice con **Claude Code**, paso a paso y en conversación: yo decidía qué quería ver y qué no, él proponía, tocaba los archivos y miraba el resultado en el navegador con capturas. Este post es el diario de cómo fue.

## Paso 1: ¿merece la pena decorar la web?

Empecé con una pregunta tonta: *"la veo muy simple, ¿vale la pena decorarla con algo con aspecto dev?"* Claude Code miró cómo estaba montado el blog (Hugo con el tema PaperMod, y unas pocas líneas de CSS mío) y me contestó que sí, con matices: que no me pasara con los efectos, porque mis posts son largos y técnicos y lo primero es que se lean cómodos.

Me propuso tres direcciones: un terminal clásico en negro y verde, un estilo dev moderno y sobrio, o lo mínimo. Elegí la **sobria**.

## Paso 2: la primera pasada (y no me convenció)

Salió una primera versión: fuente monoespaciada (JetBrains Mono, alojada en mi propia web) solo en los detalles, un prompt `~$ De Reparto a Root _` en el logo con el cursor parpadeando, un color de acento verde azulado. Era correcta, pero se lo dije tal cual: *"me parece monótono, el fondo es sólido, quiero cosas a los lados, etiquetas en cuadrados…"*

## Paso 3: pedir referencias y copiar lo bueno

Le pedí que buscara blogs de desarrolladores con buena página y que se inspirara en ellos. Encontró temas como Terminal, Stack o Devosfera, y las ideas que se repetían eran las mismas que yo echaba en falta: fondo con textura, tarjetas que parecen ventanas, etiquetas en cajitas y decoración a los lados. Con eso salió esto:

- **Fondo con cuadrícula** y un resplandor verde arriba, en lugar de un color plano.
- **Tarjetas como ventanas de terminal**, con sus tres puntos de colores, y las etiquetas como `#linux`.
- **Laterales decorativos** en pantallas anchas: números de línea a la izquierda y un `const dev = {...}` a la derecha.
- **Una presentación en la portada** y un bloque "Empieza por aquí" con tres posts, para que quien llegue sepa por dónde empezar.

## Paso 4: tres cosas que salieron mal

### 1. El fondo no cambiaba

Escribimos la regla de la cuadrícula y no pasó nada. Claude Code le preguntó al navegador qué fondo tenía el `body`, y respondió `none`. La culpa no era mía ni suya: el tema ya fijaba el fondo de las listas con un selector más específico.

```css
/* lo que hacía el tema */
[data-theme="dark"] .list { background: var(--theme); }

/* la solución: subir el peso de mi selector */
:root body.list { background-image: radial-gradient(...); }
```

En CSS no gana la regla que escribes después, gana la **más específica**. Lo había leído, pero hasta que no me pasó no lo entendí.

### 2. El acento no cambiaba en modo oscuro

Habíamos definido el color del modo oscuro con la clase `.dark`, que es lo que usa mucha gente. PaperMod no la usa: pone un atributo en la etiqueta `html`.

```css
:root[data-theme="dark"] { --accent: #2dd4bf; }
```

Lo vimos al comparar una captura: los colores seguían siendo los del modo claro. Para saber cómo marca un tema el modo oscuro no vale suponer, hay que mirar el código del propio tema.

### 3. Las tarjetas "transparentes" no lo eran

Yo veía las tarjetas demasiado semitransparentes. Subimos la opacidad y seguían igual. La causa real era otra función mía de hace tiempo: los posts que ya he leído se atenúan, y esa atenuación bajaba la opacidad de **toda la tarjeta**, no solo del texto. La solución fue atenuar solo el contenido.

No era un fallo: era una función mía chocando con otra.

## Paso 5: pensando también en las IA

Hoy a una web no solo la leen personas, también buscadores y asistentes de IA. Así que añadimos un poco para que me entiendan bien:

- Un `robots.txt` que deja entrar a todos y apunta al mapa del sitio.
- Un `llms.txt`, un archivo de texto con un resumen de quién soy y de mis mejores proyectos, pensado para que una IA lo lea de un vistazo.
- Datos estructurados de tipo `Person` en la portada, "Sobre mí" y el CV.
- Un título principal (`h1`) en la portada, que no tenía.
- Descripciones y etiquetas en todos los posts: **solo 4 de mis 20 posts tenían etiquetas**, y varios no tenían descripción.

Un fallo curioso que salió de la revisión: la descripción de mi página "Sobre mí" (la que sale en Google) empezaba con el texto del terminal decorativo de la cabecera. Había que escribirla a mano.

## Paso 6: el CV, de enlace a página

Mi página de CV era una frase y un enlace a un PDF. Ahora es una página con línea de tiempo, y lo bueno es que **los datos viven en un solo archivo** (`data/cv.yaml`). De ahí salen la página web y el PDF. El PDF lo genera Chrome sin pantalla (`--headless --print-to-pdf`) desde ese mismo archivo, así nunca se desincronizan. Mi teléfono no está escrito en el código del repositorio: el script lo lee de un archivo de configuración local.

## Lo que me llevo

- Si algo "no funciona", **preguntar al navegador** qué valor tiene de verdad (qué fondo, qué color) vale más que adivinar.
- Los temas tienen sus propias reglas y hay que leerlas antes de pisarlas.
- Un cambio visual pequeño puede destapar contenido sin cuidar: etiquetas que faltaban, descripciones raras, una foto de 1,3 MB donde bastaban 7 KB.
- Trabajar con una IA no es pedirle que lo haga todo. Yo decidía qué quería, ella proponía y probaba, y nada se daba por bueno hasta verlo en pantalla. Cuando algo no me gustaba, se lo decía y se rehacía.

Y esto, otra vez, es el porqué de este blog: cada lío es una clase que nadie me iba a dar en un curso.
