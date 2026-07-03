---
title: "Cómo monté acceso remoto a mi PC (y acabé reseteando el router sin querer)"
date: 2026-07-03
draft: false
tags: ["linux", "redes", "tailscale", "homelab"]
description: "La historia real de cómo quise jugar desde casa de mi madre y terminé aprendiendo sobre VPNs, firewalls y CGNAT por el camino."
---

## El problema: quiero jugar en casa de mi madre

Todo empezó por una tontería. Estaba pensando: "oye, si algún día no hay nadie en mi casa y me apetece coger algo de mi PC, o directamente jugar un rato desde casa de mi madre con mi propio ordenador... ¿se puede?"

La respuesta corta es sí. La respuesta larga incluye una VPN, un firewall que no era el problema, una opción escondida en un programa de streaming de juegos, y yo reseteando mi router de fábrica porque no me acordaba de una contraseña que ni recordaba haber puesto. Vamos por partes.

## Paso 1: Tailscale, o cómo hacer que dos aparatos se vean sin abrir la casa a cualquiera

Lo primero que aprendí es que "acceso remoto" no significa "abrir puertos en el router y rezar". Eso es básicamente poner un cartel en internet que dice "aquí hay un PC, pasen y vean" — y como te pille un bot escaneando puertos (que los hay, a puñados, todo el día), más vale que no tengas ninguna puerta mal cerrada.

La solución con cabeza se llama **Tailscale**: monta una red privada entre tus propios dispositivos, así estén en la otra punta del mundo, sin que nadie de fuera pueda ni verla. Instalarlo fue lo más fácil de toda la tarde:

```bash
sudo pacman -S tailscale
sudo systemctl enable --now tailscaled
sudo tailscale up
```

Me metí en el enlace que me dio la terminal, inicié sesión, y listo: mi PC (`cachyos`) ya tenía su propia IP privada, tipo `100.93.108.77`. Instalé la misma app en el móvil, y en cuestión de minutos los dos aparatos ya se veían entre sí.

La prueba de fuego fue hacer ping desde el móvil **con el WiFi apagado y datos móviles**, para simular estar fuera de casa de verdad:

```
64 bytes desde 100.69.250.62: icmp_seq=1 ttl=64 tiempo=419 ms
64 bytes desde 100.69.250.62: icmp_seq=2 ttl=64 tiempo=57.2 ms
...
0% packet loss
```

Cero paquetes perdidos. Primera victoria del día, y encima sin tener que entender qué es un NAT todavía (eso vino después, por las malas).

## Paso 2: "Imposible conectar al ordenador" — la frase que te arruina la tarde

Con la VPN funcionando, tocaba lo divertido: conectar **Moonlight** (en el móvil) con **Sunshine** (en el PC), que ya tenía configurado desde hace tiempo para jugar en local con mi Ayn Thor. En teoría, cambiar la IP de local a la de Tailscale y listo.

En la práctica, Moonlight me soltó esto:

> "Imposible conectar al ordenador, asegúrate que los puertos necesarios están permitidos"

Mi primer instinto fue pensar "vale, el firewall". Revisé `ufw` esperando encontrar el problema ahí:

```bash
sudo ufw status verbose
```

Y no. Todos los puertos de Sunshine ya estaban abiertos, ordenaditos, desde que instalé el programa. El firewall no tenía la culpa de nada. Toca seguir investigando.

## Paso 3: el culpable real estaba escondido en la configuración de Sunshine

Resulta que Sunshine tiene su propia idea de qué es "tu red local", separada por completo del firewall del sistema. Y esa idea es bastante estricta: solo confía en rangos de IP típicos de casa (tipo `192.168.x.x`). Tailscale usa un rango distinto (`100.64.0.0/10`, un rango especial llamado CGNAT), así que para Sunshine mi propio móvil, autenticado en mi propia red privada, era un completo desconocido llamando a la puerta.

La solución estaba en una opción con nombre de examen de oposición: **"Origin Web UI Allowed"**, que tenía puesta en "Solo LAN". La cambié a "Cualquiera puede acceder" — el propio programa te suelta un aviso de seguridad bastante serio al hacerlo, cosa que agradecí, porque así entendí que esa opción sí importa y no es un checkbox cualquiera.

Reinicié el servicio, probé otra vez desde el móvil con datos móviles... y **funcionó**. Vídeo, mando, todo. Estaba jugando desde mi propio PC sin estar físicamente cerca de él, por primera vez en mi vida.

## Paso 4: "espera, ¿y si eso que acabo de activar es peligroso?"

Aquí es donde toca ser un poco paranoico, que para eso estamos aprendiendo seguridad y no solo a que las cosas "funcionen". Poner "cualquiera puede acceder" suena a mala idea a primera vista. Pero la clave está en entender **por dónde puede llegar realmente alguien**:

- Sin Tailscale de por medio, ese puerto abierto en "cualquiera" sería un problema serio si además estuviera expuesto directamente a internet.
- Para que estuviera expuesto a internet de verdad, tendría que haber **port forwarding** activado en el router, redirigiendo ese puerto desde fuera hacia mi PC.

O sea, que tocaba comprobar el router. Y aquí es donde la tarde se puso interesante de verdad.

## Paso 5: no me acuerdo de la contraseña del router (clásico)

Fui a entrar al panel de administración del router para comprobar si tenía algo de port forwarding activado y... no tenía ni idea de la contraseña. Ni la del WiFi de fábrica, ni ninguna que hubiera puesto yo. Cero recuerdos.

Solución poco elegante pero efectiva: reset de fábrica con un clip, botón pequeño, mantener pulsado, esperar a que las lucecitas hagan su cosa. Al reconectar todo con las credenciales de fábrica (que sí venían impresas en la pegatina de abajo, cómo no), pude entrar por fin al panel.

## Paso 6: el descubrimiento que no me esperaba — CGNAT

Aquí venía la sorpresa del día. Mi router me mostraba esto como "IP pública":

```
Public IPv4 Address: 100.84.225.146
```

¿Os suena ese rango? Sí, el mismo tipo de rango que usa Tailscale por dentro. Resulta que mi operadora de internet usa **CGNAT** (Carrier-Grade NAT): comparte una única IP pública real entre varios clientes distintos, y mi router en realidad no tiene una IP propia visible desde internet — está detrás de otra capa de NAT que controla la operadora, no yo.

Traducido: aunque hubiera activado port forwarding a lo loco, en la práctica no habría servido de mucho, porque hay una puerta extra por delante que ni siquiera es mía. Una capa de seguridad gratis que ni sabía que tenía.

Aun así, revisé lo que sí controlo yo:

- **UPnP** (que permite a programas abrirse puertos solos, sin preguntar): estaba activado. Lo desactivé.
- **Tabla de reglas de port forwarding manuales**: completamente vacía.

Conclusión: cero exposición directa a internet. El único camino de entrada real a mi PC es la tailnet de Tailscale, con mi cuenta autenticada. La opción "cualquiera puede acceder" de Sunshine, en mi caso concreto, es segura de verdad — no solo "probablemente esté bien".

## Lo que me llevo de esta tarde

Empecé queriendo simplemente jugar desde casa de mi madre, y acabé aprendiendo qué es una VPN mesh, por qué un firewall correcto no basta si el propio programa tiene sus reglas aparte, y qué demonios es el CGNAT (algo que ni sabía que existía por la mañana). Todo esto sin abrir ni un solo puerto a internet abierto, que es justo la parte de la que estoy más orgulloso.

Ahora, si me apetece coger un archivo o echar una partida sin estar en casa, solo tengo que abrir el móvil. Sin exponer nada, sin depender de nadie más que de mí mismo.

Lo siguiente: hacer que el blog hable también inglés. Pero esa es otra historia.
