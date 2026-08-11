"""Compose City Hall elevation, top, and aerial review renders."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
BG = (237, 227, 209)
INK = (58, 52, 44)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT = ImageFont.truetype(FONT_PATH, 34)
VIEWS = ["north", "east", "south", "west", "top", "aerial", "night", "night-east"]
COLS = 3
PAD = 40
LABEL_H = 56
CELL_W = 460


def load(view):
    image = Image.open(HERE / f"city-hall-{view}.png").convert("RGB")
    height = round(image.height * CELL_W / image.width)
    return image.resize((CELL_W, height), Image.Resampling.LANCZOS)


def main():
    tiles = [load(view) for view in VIEWS]
    rows = [tiles[i:i + COLS] for i in range(0, len(tiles), COLS)]
    row_heights = [LABEL_H + max(tile.height for tile in row) for row in rows]
    width = PAD + COLS * (CELL_W + PAD)
    height = PAD + sum(row_height + PAD for row_height in row_heights)
    sheet = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(sheet)
    y = PAD
    for row_index, row in enumerate(rows):
        for column_index, tile in enumerate(row):
            center_x = PAD + column_index * (CELL_W + PAD) + CELL_W // 2
            label = VIEWS[row_index * COLS + column_index].upper()
            draw.text((center_x, y + LABEL_H // 2), label, font=FONT, fill=INK, anchor="mm")
            sheet.paste(tile, (center_x - tile.width // 2, y + LABEL_H))
        y += row_heights[row_index] + PAD
    output = HERE / "city-hall-contact-sheet.png"
    sheet.save(output)
    print(f"[contact-sheet] {output}")


if __name__ == "__main__":
    main()
