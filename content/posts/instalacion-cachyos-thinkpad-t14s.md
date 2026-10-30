---
title: "Instalé CachyOS en un ThinkPad T14s (y mi teclado en inglés casi me gana)"
date: 2026-10-30T16:46:48+01:00
draft: false
tags: ["linux", "cachyos", "thinkpad", "limine", "luks", "btrfs"]
description: "Cómo instalé CachyOS con cifrado completo en un ThinkPad T14s de segunda mano: Ventoy, Limine, LUKS2, btrfs y los tropiezos reales por el camino."
---

Hace poco os conté que me había comprado un ThinkPad T14s Gen 4 de segunda mano ([el post de la compra](/posts/portatil-segunda-mano/)). Lo quiero para estudiar DAM, programar y, más adelante, montar un laboratorio donde aprender auditoría. Windows 11 venía limpio, pero no tenía intención de quedármelo: iba a borrarlo entero.

Este post cuenta la instalación tal cual fue, con los tropiezos incluidos. Y empiezo por el primero.

## El pendrive que se quedaba en negro

Metí la ISO de CachyOS (`cachyos-desktop-linux-260809`) en un pendrive con Ventoy 1.1.16. Arranque normal: pantalla negra con un guion fijo arriba a la izquierda. Esperé como un minuto, y nada. Con **Boot in grub2 mode** arrancó a la primera.

No sé por qué falla el modo normal con este portátil y no lo he investigado. Me quedo con la solución: con este equipo, siempre grub2 mode.

Por cierto, me salté la verificación del checksum de la ISO. Sé que no es lo recomendable. Si algo hubiera fallado de forma rara, habría sido lo primero que habría comprobado.

## Probar antes de borrar

Lo bueno de un live es que pruebas el hardware sin tocar el disco. Wi-Fi, sonido, brillo, teclas de función y la luz del teclado funcionaron a la primera. Faltaba lo que más puede fastidiar en un portátil: la suspensión.

Primero, saber qué modo usa el kernel. Aquí es donde se nota que el live arranca con el teclado en inglés (la `/` me salía con la tecla del `-`) y que yo tecleaba con prisa:

```text
[liveuser@CachyOS ~]$ cat /sys/power/nem_sleep
cat: /sys/power/nem_sleep: No such file or directory
[liveuser@CachyOS ~]$ ls sys/power
ls: cannot access 'sys/power': No such file or directory
[liveuser@CachyOS ~]$ cat /sys/power/mem_sleep
[s2idle]
```

Los dos primeros errores no eran del kernel: eran míos (una `m` que se convirtió en `n` y una barra que faltaba). Con el comando bien escrito sale `[s2idle]`, que es lo esperable en este tipo de portátiles.

Para arreglar el teclado en la sesión live: Configuración del sistema → Teclado → Distribuciones, añadir Español y subirlo al primer puesto. No toca el disco.

### El susto del Wi-Fi

Ejecuté `systemctl suspend` y desperté el portátil. Volvió bien, pero el icono de red decía "sin conexión":

```text
[liveuser@CachyOS ~]$ nmcli device
DEVICE         TYPE      STATE                   CONNECTION
lo             loopback  connected (externally)  lo
wlan0          wifi      disconnected            --
p2p-dev-wlan0  wifi-p2p  disconnected            --
```

El adaptador `wlan0` estaba ahí, solo desconectado, así que el driver sobrevivía a la suspensión. Y `nmcli connection show` solo listaba `lo`: no había **ninguna** red Wi-Fi guardada.

La explicación era sencilla. Entre una prueba y otra había apagado el portátil y arrancado el live de nuevo, y un live no guarda nada, ni siquiera la red. No era un fallo de la suspensión, era un live recién arrancado.

Me conecté otra vez, volví a suspender y esta vez reconectó solo. Probé también cerrando la tapa: el punto rojo de la "i" del logo ThinkPad parpadea despacio cuando está dormido, y al abrirla todo volvió, Wi-Fi incluido.

Esa fue la prueba en el live. En el sistema instalado todavía no la he repetido, y cuando lo haga os cuento cómo sale.

## Lo que elegí en el instalador (y por qué)

**Gestor de arranque: Limine.** El instalador ofrece GRUB, rEFInd, systemd-boot y Limine. Yo pensé que, como Ventoy había necesitado el modo grub2, tocaba GRUB. No tiene nada que ver: eso es cómo arranca el pendrive, no el sistema que se instala.

Según la wiki de CachyOS, con Btrfs los snapshots funcionan con `limine-snapper-sync` y Limine tiene su propia sección en la guía de Secure Boot. GRUB destaca si quieres cifrar también `/boot`, algo que yo no necesito. Con systemd-boot y rEFInd los snapshots requieren un montaje propio que CachyOS no da hecho.

**Disco: borrar todo.** El resumen del instalador lo dejó claro antes de tocar nada:

- Tabla de particiones GPT nueva.
- `/boot`: 4 GiB, FAT32.
- El resto, 472,94 GiB: LUKS2 con btrfs dentro.
- Sin partición de swap en disco, solo zram (swap comprimida en RAM). La consecuencia es que no habrá hibernación, aunque la suspensión sí funciona.

Con Limine los kernels viven en esa partición FAT32, así que no conviene tacañear con su tamaño. 4 GiB sobra.

**Cifrado completo.** La contraseña de LUKS se teclea en cada arranque, antes del login. Escríbela en el cuadro de prueba del teclado del instalador para comprobar que salen bien los símbolos. Y guárdala bien: si la pierdes, el disco no se recupera.

**Escritorio: Plasma.** Hyprland estaba en la lista y me tentó, pero lo dejo para otro día, con su propio post. Por ahora prefiero tener paneles gráficos de salvavidas mientras aprendo.

**Paquetes:** desmarqué Firefox, porque uso Brave. Lo demás, por defecto.

## Primer arranque

Tras reiniciar y sacar el pendrive, Limine, la clave de cifrado, el login y escritorio. Comprobé lo que importaba:

```text
$ lsblk -f
NAME                  FSTYPE FSVER  FSAVAIL FSUSE% MOUNTPOINTS
zram0                 swap   1                     [SWAP]
nvme0n1
├─nvme0n1p1           vfat   FAT32  3,7G    7%     /boot
└─nvme0n1p2           crypto 2
  └─luks-…            btrfs          463,5G  2%     /home
                                                    /var/cache
                                                    /srv
                                                    /var/tmp
                                                    /root
                                                    /var/log
                                                    /
```

(He recortado las columnas de UUID y etiqueta para que se lea mejor.) Ahí está todo: `/boot` en FAT32, una partición `crypto` versión 2 (LUKS2) y btrfs dentro, montado en `/` y compañía.

```text
$ uname -r
7.3.0-5-cachyos
```

Y el Wi-Fi, que es una Qualcomm con el driver `ath11k_pci` (omito un aviso inofensivo de `pcilib` por permisos):

```text
$ lspci -k | grep -A3 -i network
01:00.0 Network controller: Qualcomm Technologies, Inc QCNFA765 Wireless Adapter (rev 01)
	Subsystem: Lenovo Device 9309
	Kernel driver in use: ath11k_pci
	Kernel modules: ath11k_pci
```

## Brave, y mi pelea con una errata

Quería Brave. Pensé que haría falta el AUR, así que busqué `yay`:

```text
$ witch yay paru
fish: Unknown command: witch
```

Había escrito `witch` en vez de `which`. Con eso no comprobé nada, y di por hecho que no estaban. Busqué en los repos:

```text
$ pacman -Ss '^yay$'
cachyos/yay 13.0.1-1
    Yet another yogurt. Pacman wrapper and AUR helper written in go.
```

Instalé `yay`, busqué Brave con `yay -Ss brave` (salida recortada a la línea que importa) y resultó que ni lo necesitaba:

```text
cachyos/brave-bin 1:1.98.60-1 (157.1 MiB 476.3 MiB)
    Web browser that blocks ads and trackers by default (binary release)
```

Brave está en el repo de CachyOS, así que bastaba un `sudo pacman -S brave-bin`. El del AUR iba dos revisiones por delante, pero compilar desde el AUR para ganar dos versiones no compensaba.

## Lo que queda por hacer

- Repetir la prueba de suspensión en el sistema ya instalado.
- Volver a activar Secure Boot (lo desactivé para arrancar el pendrive) con `sbctl`.
- Ajustar la energía con TLP y limitar la carga de la batería al 80 %.
- Meter el portátil en mi red con Tailscale.

## Lo que me llevo

1. **Prueba el hardware en el live antes de borrar nada.** Te ahorra sorpresas.
2. **Mira qué teclado tienes** antes de culpar al sistema de lo que acabas de escribir mal.
3. **Antes de culpar al driver, mira el estado real.** Mi "fallo de suspensión" era un live recién arrancado sin red guardada.
4. **Comprueba qué has buscado** antes de dar algo por hecho. Un `witch` en vez de un `which` casi me hace instalar algo que ya tenía.
5. **Pon una buena contraseña de cifrado y guárdala bien.** Si la pierdes, el disco no tiene arreglo.

En el próximo, la memoria del portátil.
