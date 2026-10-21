"""step/closed-edge-vertex-offsets: five separate open surface bodies, each a 20 mm square face
bounded by a single closed edge: a degree-1 B-spline round the square, parameter range 0 to 1, whose
one vertex sits on the curve at a small parameter past its start: 1e-9, 3e-8, 2e-7, 8e-7 and 5e-6.
The file's distance accuracy is 1e-6 mm.

    python3 scripts/generators/closed_edge_vertex_offsets.py step/closed-edge-vertex-offsets
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prism import f6  # noqa: E402

OFFSETS = [1e-9, 3e-8, 2e-7, 8e-7, 5e-6]
SIDE, GAP = 20.0, 10.0


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
    prod = add(f"PRODUCT('closed-edge-vertex-offsets','closed-edge-vertex-offsets','',(#{pc}))")
    add(f"PRODUCT_RELATED_PRODUCT_CATEGORY('part',$,(#{prod}))")
    pdf = add(f"PRODUCT_DEFINITION_FORMATION('','',#{prod})")
    pd = add(f"PRODUCT_DEFINITION('design','',#{pdf},#{pdc})")
    pds = add(f"PRODUCT_DEFINITION_SHAPE('','',#{pd})")
    zdir, xdir = dr((0, 0, 1)), dr((1, 0, 0))

    models = []
    for k, d in enumerate(OFFSETS):
        x0 = k * (SIDE + GAP)
        P = [(x0, 0, 0), (x0 + SIDE, 0, 0), (x0 + SIDE, SIDE, 0), (x0, SIDE, 0), (x0, 0, 0)]
        # the vertex: the curve's point at parameter d, on its first span (0 .. 0.25)
        f = d / 0.25
        v = tuple(P[0][i] + f * (P[1][i] - P[0][i]) for i in range(3))
        cps = ",".join(f"#{pt(p)}" for p in P)
        curve = add(f"B_SPLINE_CURVE_WITH_KNOTS('',1,({cps}),.UNSPECIFIED.,.T.,.F.,(2,1,1,1,2),(0.,0.25,0.5,0.75,1.),.UNSPECIFIED.)")
        vx = add(f"VERTEX_POINT('',#{pt(v)})")
        ec = add(f"EDGE_CURVE('',#{vx},#{vx},#{curve},.T.)")
        oe = add(f"ORIENTED_EDGE('',*,*,#{ec},.T.)")
        loop = add(f"EDGE_LOOP('',(#{oe}))")
        bound = add(f"FACE_OUTER_BOUND('',#{loop},.T.)")
        plane = add(f"PLANE('',#{add(f'AXIS2_PLACEMENT_3D({chr(39)}{chr(39)},#{pt((x0, 0, 0))},#{zdir},#{xdir})')})")
        face = add(f"ADVANCED_FACE('',(#{bound}),#{plane},.T.)")
        shell = add(f"OPEN_SHELL('',(#{face}))")
        models.append(add(f"SHELL_BASED_SURFACE_MODEL('vertex-at-{d:g}',(#{shell}))"))
    o = add(f"AXIS2_PLACEMENT_3D('',#{pt((0, 0, 0))},#{zdir},#{xdir})")
    rep = add(f"MANIFOLD_SURFACE_SHAPE_REPRESENTATION('closed-edge-vertex-offsets',(#{o},{','.join(f'#{m}' for m in models)}),#{ctx})")
    add(f"SHAPE_DEFINITION_REPRESENTATION(#{pds},#{rep})")
    head = ("ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('closed spline edges whose vertex sits just past the curve start'),'2;1');\n"
            "FILE_NAME('closed-edge-vertex-offsets.step','2026-10-20T00:00:00',('raykholo'),(''),'tangency-labs/models generator','python3 scripts/generators','');\n"
            "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));\nENDSEC;\nDATA;\n")
    return head + "".join(f"#{i + 1}={s};\n" for i, s in enumerate(out)) + "ENDSEC;\nEND-ISO-10303-21;\n"


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "closed-edge-vertex-offsets.step")
    with open(path, "w", newline="\n") as f:
        f.write(step())
    print(path, dict(bodies=len(OFFSETS), area_each=SIDE * SIDE))
