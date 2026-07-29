---
title: "Me apunté a un curso gratis de Linux Foundation (y ahora quiero el LPIC)"
date: 2026-07-29T08:00:00+02:00
draft: false
description: "Empecé el LF-UPV-101x buscando entender mejor mi propio sistema, y terminé con la certificación LPIC en el horizonte."
---

Un compañero, José Manuel, me habló de un curso gratuito de Linux Foundation en edX, el **LF-UPV-101x — Introducción a Linux**, hecho con la Universitat Politècnica de València. Yo ya llevaba unas semanas trasteando con CachyOS, publicando aquí lo que iba aprendiendo a base de romper cosas, pero seguía teniendo la sensación de estar construyendo la casa sin haber visto los planos. Así que dije: vale, vamos a por los planos.

No me metí solo a "aprender Linux en general". Fui con un objetivo concreto detrás: el curso está pensado como paso previo a la certificación **LPIC** (Linux Professional Institute Certification), y esa es la meta real. El blog documenta el camino de camionero a desarrollador; esto es la parte del camino que necesita papel que lo demuestre.

## Cómo lo estoy estudiando

Un chat nuevo por cada tema del curso. Voy pegando el contenido poco a poco, sin dejar que se resuma nada hasta que yo lo pido explícitamente — si algo se me pasa por encima demasiado rápido, no se me queda. Y cuando algo es denso, diagramas y tablas, no solo texto.

Llevo doce temas completados de dieciocho. Y por el camino han ido cayendo cosas que antes usaba sin entender del todo por qué funcionaban.

## Lo que más me está costando: login shell vs no-login shell

Esto me tuvo dando vueltas un rato. Cuando abres una terminal en tu escritorio, no es lo mismo que cuando entras por SSH a un servidor. Son dos "modos" distintos de shell, y cada uno lee un conjunto diferente de ficheros de configuración al arrancar:

```
Shell de LOGIN (ej. entrar por SSH, o login en consola)
  /etc/profile
        │
        ▼
  ~/.bash_profile  →  si no existe...
        │
        ▼
  ~/.bash_login    →  si no existe...
        │
        ▼
  ~/.profile

Shell INTERACTIVA NO-LOGIN (ej. abrir una terminal en el escritorio)
  ~/.bashrc   ← el que de verdad importa en el día a día
```

Cuando por fin até el cabo tuve uno de esos momentos de "ohhh, por eso ese alias no me funcionaba cuando entraba por SSH pero sí en mi terminal normal". Llevaba tiempo poniendo cosas donde no tocaba, sin saber que existían dos rutas distintas. Lo tengo más claro ahora, pero todavía necesito pararme a pensarlo, no me sale automático.

Otra que voy asentando poco a poco: `export`. Sin `export`, una variable de entorno es solo tuya, de esa sesión de shell concreta. En cuanto la exportas, la heredan los procesos hijos que lances desde ahí. Parece un matiz pequeño, pero cambia bastante cómo se comportan los scripts — de esas cosas que entiendo cuando lo leo, y que aún tengo que confirmar que se me quedan cuando lo necesito de verdad.

## Cosas que voy incorporando

Ojo, esto no es una lista de "ya lo sé". Es más bien la base con la que me quedo por ahora — cosas que tengo apuntadas, que entiendo cuando las repaso, y que espero que cada día se me vayan quedando un poco más:

- **Que `.` nunca debe estar en el `PATH`.** Es una puerta abierta a un ataque de caballo de Troya de manual: si alguien deja un `ls` malicioso en un directorio donde entras, y tu sistema busca primero en el directorio actual, ese `ls` falso se ejecuta antes que el de verdad. Es de las cosas que, en cuanto me lo explicaron, se quedó grabado por lo bruto del ejemplo.
- **`/proc`.** No es una carpeta cualquiera — es una ventana en vivo al kernel. Comandos como `free` o `lscpu` no "calculan" nada raro por su cuenta, simplemente leen de ahí. Esto lo tengo más fresco que otras cosas, seguramente porque lo vi con ejemplos prácticos.
- **`systemctl reload` antes que `restart`, y `restart` antes que `kill -9`.** `reload` manda una señal (SIGHUP) para que el propio proceso se recargue solo, sin cortar servicio de golpe. `restart` sí para y relanza. Y `kill -9` es el último recurso, no el primero. Esto lo tengo apuntado en la chuleta porque sé que en caliente, sin pensarlo, se me olvidaría el orden.
- **`/root` no es la raíz del sistema.** Es solo la casa del superusuario. De esas confusiones de vocabulario que seguro tenía sin darme cuenta hasta que alguien me lo aclaró.

## El "chuletario"

En paralelo he ido montando un documento — de momento cubre los primeros nueve temas, voy ampliándolo según avanzo — organizado no por tema del curso, sino por **síntoma**: "servidor lento → qué miro primero", ese tipo de cosas. No es un resumen de lo que ya domino, es más bien mi propia chuleta para el día que me llamen a arreglar algo real y no tenga la respuesta en la cabeza al momento — que hoy por hoy es lo más probable.

## Lo que queda

Seis temas por delante, y después:

- Montar una máquina virtual (virt-manager + QEMU/KVM, con Debian o Ubuntu Server) para practicar sin arriesgar mi propio sistema.
- Un repaso serio de `vi`/`vim` — puede que también `emacs` — específico para lo que pide el examen. Lo dejo para el final, cuando ya tenga todos los temas cerrados.
- Pagar el examen y presentarme al LPIC.

De momento voy topic a topic, sin prisa pero sin soltarlo. Ya iré contando cómo sigue esto.
