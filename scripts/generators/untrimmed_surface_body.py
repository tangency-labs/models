"""step/untrimmed-surface-body: an open surface body (an open box, 100 x 80 x 50 mm, no lid) whose
floor lies on a B-spline surface 4,000 mm square, trimmed to the 100 x 80 mm floor. The body's
bounding box is the trimmed faces' box; a reader that measures or frames the underlying surface
instead reports a box 40 times too wide.

    python3 scripts/generators/untrimmed_surface_body.py step/untrimmed-surface-body
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prism import f6  # noqa: E402

W, D, H = 100.0, 80.0, 50.0
BIG = 2000.0  # the floor's surface spans -BIG..BIG in X and Y


def step():
    out = []

    def add(s):
        out.append(s)
        return len(out)

    def pt(p):
        return add(f"CARTESIAN_POINT('',({f6(p[0])},{f6(p[1])},{f6(p[2])}))")

    def dr(d):
        return add(f"DIRECTION('',({f6(d[0])},{f6(d[1])},{f6(d[2])}))")

    mm = add("(LENGTH_UNIT()NAMED_UNIT(*)SI_UNIT(.MILLI.,.METRE.))")
    rad = add("(NAMED_UNIT(*)PLANE_ANGLE_UNIT()SI_UNIT($,.RADIAN.))")
    sr = add("(NAMED_UNIT(*)SI_UNIT($,.STERADIAN.)SOLID_ANGLE_UNIT())")
    unc = add(f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-06),#{mm},'distance_accuracy_value','')")
    ctx = add(f"(GEOMETRIC_REPRESENTATION_CONTEXT(3)GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{unc}))"
              f"GLOBAL_UNIT_ASSIGNED_CONTEXT((#{mm},#{rad},#{sr}))REPRESENTATION_CONTEXT('',''))")
    app = add("APPLICATION_CONTEXT('core data for automotive mechanical design processes')")
    add(f"APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,#{app})")
    pc = add(f"PRODUCT_CONTEXT('',#{app},'mechanical')")
    pdc = add(f"PRODUCT_DEFINITION_CONTEXT('part definition',#{app},'design')")
    prod = add(f"PRODUCT('untrimmed-surface-body','untrimmed-surface-body','',(#{pc}))")
    add(f"PRODUCT_RELATED_PRODUCT_CATEGORY('part',$,(#{prod}))")
    pdf = add(f"PRODUCT_DEFINITION_FORMATION('','',#{prod})")
    pd = add(f"PRODUCT_DEFINITION('design','',#{pdf},#{pdc})")
    pds = add(f"PRODUCT_DEFINITION_SHAPE('','',#{pd})")

    # the open box: floor at z=0, four walls up to z=H; vertices bottom 0-3, top 4-7
    P = [(0, 0, 0), (W, 0, 0), (W, D, 0), (0, D, 0), (0, 0, H), (W, 0, H), (W, D, H), (0, D, H)]
    V = [add(f"VERTEX_POINT('',#{pt(p)})") for p in P]
    E = {}

    def edge(a, b):
        if (a, b) in E:
            return E[(a, b)], True
        if (b, a) in E:
            return E[(b, a)], False
        pa, pb = P[a], P[b]
        d = [pb[k] - pa[k] for k in range(3)]
        L = sum(x * x for x in d) ** 0.5
        vec = add(f"VECTOR('',#{dr([x / L for x in d])},{f6(L)})")
        line = add(f"LINE('',#{pt(pa)},#{vec})")
        E[(a, b)] = add(f"EDGE_CURVE('',#{V[a]},#{V[b]},#{line},.T.)")
        return E[(a, b)], True

    def loop(vs):
        oes = []
        for i in range(len(vs)):
            e, fwd = edge(vs[i], vs[(i + 1) % len(vs)])
            oes.append(f"#{add(f'ORIENTED_EDGE({chr(39)}{chr(39)},*,*,#{e},{chr(46)}{chr(84) if fwd else chr(70)}{chr(46)})')}")
        lp = add(f"EDGE_LOOP('',({','.join(oes)}))")
        return add(f"FACE_OUTER_BOUND('',#{lp},.T.)")

    def plane(o, z, x):
        a = add(f"AXIS2_PLACEMENT_3D('',#{pt(o)},#{dr(z)},#{dr(x)})")
        return add(f"PLANE('',#{a})")

    # the floor's surface: a flat bilinear B-spline patch, 4,000 mm square, normal -Z (outward, down)
    cp = [[pt((-BIG, -BIG, 0)), pt((BIG, -BIG, 0))], [pt((-BIG, BIG, 0)), pt((BIG, BIG, 0))]]
    rows = ",".join("(" + ",".join(f"#{c}" for c in r) + ")" for r in cp)
    # u along +Y, v along +X: du x dv = Y x X = -Z, so the surface normal points out of the box
    bss = add(f"B_SPLINE_SURFACE_WITH_KNOTS('',1,1,({rows}),.PLANE_SURF.,.F.,.F.,.F.,(2,2),(2,2),(0.,1.),(0.,1.),.UNSPECIFIED.)")
    faces = [add(f"ADVANCED_FACE('floor',(#{loop([0, 3, 2, 1])}),#{bss},.T.)")]
    walls = [([0, 1, 5, 4], (0, -1, 0), (1, 0, 0)), ([1, 2, 6, 5], (1, 0, 0), (0, 1, 0)),
             ([2, 3, 7, 6], (0, 1, 0), (-1, 0, 0)), ([3, 0, 4, 7], (-1, 0, 0), (0, -1, 0))]
    for vs, n, x in walls:
        faces.append(add(f"ADVANCED_FACE('',(#{loop(vs)}),#{plane(P[vs[0]], n, x)},.T.)"))
    shell = add(f"OPEN_SHELL('',({','.join(f'#{f}' for f in faces)}))")
    model = add(f"SHELL_BASED_SURFACE_MODEL('untrimmed-surface-body',(#{shell}))")
    o = add(f"AXIS2_PLACEMENT_3D('',#{pt((0, 0, 0))},#{dr((0, 0, 1))},#{dr((1, 0, 0))})")
    rep = add(f"MANIFOLD_SURFACE_SHAPE_REPRESENTATION('untrimmed-surface-body',(#{o},#{model}),#{ctx})")
    add(f"SHAPE_DEFINITION_REPRESENTATION(#{pds},#{rep})")
    head = ("ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('open surface body on a much larger surface'),'2;1');\n"
            "FILE_NAME('untrimmed-surface-body.step','2026-10-20T00:00:00',('raykholo'),(''),'tangency-labs/models generator','python3 scripts/generators','');\n"
            "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));\nENDSEC;\nDATA;\n")
    return head + "".join(f"#{i + 1}={s};\n" for i, s in enumerate(out)) + "ENDSEC;\nEND-ISO-10303-21;\n"


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "untrimmed-surface-body.step")
    with open(path, "w", newline="\n") as f:
        f.write(step())
    print(path, dict(faces=5, area=W * D + 2 * (W + D) * H, bbox=[0, 0, 0, W, D, H], surface_extent=[-BIG, -BIG, BIG, BIG]))
