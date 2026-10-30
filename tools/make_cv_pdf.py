#!/usr/bin/env python3
"""Genera los PDF del CV a partir de data/cv.yaml con Chrome sin pantalla.

Uso: python3 tools/make_cv_pdf.py
Salida:
  static/cv/CV_Ruben_Alcaniz.pdf                       (versión pública, va en la web)
  ~/Documentos/Documentos-generados-claude-code/CV_Ruben_Alcaniz_Administracion-Logistica.pdf  (para entregar en mano)
"""
import base64, html, os, subprocess, tempfile
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
D = yaml.safe_load((ROOT / "data/cv.yaml").read_text())
PHOTO = "data:image/jpeg;base64," + base64.b64encode((ROOT / "static/img/foto-perfil.jpg").read_bytes()).decode()
e = html.escape

# El teléfono no vive en el repo: se lee de CV_TELEFONO o de ~/.config/ralcaniz/telefono.
_tel_file = Path("~/.config/ralcaniz/telefono").expanduser()
TELEFONO = os.environ.get("CV_TELEFONO") or (_tel_file.read_text().strip() if _tel_file.exists() else "")

CSS = """
@page { size: A4; margin: 11mm 14mm; }
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Noto Sans','Liberation Sans',Arial,sans-serif; font-size: 9.3pt; line-height: 1.38; color: #1c1c1c; }
header { display: flex; justify-content: space-between; align-items: center; gap: 16px; padding-bottom: 10px; border-bottom: 2.5px solid #0f766e; margin-bottom: 4px; }
h1 { margin: 0; font-size: 22pt; letter-spacing: .2px; }
.role { margin: 2px 0 5px; font-size: 10.5pt; color: #0f766e; font-weight: 600; }
.contact { font-size: 9pt; color: #444; }
.contact span + span::before { content: '·'; margin: 0 7px; color: #999; }
img { width: 74px; height: 74px; border-radius: 50%; object-fit: cover; border: 2px solid #0f766e; }
h2 { margin: 10px 0 5px; padding-bottom: 2px; font-size: 10pt; letter-spacing: 1.1px; text-transform: uppercase; color: #0f766e; border-bottom: 1px solid #cfd8d6; }
p { margin: 0 0 4px; }
.item { margin-bottom: 5px; break-inside: avoid; }
.row { display: flex; justify-content: space-between; gap: 10px; }
.t { font-weight: 700; }
.org { color: #555; }
.date { color: #0f766e; font-size: 8.8pt; white-space: nowrap; }
.skill { display: flex; gap: 8px; margin-bottom: 2px; }
.skill b { flex: 0 0 118px; font-weight: 600; color: #333; }
ul { margin: 2px 0 0; padding-left: 16px; }
li { margin-bottom: 1.5px; }
"""

def exp(items):
    out = []
    for x in items:
        txt = f"<p>{e(x['texto'])}</p>" if x.get("texto") else ""
        out.append(f"<div class='item'><div class='row'><span><span class='t'>{e(x['puesto'])}</span> <span class='org'>— {e(x['empresa'])}</span></span><span class='date'>{e(x['fecha'])}</span></div>{txt}</div>")
    return "".join(out)

def edu():
    out = []
    for x in D["formacion"]:
        out.append(f"<div class='item'><div class='row'><span><span class='t'>{e(x['titulo'])}</span> <span class='org'>— {e(x['detalle'])}</span></span><span class='date'>{e(x['fecha'])}</span></div></div>")
    return "".join(out)

def skills(groups=None):
    return "".join(f"<div class='skill'><b>{e(g['grupo'])}</b><span>{e(', '.join(g['items']))}</span></div>"
                   for g in D["habilidades"] if groups is None or g["grupo"] in groups)

def page(titular, contacto, perfil, secciones):
    head = (f"<header><div><h1>{e(D['nombre'])}</h1><div class='role'>{e(titular)}</div>"
            f"<div class='contact'>{''.join(f'<span>{e(c)}</span>' for c in contacto)}</div></div>"
            f"<img src='{PHOTO}' alt=''></header>")
    body = f"<h2>Perfil</h2><p>{e(perfil)}</p>" + "".join(f"<h2>{e(t)}</h2>{c}" for t, c in secciones)
    return f"<!doctype html><html lang='es'><meta charset='utf-8'><style>{CSS}</style><body>{head}{body}</body></html>"

proyecto = D["proyecto"]
proyecto_html = f"<p><b>{e(proyecto['titulo'])}</b> — {e(proyecto['texto'])}</p><ul>" + "".join(f"<li>{e(p)}</li>" for p in proyecto["puntos"]) + "</ul>"
interes = "<ul>" + "".join(f"<li>{e(i)}</li>" for i in D["interes"] + D.get("interes_publico", [])) + "</ul>"

PUBLICO = page(
    D["titular"],
    ["ruben@ralcaniz.dev"] + ([TELEFONO] if TELEFONO else []) + ["ralcaniz.dev", "linkedin.com/in/ralcaniz"],
    "Técnico en Sistemas Microinformáticos y Redes. Trabajé más de dos años en soporte técnico y después más de ocho en logística, "
    "de operario a responsable de equipo. Ahora retomo la informática en serio: curso módulos de Desarrollo de Aplicaciones Multiplataforma, "
    "aprendo Linux y administración de sistemas, y lo documento en un blog técnico propio.",
    [("Habilidades", skills()), ("Proyecto personal", proyecto_html),
     ("Experiencia técnica", exp(D["tecnica"])), ("Experiencia profesional", exp(D["experiencia"])),
     ("Formación", edu()), ("Datos de interés", interes)])

ADMIN = page(
    "Logística y administración · Técnico en Sistemas Microinformáticos y Redes",
    ["ruben@ralcaniz.dev"] + ([TELEFONO] if TELEFONO else []),
    "Más de ocho años en logística en Serraglass, desde operario de fábrica hasta responsable del equipo de logística. Conozco el circuito "
    "de expediciones, material, pedidos y reparto, y tengo base informática (Técnico en Sistemas Microinformáticos y Redes y formación en "
    "Gestión Logística). Busco un puesto de administración dentro del departamento de logística.",
    [("Experiencia profesional", exp(D["experiencia"])), ("Experiencia técnica", exp(D["tecnica"])),
     ("Formación", edu()), ("Informática y sistemas", skills({"Sistemas", "Herramientas"}).replace("Cloudflare (Pages, Registrar, Email Routing), ", "") if False else
                              "<p>Soporte técnico a usuarios, instalación y mantenimiento de equipos y redes. Linux y administración básica de sistemas.</p>"),
     ("Datos de interés", "<ul>" + "".join(f"<li>{e(i)}</li>" for i in D["interes"]) + "</ul>")])

def render(doc, out):
    out = Path(out).expanduser(); out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        h = Path(t) / "cv.html"; h.write_text(doc)
        subprocess.run(["google-chrome-stable", "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={out}", f"file://{h}"], check=True, capture_output=True)
    print("OK", out)

render(PUBLICO, ROOT / "static/cv/CV_Ruben_Alcaniz.pdf")
render(ADMIN, "~/Documentos/Documentos-generados-claude-code/CV_Ruben_Alcaniz_Administracion-Logistica.pdf")
