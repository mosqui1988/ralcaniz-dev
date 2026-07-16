---
title: "Me monté mi propio gestor de contraseñas (y aprendí más de lo que esperaba por el camino)"
date: 2026-07-15T23:00:00+02:00
draft: false
---

Hay proyectos que parecen sencillos hasta que te metes dentro. Este era uno de esos: "instalar un gestor de contraseñas en mi servidor", una frase que suena a tarde tranquila. Al final me llevó por Docker, certificados HTTPS, un navegador que me llamó mentiroso a la cara, y terminé automatizando algo que ni sabía que había que automatizar. Este es, de momento, el post más largo que he escrito aquí — y también el que más he disfrutado, porque es de los que más me ha costado entender de verdad, no solo copiar y pegar.

Aviso para quien llegue nuevo: no hace falta que memorices ni un solo comando de los que salen aquí. Yo tampoco me los sé de memoria. Para eso existe la documentación (la oficial, y la mía propia, que voy dejando en este blog) — lo importante es entender el porqué de cada pieza, no tener la terminal grabada en la cabeza.

## El punto de partida

Llevaba un tiempo con esta idea aparcada. La había dejado a un lado porque le faltaba una pieza concreta: un SSD decente en mi servidor casero, un Lenovo de hace once años que ya os presenté en otro post. En cuanto cerré esa migración, tocaba retomarlo.

El objetivo: un gestor de contraseñas propio, que viva en mi hardware, accesible solo desde mis dispositivos, sin depender de la nube de ninguna empresa. Se llama **Vaultwarden**.

## Por qué Vaultwarden y no "Bitwarden" a secas

Bitwarden es un gestor de contraseñas conocido, con su propio servidor en la nube. Vaultwarden es otra cosa: una reimplementación no oficial de ese mismo servidor, hecha por la comunidad, en un lenguaje (Rust) pensado para ser ligero. Tan ligero que corre sin problema en un mini PC de segunda mano como el mío, en vez de necesitar la infraestructura pensada para millones de usuarios que tiene el servidor oficial.

Lo bonito es que las apps oficiales de Bitwarden —la extensión del navegador, la app del móvil— no notan la diferencia. Hablan el mismo idioma. Solo hay que decirles "oye, no uses el servidor de la empresa, usa el mío".

## La base: una cajita aislada llamada contenedor

Para instalar Vaultwarden usé Docker, la misma herramienta que ya tenía funcionando en el servidor para otro proyecto (Syncthing, el sistema de backup de fotos). La idea de Docker, explicada sin tecnicismos: en vez de instalar un programa directamente sobre el sistema operativo —donde si algo sale mal puede arrastrar cosas que no tienen nada que ver—, lo metes en una especie de cajita aislada, con todo lo que necesita ya empaquetado dentro. Si algo se rompe, borras la cajita y ya está. El resto del servidor ni se entera.

```
┌───────────────────────────────────────────┐
│                MI SERVIDOR                │
│                                           │
│   ┌─────────────┐      ┌─────────────┐    │
│   │  Contenedor │      │  Contenedor │    │
│   │  Syncthing  │      │ Vaultwarden │    │
│   │  (fotos)    │      │(contraseñas)│    │
│   └─────────────┘      └─────────────┘    │
│                                           │
│   Cada uno aislado del otro y del sistema.│
└───────────────────────────────────────────┘
```

## La pieza de seguridad de verdad: que no exista fuera de mi red

Aquí está la decisión que más me importaba tomar bien: que este servicio, que guarda literalmente todas mis contraseñas, no fuera alcanzable desde cualquier dispositivo de mi WiFi de casa, y muchísimo menos desde internet abierto.

La solución fue **Tailscale**, una red privada virtual que ya tenía montada entre mis dispositivos desde hace tiempo. Le dije a Docker que publicara el puerto de Vaultwarden únicamente en la dirección de Tailscale de mi servidor, nunca en la de mi red local.

```
   Alguien en mi WiFi de casa          Mi propio móvil, dentro
   intenta acceder                       de mi red Tailscale
          |                                      |
          v                                      v
   [X] Nadie responde ahí              [OK] Vaultwarden contesta
   (el puerto no existe                 (autenticado, dentro
    en esa dirección)                    del túnel privado)
```

Esto significa que aunque alguien entrara en mi WiFi (algo que, por otro lado, ya tengo bastante cerrado desde hace tiempo), ese puerto sencillamente no existe para ellos. Solo mis propios dispositivos, ya autenticados en mi red Tailscale, pueden llegar hasta ahí.

## El navegador me llamó mentiroso

Con todo montado —contenedor arriba, puerto bien publicado, datos guardándose en el SSD de forma persistente—, entré al navegador esperando ver la pantalla de bienvenida. Lo que vi fue esto:

> "No estás usando un contexto seguro, necesario para que funcione la API de criptografía. Necesitas activar HTTPS."

Mi primera reacción fue de indignación un poco infantil: "¿cómo que no es seguro? ¡Está dentro de mi propia VPN cifrada!". Y tenía razón, pero el navegador no tenía forma de saberlo.

Aquí aprendí algo que no sabía: cuando usas un gestor de contraseñas, el cifrado y descifrado de tus datos ocurre **en tu propio navegador**, no en el servidor. El servidor nunca llega a ver tus contraseñas en texto plano. Para poder hacer esa magia criptográfica, el navegador exige estar en lo que llama un "contexto seguro": o bien una dirección que empiece por `https://` con un certificado válido, o bien `localhost`. Mi conexión por `http://` a secas, aunque viajara dentro de un túnel privado cifrado, no contaba como tal — el navegador simplemente mira el principio de la URL, no lo que hay detrás.

## Certificados HTTPS gratis, sin salir de mi propia red

Esto es lo que más me sorprendió de toda la sesión: no hacía falta montar un sistema complicado de certificados propios. **Tailscale puede generarte certificados HTTPS reales** —firmados por Let's Encrypt, los mismos que usa cualquier web seria de internet— para un nombre de dominio especial que solo existe dentro de tu propia red privada. Nada expuesto a internet, y aun así con el candado verde de "conexión segura" que el navegador exige.

Antes de activarlo tuve que decidir algo: activar esta función deja anotado el nombre de tu máquina en un registro público llamado *Certificate Transparency Log*. Suena más alarmante de lo que es — es un mecanismo estándar de toda la industria para poder detectar certificados falsos (alguien haciéndose pasar por un banco, por ejemplo), y lo único que queda público es el nombre, nunca la IP real ni ningún tipo de acceso. Con esa información decidí seguir adelante.

Generé el certificado con un único comando desde el propio servidor, lo monté en el contenedor... y volví a fallar. Pero de una forma que, mirando atrás, tiene gracia.

## El tropiezo del puerto equivocado

Di por hecho que al activar HTTPS, el puerto interno donde escuchaba Vaultwarden cambiaría automáticamente. No cambió. Seguía siendo el de siempre, solo que ahora hablando en HTTPS en vez de HTTP. Yo estaba intentando entrar por el puerto que había supuesto sin comprobarlo, y ahí no había nadie escuchando.

Lo que me salvó fue no fiarme del primer vistazo ("el contenedor está arriba, debería funcionar") y mirar los **logs** del contenedor — el registro real de lo que estaba pasando por dentro. Ahí estaba la respuesta, clarísima: el programa decía exactamente en qué dirección y puerto había arrancado. No coincidía con lo que yo estaba usando.

Ajustado el mapeo de puertos, volví a intentarlo: candado verde, pantalla de login cargando sin quejas. La lección se queda grabada más que el comando en sí: **cuando algo no funciona, mira los logs antes de suponer nada**.

## Un servidor, dos dispositivos, mismo tropiezo repetido (con premio)

Con el servidor ya funcionando bien, tocaba conectar mis dispositivos reales:

- **La extensión del navegador en mi PC**: hay que decirle, antes de iniciar sesión, que no use el servidor oficial de la empresa, sino el mío propio. Es una opción que suele llamarse "entorno self-hosted" o similar.
- **La app oficial en el móvil**: mismo concepto... pero aquí volví a tropezar con la misma piedra del puerto. Al escribir la dirección de mi servidor en el móvil, se me quedó sin el número de puerto al final. La app, sin ese dato, asumió el puerto estándar de HTTPS por defecto — y ahí, de nuevo, no había nadie escuchando. Un mensaje de error bastante técnico y feo en pantalla, pero la causa real era tan sencilla como un número que faltaba al final de una dirección.

Con eso corregido, llegó la prueba que de verdad importaba: guardé una entrada de contraseña de prueba desde el móvil, y en cuestión de segundos apareció también en la extensión de mi PC. Misma bóveda, dos ventanas distintas mirando al mismo sitio.

## Quién decide qué rellena mis contraseñas

Hay un detalle de Android que no existe en un ordenador normal: el sistema decide, de forma centralizada, qué aplicación se encarga de rellenar contraseñas en el resto de apps del móvil, no solo dentro del propio gestor. Por defecto, mi teléfono tenía elegida la opción de la propia marca del fabricante. Tuve que entrar en los ajustes y decirle explícitamente que a partir de ahora prefiero que sea mi propio Vaultwarden quien se encargue de eso.

## El detalle que casi se me escapa: los certificados caducan

Aquí estuve a punto de cerrar la sesión pensando que ya estaba todo hecho. Un certificado HTTPS de estos no dura para siempre — caducan cada 90 días, por diseño, como medida de seguridad de toda la industria (cuanto menos tiempo vive un certificado, menos daño puede hacer si alguna vez se compromete).

Mi primer instinto fue apuntarme un recordatorio manual para renovarlo antes de esa fecha. Pero pensándolo un poco más: eso solo resuelve esta renovación concreta. Dentro de tres meses volvería a tener el mismo problema, con otra fecha distinta que recordar, para siempre.

La solución de verdad era quitarme a mí mismo de la ecuación. Escribí un script pequeño —dos líneas, nada del otro mundo— que pide la renovación del certificado y reinicia el contenedor para que la use. Lo programé para que se ejecute solo, una vez al mes, de madrugada, usando una herramienta de Linux llamada `cron` (viene a ser el "reloj despertador" del sistema).

```
   Día 1 de cada mes, 4:00 AM
          |
          v
   ¿Le queda al certificado más de 30 días de vida?
          |
    ┌─────┴─────┐
    |           |
   Sí           No
    |           |
    v           v
  No hace     Lo renueva
  nada         y reinicia
              el contenedor
```

Como los certificados duran 90 días y esto se comprueba cada 30, siempre hay de sobra margen para renovar antes de que caduque de verdad — nunca se llega al filo. Y lo mejor: no he tenido que anotar ninguna fecha en ningún sitio. El propio sistema se acuerda por mí, para siempre.

## Un lío de nombres que tenía que aclarar

Con todo ya funcionando, me quedé pensando en algo que llevaba días sin terminar de encajar: ¿esto es Bitwarden o es Vaultwarden? Los usaba como si fueran la misma palabra, y no lo son.

Al final es más simple de lo que parece:

```
   BITWARDEN                          VAULTWARDEN
   (el cliente)                        (el servidor)

   La app del móvil,          →       El programa que instalé
   la extensión del                    en mi propio servidor,
   navegador. Lo que                   que guarda de verdad
   yo toco y veo.                      los datos cifrados.
```

Vaultwarden es una versión hecha por la comunidad del servidor de Bitwarden, pensada para poder instalarse en un ordenador modesto como el mío en vez de necesitar la infraestructura de una empresa entera. Y lo bueno es que la app oficial de Bitwarden no nota ninguna diferencia — simplemente le dices "oye, no hables con el servidor de la empresa, habla con el mío", y a partir de ahí todo funciona exactamente igual que si fuera el servicio original.

## La prueba de fuego: usarlo de verdad, no solo mirarlo

Tenía todo montado, pero montado no es lo mismo que entendido. Así que decidimos hacer la prueba tonta que de verdad aclara las cosas: registrarme en una web cualquiera y ver el proceso completo, de principio a fin, con mis propias manos.

Elegí Mastodon, una red social sin más motivo que ser un sitio real y sin complicaciones. Me registré con usuario y contraseña normales, sin usar todavía el generador de Bitwarden — y ahí me di cuenta de algo importante en el momento: la gracia de un gestor de contraseñas no es que guarde una contraseña que tú te inventas, es que te genere una que ni tú mismo podrías recordar ni adivinar. Contraseñas del tipo de letras, números y símbolos sin ningún patrón, imposibles de repetir en dos sitios distintos. Ese es el paso que de verdad marca la diferencia frente a "la de siempre con un número al final".

## El tropiezo que más rabia me dio (y el más útil)

Con la cuenta ya creada, tocaba comprobar la otra mitad de la magia: que al volver a esa web, Bitwarden me rellenara usuario y contraseña sin que yo tuviera que buscar nada. Y no pasaba nada. Ni un aviso, ni una sugerencia, nada.

Aquí es donde me tocó hacer de detective un rato, buscando por varios sitios y comparando lo que iba encontrando con lo que veía en mi propia pantalla. Fui descartando cosas por pasos:

Primero miré los ajustes de contraseñas del propio Android. Ahí Bitwarden ya estaba puesto como servicio preferido, correcto — pero, sin yo haberlo pedido, Samsung Pass y Google seguían activados también como "servicios adicionales". Con tres candidatos compitiendo por el mismo campo de texto, ninguno terminaba de saltar. Los desactivé, dejando solo Bitwarden.

Seguía sin funcionar. El verdadero culpable estaba un nivel más abajo, dentro del propio navegador: Brave tiene su propio ajuste interno de autocompletado de contraseñas, separado del de Android, y estaba pisando por completo al del sistema. En cuanto entré en la configuración del navegador y lo cambié para que usara el servicio de Android en vez del suyo propio, todo empezó a funcionar a la primera.

La lección de este tropiezo, más que el ajuste concreto, es esta: cuando algo "no funciona" en el móvil, no siempre es un único culpable — a veces hay varias capas superpuestas (el sistema, el navegador, la propia app) y cada una puede estar decidiendo cosas por su cuenta. Hay que ir descartando una a una, no rendirse en la primera.

## Sobre la parte de "buscar y preguntar"

Para llegar hasta aquí no me lo sabía todo de antemano, ni mucho menos. Fui buscando, comparando lo que leía con lo que tenía delante en la pantalla, y usando la IA como apoyo real durante todo el proceso — no como una varita mágica que resuelve sola, sino como alguien con quien ir pensando en voz alta y contrastando ideas.

Y aquí va algo que tengo cada vez más claro: la IA ya forma parte del día a día de cualquiera que esté aprendiendo esto, y es una herramienta buenísima — pero no hace el trabajo sola. Si le das poco contexto, o le preguntas mal, te puede llevar por un camino equivocado sin que te des cuenta hasta más tarde. Lo que de verdad marca la diferencia es explicar bien la situación real, revisar lo que te propone antes de aplicarlo a ciegas, y no dar nunca por hecho que "como me lo ha dicho la IA, seguro que es así". Es una herramienta más, muy potente, pero herramienta al fin y al cabo — el criterio lo sigo poniendo yo.

## Lo que me llevo de esta sesión

Repasando todo lo de hoy, ninguna pieza por separado era tremendamente difícil. Lo que sí me costó fue encadenarlas todas sin perderme: un contenedor aislado, una red privada, un certificado válido dentro de esa red, dos clientes distintos hablando con el mismo servidor, entender de una vez qué es Bitwarden y qué es Vaultwarden, y por último cazar un tropiezo de autocompletado escondido entre tres capas distintas del móvil.

Si algo me llevo de verdad es esto: no hace falta saberse todos los comandos de memoria para entender lo que estás construyendo. Yo, a día de hoy, no recuerdo la sintaxis exacta de `tailscale cert` sin mirar mis propias notas — y no pasa nada, para eso las escribo. Al principio los comandos se me hacían cuesta arriba, como si tuviera que memorizarlos todos para no quedarme atascado. Pensándolo ahora, no es para tanto: internet está lleno de documentación, y entre eso y saber preguntar bien, se llega a cualquier sitio sin necesidad de tenerlo todo en la cabeza. Lo que sí tengo claro, y eso es lo que de verdad importa, es *por qué* cada pieza está donde está: por qué el puerto solo existe en una interfaz y no en otra, por qué el navegador exigía HTTPS, por qué un script mensual es mejor que un recordatorio manual, por qué un tropiezo de autocompletado puede tener tres culpables distintos a la vez.

Mi bóveda de contraseñas vive ya en mi propio servidor, sin depender de nadie más, y además sé usarla de verdad — no solo tenerla instalada. Toca ahora ir metiendo contraseñas nuevas poco a poco, cambiando las viejas por otras generadas de verdad, según las vaya usando — sin prisa, que para eso ya no dependo de acordarme de nada a mano.
