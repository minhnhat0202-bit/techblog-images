#!/usr/bin/env python3
"""Isometric-gradient primitives in the Viettel palette → SVG string.

Usage in a scene script:
    from iso import Scene
    sc = Scene(unit=60)                       # 1 grid unit = 60 px
    sc.slab(0, 0, 0, 6, 4, 0.3, "light")      # x, y, z, w, d, h, palette
    sc.cube(1, 1, 0.3, 1, 1, 1, "red")
    html_svg = sc.svg(pad=40)                 # <svg …> with gradients + soft shadow, auto viewBox

Palettes: light · mid · dark · red · white. Axes: x runs down-right, y runs down-left, z up.
Paint order is a topological sort on bounding boxes: A before B when A is entirely farther along x or y, or lower in z.
"""
import math

COS30, SIN30 = math.cos(math.radians(30)), 0.5

PAL = {  # (top_a, top_b), (left_a, left_b), (right_a, right_b)
    "white": (("#FFFFFF", "#F7F7F8"), ("#EEEEEF", "#E2E3E5"), ("#DADBDD", "#CBCCCE")),
    "light": (("#FFFFFF", "#F2F2F2"), ("#E4E5E7", "#D2D3D5"), ("#C8C9CB", "#B5B4B4")),
    "mid":   (("#DADBDD", "#C4C5C7"), ("#B5B4B4", "#9D9D9F"), ("#8F9093", "#6F7377")),
    "dark":  (("#6B7075", "#44494D"), ("#44494D", "#34383B"), ("#2C2F32", "#1E2124")),
    "red":   (("#FF4D70", "#EE0033"), ("#EE0033", "#CC002B"), ("#C10029", "#950020")),
}

class Scene:
    def __init__(self, unit=60):
        self.u = unit
        self.items = []   # (bbox=(x0,x1,y0,y1,z0,z1), svg)
        self.defs = []
        self._gid = 0
        self.minx = self.miny = 1e9; self.maxx = self.maxy = -1e9

    # ---- projection ----
    def P(self, x, y, z):
        sx = (x - y) * COS30 * self.u
        sy = (x + y) * SIN30 * self.u - z * self.u
        self.minx, self.maxx = min(self.minx, sx), max(self.maxx, sx)
        self.miny, self.maxy = min(self.miny, sy), max(self.maxy, sy)
        return sx, sy

    def _grad(self, a, b, x1, y1, x2, y2):
        self._gid += 1
        gid = f"g{self._gid}"
        self.defs.append(f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
                         f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')
        return gid

    def _poly(self, pts, fill, stroke=None):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        s = f' stroke="{stroke}" stroke-width="1.5" stroke-linejoin="round"' if stroke else ''
        return f'<polygon points="{d}" fill="{fill}"{s}/>'

    # ---- primitives ----
    def cube(self, x, y, z, w, d, h, pal="light", edge=True):
        """Box with top / left(front-left, y+d) / right(front-right, x+w) faces."""
        t, l, r = PAL[pal]
        top = [self.P(x, y, z+h), self.P(x+w, y, z+h), self.P(x+w, y+d, z+h), self.P(x, y+d, z+h)]
        left = [self.P(x, y+d, z), self.P(x+w, y+d, z), self.P(x+w, y+d, z+h), self.P(x, y+d, z+h)]
        right = [self.P(x+w, y, z), self.P(x+w, y+d, z), self.P(x+w, y+d, z+h), self.P(x+w, y, z+h)]
        gt = self._grad(*t, 0, 0, 1, 1); gl = self._grad(*l, 0, 0, 0, 1); gr = self._grad(*r, 0, 0, 0, 1)
        ec = "rgba(255,255,255,.55)" if pal in ("light", "white", "mid") else "rgba(255,255,255,.18)"
        svg = self._poly(left, f"url(#{gl})") + self._poly(right, f"url(#{gr})") + self._poly(top, f"url(#{gt})", ec if edge else None)
        self._add((x, x+w, y, y+d, z, z+h), svg)

    def slab(self, x, y, z, w, d, h=0.25, pal="light"):
        self.cube(x, y, z, w, d, h, pal)

    def cylinder(self, x, y, z, r, h, pal="light"):
        """Vertical cylinder centred at grid (x, y)."""
        t, l, rr = PAL[pal]
        cx, cy = self.P(x, y, z); tx, ty = self.P(x, y, z+h)
        rx, ry = r * self.u * COS30 * 2 / 2 * 1.0, r * self.u * SIN30
        rx = r * self.u * COS30; ry = r * self.u * 0.5
        gb = self._grad(l[0], rr[1], 0, 0, 1, 0); gt = self._grad(*t, 0, 0, 1, 1)
        body = (f'<path d="M{cx-rx:.1f},{cy:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {cx+rx:.1f},{cy:.1f} '
                f'L{tx+rx:.1f},{ty:.1f} A{rx:.1f},{ry:.1f} 0 0 1 {tx-rx:.1f},{ty:.1f} Z" fill="url(#{gb})"/>')
        top = f'<ellipse cx="{tx:.1f}" cy="{ty:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#{gt})" stroke="rgba(255,255,255,.5)" stroke-width="1.5"/>'
        self._track(cx - rx, cy + ry); self._track(cx + rx, ty - ry)
        self._add((x-r, x+r, y-r, y+r, z, z+h), body + top)

    def hexprism(self, x, y, z, r, h, pal="light"):
        """Hexagonal prism (pointy along x) centred at (x, y) — handy for Kubernetes pods."""
        t, l, rr = PAL[pal]
        ang = [math.radians(a) for a in (0, 60, 120, 180, 240, 300)]
        base = [(x + r * math.cos(a), y + r * math.sin(a)) for a in ang]
        top = [self.P(px, py, z+h) for px, py in base]
        gt = self._grad(*t, 0, 0, 1, 1)
        sides = ""
        # visible sides: those whose outward normal points toward the viewer (+x or +y)
        for i in range(6):
            (ax, ay), (bx, by) = base[i], base[(i+1) % 6]
            nx, ny = (by - ay), -(bx - ax)  # outward normal for CCW vertex order
            if nx + ny <= 0.01:
                continue
            shade = l if ny > nx else rr
            g = self._grad(*shade, 0, 0, 0, 1)
            sides += self._poly([self.P(ax, ay, z), self.P(bx, by, z), self.P(bx, by, z+h), self.P(ax, ay, z+h)], f"url(#{g})")
        self._add((x-r, x+r, y-r, y+r, z, z+h), sides + self._poly(top, f"url(#{gt})", "rgba(255,255,255,.4)"))

    def divider(self, x1, y1, x2, y2, z, color="#DADBDD", width=2.5, dash=None):
        a, b = self.P(x1, y1, z), self.P(x2, y2, z)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self._add((min(x1,x2), max(x1,x2), min(y1,y2), max(y1,y2), z, z), f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{d}/>')

    def shadow(self, x, y, w, d, spread=1.25, opacity=0.22):
        """Soft elliptical ground shadow under a footprint (x, y, w, d)."""
        cx, cy = self.P(x + w/2, y + d/2, 0)
        rx = (w + d) * COS30 * self.u / 2 * spread; ry = rx * 0.5
        self._gid += 1; gid = f"g{self._gid}"
        self.defs.append(f'<radialGradient id="{gid}"><stop offset="0" stop-color="#44494D" stop-opacity="{opacity}"/>'
                         f'<stop offset="1" stop-color="#44494D" stop-opacity="0"/></radialGradient>')
        self._track(cx - rx, cy - ry); self._track(cx + rx, cy + ry)
        self._add((x, x+w, y, y+d, -1.0, -0.99), f'<ellipse cx="{cx:.1f}" cy="{cy + ry*0.35:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#{gid})"/>')

    def _track(self, sx, sy):
        self.minx, self.maxx = min(self.minx, sx), max(self.maxx, sx)
        self.miny, self.maxy = min(self.miny, sy), max(self.maxy, sy)

    def _add(self, bbox, svg):
        self.items.append((bbox, svg))

    @staticmethod
    def _behind(a, b, eps=1e-6):
        """True if box a must be painted before box b: a lies entirely on the far side along x, y, or below along z.
        Viewer sits at +x, +y, +z, so smaller coordinates are farther away."""
        ax0, ax1, ay0, ay1, az0, az1 = a; bx0, bx1, by0, by1, bz0, bz1 = b
        return ax1 <= bx0 + eps or ay1 <= by0 + eps or az1 <= bz0 + eps

    def _order(self):
        n = len(self.items); boxes = [b for b, _ in self.items]
        after = [[] for _ in range(n)]   # after[i] = items that must be painted after i
        indeg = [0] * n
        for i in range(n):
            for j in range(n):
                if i == j: continue
                ib, jb = self._behind(boxes[i], boxes[j]), self._behind(boxes[j], boxes[i])
                if ib and not jb:
                    after[i].append(j); indeg[j] += 1
        # Kahn's algorithm; ties broken by (z, x+y) so output is deterministic
        import heapq
        key = lambda i: (boxes[i][4], boxes[i][0] + boxes[i][2], i)
        ready = [key(i) for i in range(n) if indeg[i] == 0]; heapq.heapify(ready)
        out = []
        while ready:
            _, _, i = heapq.heappop(ready); out.append(i)
            for j in after[i]:
                indeg[j] -= 1
                if indeg[j] == 0: heapq.heappush(ready, key(j))
        if len(out) < n:  # cycle (intersecting boxes) → append the rest by heuristic
            out += sorted((i for i in range(n) if i not in out), key=key)
        return out

    def svg(self, pad=40, cls=""):
        order = self._order()
        w, h = self.maxx - self.minx + 2*pad, self.maxy - self.miny + 2*pad
        body = "".join(self.items[i][1] for i in order)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" class="{cls}" viewBox="{self.minx-pad:.1f} {self.miny-pad:.1f} {w:.1f} {h:.1f}">'
                f'<defs>{"".join(self.defs)}</defs>{body}</svg>')
