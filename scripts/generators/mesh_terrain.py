"""stl/terrain-block-1m, obj/terrain-block-1m, 3mf/terrain-block-1m: one closed, manifold triangle
mesh of 988,880 triangles (about a million): a 200 x 100 mm block whose top is a smooth wavy height field
on a 980 x 500 grid, with flat sides and a flat bottom. The same mesh in three formats.

    python3 scripts/generators/mesh_terrain.py stl|obj|3mf <out-folder>
"""

import math
import os
import struct
import sys
import zipfile

NX, NY = 980, 500          # grid cells along X and Y on the top
SX, SY = 200.0, 100.0      # block size in mm
BASE = 10.0                # block height under the waves


def height(i, j):
    x, y = SX * i / NX, SY * j / NY
    return BASE + 3.0 * math.sin(x / 9.0) * math.cos(y / 7.0) + 1.5 * math.sin((x + 2 * y) / 23.0)


def mesh():
    """Vertices and counter-clockwise (outward) triangles of the closed block."""
    V, T = [], []
    top = {}
    for j in range(NY + 1):
        for i in range(NX + 1):
            top[(i, j)] = len(V)
            V.append((round(SX * i / NX, 6), round(SY * j / NY, 6), round(height(i, j), 6)))
    for j in range(NY):
        for i in range(NX):
            a, b, c, d = top[(i, j)], top[(i + 1, j)], top[(i + 1, j + 1)], top[(i, j + 1)]
            T += [(a, b, c), (a, c, d)]
    # the bottom and the walls: the boundary ring of the top, dropped to z = 0
    ring = [(i, 0) for i in range(NX)] + [(NX, j) for j in range(NY)] + [(i, NY) for i in range(NX, 0, -1)] + [(0, j) for j in range(NY, 0, -1)]
    low = []
    for (i, j) in ring:
        low.append(len(V))
        V.append((round(SX * i / NX, 6), round(SY * j / NY, 6), 0.0))
    n = len(ring)
    for k in range(n):
        u0, u1 = top[ring[k]], top[ring[(k + 1) % n]]
        l0, l1 = low[k], low[(k + 1) % n]
        T += [(l0, l1, u1), (l0, u1, u0)]
    # the bottom: a fan from its centre, seen from below
    centre = len(V)
    V.append((SX / 2, SY / 2, 0.0))
    for k in range(n):
        T.append((centre, low[(k + 1) % n], low[k]))
    return V, T


def write_stl(path, V, T):
    with open(path, "wb") as f:
        f.write(b"terrain-block-1m, generated, CC0-1.0".ljust(80, b" "))
        f.write(struct.pack("<I", len(T)))
        for a, b, c in T:
            p, q, r = V[a], V[b], V[c]
            u = [q[k] - p[k] for k in range(3)]
            w = [r[k] - p[k] for k in range(3)]
            nx, ny, nz = u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]
            L = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            f.write(struct.pack("<12fH", nx / L, ny / L, nz / L, *p, *q, *r, 0))


def num(x):
    s = f"{x:.6f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def write_obj(path, V, T):
    with open(path, "w", newline="\n") as f:
        f.write("# terrain-block-1m, generated, CC0-1.0; millimetres\no terrain-block-1m\n")
        f.writelines(f"v {num(x)} {num(y)} {num(z)}\n" for x, y, z in V)
        f.writelines(f"f {a + 1} {b + 1} {c + 1}\n" for a, b, c in T)


def write_3mf(path, V, T):
    verts = "".join(f'<vertex x="{num(x)}" y="{num(y)}" z="{num(z)}"/>' for x, y, z in V)
    tris = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in T)
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             '<metadata name="Title">terrain-block-1m</metadata><resources><object id="1" type="model" name="terrain-block-1m"><mesh>'
             f'<vertices>{verts}</vertices><triangles>{tris}</triangles></mesh></object></resources>'
             '<build><item objectid="1"/></build></model>')
    types = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
             '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
             '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in (("[Content_Types].xml", types), ("_rels/.rels", rels), ("3D/3dmodel.model", model)):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 20, 0, 0, 0))  # fixed stamp: reproducible bytes
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)


if __name__ == "__main__":
    fmt, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    V, T = mesh()
    path = os.path.join(out, f"terrain-block-1m.{fmt}")
    {"stl": write_stl, "obj": write_obj, "3mf": write_3mf}[fmt](path, V, T)
    print(path, dict(vertices=len(V), triangles=len(T), bytes=os.path.getsize(path)))
