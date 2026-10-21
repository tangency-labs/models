"""step/sliver-faces: one solid, a 60 x 40 x 10 mm block whose outline has short steps 1 um, 10 nm,
0.1 nm and 0.01 nm long, so its side carries four sliver faces of those widths, each 10 mm tall.
The file declares a distance accuracy of 1e-6 mm: two slivers are wider than that, two narrower.

    python3 scripts/generators/sliver_faces.py step/sliver-faces
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prism import Node, Part, count, expected, step_text  # noqa: E402

STEPS = [1e-3, 1e-5, 1e-7, 1e-8]   # mm: the sliver widths


def outline():
    """Counter-clockwise: along the bottom edge, at x = 10, 20, 30, 40 the edge steps up by each width."""
    pts = [(0.0, 0.0)]
    y = 0.0
    for k, w in enumerate(STEPS):
        x = 10.0 * (k + 1)
        pts.append((x, y))
        y += w
        pts.append((x, y))
    pts += [(60.0, y), (60.0, 40.0), (0.0, 40.0)]
    return pts


part = Part("sliver-faces", outline(), 10.0)
top = Node("sliver-faces")
top.add(part)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    name = "sliver-faces.step"
    path = os.path.join(out, name)
    with open(path, "w", newline="\n") as f:
        f.write(step_text(top, name, "a block with sliver side faces"))
    print(path, count(top), expected(top))
