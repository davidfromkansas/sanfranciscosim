"""Compose the review renders into herbst-theatre-contact-sheet.png."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
BG = (237, 227, 209)
INK = (58, 52, 44)


def _font(size=34):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT = _font()
VIEWS = ["north", "east", "south", "west", "top", "aerial", "night", "night-east"]
LABELS = {
    # MIRRORED vs the Opera House twin: this building is NORTH of the court.
    "north": "NORTH (McAllister St flank)",
    "east": "EAST (Van Ness colonnade)",
    "south": "SOUTH (memorial court flank)",
    "west": "WEST (Franklin St rear)",
    "top": "TOP (roofscape)",
    "aerial": "AERIAL (app camera)",
    "night": "NIGHT (glow set)",
    "night-east": "NIGHT (entrance)",
}
COLS = 2
PAD = 40
LABEL_H = 56
CELL_W = 760


def load(view):
    img = Image.open(HERE / f"herbst-theatre-{view}.png").convert("RGB")
    h = round(img.height * CELL_W / img.width)
    return img.resize((CELL_W, h), Image.LANCZOS)


def main():
    tiles = [load(v) for v in VIEWS]
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
            label = LABELS[VIEWS[ri * COLS + ci]]
            draw.text((cx, y + LABEL_H // 2), label, font=FONT, fill=INK, anchor="mm")
            sheet.paste(tile, (cx - tile.width // 2, y + LABEL_H))
        y += row_h[ri] + PAD

    out = HERE / "herbst-theatre-contact-sheet.png"
    sheet.save(out)
    print(f"[contact-sheet] {out}")


if __name__ == "__main__":
    main()
