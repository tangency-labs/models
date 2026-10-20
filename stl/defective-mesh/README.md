# defective-mesh

One ASCII STL holding the mesh defects readers meet in real files, each in a known place: a
self-intersection, a non-manifold edge, a hole, a flipped triangle, a duplicate triangle and
degenerate triangles, on eight small cubes.

- **File:** `defective-mesh.stl`
- **Author:** raykholo
- **Made with:** `scripts/generators/defective_mesh.py` (Python 3, standard library only), writing
  ASCII STL with a normal per facet (zero for degenerate triangles), in millimetres. Run
  `python3 scripts/generators/defective_mesh.py stl/defective-mesh` to reproduce the file byte for
  byte.
- **Size:** 98 triangles. 24 KB.
- **SHA-256:** `303238a59aaa5db7073ffbbefe9596ea9442ac3e6063d2bb90d08c88891cd93d`

## Content

All cubes are 20 mm, axis-aligned, triangles facing outward unless stated. In file order:

| Triangles | Group | Defect |
|---|---|---|
| 1–24 | two cubes at (0, 0, 0) and (10, 5, 5) | they overlap by 10 × 15 × 15 mm: the mesh intersects itself |
| 25–48 | two cubes at (50, 0, 0) and (70, 0, 20) | they touch along one edge only (x = 70, z = 20): four triangles share that edge |
| 49–59 | a cube at (0, 50, 0) | one top triangle missing: a hole |
| 60–71 | a cube at (50, 50, 0) | one side triangle (the 7th) wound the wrong way |
| 72–84 | a cube at (100, 0, 0) | its first triangle written again at the end |
| 85–98 | a cube at (100, 50, 0) | two extra zero-area triangles on its faces: three collinear points, and two equal points |

## Why it is interesting

A reader has to decide what to do with each defect: keep, repair, report or refuse it. Whatever it
does, it should not crash, hang or silently drop the good cubes. The file states nothing about
which repair is right; the table above says where each defect is, so a reader's report can be
checked against it.

## Check values

| | |
|---|---|
| Triangles | 98 |
| Signed volume as written | 53,333.333 mm³ (sum over all triangles, about the origin) |
| Signed volume with the flipped triangle turned back | 62,666.667 mm³ |
| Bounding box | x 0 … 120, y 0 … 70, z 0 … 40 mm |
