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

# Sezioni per range di coordinata y (box contenitore nel .drawio).
# I sistemi esterni stanno a x>=4480.
SECTIONS = [
    ("CLIENT - View (Presentation)", 300, 800),
    ("CLIENT - Service (API Service Layer)", 919, 1560),
    ("SERVER - Controller (MVC / FrontController)", 1633, 2200),
    ("Contratti Controller -> BLL (interfacce)", 2247, 2560),
    ("SERVER - Service (Business Logic Layer)", 2609, 3080),
    ("SERVER - Repository (Data Access Layer)", 3347, 3700),
    ("SERVER - Model (Domain / Entity)", 3752, 4320),
]


def section_for(x, y):
    if x >= 4480:
        return "Sistemi esterni, Adapter & Note"
    for label, lo, hi in SECTIONS:
        if lo <= y <= hi:
            return label
    return None


def strip_tags(s):
    s = re.sub(r"<\s*br\s*/?\s*>", "\n", s, flags=re.I)
    s = re.sub(r"<\s*/?\s*(p|hr|span|div|font|b|i)[^>]*>", "", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return s


def parse_value(value):
    """Ritorna (nome, [attributi], [metodi]) da una cella classe."""
    raw = html.unescape(value)
    m = re.search(r"<b>(.*?)</b>", raw, flags=re.S | re.I)
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
classes = {}
edges = []

for c in tree.getroot().iter("mxCell"):
    cid = c.get("id")
    value = c.get("value") or ""
    if c.get("edge") == "1":
        edges.append((c.get("source"), c.get("target")))
        continue
    if c.get("vertex") != "1":
        continue
    geom = c.find("mxGeometry")
    if geom is None:
        continue
    x, y = float(geom.get("x", 0)), float(geom.get("y", 0))
    if float(geom.get("width", 0)) > 1500:  # box-sezione: salta
        continue
    name, attrs, methods = parse_value(value)
    sec = section_for(x, y)
    if not name or sec is None:
        continue
    classes[cid] = dict(name=name, section=sec, attrs=attrs, methods=methods, x=x, y=y)

order = [lbl for lbl, *_ in SECTIONS] + ["Sistemi esterni, Adapter & Note"]
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
