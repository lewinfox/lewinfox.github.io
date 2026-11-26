# Generates the 1200x630 social preview image (og:image) from the hero photo.
# Needs Pillow (pip install pillow). Usage, from the repo root:
#   python3 tools/social-image.py static/img/hero-2000.webp static/fonts/fraunces.woff2 static/fonts/inter.woff2 static/img/social.jpg

import sys
from PIL import Image, ImageDraw, ImageFont
src, serif, sans, out = sys.argv[1:5]
W, H = 1200, 630
im = Image.open(src).convert("RGB")
# Cover-crop to 1200x630, biased upwards like the site's "center 30%"
scale = max(W / im.width, H / im.height)
im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
top = round((im.height - H) * 0.3)
left = (im.width - W) // 2
im = im.crop((left, top, left + W, top + H))
# Darken the lower part so the text reads, like the site's gradient
shade = Image.new("L", (1, H))
for y in range(H):
    t = max(0.0, (y / H - 0.35) / 0.65)
    shade.putpixel((0, y), round(255 * (0.15 + 0.7 * t)))
shade = shade.resize((W, H))
im = Image.composite(Image.new("RGB", (W, H), (8, 14, 18)), im, shade)
d = ImageDraw.Draw(im)
f1 = ImageFont.truetype(serif, 84)
try:
    f1.set_variation_by_axes([72, 560])
except Exception:
    pass
f2 = ImageFont.truetype(sans, 34)
try:
    f2.set_variation_by_axes([400] if len(f2.get_variation_axes()) == 1 else [14, 400])
except Exception:
    pass
d.text((72, 410), "Lewin Fox", font=f1, fill="white")
d.text((74, 515), "Apps and websites for businesses · Queenstown, NZ", font=f2, fill=(230, 233, 234))
im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
