+++
date = '2026-07-04T16:16:20+02:00'
draft = false
title = 'Instalé Moonlight en mi tele LG sin levantarme del sofá (y sin mando)'
+++

Llevo un tiempo jugando en remoto a mi PC desde la Ayn Thor con Moonlight, gracias al lío de Tailscale que ya conté por aquí. Funciona de maravilla, pero hay un problema: la pantalla de la handheld es pequeña, y en el salón tengo una tele LG de 55 pulgadas cogiendo polvo mientras juego mirando una pantalla diminuta. Así que pensé: ¿por qué no meto Moonlight directamente en la tele?

Spoiler: se puede. Pero no es tan simple como buscar "Moonlight" en la tienda de apps de LG, porque ahí no está. Y punto.

## Por qué no está en la tienda oficial

LG no permite que cualquiera publique aplicaciones de este tipo en su Content Store. Así que la única forma de meter Moonlight en una tele LG con webOS es "por la puerta de atrás", usando algo que LG sí ofrece oficialmente para otra cosa: el Modo Desarrollador.

Investigué un poco y encontré dos caminos:

1. **Modo Desarrollador oficial de LG**: reversible, sin tocar el firmware de la tele, pensado para que programadores prueben sus apps antes de publicarlas. La única "pega" es que la sesión caduca — aunque en la práctica dura 999 horas, más de 40 días seguidos.
2. **Rootear la tele por completo** (Homebrew Channel permanente): sin caducidad, pero implica aprovechar un fallo de seguridad del firmware. Si algo sale mal a mitad del proceso, la tele se puede quedar inservible.

Con una tele de 55 pulgadas de por medio, la decisión fue fácil: nada de arriesgar el aparato por evitar reactivar un modo cada mes y medio. Modo Desarrollador, sin dudarlo.

## El plan, con la tele como cómplice

El proceso oficial de LG es este: te creas una cuenta gratuita de desarrollador en su web, instalas una app que se llama, literalmente, "Developer Mode" desde la propia tienda de la tele, inicias sesión, y activas dos interruptores: uno que activa el modo en sí (la tele se reinicia sola, qué susto la primera vez) y otro llamado "Key Server", que es el que permite que un ordenador se autentique con la tele para mandarle cosas.

Hasta aquí, todo desde el mando de la tele. Sin complicación.

## El giro: lo quería hacer desde el sofá

El plan inicial era usar una aplicación con interfaz gráfica en el PC (webOS Dev Manager) que hace todo con clics: detecta la tele, pide la clave, instala la app. Muy cómodo... si estás sentado delante del ordenador.

Yo no lo estaba. Estaba en el sofá, conectado al PC por SSH desde el móvil — es decir, con acceso solo a una terminal de texto, sin ventanas ni clics posibles. Una app gráfica ahí no sirve de nada: por SSH puedes escribir comandos, no ver interfaces.

Así que cambié de plan sobre la marcha: en vez de la app gráfica, usar la herramienta oficial de LG por línea de comandos (`ares-cli`). Resulta que es justo la misma tecnología que usa la app gráfica por debajo, solo que sin el envoltorio visual — perfecta para hacerlo todo a base de comandos desde el móvil.

## Los tropiezos (porque siempre los hay)

Primero, la herramienta se instala con `npm` (el gestor de paquetes de Node.js), y resulta que no tenía Node instalado en el PC. Un `sudo pacman -S nodejs npm` debería haber bastado, pero el mirror de descargas de CachyOS tenía un índice desactualizado y me devolvió un error 404. Con forzar la sincronización (`pacman -Syy`) se arregló — cosas de un sistema "rolling release" como Arch, donde las versiones cambian constantemente y a veces tu lista local se queda un paso por detrás.

Con Node ya instalado, instalé la herramienta de LG:

```
sudo npm install -g @webos-tools/cli
```

npm avisó de que había "scripts de instalación" bloqueados por seguridad — código que el propio paquete necesita ejecutar para compilar sus piezas de conexión SSH. Como era el paquete oficial y lo estaba instalando yo a propósito, los permití explícitamente y sanseacabó.

## Emparejando el PC con la tele

Con la herramienta ya lista, el resto fue encadenar comandos:

```
ares-setup-device
```
para darle de alta a la tele con su IP local (la que la propia app de la tele te muestra en pantalla).

```
ares-novacom --device tv --getkey
```
para pedirle la clave de acceso, usando una "passphrase" de 6 caracteres que la tele genera y muestra en pantalla — como un código de emparejamiento de un solo uso.

```
ares-device --system-info --device tv
```
para comprobar que la conexión funcionaba de verdad. Y ahí estaba: la tele respondiendo con sus datos (modelo, versión de webOS) directamente desde mi terminal, sin haber tocado el mando en ningún momento.

## Moonlight, por fin, en la tele

Con la conexión hecha, el último paso fue instalar Moonlight en sí. Existe una versión hecha por la comunidad (Moonlight TV, del proyecto webOS Homebrew), empaquetada en un archivo `.ipk` — el equivalente en webOS a un `.apk` de Android.

```
wget https://github.com/mariotaku/moonlight-tv/releases/download/v1.6.36/com.limelight.webos_1.6.36_arm.ipk
ares-install --device tv com.limelight.webos_1.6.36_arm.ipk
```

Y ya está: Moonlight apareció como un icono más en el menú de la tele, junto a Netflix y las demás apps, listo para transmitir el PC a pantalla completa.

## La sensación rara de todo esto

Lo que más gracia me hace, mirándolo con perspectiva, es que hace no tanto mi única relación con la tecnología era cargar y descargar cristal en un camión. Y aquí estaba, desde el sofá, sin tocar el mando ni una vez, instalando software no oficial en mi tele a base de comandos por SSH. Todavía me sorprende un poco a mí mismo.

Siguiente paso pendiente: probar cómo va el streaming por WiFi (la tele no tiene cable Ethernet cerca) y ver si aguanta bien la latencia jugando de verdad. Si hay tirones, ya sabéis: toca hablar de cables.
