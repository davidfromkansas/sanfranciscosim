# Pixel diffs + contact sheet — run: /usr/bin/python3 diff_ab.py
# Reads renders/in_*.png and renders/out_*.png, writes renders/diff_*.png
# (x8 amplified), renders/contact_sheet.png, and diffs.json.
import json
from PIL import Image, ImageChops, ImageDraw, ImageFont

PAIRS = ["day_near", "day_far", "night_near", "night_far",
         "elev_n", "elev_e", "elev_s", "elev_w"]
out = {}
for tag in PAIRS:
    a = Image.open(f"renders/in_{tag}.png").convert("RGBA")
    b = Image.open(f"renders/out_{tag}.png").convert("RGBA")
    pa, pb = a.load(), b.load()
    w, h = a.size
    total = n = 0
    maxd = 0
    for y in range(h):
        for x in range(w):
            ra, ga, ba, aa = pa[x, y]
            rb, gb, bb, ab = pb[x, y]
            if aa < 8 and ab < 8:      # both background
                continue
            d = (abs(ra - rb) + abs(ga - gb) + abs(ba - bb)) / 3
            total += d
            maxd = max(maxd, d)
            n += 1
    mean_pct = 100 * total / (n * 255) if n else 0.0
    out[tag] = {"mean_abs_rgb_pct": round(mean_pct, 4),
                "max_px_delta": int(maxd), "fg_pixels": n}
    diff = ImageChops.difference(a.convert("RGB"), b.convert("RGB"))
    diff = diff.point(lambda v: min(255, v * 8))
    diff.save(f"renders/diff_{tag}.png")

# contact sheet: rows = input / output / diff(x8), cols = N E S W elevations
cols = ["elev_n", "elev_e", "elev_s", "elev_w"]
cell = Image.open("renders/in_elev_n.png")
cw, ch = cell.size
cw2, ch2 = cw // 2, ch // 2
sheet = Image.new("RGB", (cw2 * 4, ch2 * 3 + 24), (24, 24, 28))
d = ImageDraw.Draw(sheet)
d.text((8, 4), "599 Third Street A/B — rows: input / optimized / diff x8 — cols: N E S W",
       fill=(220, 220, 220))
for r, pref in enumerate(["renders/in_", "renders/out_", "renders/diff_"]):
    for c, tag in enumerate(cols):
        im = Image.open(pref + tag + ".png").convert("RGB").resize((cw2, ch2))
        sheet.paste(im, (c * cw2, 24 + r * ch2))
sheet.save("renders/contact_sheet.png")

with open("diffs.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
