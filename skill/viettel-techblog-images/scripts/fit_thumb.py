#!/usr/bin/env python3
"""Bring an existing image to the 1500×1000 thumbnail canvas.

Usage: fit_thumb.py in.png --out out.png [--mode pad|cover] [--bg FFFFFF] [--webp]
  pad   (default): scale to fit inside 1500×1000 and pad with --bg (keeps the whole subject; best for icons/diagrams)
  cover            : scale to cover and center-crop (for photos/AI art whose subject is centered)
"""
import argparse, os
from PIL import Image

W, H = 1500, 1000

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image"); ap.add_argument("--out", required=True)
    ap.add_argument("--mode", choices=["pad", "cover"], default="pad"); ap.add_argument("--bg", default="FFFFFF")
    ap.add_argument("--webp", action="store_true"); ap.add_argument("--fill", type=float, default=0.6,
                    help="pad mode: tỷ lệ chiều cao canvas mà ảnh chiếm (mặc định 0.6 → chủ thể nằm trong vùng an toàn)")
    a = ap.parse_args()
    im = Image.open(a.image).convert("RGBA")
    bg = Image.new("RGBA", (W, H), "#" + a.bg.lstrip("#"))
    sw, sh = im.size
    if a.mode == "cover":
        s = max(W / sw, H / sh)
        r = im.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
        l, t = (r.size[0] - W) // 2, (r.size[1] - H) // 2
        out = r.crop((l, t, l + W, t + H))
        out = Image.alpha_composite(bg, out)
    else:
        box_w, box_h = 1000, round(H * a.fill)  # inside the safe zone
        s = min(box_w / sw, box_h / sh)
        r = im.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
        bg.paste(r, ((W - r.size[0]) // 2, (H - r.size[1]) // 2), r)
        out = bg
    out = out.convert("RGB")
    out.save(a.out)
    print(f"PNG  {a.out}  {W}×{H}  {os.path.getsize(a.out)/1024:.0f} KB")
    if a.webp:
        wp = os.path.splitext(a.out)[0] + ".webp"
        out.save(wp, "WEBP", quality=85, method=6)
        print(f"WEBP {wp}  {os.path.getsize(wp)/1024:.0f} KB")

if __name__ == "__main__":
    main()
