# dolly-ascii

Dolly Parton in your terminal.

- `dolly.sh` renders a photo-based portrait. On a truecolor terminal it draws full-color
  half-block graphics; when piped, with `NO_COLOR` set, or with `--ascii`, it prints
  plain ASCII shading.
- `dolly-handdrawn.sh` is a hand-drawn ASCII version (tinted blonde/red on a color terminal).
- `tools/gen.py` regenerates `dolly.sh` from a source image (needs Python + Pillow):
  `python3 tools/gen.py photo.png dolly.sh`

The source photograph is not included in this repository.
