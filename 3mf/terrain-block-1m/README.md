# terrain-block-1m

A closed, manifold triangle mesh of 988,880 triangles: a 200 × 100 mm block whose top is a smooth,
wavy height field, with flat sides and a flat bottom. The same mesh in other formats: [STL](../../stl/terrain-block-1m/), [OBJ](../../obj/terrain-block-1m/).

- **File:** `terrain-block-1m.3mf`
- **Author:** raykholo
- **Made with:** `scripts/generators/mesh_terrain.py` (Python 3, standard library only), writing
  3MF core specification (one object, one build item, `unit="millimeter"`; deflate-compressed package). Millimetres. Run `python3 scripts/generators/mesh_terrain.py 3mf 3mf/terrain-block-1m` to
  reproduce the file byte for byte.
- **Size:** 988,880 triangles, 494,442 vertices. 9.6 MB.
- **SHA-256:** `680fce128d2f30b1cc15a14bd2a23b5c9f92708818993201f3867f1de101ffba`

## Shape

The top is a 980 × 500 grid over 200 × 100 mm, each cell split into two triangles, at height
`10 + 3 sin(x/9) cos(y/7) + 1.5 sin((x + 2y)/23)` mm. The four sides are strips of triangles down
to z = 0, and the bottom is a fan from its centre. Every edge is shared by exactly two triangles,
in opposite directions, and all triangles face outward.

## Why it is interesting

About a million triangles in one object: it measures how fast a reader parses, welds or indexes
vertices, and builds its display mesh. The same mesh in three formats separates the cost of the
format from the cost of the mesh.

## Check values

| | |
|---|---|
| Triangles | 988,880 |
| Vertices | 494,442 (shared; an STL repeats them per triangle) |
| Volume | 201,291.674 mm³ |
| Area | 46,901.893 mm² |
| Bounding box | x 0 … 200, y 0 … 100, z 0 … 14.487 mm |
