#!/usr/bin/env python3
"""Check a Tech Blog image against the skill's rules.

Usage: check_image.py image.png --kind thumb|inline|og [--json]
Checks: dimensions, aspect ratio, file size, colors outside the Viettel palette, red coverage, and (thumb) whether the
non-white content stays inside the 1000×760 safe zone. Exit code 1 when a hard rule fails; warnings don't fail.
"""
import argparse, json, os, sys
from PIL import Image

RULES = {
    "thumb":  {"size": (1500, 1000), "max_kb": 250, "red": (0.3, 12)},
    "inline": {"width": 1688, "max_kb": 500, "red": (0, 20)},
    "og":     {"size": (1200, 630), "max_kb": 300, "red": (0, 30)},
}
SAFE = (250, 120, 1250, 880)

def classify(px):
    """Return 'red', 'gray', or 'other' for an RGB pixel. Gray = low saturation (any tint/shade of the 5 brand grays)."""
    r, g, b = px
    mx, mn = max(px), min(px)
    if mx - mn <= 22:
        return "gray"
    # Viettel red EE0033 and its tints (mix with white) / shades: hue ≈ 347°, g≈low, b slightly > g
    if r > g and r > b and (b - g) >= -6 and (b - g) <= 0.45 * (r - g) + 8:
        return "red"
    return "other"

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image"); ap.add_argument("--kind", choices=RULES.keys(), required=True); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    rule = RULES[a.kind]
    im = Image.open(a.image).convert("RGB")
    W, H = im.size
    kb = os.path.getsize(a.image) / 1024
    fails, warns, info = [], [], {"size": [W, H], "kb": round(kb)}

    if "size" in rule and (W, H) != rule["size"]:
        fails.append(f"kích thước {W}×{H}, cần {rule['size'][0]}×{rule['size'][1]}")
    if "width" in rule and W != rule["width"]:
        fails.append(f"chiều rộng {W}, cần {rule['width']} (2× cột nội dung 844)")
    if a.kind == "inline" and H > 1400:
        warns.append(f"cao {H}px — ảnh dọc chiếm cả màn mobile; cân nhắc tách hình")
    if kb > rule["max_kb"]:
        webp = os.path.splitext(a.image)[0] + ".webp"
        if os.path.exists(webp) and os.path.getsize(webp) / 1024 <= rule["max_kb"]:
            warns.append(f"PNG {kb:.0f} KB nặng, nhưng bản WebP {os.path.getsize(webp)/1024:.0f} KB đạt — giao WebP")
        else:
            fails.append(f"{kb:.0f} KB > {rule['max_kb']} KB — xuất WebP (--webp) hoặc giảm chi tiết")

    # colors: sample on a downscaled copy for speed
    small = im.resize((max(1, W // 3), max(1, H // 3)), Image.BILINEAR)
    counts = {"red": 0, "gray": 0, "other": 0, "white": 0}
    raw = small.tobytes()
    for i in range(0, len(raw), 3):
        px = (raw[i], raw[i + 1], raw[i + 2])
        if px[0] >= 236 and px[1] >= 236 and px[2] >= 236 and max(px) - min(px) <= 6:
            counts["white"] += 1
        else:
            counts[classify(px)] += 1
    total = sum(counts.values())
    pct = {k: 100 * v / total for k, v in counts.items()}
    info["colors_pct"] = {k: round(v, 2) for k, v in pct.items()}
    lo, hi = rule["red"]
    if pct["other"] > 0.5:
        fails.append(f"màu ngoài bảng Viettel: {pct['other']:.1f}% điểm ảnh (xanh/tím/cam/vàng…) — đổi về xám 44494D / đỏ EE0033")
    elif pct["other"] > 0.1:
        warns.append(f"màu ngoài bảng {pct['other']:.2f}% (có thể là anti-alias; kiểm tra lại logo/ảnh dán)")
    if pct["red"] < lo:
        warns.append(f"đỏ chỉ {pct['red']:.2f}% (< {lo}%) — thiếu điểm nhấn thương hiệu (line-art thường 0.3–2%)")
    if pct["red"] > hi:
        fails.append(f"đỏ {pct['red']:.1f}% > {hi}% — đỏ phải là điểm nhấn, không phải mảng chính")
    if a.kind == "thumb" and pct["white"] < 60:
        warns.append(f"nền sáng chỉ {pct['white']:.0f}% — thumbnail tối giản nên trống ≥ 60%")

    # safe zone (thumb): bbox of non-white pixels
    if a.kind == "thumb":
        mask = im.convert("L").point(lambda v: 0 if v >= 205 else 255)  # bỏ qua nền/texture nhạt
        bbox = mask.getbbox()
        info["content_bbox"] = bbox
        if bbox:
            l, t, r, b = bbox
            out = []
            if l < SAFE[0]: out.append(f"trái {SAFE[0]-l}px")
            if t < SAFE[1]: out.append(f"trên {SAFE[1]-t}px")
            if r > SAFE[2]: out.append(f"phải {r-SAFE[2]}px")
            if b > SAFE[3]: out.append(f"dưới {b-SAFE[3]}px")
            if out:
                warns.append("nội dung vượt vùng an toàn 1000×760: " + ", ".join(out) +
                             " — chấp nhận nếu chỉ là họa tiết tràn; chủ thể/chữ phải nằm trong")
            cw, ch = r - l, b - t
            if ch < 0.35 * H:
                warns.append(f"chủ thể cao {ch}px ({100*ch/H:.0f}% canvas) — hơi nhỏ, sẽ mất ở khung 86×86; gợi ý 45–60%")

    result = {"file": a.image, "kind": a.kind, "pass": not fails, "fails": fails, "warns": warns, **info}
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
    else:
        print(f"{a.image}: {W}×{H}, {kb:.0f} KB, màu: trắng {pct['white']:.0f}% · xám {pct['gray']:.1f}% · đỏ {pct['red']:.1f}% · khác {pct['other']:.2f}%")
        for f in fails: print("  ✗", f)
        for w in warns: print("  !", w)
        print("  ✓ đạt" if not fails else "  → chưa đạt")
    sys.exit(0 if not fails else 1)

if __name__ == "__main__":
    main()
