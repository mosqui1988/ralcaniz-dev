---
title: "Creía que ya lo tenía todo blindado (y no era así)"
date: 2026-07-18T10:00:00+02:00
draft: false
---

Hace unas semanas monté Vaultwarden en mi servidor casero — mi propio gestor de contraseñas, como Bitwarden pero corriendo en un ordenador de mi casa en vez de en los servidores de una empresa. Mi plan era simple: meter ahí dentro absolutamente todas mis contraseñas, incluida la de mi propio correo de Google, y que fueran aleatorias, imposibles de recordar de memoria. Lo único que memorizaría sería una sola contraseña: la maestra de Vaultwarden. Todo lo demás, resuelto.

Lo dejé funcionando, con cifrado fuerte y acceso solo desde mi red privada, y lo di por cerrado. Y entonces, un día cualquiera, se me ocurrió una pregunta tonta: *"¿y si pierdo el móvil?"*

Esa pregunta abrió una caja de sorpresas que no esperaba — y varias veces, según iba tirando del hilo, resultó que lo que yo mismo daba por bueno tampoco era del todo correcto. Este post es de eso: de creer que ya lo tenía atado, de chocarme con la realidad más de una vez, y de terminar con un plan que sí funciona de verdad, porque lo he probado.

Un aviso antes de empezar: no me sé estos comandos ni estos conceptos de memoria, ni falta que hace. Cada cosa que cuento aquí la fui buscando según la necesitaba — en documentación, preguntando, probando. Lo que sigue es el proceso real, con los tropiezos incluidos.

## La pregunta que lo empezó todo

Vaultwarden pide, para entrar, mi contraseña maestra. Eso lo memorizo. Pero pensé: *si pierdo el móvil, ¿cómo entro a Vaultwarden desde otro sitio para recuperar todo lo demás?*

Y ahí me choqué con algo peor de lo que esperaba. Mi correo de Google también está guardado ahí dentro, con una contraseña aleatoria que no sé de memoria. Así que si pierdo el móvil, tampoco puedo entrar en Google. Y como no puedo entrar en Google, tampoco puedo usar el típico "he olvidado mi contraseña" de cualquier otra web — porque ese proceso manda un correo de recuperación justo a la cuenta de Google a la que no puedo entrar.

Es un candado que se abre con la llave que está guardada dentro de la propia caja fuerte cerrada.

## Primer intento de solución (que resultó incompleto)

Fui a buscar qué hace Google para estos casos, y encontré los **códigos de backup**: diez códigos de un solo uso que puedes generar desde tu cuenta, pensados para entrar cuando no tienes el móvil a mano. Los generé desde `myaccount.google.com/signin-recovery`, guardé una captura, y pensé: ya está, ya tengo mi plan B.

Aquí está el primer tropiezo real, y quiero contarlo tal cual pasó porque creo que es fácil caer en el mismo error: **di por hecho que esos diez códigos bastaban por sí solos para entrar en la cuenta.** No es así. Buscando un poco más a fondo, resulta que esos códigos solo sustituyen al **segundo paso** de la verificación (el código que normalmente te manda el móvil), no a la contraseña. Para entrar en Google sigues necesitando la contraseña real primero — y la mía, aleatoria, solo vivía dentro de Vaultwarden.

O sea: había resuelto la mitad del candado, y ni me había dado cuenta de que la otra mitad seguía cerrada.

## Guardar los códigos en algún sitio (y encontrarme con la misma trampa otra vez)

Antes de resolver lo anterior, me quedaba un problema más inmediato: ¿dónde guardo estos diez códigos, para que sirvan el día que los necesite pero no estén a la vista de cualquiera?

Tengo una cuenta en MEGA (almacenamiento en la nube, cifrado) donde pensé en meterlos. Pero MEGA, como buen servicio serio, también tiene su propia **clave de recuperación**: si algún día olvido mi contraseña de MEGA, esa clave es la única forma de recuperar el acceso, porque ni la propia empresa puede leer mis archivos sin ella (así funciona el cifrado de extremo a extremo).

Y aquí me volví a chocar con la misma trampa: ¿dónde guardo la clave de recuperación de MEGA?

Fue en este punto cuando até cabos de verdad. Tenía varios círculos, uno metido dentro de otro, cada uno dependiendo del anterior. Esto en seguridad se llama **punto único de fallo**: un solo elemento que, si falla, se lleva todo lo demás por delante. Yo pensaba que había eliminado ese punto poniendo a Vaultwarden en el centro de todo. En realidad solo lo había movido de sitio — el nuevo punto único era "mi móvil", sin ningún plan real para el día que desapareciera.

## Sacar la última pieza fuera de la cadena digital

En algún punto de la cadena tiene que haber algo que no dependa de ningún servicio online. Algo que solo exista en mi cabeza, o en un sitio que yo controle directamente. Así que decidí juntar todo lo sensible (los códigos de Google, la clave de MEGA) en un único archivo comprimido y cifrado, con una contraseña que memorizara y que no viviera guardada en ningún otro sitio digital — ni en Vaultwarden, ni en ninguna nota.

**Nota importante sobre esto, que quiero aclarar bien:** el archivo en sí sí que está guardado en un sitio digital (Google Drive, en una cuenta secundaria aparte de la principal). Eso no es un problema. Lo que de verdad rompe la cadena no es *dónde* guardas el archivo, sino *qué hace falta para abrirlo* — y eso, la contraseña, no puede depender de ningún otro servicio online.

### Comprimir y cifrar

Fui a buscar cómo se hace un comprimido cifrado desde la terminal, y di con **7-Zip** (`p7zip` en Linux):

```bash
7z a -p -mhe=on -mx=9 claves-recuperacion.7z claves-recuperacion/
```

Desgloso cada parte, porque la primera vez que lo vi me pareció un jeroglífico:

- `a` → modo "añadir", crea el archivo comprimido
- `-p` → pide la contraseña de forma interactiva, por teclado. Esto importa: si la escribes pegada al comando, queda guardada en el historial de la terminal en texto plano
- `-mhe=on` → cifra también los **nombres** de los archivos de dentro, no solo el contenido. Sin esto, cualquiera podría ver que hay un archivo llamado "clave-mega.txt" aunque no pudiera abrirlo
- `-mx=9` → compresión máxima

El programa pide la contraseña dos veces, y aquí va el consejo que más se repite en todo este proceso: **esa contraseña se memoriza, no se apunta en ningún sitio digital.** Es el plan B para el día que pierdas todo lo demás — si viviera dentro de Vaultwarden, estarías guardando la llave de la caja fuerte dentro de la propia caja fuerte.

## El giro grande: qué meter realmente dentro del archivo

Al principio pensaba que con los códigos de backup de Google ya tenía suficiente. Ya sabemos que no — hace falta también la **contraseña real** de la cuenta. Así que el archivo cifrado terminó llevando:

- La contraseña real de mi cuenta de Google (la aleatoria, la misma que Vaultwarden generó)
- Los diez códigos de backup de Google (para el segundo paso, el 2FA)
- La clave de recuperación de MEGA

Con eso sí se cierra el círculo de verdad: contraseña + código de backup son las dos mitades que Google pide, y las dos están ahí.

## Probarlo de verdad, en mi propio móvil

Aquí está la parte que más me sirvió de todo el proceso, y que no me esperaba que fuera tan reveladora: decidí simular el escenario completo en mi propio móvil, como si fuera nuevo y no tuviera nada instalado.

El primer tropiezo llegó rápido: fui a buscar una app de escritorio en Android que abriera archivos `.7z`, y no encontré ninguna que fuera a la vez oficial (del propio proyecto 7-Zip) y de código abierto verificable. Las que aparecen buscando son de desarrolladores desconocidos — y no me pareció el momento de confiar a ciegas justo cuando voy a descifrar mis claves de recuperación más sensibles en un móvil recién comprado.

La alternativa que encontré fue usar **Termux**, una terminal completa para Android, de código abierto, que se instala desde F-Droid (un catálogo de software libre, no la Play Store). Dentro de Termux, instalé el mismo `p7zip` que uso en el servidor y descomprimí el archivo con los mismos comandos de siempre. Así no dependía de ninguna app de terceros de dudosa procedencia — usaba el mismo programa real, con los mismos comandos que ya conocía.

Y funcionó. Bajé el archivo desde la cuenta secundaria de Drive, lo descifré, y vi mis claves de recuperación reales, tal como estarían el día que de verdad las necesite. Un detalle que descubrí en la prueba y que no esperaba: en Termux, la contraseña **se ve en pantalla** mientras la escribes — a diferencia de la terminal del servidor, donde queda oculta. No es grave si estás a solas con el móvil, pero es justo el tipo de cosa que solo se descubre probando de verdad, no imaginando el proceso.

## El plan final, completo

Después de todos estos tropiezos, así queda la cadena real:

**Lo que memorizo** (tres cosas, ni una menos):
1. La contraseña de la cuenta secundaria de Google Drive, donde vive todo esto
2. La contraseña del archivo `.7z` en sí (distinta de la anterior — son dos candados separados)
3. La contraseña maestra de Vaultwarden, para cuando ya tenga acceso de nuevo

**Lo que hay guardado en Drive**, en una carpeta:
- `claves-recuperacion.7z`, cifrado: la contraseña real de Google, sus diez códigos de backup, la clave de recuperación de MEGA
- Un archivo de instrucciones, sin cifrar (no lleva ningún dato sensible, así que no hace falta esconderlo): los pasos exactos para el día que haga falta usar todo esto, incluido lo de instalar Termux, probado y escrito de forma que no tenga que recordar ningún comando — solo saber que la nota existe y dónde está.

## Lo que me llevo de todo esto

Cuando monté Vaultwarden pensaba que había resuelto "tener las contraseñas seguras". Y en parte sí. Pero había confundido "seguro frente a un atacante" con "seguro frente a cualquier cosa que pueda pasar" — y son cosas distintas.

Lo que de verdad aprendí no es tanto la parte técnica, sino esto: cada vez que blindas algo, hay que mirar qué hace falta para recuperarlo si ese blindaje falla — y seguir mirando, un paso más allá, qué hace falta para recuperar *eso*. En algún punto tiene que haber algo que no dependa de nada más: algo que memorices, fuera de toda cadena digital.

Y la otra cosa, la que más me costó aceptar: no basta con que el plan "parezca" que funciona sobre el papel. Dos veces di algo por resuelto (los códigos de backup, la app para abrir el `.7z`) y las dos veces estaba equivocado en algún detalle. Solo probándolo de verdad, paso a paso, en un móvil real, supe que el plan funciona tal como lo he contado aquí.

---

*Este post es el primero de una pequeña serie sobre seguridad y recuperación de acceso. En el siguiente cuento cómo automaticé también el backup cifrado de la base de datos del servidor — y un aviso que no esperaba: hasta las herramientas de seguridad tienen fecha de caducidad.*
