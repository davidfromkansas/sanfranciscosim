"""Compose the review renders into cable-car-powell-contact-sheet.png.

    python3 make_contact_sheet.py

Reads renders/ and writes renders/cable-car-powell-contact-sheet.png. The three
decision renders (in-city 1.6x, 20% grade, backlit) are on the sheet alongside
the elevations, because they are the ones the plan says can fail the asset.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
RENDERS = HERE / "renders"
BG = (237, 227, 209)
INK = (58, 52, 44)
PREFIX = "cable-car-powell"


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
VIEWS = [
    ("front", "FRONT (gripman's end, -Z)"),
    ("rear", "REAR (conductor's platform)"),
    ("left", "LEFT FLANK"),
    ("right", "RIGHT FLANK"),
    ("top", "TOP (monitor deck)"),
    ("aerial", "AERIAL (app camera, 42 deg)"),
    ("night", "NIGHT (glow set)"),
    ("backlit-detail", "BACKLIT (openness)"),
    ("in-city", "IN CITY at 1.6x (bus + sedan)"),
    ("tilted", "20.2% GRADE (Russian Hill)"),
]
COLS = 2
PAD = 36
LABEL_H = 50
CELL_W = 720


def load(view):
    img = Image.open(RENDERS / f"{PREFIX}-{view}.png").convert("RGB")
    h = round(img.height * CELL_W / img.width)
    return img.resize((CELL_W, h), Image.LANCZOS)


def main():
    tiles = [load(v) for v, _ in VIEWS]
    rows = [tiles[i : i + COLS] for i in range(0, len(tiles), COLS)]
    row_h = [LABEL_H + max(t.height for t in r) for r in rows]
    width = PAD + COLS * (CELL_W + PAD)
    height = PAD + sum(h + PAD for h in row_h)
    sheet = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(sheet)

    y = PAD
    for ri, row in enumerate(rows):
        for ci, tile in enumerate(row):
            cx = PAD + ci * (CELL_W + PAD) + CELL_W // 2
            draw.text(
                (cx, y + LABEL_H // 2), VIEWS[ri * COLS + ci][1], font=FONT, fill=INK,
                anchor="mm",
            )
            sheet.paste(tile, (cx - tile.width // 2, y + LABEL_H))
        y += row_h[ri] + PAD

    out = RENDERS / f"{PREFIX}-contact-sheet.png"
    sheet.save(out)
    print(f"[contact-sheet] {out}")


if __name__ == "__main__":
    main()
