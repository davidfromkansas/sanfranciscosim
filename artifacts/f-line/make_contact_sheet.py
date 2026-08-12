"""Compose the review renders into two contact sheets.

    python3 make_contact_sheet.py

Reads renders/ and writes

  renders/f-line-pcc-contact-sheet.png   elevations, roof, aerial, night, and
                                         the two decision renders
  renders/f-line-pcc-livery-sheet.png    the same geometry under all five
                                         proposed cities-series tints

The livery sheet is a separate deliverable rather than four more cells on the
main sheet, because it answers a different question: the main sheet asks "is
this a PCC", the livery sheet asks "does one tinted material carry five
liveries" - which is the decision `agents.js` needs before anyone writes the
tinting change.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
RENDERS = HERE / "renders"
BG = (237, 227, 209)
INK = (58, 52, 44)
SUB = (122, 110, 94)
PREFIX = "f-line-pcc"


def _font(size=30):
    for p in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT = _font()
SMALL = _font(23)

VIEWS = [
    ("front", "FRONT (cab end, -Z) - single central headlight"),
    ("rear", "REAR (single-ended: blanker, tail lights)"),
    ("left", "LEFT FLANK (blind side, 10 windows)"),
    ("right", "RIGHT FLANK (kerb side, 2 doors)"),
    ("top", "TOP (silver crown, vents, pole)"),
    ("aerial", "AERIAL (app camera, 42 deg)"),
    ("night", "NIGHT (headlight, route board, lit saloon)"),
    ("backlit", "BACKLIT at 120 m (silhouette)"),
    ("in-city", "IN CITY at 1.6x = 23.6 m (Embarcadero, + bus + sedan)"),
]

# Slug, label. Must match render_scenarios.LIVERIES.
LIVERIES = [
    ("muni-wings", 'MUNI "WINGS" 1948', "#2f7a55 - cars 1006 / 1008"),
    ("st-louis", "ST. LOUIS PUBLIC SERVICE", "#c4453c - car 1050"),
    ("boston", "BOSTON ELEVATED RAILWAY", "#e0762f - car 1059"),
    ("los-angeles", "LOS ANGELES RAILWAY", "#e0af35 - car 1052"),
    ("baltimore", "BALTIMORE TRANSIT", "#3f9aa8 - car 1063"),
]

PAD = 36
LABEL_H = 50


def load(name, cell_w):
    img = Image.open(RENDERS / f"{name}.png").convert("RGB")
    h = round(img.height * cell_w / img.width)
    return img.resize((cell_w, h), Image.LANCZOS)


def grid(entries, cols, cell_w, out_name, label_h=LABEL_H, sublabels=None):
    tiles = [load(n, cell_w) for n, *_ in entries]
    rows = [tiles[i : i + cols] for i in range(0, len(tiles), cols)]
    row_h = [label_h + max(t.height for t in r) for r in rows]
    width = PAD + cols * (cell_w + PAD)
    height = PAD + sum(h + PAD for h in row_h)
    sheet = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(sheet)

    y = PAD
    for ri, row in enumerate(rows):
        for ci, tile in enumerate(row):
            idx = ri * cols + ci
            cx = PAD + ci * (cell_w + PAD) + cell_w // 2
            entry = entries[idx]
            if sublabels:
                draw.text((cx, y + 16), entry[1], font=FONT, fill=INK, anchor="mm")
                draw.text((cx, y + 46), entry[2], font=SMALL, fill=SUB, anchor="mm")
            else:
                draw.text((cx, y + label_h // 2), entry[1], font=FONT, fill=INK, anchor="mm")
            sheet.paste(tile, (cx - tile.width // 2, y + label_h))
        y += row_h[ri] + PAD

    out = RENDERS / out_name
    sheet.save(out)
    print(f"[contact-sheet] {out}")


def main():
    grid([(f"{PREFIX}-{n}", label) for n, label in VIEWS], 2, 720,
         f"{PREFIX}-contact-sheet.png")
    grid(
        [(f"{PREFIX}-livery-{s}", a, b) for s, a, b in LIVERIES],
        2,
        700,
        f"{PREFIX}-livery-sheet.png",
        label_h=70,
        sublabels=True,
    )


if __name__ == "__main__":
    main()
