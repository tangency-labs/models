"""step/toothed-plate-50k-faces: one solid with 50,002 faces: a 500 mm square plate, 5 mm thick,
whose outline is 12,500 square teeth 0.08 mm wide and 0.5 mm deep. Every face is planar; the top
and bottom faces are each bounded by one loop of 50,000 edges.

    python3 scripts/generators/toothed_plate.py step/toothed-plate-50k-faces
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prism import Part, f6  # noqa: E402

SIDE, THICK = 500.0, 5.0
TEETH_PER_SIDE = 3125      # 4 sides x 3125 teeth x 4 edges = 50,000 outline edges
DEPTH = 0.5


def outline():
    """Counter-clockwise square-wave outline round the square: each tooth goes out, along, in, along."""
    pitch = SIDE / TEETH_PER_SIDE   # 0.16 mm: a tooth 0.08 wide, a gap 0.08 wide
    half = pitch / 2
    pts = []
    # each side: start corner, along direction, outward normal
    sides = [((0, 0), (1, 0), (0, -1)), ((SIDE, 0), (0, 1), (1, 0)), ((SIDE, SIDE), (-1, 0), (0, 1)), ((0, SIDE), (0, -1), (-1, 0))]
    for (sx, sy), (dx, dy), (nx, ny) in sides:
        for k in range(TEETH_PER_SIDE):
            t0, t1 = k * pitch, k * pitch + half
            for t, out in ((t0, 0), (t0, DEPTH), (t1, DEPTH), (t1, 0)):
                pts.append((round(sx + dx * t + nx * out, 6), round(sy + dy * t + ny * out, 6)))
    return pts


def step_text(part, file_name):
    """One prism as AP214, writing each distinct point, direction, vector and placement once."""
    out, seen = [], {}

    def add(s, share=False):
        if share and s in seen:
            return seen[s]
        out.append(s)
        if share:
            seen[s] = len(out)
        return len(out)

    def pt(p):
        return add(f"CARTESIAN_POINT('',({f6(p[0])},{f6(p[1])},{f6(p[2])}))", True)

    def dr(d):
        return add(f"DIRECTION('',({f6(d[0])},{f6(d[1])},{f6(d[2])}))", True)

    def ax(o, z, x):
        return add(f"AXIS2_PLACEMENT_3D('',#{pt(o)},#{dr(z)},#{dr(x)})", True)

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
    prod = add(f"PRODUCT('{part.name}','{part.name}','',(#{pc}))")
    add(f"PRODUCT_RELATED_PRODUCT_CATEGORY('part',$,(#{prod}))")
    pdf = add(f"PRODUCT_DEFINITION_FORMATION('','',#{prod})")
    pd = add(f"PRODUCT_DEFINITION('design','',#{pdf},#{pdc})")
    pds = add(f"PRODUCT_DEFINITION_SHAPE('','',#{pd})")

    n, h = len(part.poly), part.h
    P = [(x, y, 0.0) for x, y in part.poly] + [(x, y, h) for x, y in part.poly]
    V = [add(f"VERTEX_POINT('',#{pt(p)})") for p in P]

    def edge(a, b):
        pa, pb = P[a], P[b]
        d = [pb[k] - pa[k] for k in range(3)]
        L = math.sqrt(sum(x * x for x in d))
        vec = add(f"VECTOR('',#{dr([x / L for x in d])},{f6(L)})", True)
        line = add(f"LINE('',#{pt(pa)},#{vec})")
        return add(f"EDGE_CURVE('',#{V[a]},#{V[b]},#{line},.T.)")

    bot = [edge(i, (i + 1) % n) for i in range(n)]
    tops = [edge(n + i, n + (i + 1) % n) for i in range(n)]
    ver = [edge(i, n + i) for i in range(n)]

    def oe(e, fwd):
        return add(f"ORIENTED_EDGE('',*,*,#{e},{'.T.' if fwd else '.F.'})")

    def face(oes, o, z, x):
        loop = add(f"EDGE_LOOP('',({','.join(f'#{e}' for e in oes)}))")
        bound = add(f"FACE_OUTER_BOUND('',#{loop},.T.)")
        plane = add(f"PLANE('',#{ax(o, z, x)})")
        return add(f"ADVANCED_FACE('',(#{bound}),#{plane},.T.)")

    faces = [face([oe(bot[i], False) for i in reversed(range(n))], P[0], (0, 0, -1), (1, 0, 0)),
             face([oe(tops[i], True) for i in range(n)], P[n], (0, 0, 1), (1, 0, 0))]
    for i in range(n):
        j = (i + 1) % n
        dx, dy = P[j][0] - P[i][0], P[j][1] - P[i][1]
        L = math.hypot(dx, dy)
        faces.append(face([oe(bot[i], True), oe(ver[j], True), oe(tops[i], False), oe(ver[i], False)],
                          P[i], (dy / L, -dx / L, 0), (dx / L, dy / L, 0)))
    shell = add(f"CLOSED_SHELL('',({','.join(f'#{f}' for f in faces)}))")
    solid = add(f"MANIFOLD_SOLID_BREP('{part.name}',#{shell})")
    o = ax((0, 0, 0), (0, 0, 1), (1, 0, 0))
    rep = add(f"ADVANCED_BREP_SHAPE_REPRESENTATION('{part.name}',(#{o},#{solid}),#{ctx})")
    add(f"SHAPE_DEFINITION_REPRESENTATION(#{pds},#{rep})")
    head = ("ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('one solid of 50,002 planar faces'),'2;1');\n"
            f"FILE_NAME('{file_name}','2026-10-20T00:00:00',('raykholo'),(''),'tangency-labs/models generator','python3 scripts/generators','');\n"
            "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));\nENDSEC;\nDATA;\n")
    return head + "".join(f"#{i + 1}={s};\n" for i, s in enumerate(out)) + "ENDSEC;\nEND-ISO-10303-21;\n"


part = Part("toothed-plate", outline(), THICK)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    name = "toothed-plate-50k-faces.step"
    path = os.path.join(out, name)
    with open(path, "w", newline="\n") as f:
        f.write(step_text(part, name))
    poly = part.poly
    area = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly))) / 2
    print(path, dict(faces=part.faces, edges=part.edges, vertices=part.vertices, volume=round(area * THICK, 3), bytes=os.path.getsize(path)))
