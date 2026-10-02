---
title: "Una tormenta, un certificado a punto de caducar y un simulacro de catástrofe"
date: 2026-10-02T21:58:04+02:00
draft: false
description: "Una tarde de tormenta reinició mi servidor siete veces. Al revisar que todo seguía bien encontré un certificado que caducaba en once días, un backup que 'no existía' y una pregunta incómoda: si mañana se rompe el servidor, me roban el móvil o pasa algo peor, ¿de verdad podría recuperar mis contraseñas?"
---

Ayer hubo tormenta y en casa se fue la luz unas cuantas veces. Mi servidor no tiene SAI (una batería que lo mantenga encendido durante los cortes), así que con cada apagón se iba, y con cada vuelta de la luz arrancaba solo. Lo sé porque me llegaron cuatro correos seguidos con el asunto **"[server] Servidor reiniciado"**: el [aviso que monté hace unas semanas](/posts/aviso-reinicio-servidor-msmtp/) funcionó justo cuando tenía que funcionar.

Al día siguiente pensé: después de tanto encendido y apagado de golpe, ¿estará todo bien? Así que hice una revisión completa. Y sí, todo arrancaba. Pero salieron tres cosas que no esperaba.

## Lo que revisé

Nada del otro mundo, es lo que miraría cualquiera:

- **Los contenedores** (las cajitas de Docker donde corre cada programa): si están encendidos, si están "sanos" y si arrancan solos cuando el servidor se reinicia.
- **Los discos**: espacio libre y que el disco externo de las fotos siga montado.
- **Los servicios del sistema**: si alguno ha fallado.
- **El historial de arranques**, con `last -x reboot`. Este comando enseña cada vez que el servidor ha arrancado, y si antes se apagó bien o de golpe.

Lo del historial me dio un pequeño susto: siete arranques en una tarde, todos marcados como `crash`. Pero `crash` aquí no significa que algo se haya roto. Significa que el servidor no se apagó "con educación", cerrando sus cosas antes de apagarse. Que es exactamente lo que pasa cuando le quitas la luz. Con la tormenta, cuadraba.

Hasta ahí, todo bien. Lo interesante vino después.

## Sorpresa 1: un certificado que caducaba en once días

Mi gestor de contraseñas (Vaultwarden) funciona con HTTPS, y para eso necesita un **certificado**: una especie de carné que demuestra que el servidor es quien dice ser. El mío lo emite Tailscale gratis y **dura unos 90 días**. Al revisarlo:

```bash
openssl x509 -enddate -noout -in server.crt
```

Este comando abre el certificado y enseña su fecha de caducidad (`notAfter`). Y salía **13 de octubre**. Once días.

"No pasa nada, tengo un script que lo renueva solo el día 1 de cada mes", pensé. Y efectivamente, el 1 de octubre se ejecutó. Pero en su registro ponía esto:

```
Public cert unchanged
```

"Certificado sin cambios." Tailscale decidió que todavía no tocaba renovarlo. Y el siguiente intento sería el 1 de noviembre… con el certificado ya caducado desde el 13 de octubre. A partir de ese día, la app de contraseñas de mi móvil se habría negado a conectar.

El fallo no estaba en el script, sino en **cada cuánto** se ejecutaba. Un intento al mes para algo que solo se renueva en una ventana corta antes de caducar es jugar a la lotería. La solución:

1. Renovarlo a mano en ese momento. Ahora caduca a finales de diciembre.
2. Cambiar la tarea programada de "el día 1 de cada mes" a **"cada miércoles"**. Si no toca renovar, no pasa nada: dice "sin cambios" y listo. Pero nunca más va a llegar tarde.

Las tareas programadas se definen en el `crontab` con cinco campos de tiempo, y me ayudó mucho aprender a leerlos:

```
 ┌──────── minuto (0)
 │ ┌────── hora (4 de la mañana)
 │ │ ┌──── día del mes (* = cualquiera)
 │ │ │ ┌── mes (* = cualquiera)
 │ │ │ │ ┌ día de la semana (3 = miércoles)
 0 4 * * 3  renovar-cert.sh
```

Antes ponía `0 4 1 * *`: "a las 4:00 del día 1". Un número cambiado y problema resuelto.

### El tropiezo de turno

Para esto hacía falta `sudo` (permisos de administrador), así que me tocaba ejecutarlo a mí desde una terminal. Abro la terminal, pego los comandos, pongo mi contraseña y…

```
sudo: /home/ruben/vaultwarden/renovar-cert.sh: command not found
```

¿Cómo que no existe? Llevo semanas con ese script… **en el servidor**. Yo estaba en la terminal de mi ordenador. Me había saltado el primer paso, el `ssh` para conectarme al servidor. El ordenador buscaba un archivo que nunca había tenido.

Lección rápida: antes de pegar un comando, mira el prompt. Si no pone `ruben@server`, no estás donde crees.

## Sorpresa 2: el backup que "no existía"

Durante la revisión, al buscar los backups de las contraseñas, solo apareció una copia semanal **en el mismo disco del servidor**. Eso no es un backup de verdad: si se rompe el disco, se van el original y la copia a la vez. Busqué en mi Google Drive el backup cifrado que, según mis notas, se subía cada semana… y nada.

Al revisar las tareas programadas del administrador del sistema (root) apareció:

```
0 4 * * 0  backup-vaultwarden.sh
```

Cada domingo a las 4:00. Existía, solo que lo sube a **una cuenta secundaria de Google**, no a la principal. Por eso no lo encontraba. El registro lo confirmó: "Backup completado con éxito" todos los domingos.

El script, por cierto, está mejor montado de lo que recordaba:

1. Hace una copia de la base de datos con `sqlite3 .backup`. Es una forma de copiarla "en caliente" sin pillarla a medio escribir.
2. La **cifra** con GPG (AES256), como meterla en una caja fuerte.
3. La sube a Drive con `rclone`.
4. Guarda las 30 últimas copias y borra las más viejas.

## Sorpresa 3: la pregunta incómoda

Aquí llegó la parte que más me ha hecho pensar. Para abrir esa caja fuerte cifrada hace falta una **llave** (una contraseña). ¿Y dónde estaba esa llave? En un archivo… **dentro del propio servidor**.

```
   💥 Se rompe el servidor
        │
        ├── Gestor de contraseñas ...... perdido
        ├── Llave de la caja fuerte .... perdida (estaba en el servidor)
        │
        └── ☁️ Drive: la caja fuerte sigue ahí, a salvo
                 │
                 └── ¿Con qué la abro? 🔑 ❓
```

Tenía el backup perfecto de una caja fuerte que, el día que la necesitara, no podría abrir. Así que la llave a papel, y el papel a un sitio de casa.

## El simulacro

Apuntar la llave está muy bien, pero ¿la apunté bien? Un papel con un carácter mal copiado vale lo mismo que no tener papel. Así que hicimos una **prueba de restauración**: un script que:

1. Descarga de Drive la copia más reciente.
2. Me pide la contraseña, que escribo **leyéndola del papel** y no copiándola del servidor. Esa es la gracia.
3. Abre la base de datos y comprueba que está entera y cuántas entradas tiene.
4. Borra todo lo descargado al terminar.

Resultado:

```
✅ Descifrada: la contraseña apuntada es correcta.
Integridad:       ok
Entradas:         25
```

Mis 25 contraseñas, sacadas de un backup en la nube y abiertas con una llave escrita a boli.

## La cadena completa

Con el simulacro superado me hice la pregunta definitiva: si mañana el servidor desaparece, ¿qué necesito para llegar hasta mis contraseñas? Lo dibujé:

```
 🧠 De memoria                         📄 En papel
 ├─ Cuenta secundaria de Google ──┐    │
 │                                ▼    ▼
 │                        ☁️ Drive → 🔓 Backup descifrado
 │                                         │
 └─ Contraseña maestra del gestor ─────────┴──► ✅ Todas las demás
```

Solo tengo que recordar **dos contraseñas**, y una más en papel. Todas las demás (las de verdad, las aleatorias de 20 caracteres) viajan dentro del backup.

Al dibujarlo apareció un último eslabón débil: la **verificación en dos pasos** de Google. Si en el desastre pierdo también el móvil, Google me pediría un código que no podría recibir. La solución son los **códigos alternativos**: diez códigos de un solo uso que Google te da para estos casos. Van al mismo papel, de las dos cuentas.

## Jugando a lo peor

Con la cadena dibujada, me puse en modo catastrofista y repasé un desastre detrás de otro. No para asustarme, sino para encontrar dónde se rompería la cadena antes de que se rompa de verdad.

| Qué pasa | ¿Pierdo mis contraseñas? | Por qué |
|---|---|---|
| Se muere el servidor | No | Backup en Drive + llave en papel. Mientras tanto, la app del móvil guarda una copia que se puede consultar sin conexión (siempre que no cierre sesión) |
| Me roban el móvil | No | Las contraseñas están en el servidor, y los códigos alternativos sustituyen al móvil en la verificación de Google |
| Se muere el servidor y me roban el móvil a la vez | No | Cuenta secundaria de memoria + códigos alternativos del papel → Drive → backup → llave del papel |
| Alguien entra en mi cuenta de Drive | No se lleva nada útil | Solo ve cajas fuertes cifradas. Sin la llave del papel, son ruido |
| Alguien encuentra el papel | Tampoco le basta | Tiene la llave, pero no la caja: le faltan mi cuenta de Google y mi contraseña maestra, que no están escritas en ningún sitio |
| Se quema la casa (servidor y papel) | Aquí sí me la juego | Me quedaría la copia del móvil, si sobrevive. El siguiente paso sería tener una segunda copia del papel fuera de casa |

Lo que más me gustó de este ejercicio es ver que **ninguna pieza sola sirve de nada**. El backup sin la llave es ruido. La llave sin el backup es un papel con letras raras. Y las dos juntas siguen sin servir sin la contraseña maestra, que solo está en mi cabeza. Para entrar hace falta juntarlo todo, y eso solo puedo hacerlo yo.

La fila de la casa quemada se queda como deberes. Es poco probable, pero ahora sé exactamente qué me faltaría.

Y para no depender de acordarme de nada de esto en un momento de nervios, escribí una **guía de emergencia** paso a paso, desde instalar el sistema de cero hasta volver a entrar en el gestor. Está impresa junto al papel y guardada también en la cuenta secundaria de Drive.

## Lo que me llevo

Que **un backup que nunca has restaurado no es un backup, es una esperanza.** Hasta hoy yo "tenía backup". Ahora sé que funciona, porque lo he abierto.

Que las tareas automáticas también hay que revisarlas. El script del certificado llevaba meses funcionando "bien", y casi me deja tirado por algo tan tonto como su calendario.

Y que el sitio donde guardas la llave importa tanto como la caja fuerte. Si la llave vive dentro de lo que quieres proteger, en realidad no tienes llave.

Lo próximo, cuando el presupuesto lo permita: un SAI para que la próxima tormenta no me reinicie el servidor siete veces en una tarde.
