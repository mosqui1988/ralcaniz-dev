---
title: "Sobre mí"
description: "Rubén Alcañiz: de la logística del vidrio a la informática. Técnico en Sistemas Microinformáticos y Redes, estudiante de DAM, con homelab propio y rumbo a la ciberseguridad."
hidemeta: true
disableShare: true
comments: false
---

{{< perfil-terminal >}}

Soy Rubén Alcañiz Meseguer. He trabajado en la logística del vidrio desde dentro y he pasado por casi todos los puestos: operario de fábrica en la preparación de expediciones, transportista con camión grúa, conductor de tráiler y responsable del equipo de logística. Un trabajo físico y con responsabilidad, donde aprendí a organizar, cumplir plazos y trabajar con equipos y procesos reales.

Una lesión persistente en los brazos, derivada de la manipulación de cargas pesadas, me obligó a parar y a replantearme el camino. No fue una decisión con muchas alternativas — tocaba reinventarme, y decidí hacerlo hacia la informática y el desarrollo de software.

No parto completamente de cero. Hace años saqué el título de Técnico en Sistemas Microinformáticos y Redes y trabajé un tiempo dando soporte técnico — la vida me llevó por otro camino, pero esa base sigue ahí, y ahora quiero recuperarla y construir encima.

Hoy ya estoy dentro del CFGS de Desarrollo de Aplicaciones Multiplataforma (DAM), aunque con una plaza parcial: de momento curso **Programación**, **Entornos de Desarrollo** e **Inglés**. Es un primer paso, y mientras tanto sigo aprendiendo por mi cuenta.

## Mientras tanto, no me quedo quieto

Este blog, **"De Reparto a Root"**, es donde documento lo que voy aprendiendo por mi cuenta: monté mi propio homelab, migré a CachyOS (Arch Linux), y voy resolviendo problemas reales según me los encuentro. El patrón es siempre el mismo: quiero algo → investigo → la lío al intentarlo → lo resuelvo → lo cuento aquí, tal cual, sin postureo.

### Con qué trabajo

`Linux (Arch/CachyOS, Debian)` `Docker` `Tailscale` `Syncthing` `Immich` `Vaultwarden` `SQLite` `btrfs` `LUKS` `Wake-on-LAN` `Moonlight / Sunshine` `RustDesk` `msmtp`

### Sistemas y Linux
- 🐧 [Cambié de sistema operativo por completo](/posts/migracion-cachyos/), tanto en mi PC principal como en un dispositivo portátil, sustituyendo Windows por Linux sin vuelta atrás
- 💻 [Instalé CachyOS en un ThinkPad T14s](/posts/instalacion-cachyos-thinkpad-t14s/) con cifrado de disco, btrfs y Limine
- 🎮 [Le metí Linux a mi ROG Ally](/posts/post-cachyos-rog-ally/) (CachyOS Handheld Edition, instalada con Ventoy)
- 📚 [Me apunté a un curso de Linux Foundation](/posts/curso-linux-lf-upv-101x/), con el LPIC en el horizonte

### Servidor y red
- 🖥️ [Levanté mi propio servidor casero](/posts/servidor-bridge-wol/) (Debian + Docker) como puente de infraestructura, con Wake-on-LAN real: enciendo mi PC principal desde cualquier red del mundo
- 🔌 [Diseñé acceso remoto seguro a toda mi red](/posts/acceso-remoto-tailscale/) sin abrir un solo puerto a internet, usando una VPN mesh (Tailscale)
- 🕹️ [Monté streaming remoto de juegos de punta a punta](/posts/servidor-streaming-personal/), confirmado incluso jugando desde datos móviles fuera de casa
- 🖱️ [Probé escritorio remoto en Wayland](/posts/post-rustdesk-wayland/) con VNC y RustDesk, aprendiendo a leer logs en vez de probar a ciegas
- 📧 [Hice que el servidor me avise por correo](/posts/aviso-reinicio-servidor-msmtp/) cuando se va la luz y vuelve
- 💽 [Le cambié el disco al servidor](/posts/migracion-ssd-servidor/) sin perder nada por el camino

### Mis datos, bajo mi control
- ☁️ [Monté mi propio backup de fotos entre mis dispositivos](/posts/backup-fotos-syncthing/) con Syncthing, sin depender de Google Fotos ni de ninguna nube de terceros
- 📸 [Me hice mi propio Google Fotos en casa](/posts/immich-galeria-fotos/) con Immich, en solo lectura y accesible únicamente por mi red privada
- 🔑 [Me monté mi propio gestor de contraseñas](/posts/post-vaultwarden-tailscale/) (Vaultwarden) y luego [probé a recuperarlo desde cero](/posts/simulacro-catastrofe-contrasenas/) en un simulacro de catástrofe
- 🔐 [Descubrí que mi plan de seguridad tenía un agujero](/posts/creia-que-lo-tenia-blindado/) (si perdía el móvil, me quedaba sin acceso a todo) y lo arreglé
- 🛡️ [Automaticé un backup semanal cifrado](/posts/servidor-tambien-necesitaba-seguro/) del servidor a la nube, copiando la base de datos de forma segura

### Hardware
- 🔧 [Diagnostiqué una torre que no arrancaba](/posts/odisea-diagnostico-ram-cpu/) descartando pieza por pieza, y evité mandar a RMA una CPU sana

## Hacia dónde voy

A corto plazo: sacar adelante los módulos que estoy cursando (Programación, Entornos de Desarrollo e Inglés) y seguir construyendo bases sólidas por mi cuenta. Hacia donde más me tira es la **ciberseguridad**, junto con **servidores y redes**: montar cosas, protegerlas y comprobar que de verdad se pueden recuperar. Es lo que ya practico en mi homelab: una VPN sin puertos abiertos a internet, copias de seguridad cifradas y un simulacro de recuperación desde cero. El camino concreto ya se irá viendo. No espero llegar de un salto: primero quiero los fundamentos bien puestos, y este blog es la prueba de que los estoy construyendo en público, con ganas, aunque el ritmo sea irregular.

Tengo ganas de hacer cosas. Si te interesa ver cómo avanza esto, sígueme el rastro por aquí.

📬 [ruben@ralcaniz.dev](mailto:ruben@ralcaniz.dev) · 📄 [Ver mi CV](/cv/)

{{< linkedin-badge >}}


Fuera del terminal, mi hobby desde 2015 es la impresión 3D. Ahora mismo la tengo en pausa, pero tengo ganas de volver a ella. [Cuento más por aquí →](/impresion-3d/)
