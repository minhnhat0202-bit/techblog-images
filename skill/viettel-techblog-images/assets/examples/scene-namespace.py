# Cảnh isometric cho thumbnail "Namespace trong Kubernetes" — chạy: python3 scene.py > art.svg
import sys, os; sys.path.insert(0, os.path.expanduser('~/.claude/skills/viettel-techblog-images/scripts'))
from iso import Scene
sc = Scene(unit=70)
sc.shadow(0, 0, 6, 4, spread=1.15, opacity=0.20)
sc.slab(0, 0, 0, 6, 4, 0.35, "light")                      # cluster
for xx in (2, 4): sc.divider(xx, 0.2, xx, 3.8, 0.35, color="#C9CACC", width=3, dash="4 12")   # ranh giới namespace
for lane, x0 in enumerate((1, 3, 5)):                        # pods, lane giữa = namespace được nói tới
    pal = "red" if lane == 1 else "mid"
    for yy in (1.0, 3.0): sc.hexprism(x0, yy, 0.35, 0.62, 1.0 if lane == 1 else 0.8, pal)
print(sc.svg(pad=30))
