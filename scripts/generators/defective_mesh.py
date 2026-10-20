"""stl/defective-mesh: one ASCII STL holding the mesh defects readers meet in real files, each in a
known place: two cubes that overlap (self-intersection), two cubes that touch along one edge only
(a non-manifold edge, used by four triangles), a cube with one triangle missing (a hole), a cube
with one triangle flipped, a cube with one triangle written twice, and degenerate triangles (zero
area: three collinear points, and two equal points).

    python3 scripts/generators/defective_mesh.py stl/defective-mesh
"""

import os
import sys


def cube(o, s):
    """12 outward triangles of an axis-aligned cube with corner o and side s."""
    x, y, z = o
    p = [(x, y, z), (x + s, y, z), (x + s, y + s, z), (x, y + s, z),
         (x, y, z + s), (x + s, y, z + s), (x + s, y + s, z + s), (x, y + s, z + s)]
    quads = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    tris = []
    for a, b, c, d in quads:
        tris += [(p[a], p[b], p[c]), (p[a], p[c], p[d])]
    return tris


def solids():
    out = []
    # 1-2: two 20 mm cubes overlapping by 10 mm along X (self-intersecting union)
    out.append(("overlapping-cubes", cube((0, 0, 0), 20) + cube((10, 5, 5), 20)))
    # 3-4: two 20 mm cubes sharing only the edge x = 70, z = 20 (a non-manifold edge)
    out.append(("edge-touching-cubes", cube((50, 0, 0), 20) + cube((70, 0, 20), 20)))
    # 5: a cube with its last top triangle missing (a hole)
    c = cube((0, 50, 0), 20)
    out.append(("cube-with-hole", c[:3] + c[4:]))
    # 6: a cube with one side triangle flipped (inconsistent orientation)
    c = cube((50, 50, 0), 20)
    a, b, d = c[6]
    out.append(("cube-with-flipped-triangle", c[:6] + [(a, d, b)] + c[7:]))
    # 7: a cube with one triangle written twice
    c = cube((100, 0, 0), 20)
    out.append(("cube-with-duplicate-triangle", c + [c[0]]))
    # 8: a closed cube plus two degenerate triangles on its surface (collinear points; two equal points)
    c = cube((100, 50, 0), 20)
    out.append(("cube-with-degenerate-triangles", c + [((100, 50, 0), (110, 50, 0), (120, 50, 0)), ((100, 50, 20), (100, 50, 20), (120, 50, 20))]))
    return out


def num(x):
    return f"{x:.6e}"


def normal(t):
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = t
    u, v = (bx - ax, by - ay, bz - az), (cx - ax, cy - ay, cz - az)
    n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    L = sum(x * x for x in n) ** 0.5
    return tuple(x / L for x in n) if L else (0.0, 0.0, 0.0)


def text():
    lines = ["solid defective-mesh"]
    for name, tris in solids():
        for t in tris:
            n = normal(t)
            lines.append(f"  facet normal {num(n[0])} {num(n[1])} {num(n[2])}")
            lines.append("    outer loop")
            lines += [f"      vertex {num(p[0])} {num(p[1])} {num(p[2])}" for p in t]
            lines.append("    endloop")
            lines.append("  endfacet")
    lines.append("endsolid defective-mesh")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "defective-mesh.stl")
    with open(path, "w", newline="\n") as f:
        f.write(text())
    print(path, {name: len(t) for name, t in solids()}, "triangles", sum(len(t) for _, t in solids()))
