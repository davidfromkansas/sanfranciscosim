"""Assemble the review contact sheet for 424 Brannan.

    /Applications/Blender.app/Contents/MacOS/Blender -b --python make_contact_sheet.py

Uses Blender's bundled Pillow-free image API so no extra dependency is needed.
Tiles: top (the primary image for a ground asset), aerial, grazing, night, and
the four site-frame elevations.
"""
import os
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
PREFIX = "424-brannan"
# (row height, [tiles]). The elevations are 1800x400 letterboxes and would
# otherwise leave 400 px of empty table under each one.
LAYOUT = [
    (760, ["top", "aerial"]),
    (560, ["grazing", "aerial-night"]),
    (215, ["ritch", "brannan"]),
    (215, ["zoe", "north"]),
]
CELL_W = 940
PAD = 12


def load(name):
    p = os.path.join(HERE, f"{PREFIX}-{name}.png")
    return bpy.data.images.load(p) if os.path.exists(p) else None


def main():
    cols = max(len(r[1]) for r in LAYOUT)
    W = cols * CELL_W + (cols + 1) * PAD
    H = sum(r[0] for r in LAYOUT) + (len(LAYOUT) + 1) * PAD
    sheet = bpy.data.images.new("contact", W, H, alpha=False)
    buf = [0.13, 0.12, 0.11, 1.0] * (W * H)

    y_cursor = PAD
    for cell_h, row in LAYOUT:
        for c, name in enumerate(row):
            img = load(name)
            if img is None:
                continue
            iw, ih = img.size
            scale = min(CELL_W / iw, cell_h / ih)
            tw, th = int(iw * scale), int(ih * scale)
            ox = PAD + c * (CELL_W + PAD) + (CELL_W - tw) // 2
            # sheet origin is bottom-left; rows run top to bottom
            oy = H - (y_cursor + (cell_h - th) // 2 + th)
            px = list(img.pixels)
            for y in range(th):
                sy = min(ih - 1, int(y / scale))
                srow = sy * iw * 4
                drow = (oy + y) * W * 4
                for x in range(tw):
                    sx = min(iw - 1, int(x / scale))
                    si = srow + sx * 4
                    di = drow + (ox + x) * 4
                    buf[di] = px[si]
                    buf[di + 1] = px[si + 1]
                    buf[di + 2] = px[si + 2]
                    buf[di + 3] = 1.0
            bpy.data.images.remove(img)
        y_cursor += cell_h + PAD

    sheet.pixels = buf
    sheet.filepath_raw = os.path.join(HERE, f"{PREFIX}-contact-sheet.png")
    sheet.file_format = "PNG"
    sheet.save()
    print("wrote", sheet.filepath_raw)


if __name__ == "__main__":
    main()
