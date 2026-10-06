#!/usr/bin/env python3
"""Show how a thumbnail will look inside every real container of viettelcloud.vn/tech-blog (object-fit: cover, center).

Usage: preview_crops.py thumb.png --out preview.png [--zoom 1.5]
Containers measured 06/10/2026 (desktop 1440 unless noted). Output: a contact sheet PNG — open it and check that the
subject survives the 86×86 square and the 398×208 wide crop.
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont

CONTAINERS = [
    ("Nổi bật 386×290", 386, 290), ("Lưới 287×210", 287, 210), ("Danh sách 253×188", 253, 188),
    ("Liên quan 414×290", 414, 290), ("Sidebar đầu 398×208", 398, 208), ("Sidebar nhỏ 86×86", 86, 86),
    ("Mobile 358×210", 358, 210),
]

def cover(im, w, h):
    sw, sh = im.size
    s = max(w / sw, h / sh)
    rw, rh = round(sw * s), round(sh * s)
    r = im.resize((rw, rh), Image.LANCZOS)
    l, t = (rw - w) // 2, (rh - h) // 2
    return r.crop((l, t, l + w, t + h))

def font(size):
    for p in ("/Library/Fonts/Roboto-Regular.ttf", os.path.expanduser("~/Library/Fonts/Roboto-Regular.ttf"),
              "/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image"); ap.add_argument("--out", required=True); ap.add_argument("--zoom", type=float, default=1.5)
    a = ap.parse_args()
    im = Image.open(a.image).convert("RGB")
    z = a.zoom
    pad, label_h = 40, 34
    tiles = [(name, cover(im, w, h).resize((round(w * z), round(h * z)), Image.LANCZOS)) for name, w, h in CONTAINERS]
    # layout: 3 per row
    cols = 3
    col_w = max(t.size[0] for _, t in tiles) + pad
    rows = [tiles[i:i + cols] for i in range(0, len(tiles), cols)]
    row_h = [max(t.size[1] for _, t in r) + label_h + pad for r in rows]
    W = cols * col_w + pad
    H = sum(row_h) + pad + 60
    sheet = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(sheet)
    f, fh = font(20), font(24)
    d.text((pad, 20), f"{os.path.basename(a.image)}  {im.size[0]}×{im.size[1]}  - object-fit: cover trong 7 khung cua trang (zoom {z}×)", fill="#44494D", font=fh)
    y = 60 + pad // 2
    for r, rh in zip(rows, row_h):
        x = pad
        for name, t in r:
            d.text((x, y), name, fill="#44494D", font=f)
            sheet.paste(t, (x, y + label_h))
            d.rectangle([x - 1, y + label_h - 1, x + t.size[0], y + label_h + t.size[1]], outline="#DADBDD")
            x += col_w
        y += rh
    sheet.save(a.out)
    print(f"preview → {a.out}  {sheet.size[0]}×{sheet.size[1]}")

if __name__ == "__main__":
    main()
