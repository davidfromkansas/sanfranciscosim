"""Compose the Oracle Park review renders into a labeled contact sheet."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent; BG=(237,227,209); INK=(58,52,44)
FONT=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",34)
VIEWS=["north","east","south","west","top","aerial"]; COLS=3; PAD=40; LABEL_H=56; CELL_W=460

def load(view):
    im=Image.open(HERE/f"oracle-park-{view}.png").convert("RGB"); h=round(im.height*CELL_W/im.width)
    return im.resize((CELL_W,h),Image.LANCZOS)

def main():
    tiles=[load(v) for v in VIEWS]; rows=[tiles[i:i+COLS] for i in range(0,len(tiles),COLS)]
    heights=[LABEL_H+max(t.height for t in row) for row in rows]
    sheet=Image.new("RGB",(PAD+COLS*(CELL_W+PAD),PAD+sum(h+PAD for h in heights)),BG); draw=ImageDraw.Draw(sheet); y=PAD
    for ri,row in enumerate(rows):
        for ci,tile in enumerate(row):
            cx=PAD+ci*(CELL_W+PAD)+CELL_W//2; label=VIEWS[ri*COLS+ci].upper()
            draw.text((cx,y+LABEL_H//2),label,font=FONT,fill=INK,anchor="mm"); sheet.paste(tile,(cx-tile.width//2,y+LABEL_H))
        y+=heights[ri]+PAD
    out=HERE/"oracle-park-contact-sheet.png"; sheet.save(out); print("[contact-sheet]",out)
if __name__=="__main__": main()
