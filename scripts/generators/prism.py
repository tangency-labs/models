"""Planar prism solids written as STEP (AP214) or IGES 5.3 (186 manifold solid B-reps), with
assemblies: STEP next-assembly-usage occurrences placed by item-defined transformations, IGES
subfigure definitions (308) placed by singular subfigure instances (408).

Standard library only. Every model here is generated from code, so the files are reproducible:
run the model's script and compare the SHA-256 with its README.

A part is a polygon (counter-clockwise, in the XY plane, millimetres) extruded along +Z by a
height. Faces: bottom, top and one side per polygon edge, all planar, normals outward.
"""

import math


# ---------- geometry ----------

def regular(n, r, phase=0.0):
    return [(r * math.cos(phase + 2 * math.pi * i / n), r * math.sin(phase + 2 * math.pi * i / n)) for i in range(n)]


def rect(w, d):
    return [(-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)]


def l_section(w, d, t):
    """An L: a w x d bounding box with legs t thick (not convex)."""
    return [(0, 0), (w, 0), (w, t), (t, t), (t, d), (0, d)]


def area2(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))


class Part:
    def __init__(self, name, poly, height):
        if area2(poly) <= 0:
            raise ValueError(f"{name}: polygon must be counter-clockwise")
        self.name, self.poly, self.h = name, poly, height

    @property
    def faces(self):
        return len(self.poly) + 2

    @property
    def edges(self):
        return 3 * len(self.poly)

    @property
    def vertices(self):
        return 2 * len(self.poly)


# A placement is (rotation 3x3 as rows, translation). Rotations are built from axis angles.

def rot(axis, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    x, y, z = axis
    n = math.sqrt(x * x + y * y + z * z)
    x, y, z = x / n, y / n, z / n
    return [[c + x * x * (1 - c), x * y * (1 - c) - z * s, x * z * (1 - c) + y * s],
            [y * x * (1 - c) + z * s, c + y * y * (1 - c), y * z * (1 - c) - x * s],
            [z * x * (1 - c) - y * s, z * y * (1 - c) + x * s, c + z * z * (1 - c)]]


IDENTITY = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


class Node:
    """An assembly: a name and children (Part or Node), each with a rotation and translation."""

    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []  # [(Part | Node, R, t)]

    def add(self, child, R=IDENTITY, t=(0, 0, 0)):
        self.children.append((child, R, tuple(t)))
        return self


def count(node):
    """(solid instances, face instances, distinct parts, assembly nodes, occurrences)."""
    parts, nodes = set(), set()
    def walk(n):
        nodes.add(id(n))
        s = f = o = 0
        for c, _, _ in n.children:
            o += 1
            if isinstance(c, Part):
                parts.add(id(c)); s += 1; f += c.faces
            else:
                a, b, d = walk(c); s += a; f += b; o += d
        return s, f, o
    s, f, o = walk(node)
    return dict(solids=s, faces=f, distinct_parts=len(parts), assemblies=len(nodes), occurrences=o)


def f6(x):
    """A real in the shortest form that round-trips at 1e-9 mm, never '-0.'."""
    v = round(x, 9)
    if v == 0:
        return "0."
    s = repr(v)
    if "e" in s or "E" in s:
        s = f"{v:.12E}"
        return s
    return s if "." in s else s + "."


# ---------- STEP AP214 ----------

def step_text(root, file_name, description):
    out = []

    def add(s):
        out.append(s)
        return len(out)

    def pt(p):
        return add(f"CARTESIAN_POINT('',({f6(p[0])},{f6(p[1])},{f6(p[2])}))")

    def dr(d):
        return add(f"DIRECTION('',({f6(d[0])},{f6(d[1])},{f6(d[2])}))")

    def ax(o, z, x):
        return add(f"AXIS2_PLACEMENT_3D('',#{pt(o)},#{dr(z)},#{dr(x)})")

    # context
    mm = add("(LENGTH_UNIT()NAMED_UNIT(*)SI_UNIT(.MILLI.,.METRE.))")
    rad = add("(NAMED_UNIT(*)PLANE_ANGLE_UNIT()SI_UNIT($,.RADIAN.))")
    sr = add("(NAMED_UNIT(*)SI_UNIT($,.STERADIAN.)SOLID_ANGLE_UNIT())")
    unc = add(f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-06),#{mm},'distance_accuracy_value','')")
    ctx = add(f"(GEOMETRIC_REPRESENTATION_CONTEXT(3)GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{unc}))"
              f"GLOBAL_UNIT_ASSIGNED_CONTEXT((#{mm},#{rad},#{sr}))REPRESENTATION_CONTEXT('',''))")
    appctx = add("APPLICATION_CONTEXT('core data for automotive mechanical design processes')")
    add(f"APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,#{appctx})")
    pctx = add(f"PRODUCT_CONTEXT('',#{appctx},'mechanical')")
    pdctx = add(f"PRODUCT_DEFINITION_CONTEXT('part definition',#{appctx},'design')")

    def product(name):
        p = add(f"PRODUCT('{name}','{name}','',(#{pctx}))")
        add(f"PRODUCT_RELATED_PRODUCT_CATEGORY('part',$,(#{p}))")
        f = add(f"PRODUCT_DEFINITION_FORMATION('','',#{p})")
        pd = add(f"PRODUCT_DEFINITION('design','',#{f},#{pdctx})")
        pds = add(f"PRODUCT_DEFINITION_SHAPE('','',#{pd})")
        return pd, pds

    origin = None

    def brep(part):
        n, h = len(part.poly), part.h
        P = [(x, y, 0.0) for x, y in part.poly] + [(x, y, h) for x, y in part.poly]
        V = [add(f"VERTEX_POINT('',#{pt(p)})") for p in P]

        def edge(a, b):
            pa, pb = P[a], P[b]
            d = [pb[k] - pa[k] for k in range(3)]
            L = math.sqrt(sum(x * x for x in d))
            u = [x / L for x in d]
            vec = add(f"VECTOR('',#{dr(u)},{f6(L)})")
            line = add(f"LINE('',#{pt(pa)},#{vec})")
            return add(f"EDGE_CURVE('',#{V[a]},#{V[b]},#{line},.T.)")

        bot = [edge(i, (i + 1) % n) for i in range(n)]
        top = [edge(n + i, n + (i + 1) % n) for i in range(n)]
        ver = [edge(i, n + i) for i in range(n)]

        def oe(e, fwd):
            return f"#{add(f'ORIENTED_EDGE({chr(39)}{chr(39)},*,*,#{e},{'.T.' if fwd else '.F.'})')}"

        def face(oes, o, z, x):
            loop = add(f"EDGE_LOOP('',({','.join(oes)}))")
            bound = add(f"FACE_OUTER_BOUND('',#{loop},.T.)")
            plane = add(f"PLANE('',#{ax(o, z, x)})")
            return add(f"ADVANCED_FACE('',(#{bound}),#{plane},.T.)")

        faces = [face([oe(bot[i], False) for i in reversed(range(n))], P[0], (0, 0, -1), (1, 0, 0)),
                 face([oe(top[i], True) for i in range(n)], P[n], (0, 0, 1), (1, 0, 0))]
        for i in range(n):
            j = (i + 1) % n
            dx, dy = P[j][0] - P[i][0], P[j][1] - P[i][1]
            L = math.hypot(dx, dy)
            faces.append(face([oe(bot[i], True), oe(ver[j], True), oe(top[i], False), oe(ver[i], False)],
                              P[i], (dy / L, -dx / L, 0), (dx / L, dy / L, 0)))
        shell = add(f"CLOSED_SHELL('',({','.join(f'#{f}' for f in faces)}))")
        return add(f"MANIFOLD_SOLID_BREP('{part.name}',#{shell})")

    reps, pds_of = {}, {}

    def define(node):
        """Product + shape representation for a part or an assembly (once each)."""
        nonlocal origin
        if id(node) in reps:
            return reps[id(node)]
        pd, pds = product(node.name)
        o = ax((0, 0, 0), (0, 0, 1), (1, 0, 0))
        if isinstance(node, Part):
            rep = add(f"ADVANCED_BREP_SHAPE_REPRESENTATION('{node.name}',(#{o},#{brep(node)}),#{ctx})")
        else:
            rep = add(f"SHAPE_REPRESENTATION('{node.name}',(#{o}),#{ctx})")
        add(f"SHAPE_DEFINITION_REPRESENTATION(#{pds},#{rep})")
        reps[id(node)] = (pd, rep, o)
        if not isinstance(node, Part):
            k = 0
            for child, R, t in node.children:
                cpd, crep, co = define(child)
                k += 1
                nm = f"{child.name}:{k}"
                nauo = add(f"NEXT_ASSEMBLY_USAGE_OCCURRENCE('{nm}','{nm}','',#{pd},#{cpd},$)")
                npds = add(f"PRODUCT_DEFINITION_SHAPE('','',#{nauo})")
                z = (R[0][2], R[1][2], R[2][2])
                x = (R[0][0], R[1][0], R[2][0])
                tgt = ax(t, z, x)
                # the child's origin (in the child's representation) maps to the placement in the parent's
                idt = add(f"ITEM_DEFINED_TRANSFORMATION('','',#{co},#{tgt})")
                rr = add(f"(REPRESENTATION_RELATIONSHIP('','',#{crep},#{rep})REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION(#{idt})SHAPE_REPRESENTATION_RELATIONSHIP())")
                add(f"CONTEXT_DEPENDENT_SHAPE_REPRESENTATION(#{rr},#{npds})")
        return reps[id(node)]

    define(root)
    head = ("ISO-10303-21;\nHEADER;\n"
            f"FILE_DESCRIPTION(('{description}'),'2;1');\n"
            f"FILE_NAME('{file_name}','2026-10-20T00:00:00',('raykholo'),(''),'tangency-labs/models generator','python3 scripts/generators','');\n"
            "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));\nENDSEC;\nDATA;\n")
    body = "".join(f"#{i + 1}={s};\n" for i, s in enumerate(out))
    return head + body + "ENDSEC;\nEND-ISO-10303-21;\n"


# ---------- IGES 5.3 ----------

class Iges:
    """Directory entries and parameter data, written in fixed 80-column records."""

    def __init__(self):
        self.ents = []  # (type, form, params list, status, matrix_de, label)

    def add(self, typ, params, form=0, status="00000000", matrix=0, label=""):
        self.ents.append([typ, form, params, status, matrix, label])
        return 2 * len(self.ents) - 1  # the entity's DE sequence number

    def set_status(self, de, status):
        self.ents[(de - 1) // 2][3] = status

    def text(self, file_name, max_coord):
        def h(s):
            return f"{len(s)}H{s}"
        g = [h(","), h(";"), h("tangency-labs/models generator"), h(file_name), h("python3 scripts/generators"),
             h("prism.py IGES 5.3"), "32", "38", "6", "308", "15", h(file_name), "1.", "2", h("MM"), "1", "1.",
             h("20261020.000000"), "1.E-06", f6(max_coord), h("raykholo"), h(""), "11", "0", h("20261020.000000")]
        s_lines = ["Generated by scripts/generators (github.com/tangency-labs/models), CC0"]

        def wrap(items, width, end):
            """Join parameters with ',' and end with ';', split into lines of at most width chars."""
            lines, cur = [], ""
            for i, it in enumerate(items):
                tok = it + (end if i == len(items) - 1 else ",")
                if len(cur) + len(tok) > width:
                    lines.append(cur); cur = ""
                cur += tok
            lines.append(cur)
            return lines

        g_lines = wrap(g, 72, ";")
        d_lines, p_lines = [], []
        for idx, (typ, form, params, status, matrix, label) in enumerate(self.ents):
            de = 2 * idx + 1
            pl = wrap([str(typ)] + [str(p) for p in params], 64, ";")
            start = len(p_lines) + 1
            for line in pl:
                p_lines.append(f"{line:<64}{de:>8}")
            d_lines.append(f"{typ:>8}{start:>8}{0:>8}{0:>8}{0:>8}{0:>8}{matrix:>8}{0:>8}{status:>8}")
            d_lines.append(f"{typ:>8}{0:>8}{0:>8}{len(pl):>8}{form:>8}{'':>8}{'':>8}{label[:8]:>8}{0:>8}")
        rec = []
        rec += [f"{l:<72}S{i + 1:>7}" for i, l in enumerate(s_lines)]
        rec += [f"{l:<72}G{i + 1:>7}" for i, l in enumerate(g_lines)]
        rec += [f"{l:<72}D{i + 1:>7}" for i, l in enumerate(d_lines)]
        rec += [f"{l:<72}P{i + 1:>7}" for i, l in enumerate(p_lines)]
        rec.append(f"S{len(s_lines):>7}G{len(g_lines):>7}D{len(d_lines):>7}P{len(p_lines):>7}{'':<40}T{1:>7}")
        return "\n".join(rec) + "\n"


DEP = "00010000"     # physically dependent
DEF = "00000200"     # independent, used as a definition (subfigure definitions)


def iges_solid(ig, part):
    """A 186 manifold solid B-rep for the prism; every entity under it is physically dependent."""
    n, hgt = len(part.poly), part.h
    P = [(x, y, 0.0) for x, y in part.poly] + [(x, y, hgt) for x, y in part.poly]
    vl = ig.add(502, [len(P)] + [f6(c) for p in P for c in p], form=1, status=DEP)
    edges = []  # (a, b) vertex indices, 1-based in the vertex list

    def line(a, b):
        pa, pb = P[a], P[b]
        return ig.add(110, [f6(c) for c in pa + pb], status=DEP)

    E = [(i, (i + 1) % n) for i in range(n)] + [(n + i, n + (i + 1) % n) for i in range(n)] + [(i, n + i) for i in range(n)]
    curves = [line(a, b) for a, b in E]
    params = [len(E)]
    for (a, b), c in zip(E, curves):
        params += [c, vl, a + 1, vl, b + 1]
    el = ig.add(504, params, form=1, status=DEP)
    bot = list(range(n)); top = [n + i for i in range(n)]; ver = [2 * n + i for i in range(n)]

    def loop(es):  # [(edge index 0-based, forward)]
        p = [len(es)]
        for e, fwd in es:
            p += [0, el, e + 1, 1 if fwd else 0, 0]
        return ig.add(508, p, form=1, status=DEP)

    def plane(o, z):
        pt = ig.add(116, [f6(c) for c in o], status=DEP)
        dn = ig.add(123, [f6(c) for c in z], status=DEP)
        return ig.add(190, [pt, dn], status=DEP)

    def face(es, o, z):
        return ig.add(510, [plane(o, z), 1, 1, loop(es)], form=1, status=DEP)

    faces = [face([(bot[i], False) for i in reversed(range(n))], P[0], (0, 0, -1)),
             face([(top[i], True) for i in range(n)], P[n], (0, 0, 1))]
    for i in range(n):
        j = (i + 1) % n
        dx, dy = P[j][0] - P[i][0], P[j][1] - P[i][1]
        L = math.hypot(dx, dy)
        faces.append(face([(bot[i], True), (ver[j], True), (top[i], False), (ver[i], False)], P[i], (dy / L, -dx / L, 0)))
    shell = ig.add(514, [len(faces)] + [x for f in faces for x in (f, 1)], form=1, status=DEP)
    return ig.add(186, [shell, 1, 0], status=DEP, label=part.name[:8].upper())


def iges_text(root, file_name):
    """root: a Node. Every Node becomes a 308 definition (deepest first); every child placement a 408.
    The top Node's children are written as independent 408 instances (the file's assembly)."""
    ig = Iges()
    solid_de, sub_de, depth = {}, {}, {}

    def matrix(R, t):
        return ig.add(124, [f6(R[i][j]) if j < 3 else f6(t[i]) for i in range(3) for j in range(4)], status=DEP)

    def part_sub(part):
        # a part becomes a one-member subfigure, so every placement is a 408
        if id(part) not in sub_de:
            s = iges_solid(ig, part)
            sub_de[id(part)] = ig.add(308, [0, f"{len(part.name)}H{part.name}", 1, s], status=DEF)
            depth[id(part)] = 0
        return sub_de[id(part)]

    def instance(child, R, t, status):
        d = part_sub(child) if isinstance(child, Part) else node_sub(child)
        # an unrotated placement uses the 408's own X, Y, Z; a rotated one puts rotation and translation in
        # the 408's transformation matrix (124), so both placement mechanisms are exercised (X' = M (S x + T)).
        if R == IDENTITY:
            return ig.add(408, [d, f6(t[0]), f6(t[1]), f6(t[2]), "1."], status=status)
        m = matrix(R, t)
        return ig.add(408, [d, "0.", "0.", "0.", "1."], status=status, matrix=m)

    def node_sub(node):
        if id(node) not in sub_de:
            members = [instance(c, R, t, DEP) for c, R, t in node.children]
            dmax = 1 + max(depth[id(c)] for c, _, _ in node.children)
            sub_de[id(node)] = ig.add(308, [dmax, f"{len(node.name)}H{node.name}", len(members)] + members, status=DEF)
            depth[id(node)] = dmax
        return sub_de[id(node)]

    for c, R, t in root.children:
        instance(c, R, t, "00000000")
    return ig.text(file_name, 1000.0)


def expected(root):
    """Analytic totals for checking a reader: solid count, total volume (mm3), world bounding box."""
    vol, lo, hi, n = 0.0, [math.inf] * 3, [-math.inf] * 3, 0

    def walk(node, R, t):
        nonlocal vol, n
        for c, Rc, tc in node.children:
            R2 = matmul(R, Rc)
            t2 = [sum(R[i][k] * tc[k] for k in range(3)) + t[i] for i in range(3)]
            if isinstance(c, Part):
                n += 1
                vol += abs(area2(c.poly)) / 2 * c.h
                for x, y in c.poly:
                    for z in (0.0, c.h):
                        p = [sum(R2[i][k] * (x, y, z)[k] for k in range(3)) + t2[i] for i in range(3)]
                        for i in range(3):
                            lo[i], hi[i] = min(lo[i], p[i]), max(hi[i], p[i])
            else:
                walk(c, R2, t2)
    walk(root, IDENTITY, [0, 0, 0])
    return dict(solids=n, volume=round(vol, 3), bbox=[round(v, 3) for v in lo + hi])
