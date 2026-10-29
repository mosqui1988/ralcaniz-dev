---
title: "Me compré un portátil de empresa de segunda mano (y esto es lo que miré antes de pagar)"
date: 2026-10-29T21:31:49+01:00
draft: false
tags: ["hardware", "linux", "segunda mano", "seguridad"]
description: "Iba a recogerlo un conocido en Madrid y acabé yendo yo a Dénia. Esto es lo que comprobé del ThinkPad T14s antes de pagar: garantía, BIOS, Absolute y batería."
---

Hay planes que salen a la primera y planes que acaban con un viaje a Dénia. Este fue de los segundos.

## Para qué quería otro ordenador

Estoy estudiando 1.º de DAM online y quiero meterme en ciberseguridad. Tengo la Torre, pero por las mañanas no siempre puedo usarla, y esas son justo las horas en las que mejor estudio.

Necesitaba algo portátil, con Linux, que aguantara máquinas virtuales para montar un laboratorio de auditorías y que no costara un riñón. (Los necesito los dos, gracias.)

## El elegido

Un **ThinkPad T14s Gen 4 con AMD**: Ryzen 7 PRO 7840U, 32 GB de RAM (soldada, no se puede ampliar) y un SSD de 512 GB.

Antes de decidirme fui a buscar cómo se lleva con Linux. No encontré una página dedicada a este modelo exacto en la Arch Wiki, pero sus hermanos (el T14 y el P14s Gen 4 AMD) sí están documentados: el lector de huellas funciona con las herramientas de siempre y el firmware se puede actualizar desde Linux. Con una pega que anoté: la suspensión es el punto flojo de esta familia. Ya lo comprobaré yo.

## El plan que se tuerce

El portátil estaba en Madrid. Lo iba a recoger un conocido, pero la cosa se alargaba y no terminaba de cerrarse. Así que hablé yo directamente con el vendedor, le dije que si hacía falta me plantaba en Madrid, y me contó que se iba a pasar unos días de vacaciones a Dénia. Dénia me pilla bastante más cerca que Madrid, y a nadie le amarga un día de playa con excusa.

```
PLAN A:  Madrid ──► conocido ──► yo (algún día)

PLAN B:  vendedor (de vacaciones) ──► Dénia ◄── yo, en persona
```

Spoiler: el plan B salió mejor, porque pude revisar el equipo con él delante y **antes de pagar**.

## Lo que miré antes de pagar

Un portátil de empresa de segunda mano puede ser una ganga o un problema con teclado. Y no quería averiguarlo después de pagar, así que fui con una lista, como el que va al súper con hambre pero con disciplina:

```
ANTES DE PAGAR
 ├─ Número de serie ──► garantía en la web de Lenovo
 ├─ BIOS ─────────────► sin contraseña · Absolute Persistence
 ├─ Windows ──────────► sin cuenta de empresa
 ├─ Batería ──────────► ciclos y salud
 └─ Físico ───────────► bisagras · pantalla · teclado · USB-C
```

**Número de serie y garantía.** En la pegatina de abajo viene el número de serie. Lo metí en la web de garantía de Lenovo desde el móvil y salió vigente. Ya con Windows arrancado, la aplicación Lenovo Vantage lo confirma: 18 meses restantes, lo que cuadra con una fabricación de marzo de 2025.

**BIOS sin contraseña de supervisor.** Si el equipo la tiene, no puedes tocar nada de la BIOS. Mi BIOS entró directa, sin pedir nada.

**Absolute Persistence (antes Computrace).** Es un antirrobo que viene metido *dentro* de la BIOS de muchos portátiles de empresa. Lo especial es que **sobrevive a formatear**: aunque cambies el disco o reinstales Windows, la BIOS lo vuelve a poner. Si la empresa que lo tenía no lo dio de baja, puedes acabar con un equipo bloqueado o marcado como robado.

En la BIOS aparece en *Security → Absolute Persistence Module*, y mi equipo lo tiene **desactivado**, que es lo que quería ver.

Además, en Lenovo Vantage el servicio Smart Lock (que funciona con Absolute) aparece con un botón de *Comprar*, o sea, no está contratado en este equipo.

**Windows limpio.** En *Configuración → Cuentas → Acceso a trabajo o escuela* no había nada, y el nombre del equipo era el genérico `DESKTOP-algo`. Nadie lo había personalizado antes, ni siquiera con un «PORTATIL-DE-PACO».

**Batería.** Con `powercfg /batteryreport` en un terminal de Windows saca un informe con los ciclos de carga y la salud. Salió bien.

**Físico.** Bisagras firmes, pantalla robusta, sin golpes, teclado completo y la luz del teclado respondiendo a *Fn + Espacio*.

## ¿Y si le pongo Linux, pierdo la garantía?

Esta pregunta me la hice yo antes de borrar Windows, y fui a buscar. No encontré ningún texto oficial de Lenovo que diga que cambiar de sistema operativo anule la garantía de hardware. Lo que cuentan los foros es que no se anula, pero que pueden negarte soporte de software, o rechazar una reparación si demuestran que el sistema causó la avería. Eso lo dejo como lo que he leído, no como asesoramiento legal.

Lo que sí sé es que el **número de serie no cambia** al instalar Linux: está en la etiqueta y grabado en el firmware, no en Windows.

Mi plan de seguro: guardar una captura de la página de garantía (para mí, no para publicar) y, si algún día tengo que mandarlo a reparar, reinstalar Windows 11 desde una ISO oficial antes de enviarlo.

## Primer arranque (spoiler)

Esa misma tarde le enchufé un pendrive con **CachyOS** (preparado con Ventoy) en modo live, sin instalar nada. Elegí la ISO, pulsé Enter en *Boot in normal mode* y me quedé mirando una pantalla negra con un guion fijo arriba a la izquierda. Esperé un minuto entero, sin que pasara nada, y por un momento pensé que ya la había liado. Récord personal: portátil roto el mismo día que lo compro.

Reinicié, volví a Ventoy y esta vez elegí **Boot in grub2 mode**. Ahí sí: apareció el menú de CachyOS, y después el escritorio KDE. No sé exactamente por qué el modo normal se cuelga en este portátil; la próxima vez voy directo a grub2.

Una vez dentro funcionaron el Wi-Fi, el sonido, el brillo y la luz del teclado.

Lo que viene (instalarlo cifrado, probar la suspensión y montar el laboratorio) va en el siguiente post.

## Cierre

Gracias al vendedor, que fue honesto en todo y me dejó mirar el equipo con calma. Y como siempre, Claude me ayudó a montar la lista y a buscar lo que no sabía; los botones los toqué yo. Si algo explota, la culpa es mía.
