"""Compose the street-kit review renders into streetkit-contact-sheet.png.

    python3 make_contact_sheet.py

Each tile is labelled with the piece id and its triangle count / footprint, so
the sheet doubles as the contract table's visual half.
"""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
KIT = HERE.parent.parent / "app" / "public" / "sf-assets" / "streetkit"
BG = (237, 227, 209)
INK = (58, 52, 44)
SUB = (120, 108, 92)
TITLE = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
SMALL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)
COLS = 5
PAD = 26
LABEL_H = 62
CELL_W = 300


def main():
    index = json.loads((KIT / "streetkit_index.json").read_text())
    pieces = index["pieces"]
    tiles = []
    for p in pieces:
        img = Image.open(HERE / "renders" / f"{p['id']}.png").convert("RGB")
        h = round(img.height * CELL_W / img.width)
        tiles.append(img.resize((CELL_W, h), Image.LANCZOS))

    rows = [tiles[i : i + COLS] for i in range(0, len(tiles), COLS)]
    row_h = [max(t.height for t in r) + LABEL_H for r in rows]
    width = PAD + COLS * (CELL_W + PAD)
    height = PAD + sum(h + PAD for h in row_h)
    sheet = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(sheet)

    y = PAD
    for ri, row in enumerate(rows):
        for ci, tile in enumerate(row):
            p = pieces[ri * COLS + ci]
            cx = PAD + ci * (CELL_W + PAD) + CELL_W // 2
            draw.text((cx, y + 18), p["id"], font=TITLE, fill=INK, anchor="mm")
            dims = " x ".join(f"{v:.2f}" for v in p["dims"])
            draw.text((cx, y + 44), f"{p['tris']} tris   {dims} m", font=SMALL, fill=SUB, anchor="mm")
            sheet.paste(tile, (cx - tile.width // 2, y + LABEL_H))
        y += row_h[ri] + PAD

    out = HERE / "streetkit-contact-sheet.png"
    sheet.save(out)
    print(f"[contact-sheet] {out} ({sheet.width}x{sheet.height})")


if __name__ == "__main__":
    main()
