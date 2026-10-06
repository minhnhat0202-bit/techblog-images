#!/usr/bin/env python3
"""Render an HTML file to PNG (and optionally WebP) with Google Chrome headless.

Usage:
  render.py page.html --preset thumb --out out.png [--webp] [--safe] [--scale 1]
  render.py page.html --size 1688x1400 --out out.png
  render.py --check-env

Presets (W×H): thumb 1500×1000 · inline-16x9 1688×950 · inline-3x2 1688×1126 · inline-2x1 1688×844 ·
inline-4x3 1688×1266 · og 1200×630. The HTML must fill the viewport (templates in assets/templates do).
--safe adds class "show-safe" to <body> so the template's safe-zone overlay is drawn (QA only).
"""
import argparse, os, shutil, subprocess, sys, tempfile

PRESETS = {
    "thumb": (1500, 1000), "inline-16x9": (1688, 950), "inline-3x2": (1688, 1126),
    "inline-2x1": (1688, 844), "inline-4x3": (1688, 1266), "og": (1200, 630),
}
CHROME_CANDIDATES = [
    os.environ.get("CHROME_BIN", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    shutil.which("google-chrome") or "", shutil.which("chromium") or "", shutil.which("chromium-browser") or "",
]

def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    return None

def check_env():
    ok = True
    chrome = find_chrome()
    print(f"Chrome: {chrome or 'KHÔNG THẤY — cài Google Chrome hoặc đặt $CHROME_BIN'}")
    ok &= bool(chrome)
    try:
        import PIL; print(f"Pillow: {PIL.__version__}")
    except ImportError:
        print("Pillow: thiếu — pip3 install pillow (cần cho --webp, preview_crops.py, check_image.py)"); ok = False
    fonts = []
    for d in (os.path.expanduser("~/Library/Fonts"), "/Library/Fonts"):
        if os.path.isdir(d):
            fonts += [f for f in os.listdir(d) if "beausans" in f.lower().replace(" ", "") or "roboto" in f.lower()]
    print(f"Font: {'FS PF BeauSans Pro có' if any('beau' in f.lower() for f in fonts) else 'FS PF BeauSans Pro THIẾU → fallback Roboto/Arial'}"
          f"{'; Roboto có' if any('roboto' in f.lower() for f in fonts) else '; Roboto thiếu → Arial'}")
    return ok

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", nargs="?")
    ap.add_argument("--preset", choices=PRESETS.keys())
    ap.add_argument("--size", help="WxH tùy ý, ví dụ 1688x1400")
    ap.add_argument("--out", help="đường dẫn PNG xuất ra")
    ap.add_argument("--webp", action="store_true", help="xuất thêm .webp q85 cạnh PNG")
    ap.add_argument("--quality", type=int, default=85)
    ap.add_argument("--safe", action="store_true", help="vẽ khung vùng an toàn (QA)")
    ap.add_argument("--scale", type=float, default=1.0, help="device scale factor (mặc định 1 = đúng pixel)")
    ap.add_argument("--check-env", action="store_true")
    a = ap.parse_args()

    if a.check_env:
        sys.exit(0 if check_env() else 1)
    if not a.html or not a.out:
        ap.error("cần <html> và --out (hoặc --check-env)")
    if a.size:
        w, h = (int(x) for x in a.size.lower().split("x"))
    elif a.preset:
        w, h = PRESETS[a.preset]
    else:
        ap.error("cần --preset hoặc --size")

    chrome = find_chrome()
    if not chrome:
        sys.exit("Không tìm thấy Chrome. Cài Google Chrome hoặc đặt biến môi trường CHROME_BIN.")

    src = os.path.abspath(a.html)
    html_path = src
    tmpdir = None
    if a.safe:
        # copy next to the source so relative asset paths keep working
        tmpdir = tempfile.mkdtemp(prefix="vtimg-", dir=os.path.dirname(src))
        text = open(src, encoding="utf-8").read()
        if "<body" in text:
            head, rest = text.split("<body", 1)
            tag, after = rest.split(">", 1)
            tag = tag.replace('class="', 'class="show-safe ', 1) if 'class="' in tag else tag + ' class="show-safe"'
            text = head + "<body" + tag + ">" + after
        html_path = os.path.join(tmpdir, "safe.html")
        open(html_path, "w", encoding="utf-8").write(text)
        # relative paths: point the tmp file back at the source directory via <base>
        if "<base" not in text:
            text = text.replace("<head>", f'<head><base href="file://{os.path.dirname(src)}/">', 1)
            open(html_path, "w", encoding="utf-8").write(text)

    out_png = os.path.abspath(a.out)
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    cmd = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--no-default-browser-check",
           f"--force-device-scale-factor={a.scale}", f"--window-size={w},{h}", "--virtual-time-budget=4000",
           "--default-background-color=FFFFFFFF", f"--screenshot={out_png}", "file://" + html_path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if tmpdir:
        shutil.rmtree(tmpdir, ignore_errors=True)
    if not os.path.exists(out_png):
        sys.exit("Chrome không xuất được ảnh:\n" + (r.stderr or r.stdout)[-2000:])

    try:
        from PIL import Image
        im = Image.open(out_png)
        if im.size != (int(w * a.scale), int(h * a.scale)):
            print(f"CẢNH BÁO: ảnh {im.size} khác kích thước yêu cầu {(w, h)}")
        print(f"PNG  {out_png}  {im.size[0]}×{im.size[1]}  {os.path.getsize(out_png)/1024:.0f} KB")
        if a.webp:
            out_webp = os.path.splitext(out_png)[0] + ".webp"
            im.convert("RGB").save(out_webp, "WEBP", quality=a.quality, method=6)
            print(f"WEBP {out_webp}  {os.path.getsize(out_webp)/1024:.0f} KB")
    except ImportError:
        print(f"PNG  {out_png}  {os.path.getsize(out_png)/1024:.0f} KB  (cài Pillow để kiểm tra kích thước / xuất WebP)")

if __name__ == "__main__":
    main()
