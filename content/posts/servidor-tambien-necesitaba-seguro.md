---
title: "El servidor también necesitaba su propio seguro"
date: 2026-07-18T12:30:00+02:00
draft: false
---

En el post anterior conté cómo descubrí un agujero real en mi plan de seguridad: si perdía el móvil, me quedaba sin poder entrar en nada, ni siquiera en mi propio correo. Lo resolví con un archivo cifrado, guardado en un sitio aparte, que rompe esa cadena.

Pero mientras resolvía eso, me quedó una pregunta rondando: ¿y si el problema no es que yo pierdo el acceso, sino que es el propio servidor el que deja de existir? Un fallo de disco, un cortocircuito, lo que sea — mi servidor casero es un ordenador de segunda mano de hace más de diez años, comprado por 40 euros. No tiene garantía de fabricante que valga nada. Si un día simplemente no vuelve a encender, ahí dentro estaba toda mi base de datos de contraseñas, sin ninguna copia en ningún otro sitio.

Así que me puse a automatizar un backup semanal, cifrado, subido a la nube. Aviso como siempre: no me sé estos comandos de memoria, cada cosa la fui buscando según la necesitaba.

## Por qué no basta con copiar el archivo sin más

La base de datos de Vaultwarden es un archivo SQLite — un tipo de base de datos que, en vez de necesitar un servidor aparte, es simplemente un archivo. Pero Vaultwarden la usa en un modo llamado **WAL** (*Write-Ahead Log*): las escrituras más recientes no se guardan directamente en el archivo principal, sino en uno aparte que espera a "asentarse" más adelante.

Esto significa que si copio solo el archivo principal con un `cp` normal, mientras el programa sigue funcionando, puedo llevarme una copia incompleta — me faltarían las últimas escrituras, las que todavía estaban esperando en el archivo auxiliar.

Busqué cómo resolver esto bien, y encontré el comando adecuado: `sqlite3` tiene un modo `.backup` que sabe fusionar ambos archivos de forma segura, incluso con el programa funcionando en ese mismo instante:

```bash
sqlite3 /ruta/a/db.sqlite3 ".backup '/ruta/temporal/copia.sqlite3'"
```

Una fotografía nítida, en vez de una foto movida.

## Cifrar antes de subir

Con la copia ya hecha, tocaba cifrarla antes de mandarla a ningún sitio externo — nunca subir una base de datos de contraseñas en plano a una nube, por mucho que esa nube prometa ser segura. Usé **GPG**, una herramienta de cifrado muy extendida en el mundo Linux:

```bash
gpg --batch --yes --passphrase-file /ruta/a/mi-contraseña \
    --symmetric --cipher-algo AES256 \
    mi-copia.sqlite3
```

`--symmetric` significa que se usa una sola contraseña para cifrar y descifrar, a diferencia del cifrado con un par de claves pública/privada, pensado para cuando alguien más te manda archivos cifrados a ti. Aquí no hace falta: solo necesito recuperarlo yo mismo.

La contraseña la guardé en un archivo aparte, con permisos muy restringidos, en vez de escribirla directamente dentro del script — así, si algún día comparto ese script con alguien, la contraseña no viaja pegada a él.

## Subir con rclone, sin pantalla

Para subir el archivo cifrado a Google Drive desde el servidor —que no tiene pantalla ni navegador, solo se controla por línea de comandos— usé una herramienta llamada **rclone**, una especie de gestor de archivos para la nube controlable desde la terminal.

Configurar rclone contra Google Drive tiene una vuelta curiosa cuando el ordenador no tiene navegador: el proceso de autorización de Google normalmente abre una ventana para que inicies sesión. Como mi servidor no tiene pantalla, tuve que empezar la configuración ahí, decirle que no tenía navegador disponible, copiar el comando que me dio y ejecutarlo en mi otro ordenador (que sí tiene pantalla), iniciar sesión ahí, y traer de vuelta el código de autorización al servidor.

## El aviso que no esperaba: hasta las herramientas de seguridad caducan

Mientras probaba que todo funcionaba, rclone me soltó un aviso que no vi venir: la identidad que usa por defecto para hablar con Google Drive —compartida entre todos los usuarios de rclone del mundo— se está retirando durante este año, y en algún momento dejará de funcionar sin previo aviso exacto.

Me costó decidir si merecía la pena pararlo todo por esto. Al final pensé: no tiene sentido montar un sistema de seguridad que puede romperse solo, en silencio, dentro de unos meses, justo el día que menos lo esperas. Así que antes de seguir, me puse a crear mi **propia identidad de aplicación** en Google Cloud, un trámite gratuito que consiste, a grandes rasgos, en:

- Crear un proyecto nuevo en la consola de Google Cloud
- Activar ahí la API de Google Drive
- Configurar una "pantalla de consentimiento", diciéndole a Google que esta aplicación solo la voy a usar yo mismo
- Crear unas credenciales propias, de tipo "aplicación de escritorio"
- Volver a rclone y decirle que usara esta identidad propia en vez de la compartida

Con eso, mi backup ya no depende de una pieza compartida que puede desaparecer sin avisar.

## Programarlo solo, y comprobar que de verdad funciona

Con todas las piezas montadas, até el script al **crontab** —el programador de tareas de Linux— para que corriera solo, cada domingo a las 4 de la madrugada, sin que yo tuviera que acordarme:

```
0 4 * * 0 /ruta/al/script/backup-vaultwarden.sh
```

Y aquí quiero remarcar algo que aprendí y que me parece la parte más importante de todo esto: **un backup que nunca has probado a restaurar no es un backup, es una esperanza.** Así que antes de darlo por bueno, hice la prueba completa al revés: bajé el archivo subido, lo descifré con la misma contraseña, y comprobé que la base de datos resultante era legible de verdad, no solo que "existía":

```bash
sqlite3 db-recuperada.sqlite3 "SELECT count(*) FROM users;"
```

Me devolvió un `1` — mi único usuario, intacto. Solo entonces di el proceso por cerrado.

## El segundo tropiezo del día: la llave de emergencia que no era la llave

Con el backup ya funcionando, me quedaba un cabo suelto que había ignorado hasta entonces: Vaultwarden tiene un panel de administración aparte del login normal, protegido por un valor llamado `ADMIN_TOKEN`. Es una puerta de emergencia real: si algún día el segundo factor de mi propia cuenta me bloqueara a mí mismo, desde ese panel puedo desactivarlo manualmente. Es una ventaja que solo tiene sentido porque el servidor es mío — un usuario normal de un Bitwarden en la nube no podría hacer nada parecido.

El problema es que, al mirar mi configuración, solo tenía guardado el **hash** de ese token, no el token real. Un hash es el resultado de un cálculo que no se puede deshacer — es la gracia de cómo funciona: sirve para comprobar que algo coincide, pero no permite recuperar el original a partir de él. Así que si alguna vez tuve el token real en algún sitio, ya no lo tenía en ningún lado accesible.

No quedaba otra que generar uno nuevo. Con `openssl` saqué un valor aleatorio, y con una herramienta que trae el propio Vaultwarden generé su hash correspondiente, para meterlo en la configuración del servidor.

### El fallo silencioso de los símbolos de dólar

Al meter el hash nuevo en el archivo de configuración del contenedor (un `docker-compose.yml`, que de paso escribí para dejar toda la configuración del servidor documentada en un solo sitio, algo que no tenía hasta ese momento), probé a entrar en el panel de administración y me dio error: "Invalid admin token".

Probé varias veces, hasta que Vaultwarden, con buen criterio, me bloqueó temporalmente por exceso de intentos fallidos —una protección normal contra quien intente adivinar el token a base de probar.

El motivo del fallo resultó ser algo pequeño pero con truco: el símbolo `$`, que el hash de mi token lleva varias veces, tiene un significado especial dentro de un archivo de este tipo. El programa que lee la configuración lo interpreta como el inicio de una variable, e intenta sustituirlo por algo que no existe — dejando ese trozo vacío, sin avisar de ningún error. Mi hash, lleno de símbolos `$`, se estaba rompiendo en silencio cada vez que el archivo se leía.

La solución fue escribir cada símbolo `$` por duplicado (`$$`) dentro de ese archivo concreto. Y aun así tardé dos intentos en arreglarlo del todo: la primera corrección solo tapó parte de los símbolos, se me quedó uno suelto sin duplicar, cerca del final de la cadena, y el archivo se seguía cortando en el mismo punto. Solo comparando con calma, carácter a carácter, el hash guardado contra el original, encontré el que faltaba.

Fue un rato de cabezazos por algo tan pequeño como un símbolo de puntuación. Pero es exactamente el tipo de detalle que solo se aprende chocándose con él — ninguna guía genérica te avisa de esto, porque depende de la combinación exacta de herramientas que estés usando.

## Lo que me llevo de esta segunda parte

Si el primer post iba de "cada blindaje necesita su propio plan B", este añade otra capa: **incluso las piezas de infraestructura que sostienen ese plan B tienen sus propios puntos débiles** —una identidad compartida que caduca sin avisar, un símbolo de puntuación que rompe un archivo en silencio. No es que el trabajo de blindarse termine nunca del todo; es que cada vuelta que le das revela una capa más.

Y la lección práctica, otra vez: probarlo de verdad. No solo montar el backup, sino restaurarlo. No solo generar el token nuevo, sino entrar de verdad con él en el panel antes de darlo por bueno. Las dos veces que lo hice, encontré algo que no funcionaba como esperaba.

---

*Con esto queda cerrado, por ahora, el bloque de seguridad y recuperación de cuentas: un archivo cifrado con lo esencial para entrar de nuevo en todo si pierdo el acceso, un backup semanal automático de las contraseñas del servidor, y las instrucciones escritas para no tener que recordar ningún paso el día que de verdad haga falta.*
