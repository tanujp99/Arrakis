"""
Generates the completion badge sprites for Source/Images/Badges.

Kept in the repo so the art is reproducible and reviewable as text rather
than arriving as opaque binaries. Each sprite is authored as a 16x16
character grid and scaled up with nearest-neighbour, so it stays crisp at
any size instead of turning to soup on a 4K display.

Run:  python tools/make_badges.py
"""

from PIL import Image
import os

SCALE = 16          # 16x16 authored, 256x256 written
OUT = os.path.join(os.path.dirname(__file__), "..", "Source", "Images", "Badges")

# Trophy. Read as a cup with handles, a stem and a plinth.
TROPHY = """
................
................
..KKKKKKKKKKKK..
..KLLLLLLLLLLK..
.KKLLLLLLLLLLKK.
.KMKLLLLLLLLKMK.
.KMKKLLLLLLKKMK.
.KMMKKLLLLKKMMK.
..KKK.KLLK.KKK..
.......KLK......
.......KMK......
......KKMKK.....
.....KLMMMLK....
.....KKKKKKK....
....KBBBBBBBK...
....KKKKKKKKK...
"""

# Cut gem. Facets are implied by a lighter top band and a darker lower half.
GEM = """
................
................
................
................
....KKKKKKKK....
...KLLLLLLLLK...
..KLMMMMMMMMLK..
..KBMMMMMMMMBK..
...KBMMMMMMBK...
....KBMMMMBK....
.....KBMMBK.....
......KBBK......
.......KK.......
................
................
................
"""

def fracture(gem):
    """
    Abandoned reuses the gem, split by a fracture.

    Derived rather than hand-typed: drawing the crack by eye produced
    scattered pixels that read as dirt on the sprite instead of a break.
    Walking a single column per row guarantees one continuous line.
    """
    rows = [list(r) for r in gem.strip("\n").split("\n")]
    crack = {5: 8, 6: 7, 7: 8, 8: 7, 9: 8, 10: 7, 11: 7, 12: 7}
    for y, x in crack.items():
        if rows[y][x] != ".":
            rows[y][x] = "K"
    return "\n".join("".join(r) for r in rows)

# In progress. A hollow ring: something is happening, nothing is earned.
# In progress. A small pip, not a ring: it has to say "started" without
# competing with the cover art it sits on.
RING = """
................
................
................
................
................
.......KK.......
......KLLK......
.....KLMMLK.....
.....KLMMLK.....
......KLLK......
.......KK.......
................
................
................
................
................
"""

# K outline, L light, M mid, B dark
PALETTES = {
    "badge_completed": (TROPHY, {"K": "#4A3200", "L": "#FFE07A", "M": "#E9B824", "B": "#8A6508"}),
    "badge_beaten":    (GEM,    {"K": "#06301F", "L": "#7DF3C0", "M": "#10B981", "B": "#0A6E4E"}),
    "badge_abandoned": (fracture(GEM), {"K": "#26292E", "L": "#8B9199", "M": "#5A5F66", "B": "#3A3E44"}),
    "progress_active": (RING,   {"K": "#1E1E1E", "L": "#F2F2F2", "M": "#F2F2F2", "B": "#BFBFBF"}),
    "progress_onhold": (RING,   {"K": "#3D2A00", "L": "#F5C56B", "M": "#F5A623", "B": "#B8791A"}),
}


def hexrgba(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def build(grid, palette, name):
    rows = [r for r in grid.strip("\n").split("\n")]
    assert len(rows) == 16, f"{name}: {len(rows)} rows, expected 16"
    for i, r in enumerate(rows):
        assert len(r) == 16, f"{name}: row {i} is {len(r)} wide, expected 16"

    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            assert ch in palette, f"{name}: no palette entry for {ch!r}"
            px[x, y] = hexrgba(palette[ch])
    return img.resize((16 * SCALE, 16 * SCALE), Image.NEAREST)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (grid, palette) in PALETTES.items():
        img = build(grid, palette, name)
        path = os.path.normpath(os.path.join(OUT, name + ".png"))
        img.save(path)
        print("wrote", path)


if __name__ == "__main__":
    main()
