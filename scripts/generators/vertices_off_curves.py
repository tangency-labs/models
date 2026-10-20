"""step/vertices-off-curves: an open surface model, a 4 x 4 grid of square faces 50 mm across
(a 200 x 200 mm sheet, gently domed), whose edge curves end 0.19 mm beside their vertices, while the
file declares a distance accuracy of 0.01 mm. Every edge is a B-spline curve; every face a
bilinear B-spline patch through the true corner points.

Exporters do write this: an edge's curve and its vertex disagree by more than the declared
accuracy, though the gap is small next to the model.

    python3 scripts/generators/vertices_off_curves.py step/vertices-off-curves
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prism import f6  # noqa: E402

N, CELL = 4, 50.0
GAP = 0.19          # how far each curve end sits beside its vertex, mm
ACCURACY = 0.01     # the file's declared distance accuracy, mm


def z(x, y):
    return 8.0 * math.sin(math.pi * x / (N * CELL)) * math.sin(math.pi * y / (N * CELL))


def step():
    out = []

    def add(s):
        out.append(s)
        return len(out)

    def pt(p):
        return add(f"CARTESIAN_POINT('',({f6(p[0])},{f6(p[1])},{f6(p[2])}))")

    mm = add("(LENGTH_UNIT()NAMED_UNIT(*)SI_UNIT(.MILLI.,.METRE.))")
    rad = add("(NAMED_UNIT(*)PLANE_ANGLE_UNIT()SI_UNIT($,.RADIAN.))")
    sr = add("(NAMED_UNIT(*)SI_UNIT($,.STERADIAN.)SOLID_ANGLE_UNIT())")
    unc = add(f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE({f6(ACCURACY)}),#{mm},'distance_accuracy_value','')")
    ctx = add(f"(GEOMETRIC_REPRESENTATION_CONTEXT(3)GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{unc}))"
              f"GLOBAL_UNIT_ASSIGNED_CONTEXT((#{mm},#{rad},#{sr}))REPRESENTATION_CONTEXT('',''))")
    app = add("APPLICATION_CONTEXT('core data for automotive mechanical design processes')")
    add(f"APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,#{app})")
    pc = add(f"PRODUCT_CONTEXT('',#{app},'mechanical')")
    pdc = add(f"PRODUCT_DEFINITION_CONTEXT('part definition',#{app},'design')")
    prod = add(f"PRODUCT('vertices-off-curves','vertices-off-curves','',(#{pc}))")
    add(f"PRODUCT_RELATED_PRODUCT_CATEGORY('part',$,(#{prod}))")
    pdf = add(f"PRODUCT_DEFINITION_FORMATION('','',#{prod})")
    pd = add(f"PRODUCT_DEFINITION('design','',#{pdf},#{pdc})")
    pds = add(f"PRODUCT_DEFINITION_SHAPE('','',#{pd})")

    P = {(i, j): (i * CELL, j * CELL, z(i * CELL, j * CELL)) for i in range(N + 1) for j in range(N + 1)}
    V = {k: add(f"VERTEX_POINT('',#{pt(p)})") for k, p in P.items()}

    def off(p, d):
        """p moved GAP sideways from the edge direction d, in the XY plane."""
        L = math.hypot(d[0], d[1])
        nx, ny = -d[1] / L, d[0] / L
        return (p[0] + GAP * nx, p[1] + GAP * ny, p[2])

    E = {}

    def edge(a, b):
        if (a, b) in E:
            return E[(a, b)], True
        if (b, a) in E:
            return E[(b, a)], False
        pa, pb = P[a], P[b]
        d = (pb[0] - pa[0], pb[1] - pa[1])
        # a cubic through four points of the true edge, its two ends moved GAP sideways
        pts = []
        for k in range(4):
            t = k / 3
            x, y = pa[0] + t * d[0], pa[1] + t * d[1]
            q = (x, y, z(x, y))
            pts.append(off(q, d) if k in (0, 3) else q)
        ids = ",".join(f"#{pt(q)}" for q in pts)
        c = add(f"B_SPLINE_CURVE_WITH_KNOTS('',3,({ids}),.UNSPECIFIED.,.F.,.F.,(4,4),(0.,1.),.UNSPECIFIED.)")
        E[(a, b)] = add(f"EDGE_CURVE('',#{V[a]},#{V[b]},#{c},.T.)")
        return E[(a, b)], True

    faces = []
    for i in range(N):
        for j in range(N):
            ring = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]  # counter-clockwise from above: normal +Z
            oes = []
            for k in range(4):
                e, fwd = edge(ring[k], ring[(k + 1) % 4])
                oes.append(f"#{add(f'ORIENTED_EDGE({chr(39)}{chr(39)},*,*,#{e},{chr(46)}{chr(84) if fwd else chr(70)}{chr(46)})')}")
            loop = add(f"EDGE_LOOP('',({','.join(oes)}))")
            bound = add(f"FACE_OUTER_BOUND('',#{loop},.T.)")
            # bilinear patch through the corners, u along +X, v along +Y: du x dv = +Z
            c = [[P[(i, j)], P[(i, j + 1)]], [P[(i + 1, j)], P[(i + 1, j + 1)]]]
            rows = ",".join("(" + ",".join(f"#{pt(q)}" for q in r) + ")" for r in c)
            s = add(f"B_SPLINE_SURFACE_WITH_KNOTS('',1,1,({rows}),.UNSPECIFIED.,.F.,.F.,.F.,(2,2),(2,2),(0.,1.),(0.,1.),.UNSPECIFIED.)")
            faces.append(add(f"ADVANCED_FACE('',(#{bound}),#{s},.T.)"))
    shell = add(f"OPEN_SHELL('',({','.join(f'#{f}' for f in faces)}))")
    model = add(f"SHELL_BASED_SURFACE_MODEL('vertices-off-curves',(#{shell}))")
    o = add(f"AXIS2_PLACEMENT_3D('',#{pt((0, 0, 0))},#{add(chr(68) + 'IRECTION' + chr(40) + chr(39) + chr(39) + ',(0.,0.,1.))')},#{add('DIRECTION(' + chr(39) + chr(39) + ',(1.,0.,0.))')})")
    rep = add(f"MANIFOLD_SURFACE_SHAPE_REPRESENTATION('vertices-off-curves',(#{o},#{model}),#{ctx})")
    add(f"SHAPE_DEFINITION_REPRESENTATION(#{pds},#{rep})")
    head = ("ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('surface grid whose edge curves end beside their vertices'),'2;1');\n"
            "FILE_NAME('vertices-off-curves.step','2026-10-20T00:00:00',('raykholo'),(''),'tangency-labs/models generator','python3 scripts/generators','');\n"
            "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));\nENDSEC;\nDATA;\n")
    return head + "".join(f"#{i + 1}={s};\n" for i, s in enumerate(out)) + "ENDSEC;\nEND-ISO-10303-21;\n"


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "vertices-off-curves.step")
    with open(path, "w", newline="\n") as f:
        f.write(step())
    print(path, dict(faces=N * N, edges=2 * N * (N + 1), vertices=(N + 1) ** 2, gap_mm=GAP, accuracy_mm=ACCURACY))
