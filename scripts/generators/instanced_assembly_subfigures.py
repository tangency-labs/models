"""iges/instanced-assembly-subfigures: an IGES 5.3 assembly whose parts are placed only by subfigure
instances (408) of subfigure definitions (308), nested three levels deep, with rotations about
every axis carried by the instances' transformation matrices (124).

    python3 scripts/generators/instanced_assembly_subfigures.py iges/instanced-assembly-subfigures
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prism import IDENTITY, Node, Part, count, expected, iges_text, l_section, matmul, rect, regular, rot  # noqa: E402

base = Part("base-plate", rect(200, 140), 8)
post = Part("hex-post", regular(6, 9), 60)
cap = Part("square-cap", rect(16, 16), 4)
bracket = Part("l-bracket", l_section(40, 30, 6), 50)
pin = Part("pin", regular(8, 3, 0.2), 70)

# level 3: a post with a cap on each end (the lower cap turned 45 degrees)
capped = Node("capped-post")
capped.add(post)
capped.add(cap, rot((0, 0, 1), 45), (0, 0, -4))
capped.add(cap, IDENTITY, (0, 0, 60))

# level 2: a bracket with a capped post beside it, the post leaning 15 degrees about X
corner = Node("corner-module")
corner.add(bracket)
corner.add(capped, rot((1, 0, 0), 15), (60, 20, 6))

# level 1 (the file): the plate, four corner modules turned 0/90/180/270 about Z, and two pins
# tilted about X and Y; one module also tipped over about the diagonal axis
top = Node("instanced-assembly-subfigures")
top.add(base, IDENTITY, (0, 0, -8))
for k, (x, y) in enumerate([(-80, -50), (80, -50), (80, 50), (-80, 50)]):
    top.add(corner, rot((0, 0, 1), 90 * k), (x, y, 0))
top.add(corner, matmul(rot((1, 1, 0), 120), rot((0, 0, 1), 30)), (0, 0, 120))
top.add(pin, rot((1, 0, 0), 30), (-30, 0, 0))
top.add(pin, rot((0, 1, 0), -30), (30, 0, 0))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "instanced-assembly-subfigures.igs")
    with open(path, "w", newline="\n") as f:
        f.write(iges_text(top, "instanced-assembly-subfigures.igs"))
    print(path, count(top), expected(top))
