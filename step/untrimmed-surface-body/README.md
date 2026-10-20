# untrimmed-surface-body

An open surface body (a box without a lid, 100 × 80 × 50 mm) whose floor lies on a B-spline surface
4,000 mm square, trimmed to the 100 × 80 mm floor. The body's bounding box is 100 × 80 × 50 mm;
its floor's underlying surface is 40 times wider.

- **File:** `untrimmed-surface-body.step`
- **Author:** raykholo
- **Made with:** `scripts/generators/untrimmed_surface_body.py` (Python 3, standard library only).
  It writes STEP AP214 (`AUTOMOTIVE_DESIGN`) directly, in millimetres, with a distance accuracy of
  1e-6 mm. Run `python3 scripts/generators/untrimmed_surface_body.py step/untrimmed-surface-body` to
  reproduce the file byte for byte.
- **Application protocol:** AP214, as a manifold surface shape representation (one shell-based
  surface model, one open shell).
- **Size:** 1 surface body; 5 faces (4 planes and 1 bilinear B-spline surface), 12 edges, 8
  vertices. 6.3 KB.
- **SHA-256:** `2decd6561114628a67d4e3ee396f56ee4ae1dfbdacc2ef4acfe1b5841ca4552b`

## Why it is interesting

Surface models exported from CAD often keep a face's whole underlying surface, much larger than the
trimmed face. A reader that measures, frames or bounds the surface instead of the trimmed face
reports a box of about 4,000 × 4,000 × 50 mm, zooms the view out to it, or sizes meshing and
tolerances from it. The faces themselves are simple, so any difference comes from the bounding.

## Check values

| | |
|---|---|
| Bodies | 1 open surface body (no solid) |
| Faces | 5 |
| Area | 26,000 mm² |
| Bounding box | x 0 … 100, y 0 … 80, z 0 … 50 mm |
| Floor's underlying surface | x −2,000 … 2,000, y −2,000 … 2,000 mm at z 0 |
