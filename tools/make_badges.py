"""
Generates the completion badge sprites for Source/Images/Badges.

Kept in the repo so the art is reproducible and reviewable as text rather
than arriving as opaque binaries. Each sprite is authored as a 16x16
character grid and scaled up with nearest-neighbour, so it stays crisp at
any size instead of turning to soup on a 4K display.

Run:  python tools/make_badges.py

Playnite holds the PNGs open while it is running. Close it first or the
write fails with a permission error.
"""

from PIL import Image
import os

SCALE = 16          # 16x16 authored, 256x256 written
OUT = os.path.join(os.path.dirname(__file__), "..", "Source", "Images", "Badges")


# --------------------------------------------------------------------------
# sprites
# --------------------------------------------------------------------------

# Trophy. Used on the details panel for anything finished, beaten or
# completed alike: there is room there for the handles and stem to read.
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

# Medal. Used on grid tiles for a completed game, where a trophy's handles
# and stem collapse into noise but a disc on a ribbon still reads.
MEDAL = """
................
.....KKKKKK.....
....KBBBBBBK....
...KBBAAAABBK...
..KBBAAAAAABBK..
..KBAAAAAAAABK..
..KBBAAAAAABBK..
...KBBAAAABBK...
....KBBBBBBK....
.....KKKKKK.....
...KRRK..KRRK...
..KRRRK..KRRRK..
..KRRK....KRRK..
..KK........KK..
................
................
"""

# Cut gem, brilliant cut seen face on. Grid tiles use it for a beaten game.
#
# Crown across the top: a bright table with lighter side facets falling away
# from it. Pavilion below: facets converging on the point, with a lighter
# column down the centre standing in for the reflection that makes a real
# stone look lit from inside. Five tones plus the outline, which is what a
# gem needs to stop reading as a coloured triangle.
GEM = """
................
................
....KKKKKKKK....
...KAAAAAAAAK...
..KBBAAAAAABBK..
.KBBBCCCCCCBBBK.
..KEDDDDDDDDEK..
...KEDDCCDDEK...
....KEDCCDEK....
.....KECCEK.....
......KCCK......
.......KK.......
................
................
................
................
"""

# In progress. A small pip parked in the bottom-right of the canvas, not a
# ring in the middle of it: centred, it read as something placed on the
# artwork rather than a marker tucked out of the way.
PIP = """
................
................
................
................
................
................
................
................
................
................
...........KK...
..........KAAK..
.........KADDAK.
.........KADDAK.
..........KAAK..
...........KK...
"""


def fracture(gem):
    """
    Abandoned reuses the gem, split by a fracture.

    Derived rather than hand-typed: drawing the crack by eye produced
    scattered pixels that read as dirt on the sprite instead of a break.
    Walking a single column per row guarantees one continuous line.
    """
    rows = [list(r) for r in gem.strip("\n").split("\n")]
    crack = {3: 8, 4: 7, 5: 8, 6: 7, 7: 8, 8: 7, 9: 8, 10: 7}
    for y, x in crack.items():
        if rows[y][x] != ".":
            rows[y][x] = "K"
    return "\n".join("".join(r) for r in rows)


# --------------------------------------------------------------------------
# colour
# --------------------------------------------------------------------------

def hexrgba(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def mix(c, t, amt):
    c, t = hexrgba(c)[:3], hexrgba(t)[:3]
    return "#%02X%02X%02X" % tuple(round(a + (b - a) * amt) for a, b in zip(c, t))


def ramp(base, outline=None):
    """
    Builds a sprite's five tones from a single colour.

    Hand-picking every shade meant a new gem needed five judgement calls and
    tended to come out flat, because the steps were never quite even. Mixing
    toward white and black instead keeps the ramp consistent, so a sprite is
    defined by the one colour it actually is.
    """
    return {
        "A": mix(base, "#FFFFFF", 0.78),   # table highlight
        "B": mix(base, "#FFFFFF", 0.48),   # crown facets
        "C": mix(base, "#FFFFFF", 0.20),   # girdle, centre reflection
        "D": base,                          # body
        "E": mix(base, "#000000", 0.34),   # pavilion shadow
        "K": outline or mix(base, "#000000", 0.78),
    }


def medal_palette(gold, ribbon):
    """The medal needs two ramps: the disc's gold and the ribbon's red."""
    g, r = ramp(gold), ramp(ribbon)
    return {"K": g["K"], "A": g["B"], "B": g["D"], "R": r["D"]}


def trophy_palette(gold):
    g = ramp(gold)
    return {"K": g["K"], "L": g["A"], "M": g["D"], "B": g["E"]}


PALETTES = {
    "badge_trophy":    (TROPHY, trophy_palette("#E9B824")),
    "badge_medal":     (MEDAL, medal_palette("#E9B824", "#D8324B")),
    "badge_beaten":    (GEM, ramp("#10B981")),
    "badge_abandoned": (fracture(GEM), ramp("#5A5F66")),
    "pip_playing":     (PIP, ramp("#22C55E")),
    "pip_plan":        (PIP, ramp("#E8EAED")),
    "pip_onhold":      (PIP, ramp("#F5A623")),
}


# --------------------------------------------------------------------------

def build(grid, palette, name):
    rows = grid.strip("\n").split("\n")
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
