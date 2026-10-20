"""step/component-tree-650: a deep and wide product tree of about 650 components (assemblies and
part occurrences), every assembly a distinct product with its own name, for model-browser stress:
expanding, collapsing, hiding and showing large trees.

    python3 scripts/generators/component_tree.py step/component-tree-650
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prism import IDENTITY, Node, Part, count, expected, rect, regular, rot, step_text  # noqa: E402

PARTS = [Part(f"part-{i:02d}", regular(4 + i % 5, 3 + i % 3, 0.2 * i), 3 + i % 4) for i in range(12)]
PARTS += [Part(f"bar-{i:02d}", rect(12 + i, 3), 2) for i in range(4)]


def tree():
    """root: 5 groups; group: 5 sub-groups; sub-group: 5 modules (distinct products); module: 4 parts.
    Components: 5 + 25 + 125 assemblies + 500 part occurrences = 655."""
    root = Node("component-tree-650")
    k = 0
    for g in range(5):
        group = Node(f"group-{g}")
        for s in range(5):
            sub = Node(f"group-{g}-{s}")
            for m in range(5):
                mod = Node(f"module-{g}-{s}-{m}")
                for p in range(4):
                    mod.add(PARTS[k % len(PARTS)], rot((0, 0, 1), 30 * p), (p * 15.0, 0, 0))
                    k += 1
                sub.add(mod, IDENTITY, (0, m * 12.0, 0))
            group.add(sub, IDENTITY, (s * 70.0, 0, 0))
        root.add(group, rot((0, 0, 1), 0), (0, g * 70.0, 0))
    return root


top = tree()

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    name = "component-tree-650.step"
    path = os.path.join(out, name)
    with open(path, "w", newline="\n") as f:
        f.write(step_text(top, name, "a product tree of 655 components"))
    print(path, count(top), expected(top))
