"""step/tessellated-brep-mix: an AP242 assembly of three parts, two exact (a B-rep block and a B-rep
hexagonal post) and one given only as a tessellation (a closed triangulated dome, as a
triangulated surface set), placed side by side. Readers have to take exact and faceted geometry
from one file.

    python3 scripts/generators/tessellated_brep_mix.py step/tessellated-brep-mix
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prism import Part, f6, rect, regular  # noqa: E402

NLAT, NLON, R = 12, 24, 20.0   # dome tessellation: latitude rings, longitude steps, radius


def dome():
    """A closed hemisphere of radius R on z = 0: vertices and outward counter-clockwise triangles."""
    V = [(0.0, 0.0, R)]
    for i in range(1, NLAT + 1):
        th = (math.pi / 2) * i / NLAT
        for j in range(NLON):
            ph = 2 * math.pi * j / NLON
            V.append((R * math.sin(th) * math.cos(ph), R * math.sin(th) * math.sin(ph), R * math.cos(th)))
    centre = len(V)
    V.append((0.0, 0.0, 0.0))
    ring = lambda i, j: 1 + (i - 1) * NLON + (j % NLON)
    T = []
    for j in range(NLON):
        T.append((0, ring(1, j), ring(1, j + 1)))
    for i in range(1, NLAT):
        for j in range(NLON):
            a, b, c, d = ring(i, j), ring(i + 1, j), ring(i + 1, j + 1), ring(i, j + 1)
            T += [(a, b, c), (a, c, d)]
    for j in range(NLON):  # the flat bottom, seen from below
        T.append((centre, ring(NLAT, j + 1), ring(NLAT, j)))
    return V, T


def step():
    out = []

    def add(s):
        out.append(s)
        return len(out)

    def pt(p):
        return add(f"CARTESIAN_POINT('',({f6(p[0])},{f6(p[1])},{f6(p[2])}))")

    def dr(d):
        return add(f"DIRECTION('',({f6(d[0])},{f6(d[1])},{f6(d[2])}))")

    def ax(o, z=(0, 0, 1), x=(1, 0, 0)):
        return add(f"AXIS2_PLACEMENT_3D('',#{pt(o)},#{dr(z)},#{dr(x)})")

    mm = add("(LENGTH_UNIT()NAMED_UNIT(*)SI_UNIT(.MILLI.,.METRE.))")
    rad = add("(NAMED_UNIT(*)PLANE_ANGLE_UNIT()SI_UNIT($,.RADIAN.))")
    sr = add("(NAMED_UNIT(*)SI_UNIT($,.STERADIAN.)SOLID_ANGLE_UNIT())")
    unc = add(f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-06),#{mm},'distance_accuracy_value','')")
    ctx = add(f"(GEOMETRIC_REPRESENTATION_CONTEXT(3)GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{unc}))"
              f"GLOBAL_UNIT_ASSIGNED_CONTEXT((#{mm},#{rad},#{sr}))REPRESENTATION_CONTEXT('',''))")
    app = add("APPLICATION_CONTEXT('managed model based 3d engineering')")
    add(f"APPLICATION_PROTOCOL_DEFINITION('international standard','ap242_managed_model_based_3d_engineering',2014,#{app})")
    pc = add(f"PRODUCT_CONTEXT('',#{app},'mechanical')")
    pdc = add(f"PRODUCT_DEFINITION_CONTEXT('part definition',#{app},'design')")

    def product(name):
        p = add(f"PRODUCT('{name}','{name}','',(#{pc}))")
        f = add(f"PRODUCT_DEFINITION_FORMATION('','',#{p})")
        pd = add(f"PRODUCT_DEFINITION('design','',#{f},#{pdc})")
        return pd, add(f"PRODUCT_DEFINITION_SHAPE('','',#{pd})")

    def brep(part):
        n, h = len(part.poly), part.h
        P = [(x, y, 0.0) for x, y in part.poly] + [(x, y, h) for x, y in part.poly]
        V = [add(f"VERTEX_POINT('',#{pt(p)})") for p in P]

        def edge(a, b):
            d = [P[b][k] - P[a][k] for k in range(3)]
            L = math.sqrt(sum(x * x for x in d))
            vec = add(f"VECTOR('',#{dr([x / L for x in d])},{f6(L)})")
            return add(f"EDGE_CURVE('',#{V[a]},#{V[b]},#{add(f'LINE({chr(39)}{chr(39)},#{pt(P[a])},#{vec})')},.T.)")

        bot = [edge(i, (i + 1) % n) for i in range(n)]
        top = [edge(n + i, n + (i + 1) % n) for i in range(n)]
        ver = [edge(i, n + i) for i in range(n)]

        def face(es, o, z, x):
            oes = ",".join(f"#{add(f'ORIENTED_EDGE({chr(39)}{chr(39)},*,*,#{e},{chr(46)}{chr(84) if f else chr(70)}{chr(46)})')}" for e, f in es)
            loop = add(f"EDGE_LOOP('',({oes}))")
            return add(f"ADVANCED_FACE('',(#{add(f'FACE_OUTER_BOUND({chr(39)}{chr(39)},#{loop},.T.)')}),#{add(f'PLANE({chr(39)}{chr(39)},#{ax(o, z, x)})')},.T.)")

        faces = [face([(bot[i], False) for i in reversed(range(n))], P[0], (0, 0, -1), (1, 0, 0)),
                 face([(top[i], True) for i in range(n)], P[n], (0, 0, 1), (1, 0, 0))]
        for i in range(n):
            j = (i + 1) % n
            dx, dy = P[j][0] - P[i][0], P[j][1] - P[i][1]
            L = math.hypot(dx, dy)
            faces.append(face([(bot[i], True), (ver[j], True), (top[i], False), (ver[i], False)], P[i], (dy / L, -dx / L, 0), (dx / L, dy / L, 0)))
        shell = add(f"CLOSED_SHELL('',({','.join(f'#{f}' for f in faces)}))")
        return add(f"MANIFOLD_SOLID_BREP('{part.name}',#{shell})")

    parts = []
    for part in (Part("block", rect(40, 30), 12), Part("hex-post", regular(6, 10), 35)):
        pd, pds = product(part.name)
        o = ax((0, 0, 0))
        rep = add(f"ADVANCED_BREP_SHAPE_REPRESENTATION('{part.name}',(#{o},#{brep(part)}),#{ctx})")
        add(f"SHAPE_DEFINITION_REPRESENTATION(#{pds},#{rep})")
        parts.append((pd, rep, o))

    V, T = dome()
    pd, pds = product("faceted-dome")
    coords = add(f"COORDINATES_LIST('',{len(V)},(" + ",".join(f"({f6(x)},{f6(y)},{f6(z)})" for x, y, z in V) + "))")
    tris = ",".join(f"({a + 1},{b + 1},{c + 1})" for a, b, c in T)
    tss = add(f"TRIANGULATED_SURFACE_SET('faceted-dome',#{coords},{len(V)},(),({','.join(str(k + 1) for k in range(len(V)))}),({tris}))")
    o = ax((0, 0, 0))
    rep = add(f"TESSELLATED_SHAPE_REPRESENTATION('faceted-dome',(#{o},#{tss}),#{ctx})")
    add(f"SHAPE_DEFINITION_REPRESENTATION(#{pds},#{rep})")
    parts.append((pd, rep, o))

    root_pd, root_pds = product("tessellated-brep-mix")
    ro = ax((0, 0, 0))
    root_rep = add(f"SHAPE_REPRESENTATION('tessellated-brep-mix',(#{ro}),#{ctx})")
    add(f"SHAPE_DEFINITION_REPRESENTATION(#{root_pds},#{root_rep})")
    for k, ((cpd, crep, co), x) in enumerate(zip(parts, (0.0, 60.0, 120.0))):
        nauo = add(f"NEXT_ASSEMBLY_USAGE_OCCURRENCE('{k + 1}','{k + 1}','',#{root_pd},#{cpd},$)")
        npds = add(f"PRODUCT_DEFINITION_SHAPE('','',#{nauo})")
        idt = add(f"ITEM_DEFINED_TRANSFORMATION('','',#{co},#{ax((x, 0, 0))})")
        rr = add(f"(REPRESENTATION_RELATIONSHIP('','',#{crep},#{root_rep})REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION(#{idt})SHAPE_REPRESENTATION_RELATIONSHIP())")
        add(f"CONTEXT_DEPENDENT_SHAPE_REPRESENTATION(#{rr},#{npds})")
    head = ("ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('exact and tessellated parts in one assembly'),'2;1');\n"
            "FILE_NAME('tessellated-brep-mix.step','2026-10-20T00:00:00',('raykholo'),(''),'tangency-labs/models generator','python3 scripts/generators','');\n"
            "FILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF { 1 0 10303 442 1 1 4 }'));\nENDSEC;\nDATA;\n")
    return head + "".join(f"#{i + 1}={s};\n" for i, s in enumerate(out)) + "ENDSEC;\nEND-ISO-10303-21;\n", len(V), len(T)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "tessellated-brep-mix.step")
    text, nv, nt = step()
    with open(path, "w", newline="\n") as f:
        f.write(text)
    print(path, dict(dome_vertices=nv, dome_triangles=nt))
