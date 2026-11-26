# Usage:
#   python3 tools/fox-logo.py component > templates/partials/logo.html   (header logo)
#   python3 tools/fox-logo.py > static/fox.svg                       (standalone, white)

import math, sys

def bez(p, t):
    (x0,y0),(x1,y1),(x2,y2),(x3,y3) = p
    u = 1-t
    x = u**3*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t**3*x3
    y = u**3*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t**3*y3
    dx = 3*u*u*(x1-x0) + 6*u*t*(x2-x1) + 3*t*t*(x3-x2)
    dy = 3*u*u*(y1-y0) + 6*u*t*(y2-y1) + 3*t*t*(y3-y2)
    return x, y, dx, dy

def brush(p, w, start=0.15, end=0.0, peak=0.45, n=28, round_end=False):
    """Filled tapered stroke along a cubic. Width rises from start*w to w at `peak`, falls to end*w.
    round_end finishes the stroke with a semicircle instead of a flat cut or a sharp point."""
    left, right = [], []
    for i in range(n+1):
        t = i/n
        if t <= peak:
            k = start + (1-start) * math.sin(t/peak * math.pi/2)
        else:
            k = end + (1-end) * math.cos((t-peak)/(1-peak) * math.pi/2)
        x, y, dx, dy = bez(p, t)
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy/L, dx/L
        h = w*k/2
        left.append((x+nx*h, y+ny*h)); right.append((x-nx*h, y-ny*h))
    cap = []
    if round_end:
        # x, y, dx, dy, h still hold the values at the end of the stroke:
        # sweep a semicircle round the tip, from the left edge to the right edge
        a = math.atan2(dy, dx)
        for j in range(1, 12):
            th = a + math.pi/2 - math.pi*j/12
            cap.append((x + h*math.cos(th), y + h*math.sin(th)))
    pts = left + cap + right[::-1]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"

def brush_profile(p, w, knots, n=48):
    """Like brush(), but width follows (t, k) knots, smoothly interpolated."""
    def k_at(t):
        for (t0, k0), (t1, k1) in zip(knots, knots[1:]):
            if t0 <= t <= t1:
                f = (t - t0) / (t1 - t0)
                f = (1 - math.cos(f * math.pi)) / 2
                return k0 + (k1 - k0) * f
        return knots[-1][1]
    left, right = [], []
    for i in range(n+1):
        t = i/n
        x, y, dx, dy = bez(p, t)
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy/L, dx/L
        h = w*k_at(t)/2
        left.append((x+nx*h, y+ny*h)); right.append((x-nx*h, y-ny*h))
    pts = left + right[::-1]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"

# Fox at full stretch, running to the right. viewBox 0 0 160 64
parts = [
  # body: one S-curve, thick haunch, narrow waist, deep chest
  brush_profile([(30,36),(52,14),(86,42),(114,15)], 13,
                [(0, 0.3), (0.22, 1.0), (0.5, 0.5), (0.8, 1.0), (1, 0.6)]),
  # neck and head, snout forward
  brush([(108,19),(115,11),(126,8),(143,12)], 9, start=0.8, end=0.22, peak=0.3, round_end=True),
  # ears, both pricked
  brush([(117,13),(118,8),(119,4),(121,1)], 5, start=1.0, end=0.0, peak=0.15),
  brush([(123,12),(125,8),(127,4),(130,2)], 5, start=1.0, end=0.0, peak=0.15),
  # front legs reaching forward together
  brush([(102,24),(116,31),(128,35),(143,36)], 4.6, start=1.0, end=0.15, peak=0.25),
  brush([(97,26),(110,37),(123,41),(136,45)], 4.6, start=1.0, end=0.15, peak=0.25),
  # back legs trailing out behind
  brush([(46,30),(34,38),(21,41),(7,41)], 4.6, start=1.0, end=0.15, peak=0.25),
  brush([(52,30),(42,42),(28,48),(13,51)], 4.6, start=1.0, end=0.15, peak=0.25),
  # tail: long, streaming back with a gentle wave
  brush_profile([(40,28),(24,18),(14,32),(1,22)], 10,
                [(0, 0.5), (0.3, 1.0), (0.75, 0.65), (1, 0.05)]),
]
# eye: punched out of the head (index 1) as a hole
ex, ey, er = 129, 11.2, 1.7
parts[1] += f" M{ex-er} {ey} a{er} {er} 0 1 0 {2*er} 0 a{er} {er} 0 1 0 {-2*er} 0 Z"
body = "\n  ".join(
    f'<path fill-rule="evenodd" d="{d}"/>' if i == 1 else f'<path d="{d}"/>'
    for i, d in enumerate(parts))
mode = sys.argv[1] if len(sys.argv) > 1 else "white"
if mode == "paths":
    print(body)
elif mode == "component":
    # templates/partials/logo.html: inlined in the header, takes the text colour
    print(f'<svg class="brand-mark" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 64" fill="currentColor">\n  {body}\n</svg>')
else:
    print(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 64" fill="#fff">\n  {body}\n</svg>')
