"""Genera DiagrammaClassi.md a partire da 'Diagramma Classi.drawio' (fonte di verita).
Script di utilita una tantum (non fa parte dell'applicazione).
Eseguire dalla cartella docs/Diagrammi/:  python _gen_diagramma_md.py
"""
import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "Diagramma Classi.drawio"
OUT = HERE / "DiagrammaClassi.md"

# Le sezioni sono rilevate DINAMICAMENTE dai banner presenti nel .drawio
# (robusto a spostamenti/traslazioni del diagramma). Keyword -> etichetta canonica.
SECTION_KEYS = [
    ("API SERVICE", "CLIENT - Service (API Service Layer)"),
    ("VIEW", "CLIENT - View (Presentation)"),
    ("CONTRATTI", "Contratti Controller -> BLL (interfacce)"),
    ("CONTROLLER", "SERVER - Controller (MVC / FrontController)"),
    ("BUSINESS LOGIC", "SERVER - Service (Business Logic Layer)"),
    ("DATA ACCESS", "SERVER - Repository (Data Access Layer)"),
    ("MODEL", "SERVER - Model (Domain / Entity)"),
    ("SISTEMI ESTERN", "Sistemi esterni, Adapter & Note"),
]
ORDER = ["CLIENT - View (Presentation)",
         "CLIENT - Service (API Service Layer)",
         "SERVER - Controller (MVC / FrontController)",
         "Contratti Controller -> BLL (interfacce)",
         "SERVER - Service (Business Logic Layer)",
         "SERVER - Repository (Data Access Layer)",
         "SERVER - Model (Domain / Entity)",
         "Sistemi esterni, Adapter & Note"]


def banner_label(text_upper):
    for key, label in SECTION_KEYS:
        if key in text_upper:
            return label
    return None


def strip_tags(s):
    s = re.sub(r"<\s*br\s*/?\s*>", "\n", s, flags=re.I)
    s = re.sub(r"<\s*/?\s*(p|hr|span|div|font|b|i)[^>]*>", "", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return s


def _has_bold(value):
    """True se la cella contiene un nome in grassetto (<b> oppure font-weight:700/bold)."""
    return "<b>" in value or re.search(r"font-weight:\s*(700|bold)", value, re.I) is not None


def parse_value(value):
    """Ritorna (nome, [attributi], [metodi]) da una cella classe."""
    raw = html.unescape(value)
    m = re.search(r"<b>(.*?)</b>", raw, flags=re.S | re.I)
    if not m:
        m = re.search(r'font-weight:\s*(?:700|bold)[^>]*>(.*?)</span>', raw, flags=re.S | re.I)
    name = strip_tags(m.group(1)).strip() if m else None
    body = raw[m.end():] if m else raw
    parts = re.split(r"<\s*hr[^>]*>", body, flags=re.I)
    blocks = []
    for p in parts:
        lines = [ln.strip() for ln in strip_tags(p).splitlines() if ln.strip()]
        if lines:
            blocks.append(lines)
    attrs, methods = [], []
    for block in blocks:
        for ln in block:
            if ln.startswith(("+", "#", "~")) or "(" in ln:
                methods.append(ln)
            elif ln.startswith("-"):
                attrs.append(ln)
            else:
                (methods if "(" in ln else attrs).append(ln)
    return name, attrs, methods


tree = ET.parse(SRC)
root = tree.getroot()

# --- pass 1: rileva i rettangoli-sezione dai banner (vertici grandi, senza <b>Nome</b>) ---
section_rects = {}
for c in root.iter("mxCell"):
    if c.get("vertex") != "1":
        continue
    raw = c.get("value") or ""
    g = c.find("mxGeometry")
    if g is None or _has_bold(raw):      # i box-classe hanno nome in grassetto: non sono banner
        continue
    w, h = float(g.get("width", 0)), float(g.get("height", 0))
    if w < 800 and h < 1000:             # i banner sono grandi contenitori
        continue
    lbl = banner_label(html.unescape(strip_tags(raw)).upper())
    if lbl and lbl not in section_rects:
        section_rects[lbl] = (float(g.get("x", 0)), float(g.get("y", 0)), w, h)


def section_for(x, y, w, h):
    """assegna per centro-dentro-rettangolo; in caso di overlap, il rettangolo piu piccolo."""
    cx, cy = x + w / 2, y + h / 2
    best, best_area = None, None
    for lbl, (sx, sy, sw, sh) in section_rects.items():
        if sx <= cx <= sx + sw and sy <= cy <= sy + sh:
            area = sw * sh
            if best_area is None or area < best_area:
                best, best_area = lbl, area
    return best


# --- pass 2: classi (vertici con <b>Nome</b>) + edges ---
classes = {}
edges = []
for c in root.iter("mxCell"):
    cid = c.get("id")
    value = c.get("value") or ""
    if c.get("edge") == "1":
        edges.append((c.get("source"), c.get("target")))
        continue
    if c.get("vertex") != "1" or not _has_bold(value):
        continue
    geom = c.find("mxGeometry")
    if geom is None:
        continue
    x, y = float(geom.get("x", 0)), float(geom.get("y", 0))
    w, h = float(geom.get("width", 0)), float(geom.get("height", 0))
    name, attrs, methods = parse_value(value)
    sec = section_for(x, y, w, h)
    if not name or sec is None:
        continue
    classes[cid] = dict(name=name, section=sec, attrs=attrs, methods=methods, x=x, y=y)

order = ORDER
by_sec = {lbl: [] for lbl in order}
for info in classes.values():
    by_sec[info["section"]].append(info)
for lbl in by_sec:
    by_sec[lbl].sort(key=lambda d: (d["x"], d["y"]))

sec_of = {cid: classes[cid]["section"] for cid in classes}
rel_counts = {}
for s, t in edges:
    if s in sec_of and t in sec_of:
        key = (sec_of[s], sec_of[t])
        rel_counts[key] = rel_counts.get(key, 0) + 1

total = sum(len(v) for v in by_sec.values())

L = []
L.append("# Diagramma delle Classi - SmartMobility")
L.append("")
L.append("> Export testuale di `Diagramma Classi.drawio` (fonte di verita).")
L.append("> Rigenerato automaticamente da `docs/Diagrammi/_gen_diagramma_md.py`.")
L.append("> Organizzato per layer architetturale (Client/Server + MVC a tre tier).")
L.append("")
L.append("## Indice delle classi")
L.append("")
L.append(f"Totale elementi identificati: **{total}**.")
L.append("")
for lbl in order:
    items = by_sec[lbl]
    if not items:
        continue
    names = ", ".join(f"`{d['name']}`" for d in items)
    L.append(f"- **{lbl}** ({len(items)}): {names}")
L.append("")
L.append("---")
L.append("")

for lbl in order:
    items = by_sec[lbl]
    if not items:
        continue
    L.append(f"## {lbl}")
    L.append("")
    for d in items:
        L.append(f"### `{d['name']}`")
        L.append("")
        if d["attrs"]:
            L += ["**Attributi**", "", "```", *d["attrs"], "```", ""]
        if d["methods"]:
            L += ["**Metodi**", "", "```", *d["methods"], "```", ""]
    L += ["---", ""]

L.append("## Relazioni tra layer")
L.append("")
L.append(f"Il diagramma contiene **{len(edges)}** relazioni (in prevalenza dipendenze d'uso `Use`).")
L.append("Riepilogo delle dipendenze direzionali tra layer (origine -> destinazione):")
L.append("")
L.append("| Da (layer) | A (layer) | N. dipendenze |")
L.append("|---|---|---|")
for (a, b), n in sorted(rel_counts.items(), key=lambda kv: -kv[1]):
    L.append(f"| {a} | {b} | {n} |")
L.append("")

OUT.write_text("\n".join(L), encoding="utf-8")
print(f"Scritto {OUT.name}: {total} classi, {len(edges)} edge")
