"""step/large-assembly-700 and step/large-assembly-1200: flat assemblies of many simple distinct parts,
each placed many times. The root holds one sub-assembly per row; each row places parts on a grid,
turned about Z in 15 degree steps. Every part is a planar prism (polygons of 3 to 12 sides, boxes and
L-sections), so the geometry is trivial and the load time is about the product structure and the
number of instances.

    python3 scripts/generators/large_assembly.py 700 step/large-assembly-700
    python3 scripts/generators/large_assembly.py 1200 step/large-assembly-1200
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prism import Node, Part, count, expected, l_section, rect, regular, rot, step_text  # noqa: E402

LAYOUT = {700: (35, 20, 35), 1200: (60, 24, 50)}  # bodies: (distinct parts, rows, parts per row)


def parts(n):
    out = []
    for i in range(n):
        kind = i % 3
        h = 4 + (i * 7) % 23
        if kind == 0:
            out.append(Part(f"prism-{i:03d}", regular(3 + i % 10, 6 + (i % 5) * 1.5, 0.1 * i), h))
        elif kind == 1:
            out.append(Part(f"block-{i:03d}", rect(8 + (i % 6) * 2, 6 + (i % 4) * 3), h))
        else:
            out.append(Part(f"angle-{i:03d}", l_section(14 + i % 5 * 2, 12 + i % 3 * 2, 3), h))
    return out


def model(total):
    n, rows, per_row = LAYOUT[total]
    ps = parts(n)
    root = Node(f"large-assembly-{total}")
    pitch = 30.0
    for r in range(rows):
        row = Node(f"row-{r:02d}")
        for c in range(per_row):
            part = ps[(r * 7 + c) % n]
            row.add(part, rot((0, 0, 1), 15 * ((r + c) % 24)), (c * pitch, 0, 0))
        root.add(row, rot((0, 0, 1), 0), (0, r * pitch, 0))
    return root


if __name__ == "__main__":
    total = int(sys.argv[1])
    out = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(out, exist_ok=True)
    root = model(total)
    name = f"large-assembly-{total}.step"
    path = os.path.join(out, name)
    with open(path, "w", newline="\n") as f:
        f.write(step_text(root, name, f"flat assembly of {total} prism bodies"))
    print(path, count(root), expected(root))
