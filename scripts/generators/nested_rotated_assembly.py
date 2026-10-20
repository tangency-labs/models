"""step/nested-rotated-assembly: four levels of components, every placement at every level turned
about a different, mostly oblique axis, so a reader must compose the rotations in the right order
to put the parts where they belong.

    python3 scripts/generators/nested_rotated_assembly.py step/nested-rotated-assembly
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prism import Node, Part, count, expected, l_section, rect, regular, rot, step_text  # noqa: E402

key = Part("keyed-block", [(0, 0), (30, 0), (30, 10), (20, 10), (20, 20), (0, 20)], 12)   # asymmetric, so a wrong turn shows
peg = Part("tri-peg", regular(3, 5), 24)
plate = Part("plate", rect(60, 40), 4)
angle = Part("angle", l_section(25, 18, 4), 30)

# level 4: a keyed block with a peg standing on it, the peg turned 20 degrees about Z
cell = Node("cell")
cell.add(key)
cell.add(peg, rot((0, 0, 1), 20), (8, 6, 12))

# level 3: two cells on a plate, turned about oblique axes
pair = Node("pair")
pair.add(plate, rot((0, 0, 1), 5), (0, 0, 0))
pair.add(cell, rot((1, 1, 0), 25), (-25, -15, 4))
pair.add(cell, rot((1, -1, 1), -40), (10, 5, 4))

# level 2: three pairs around Z and an angle, each tipped about a different axis
ring = Node("ring")
for k in range(3):
    ring.add(pair, rot((0.3, 0.2, 1), 120 * k + 10), (0, 0, 15 * k))
ring.add(angle, rot((1, 0, 0), 90), (40, 0, 0))

# level 1 (the file): two rings, one upside down about an oblique axis
top = Node("nested-rotated-assembly")
top.add(ring, rot((0, 1, 0), 12), (0, 0, 0))
top.add(ring, rot((1, 2, 3), 180), (150, 0, 60))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    name = "nested-rotated-assembly.step"
    path = os.path.join(out, name)
    with open(path, "w", newline="\n") as f:
        f.write(step_text(top, name, "four levels of rotated components"))
    print(path, count(top), expected(top))
