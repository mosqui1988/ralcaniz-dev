---
title: "Mis proyectos, igual en los tres ordenadores"
date: 2026-11-04T19:45:00+01:00
draft: false
description: "Quería guardar algo en la torre y encontrarlo en el portátil, en la misma carpeta. Cómo lo monté con Syncthing y un servidor, y los dos problemas que me encontré."
tags: ["syncthing", "docker", "homelab", "linux"]
---

Tengo tres ordenadores: la torre, donde estudio DAM; un portátil, para cuando me muevo; y el servidor de casa, que está siempre encendido. Lo que quería era sencillo de decir: **que lo que guardo en uno aparezca solo en los otros dos, en la misma carpeta y con el mismo nombre**.

{{< captura wide="true" src="sync-tres-equipos.png" alt="Tres cajas, torre, servidor y portátil, cada una con la carpeta Proyectos, unidas por flechas de copia" caption="Lo que quería: la misma carpeta en los tres equipos, sincronizada sola" >}}

Aviso como siempre: no me sé estos comandos de memoria. Los fui descubriendo según me los encontraba, con Claude Code echándome una mano desde la terminal.

## Qué quería y por qué

Hasta ahora solo sincronizaba la carpeta de las clases. Todo lo demás (el blog, las prácticas, mis pruebas) vivía en la torre, y para llevármelo tocaba copiarlo a mano. Funciona hasta el día que te olvidas de copiar algo.

Quería una sola carpeta, `Proyectos`, con todo dentro (la de las clases también). Y que el servidor guardara una copia, para no depender de que los otros dos estén encendidos.

Para esto uso **Syncthing**, un programa que copia carpetas entre ordenadores sin pasar por ninguna nube. Ya lo tenía en marcha. Lo difícil vino después.

## Problema 1: una carpeta pesaba 65 GB

Antes de sincronizar nada, miré cuánto pesaba `Proyectos`: **68 GB**. Y 65 eran una sola carpeta de juegos de otro aparato. En el portátil cabría, pero no hacía falta: se pasaría horas copiándola y se comería sitio para nada.

{{< captura wide="true" src="sync-peso-carpeta.png" alt="Barra de 68 GB donde 65 GB son una carpeta de juegos que no se copia y el resto, unos 2 GB, sí viaja" caption="Casi todo el peso era una carpeta que no necesitaba copiar" >}}

Syncthing tiene un archivo llamado `.stignore`, que es una lista de "esto no lo copies". El mío lleva cuatro líneas:

```
/Juegos
node_modules
build
dist
```

- `/Juegos`: la carpeta pesada. La barra del principio significa "empieza desde `Proyectos`", así que solo afecta a esa.
- `node_modules`, `build` y `dist`: carpetas que los proyectos de programación vuelven a crear solos al compilar. Moverlas de un ordenador a otro es perder tiempo, y salen en cualquier subcarpeta.

Con esto pasé de 68 GB a unos 2.

Una cosa que me pilló: **el `.stignore` no se sincroniza**. Cada ordenador tiene el suyo, así que hay que copiarlo a mano a los tres.

## Problema 2: el servidor vive dentro de una caja

Mi servidor ejecuta Syncthing dentro de **Docker**, que es como una caja cerrada con su propio sistema de archivos. La trampa es que, cuando le dices a Syncthing "guarda esto en `/var/syncthing/proyectos`", esa ruta existe **dentro de la caja**, no en el disco real.

{{< captura wide="true" src="sync-docker-caja.png" alt="Syncthing dentro de una caja de Docker. Sin volumen, los archivos se quedan en la ruta de dentro de la caja y el disco real queda vacío. Con un volumen, esa ruta se conecta con una carpeta real del disco" caption="Sin volumen, los archivos se quedan dentro de la caja. Con volumen, llegan al disco real" >}}

Si aceptas la carpeta sin más, los archivos acaban en un rincón interno de Docker que no puedes ver, y se pierden si algún día recreas la caja. Hay que conectar una carpeta real con una ruta de dentro. A esa conexión se le llama **volumen**, y se pone con una línea en el archivo `docker-compose.yml`:

```yaml
volumes:
  - /home/usuario/Proyectos:/var/syncthing/proyectos
```

Se lee así: **lo de la izquierda es la carpeta real del disco, lo de la derecha es cómo la ve Syncthing desde dentro de la caja**.

Antes de tocarlo hice una copia del archivo, y luego recreé solo ese contenedor. El resto de cosas del servidor ni se enteraron.

## Lo que me llevo

- **Mira cuánto pesa algo antes de sincronizarlo.** Casi lo copio todo sin darme cuenta de que 65 GB sobraban.
- **Haz una copia antes de tocar nada.** Yo guardé el archivo de Docker antes de cambiarlo, por si algo salía mal.
- **Con Docker, la ruta que ves no es la del disco.** Hay que conectarla con un volumen.

Los tres equipos acabaron con **8.027 archivos y 1,97 GB**, exactamente los mismos números en cada uno. Ahora guardo algo en la torre y aparece en el servidor y en el portátil, en el mismo sitio. En el próximo post cuento lo que más ilusión me hacía de todo esto: una memoria compartida para que Claude Code sepa lo que hice en cada ordenador.
