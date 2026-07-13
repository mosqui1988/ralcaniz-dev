---
title: "Monté mi propio backup de fotos (y un ordenador se negó a hablar con el otro)"
date: 2026-07-12T19:19:00+02:00
draft: false
---

Hay una cosa que me da bastante repelús: tener todas mis fotos solo en el móvil. Si se me cae, se moja o me lo roban, esos recuerdos se van con él. Como en casa ya tengo un par de ordenadores montados como servidores que funcionan las 24 horas, me pareció una tontería no aprovecharlos para esto. Así que me puse a montar mi propio backup de fotos, sin depender de Google Fotos ni de ninguna nube de pago.

## Lo que quería conseguir

Nada complicado, pero con una condición clara: quería tres "copias de seguridad de la copia de seguridad", por así decirlo.

1. Que las fotos del móvil se subieran solas a mi servidor de casa en cuanto hubiera wifi.
2. Poder borrar fotos del móvil sin miedo, porque la copia de verdad ya está guardada en el servidor.
3. Que mi ordenador de trabajo (la Torre) también tuviera una copia extra, por si el servidor tiene algún problema serio algún día (se rompe el disco, por ejemplo).

Para esto usé un programa llamado **Syncthing**. Es como un Dropbox, pero sin Dropbox: los archivos viajan directamente entre mis propios aparatos, sin pasar por ningún servidor de una empresa. Todo dentro de mi propia red privada (Tailscale), que ya tenía montada de antes.

## Cómo lo organicé

No quería que todos mis aparatos se sincronizaran entre sí sin ton ni son. Quería que mi servidor (un mini ordenador Lenovo que tengo encendido siempre) fuera el centro de todo, y que cada aparato hablara solo con él, nunca entre ellos directamente.

```
        📱 Móvil                🖥️  Servidor (Lenovo)         💻 Torre
     "solo mando fotos"        "aquí se guarda todo         "solo recibo
                                 de verdad"                   una copia"

  Subo fotos  ────────>   Se quedan guardadas   ────────>   Recibo copia
  Borro en el móvil       aquí para siempre                 Si borro aquí
  → no pasa nada aquí                                       por error, no
                                                               se borra allí
```

Cada aparato tiene un "modo" distinto:

- **El móvil, en modo "solo enviar"**: manda fotos pero nunca recibe cambios de vuelta. Así puedo vaciar el carrete del móvil cuando quiera sin miedo a perder nada, porque ya está guardado en el servidor.
- **El servidor, sin restricciones**: es el único sitio donde las fotos son "de verdad". Si algo se borra ahí, se borra en serio — pero soy yo quien lo decide a propósito, no un accidente desde otro aparato.
- **La Torre, en modo "solo recibir"**: tiene una copia extra, pero no puede modificar el original. Si algún día borro algo sin querer en el ordenador, el programa simplemente lo vuelve a bajar del servidor solo. Cero riesgo.

## Manos a la obra

Instalé Syncthing en el servidor usando Docker (una forma de tener programas instalados de manera aislada, como en cajitas separadas, sin que se líen unos con otros). Hice dos carpetas separadas, una para mis fotos y otra para las de mi pareja, cada una visible solo para quien toca.

En el móvil instalé una app llamada Syncthing-Fork, la emparejé con el servidor escaneando un código QR, y le dije que vigilara la carpeta de fotos del teléfono. En pocos minutos ya tenía casi 5GB y más de 160 fotos copiadas. Cambié el móvil a modo "solo enviar" y esa parte quedó lista.

En la Torre instalé el mismo programa, esta vez directamente (sin Docker). Hasta aquí todo iba según lo previsto.

## Aquí me atasqué: el ordenador que no quería saludar

Le dije al servidor "oye, ya conoces a la Torre, tráeme sus archivos" — y no pasaba nada. En la pantalla del servidor, la Torre aparecía como "Desconectado". Algo no cuadraba.

Fui comprobando cosas, una por una, para no dar palos de ciego:

- **`ufw status`** en la Torre → esto me enseña qué puertos tiene abiertos o cerrados el cortafuegos (una especie de portero que decide qué conexiones entran y salen). Estaban abiertos los puertos correctos, así que no era eso.
- **`ss -tlnp | grep 22000`** en la Torre → este comando enseña qué programas están "escuchando" en cada puerto, es decir, esperando conexiones. Syncthing sí estaba ahí, esperando. Tampoco era eso.
- **`nc -zv 192.168.1.3 22000`** desde el servidor → este comando prueba si se puede llegar hasta un puerto concreto de otro aparato, sin mandar datos de verdad, solo para comprobar que "la puerta está abierta". Y sí, se podía llegar sin problema. Así que la red en sí no era el problema.

Como todo lo de red estaba bien, miré directamente los mensajes que el propio Syncthing iba dejando por el camino (sus "logs", es decir, su diario de lo que va haciendo). En el servidor vi que la conexión sí se llegaba a abrir, pero se cortaba sola un segundo después, una y otra vez.

La pista de verdad la encontré con este comando, ejecutado en la Torre:

```bash
journalctl --user -u syncthing -n 100 --no-pager | grep -i "192.168.1.2"
```

Te explico qué hace cada trozo, porque no lo había usado antes:
- `journalctl` enseña el diario de mensajes del sistema.
- `--user -u syncthing` le dice que solo quiero los mensajes de Syncthing (y de la versión que corre como "mi usuario", no como administrador).
- `-n 100` quiere decir "dame los últimos 100 mensajes", para no tragarme el diario entero.
- `--no-pager` es para que lo saque todo seguido en la pantalla, sin tener que ir pasando página.
- `| grep -i "192.168.1.2"` filtra y me enseña solo las líneas que mencionan la IP de mi servidor.

Y ahí apareció el mensaje que lo explicaba todo:

```
Connection rejected ... error="unknown device"
```

Traducido: **"dispositivo desconocido, rechazado"**. Y ahí até cabos: yo había dicho en el servidor "conozco a la Torre", pero nunca le había dicho a la Torre "oye, tú también conoces al servidor". Es como si yo te reconociera a ti por la calle, pero tú a mí no me sonaras de nada — normal que no me abrieras la puerta. Hacen falta las dos partes.

## La solución

Fui a la pantalla de Syncthing en la Torre, añadí a mano el "identificador" del servidor (un código larguísimo, tipo DNI del aparato), y en segundos la conexión se quedó fija, sin cortes. Lo comprobé volviendo a mirar el diario de mensajes, y esta vez solo vi líneas de tipo "conexión establecida", sin ningún rechazo más.

Con eso resuelto, compartí la carpeta de fotos desde el servidor hacia la Torre, y en la Torre la puse en modo "solo recibir", tal como había planeado desde el principio.

Antes de darlo por cerrado me hice una pregunta importante: si borro fotos desde el ordenador, ¿se borran también en el servidor? Con el modo "solo recibir", la respuesta es no. Si borro algo sin querer, el programa simplemente detecta que "algo cambió por aquí sin permiso" y vuelve a traer el archivo desde el servidor. Es justo la red de seguridad que quería: el único sitio donde de verdad se puede borrar algo para siempre es el propio servidor, y solo si lo hago yo a propósito.

## Cómo quedó todo

```
   📱 Móvil                🖥️  Servidor (Lenovo)        💻 Torre
  Solo enviar        ──>   Guarda todo de verdad  ──>  Solo recibir
```

Tres capas, cada una protegida de que las otras dos la puedan estropear por accidente. Y de paso me llevo una lección que seguro me sirve más adelante: cuando dos aparatos tienen que confiar el uno en el otro, casi nunca basta con configurarlo en uno solo — hay que comprobar los dos lados antes de asumir que "ya debería funcionar".

Queda pendiente hacer lo mismo con el móvil de mi pareja en cuanto le ponga a punto el teléfono — pero eso ya será la próxima entrada.
