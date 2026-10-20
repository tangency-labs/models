"""iges/trimmed-patch-cube: a closed 100 mm cube given only as trimmed surfaces (144), nine B-spline
patches (128) per side, each trimmed by a curve on surface (142) whose model-space curve is a
composite (102) of line (110) and B-spline (126) pieces. Some trims are written with pieces running
end to start, and some pieces stop 0.02 mm short of the next one, as exporters do.

There are no solid entities: a reader sews the 54 faces into a closed shell to get a solid.

    python3 scripts/generators/trimmed_patch_cube.py iges/trimmed-patch-cube
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prism import DEP, Iges, f6  # noqa: E402

L, K = 100.0, 3           # cube size, patches per side along each direction
GAP = 0.02                # how far a shortened trim piece stops before the next, mm

# the six sides: origin corner, u direction, v direction (u x v points out of the cube)
SIDES = [((0, 0, 0), (0, 1, 0), (1, 0, 0)),   # z = 0, normal -Z
         ((0, 0, L), (1, 0, 0), (0, 1, 0)),   # z = L, normal +Z
         ((0, 0, 0), (1, 0, 0), (0, 0, 1)),   # y = 0, normal -Y
         ((0, L, 0), (0, 0, 1), (1, 0, 0)),   # y = L, normal +Y
         ((0, 0, 0), (0, 0, 1), (0, 1, 0)),   # x = 0, normal -X
         ((L, 0, 0), (0, 1, 0), (0, 0, 1))]   # x = L, normal +X


def at(o, u, v, a, b):
    return tuple(o[k] + a * u[k] + b * v[k] for k in range(3))


def cube():
    ig = Iges()
    n = 0
    for s, (o, u, v) in enumerate(SIDES):
        step = L / K
        for i in range(K):
            for j in range(K):
                n += 1
                c = [at(o, u, v, i * step, j * step), at(o, u, v, (i + 1) * step, j * step),
                     at(o, u, v, (i + 1) * step, (j + 1) * step), at(o, u, v, i * step, (j + 1) * step)]
                # the patch: degree 1 x 1, control points (u-major as IGES orders them: s fastest)
                cps = [c[0], c[1], c[3], c[2]]
                surf = ig.add(128, [1, 1, 1, 1, 0, 0, 1, 0, 0, "0.", "0.", "1.", "1.", "0.", "0.", "1.", "1.", "1.", "1.", "1.", "1."]
                              + [f6(x) for p in cps for x in p] + ["0.", "1.", "0.", "1."], status=DEP)
                # the trim: four pieces round the patch, counter-clockwise seen from outside
                pieces = []
                for e in range(4):
                    a, b = c[e], c[(e + 1) % 4]
                    reverse = (n + e) % 5 == 0            # some pieces written end to start
                    short = (n * 7 + e) % 6 == 0          # some pieces stop GAP before the next
                    if short:
                        d = [b[k] - a[k] for k in range(3)]
                        ln = sum(x * x for x in d) ** 0.5
                        b = tuple(b[k] - GAP * d[k] / ln for k in range(3))
                    p, q = (b, a) if reverse else (a, b)
                    if (n + e) % 2:
                        pieces.append(ig.add(110, [f6(x) for x in p + q], status=DEP))
                    else:
                        # the same straight piece as a degree-1 B-spline (126), knots 0..1
                        pieces.append(ig.add(126, [1, 1, 0, 0, 1, 0, "0.", "0.", "1.", "1.", "1.", "1."]
                                             + [f6(x) for x in p + q] + ["0.", "1.", "0.", "0.", "0."], status=DEP))
                comp = ig.add(102, [4] + pieces, status=DEP)
                cos = ig.add(142, [0, surf, 0, comp, 2], status=DEP)
                ig.add(144, [surf, 1, 0, cos], label=f"S{s}P{i}{j}")
    return ig.text("trimmed-patch-cube.igs", L), n


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "trimmed-patch-cube.igs")
    text, n = cube()
    with open(path, "w", newline="\n") as f:
        f.write(text)
    print(path, dict(faces=n, volume=L ** 3, area=6 * L * L))
