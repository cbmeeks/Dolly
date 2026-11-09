import base64, gzip, sys
from PIL import Image, ImageEnhance

SRC = sys.argv[1]
OUT = sys.argv[2]
W = 100  # columns

img = Image.open(SRC).convert("RGB")
img = ImageEnhance.Contrast(img).enhance(1.15)

# --- truecolor half-block version: 1 col = 1 px wide, 1 row = 2 px tall
px = img.resize((W, W * img.height // img.width // 2 * 2), Image.LANCZOS)
w, h = px.size
lines = []
for y in range(0, h, 2):
    row = []
    for x in range(w):
        tr, tg, tb = px.getpixel((x, y))
        br, bg, bb = px.getpixel((x, y + 1))
        row.append(f"\x1b[38;2;{tr};{tg};{tb}m\x1b[48;2;{br};{bg};{bb}m▀")
    lines.append("".join(row) + "\x1b[0m")
color = "\n".join(lines) + "\n"

# --- plain ASCII version (chars are ~2x taller than wide)
g = ImageEnhance.Contrast(img.convert("L")).enhance(1.3)
g = g.resize((W, W * img.height // img.width // 2), Image.LANCZOS)
ramp = " .:-=+*#%@"
gw, gh = g.size
ascii_lines = []
for y in range(gh):
    ascii_lines.append("".join(ramp[g.getpixel((x, y)) * (len(ramp) - 1) // 255] for x in range(gw)).rstrip())
plain = "\n".join(ascii_lines) + "\n"

enc = lambda s: base64.b64encode(gzip.compress(s.encode(), 9)).decode()
script = f'''#!/usr/bin/env bash
# Renders a photo-style portrait of Dolly Parton in the terminal.
#   - Truecolor terminal on a TTY: full-color half-block rendering.
#   - Otherwise (piped, NO_COLOR set, or --ascii): plain ASCII shading.
# Usage: ./dolly.sh [--ascii]
set -euo pipefail

COLOR_ART=$(cat <<'__COLOR__'
{enc(color)}
__COLOR__
)

PLAIN_ART=$(cat <<'__PLAIN__'
{enc(plain)}
__PLAIN__
)

show() {{ printf '%s' "$1" | base64 -d | gzip -dc; }}

if [[ "${{1:-}}" != "--ascii" && -t 1 && -z "${{NO_COLOR:-}}" ]]; then
  show "$COLOR_ART"
else
  show "$PLAIN_ART"
fi
'''
open(OUT, "w").write(script)
print("rows", len(lines), "cols", W, "bytes", len(script))
