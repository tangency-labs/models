# vertices-off-curves

An open surface model, a 4 × 4 grid of gently domed faces 200 mm across, whose edge curves end
0.19 mm beside their vertices while the file declares a distance accuracy of 0.01 mm.

- **File:** `vertices-off-curves.step`
- **Author:** raykholo
- **Made with:** `scripts/generators/vertices_off_curves.py` (Python 3, standard library only;
  number formatting from `scripts/generators/prism.py`). It writes STEP AP214
  (`AUTOMOTIVE_DESIGN`) directly, in millimetres. Run
  `python3 scripts/generators/vertices_off_curves.py step/vertices-off-curves` to reproduce the file
  byte for byte.
- **Application protocol:** AP214, as a manifold surface shape representation (one shell-based
  surface model, one open shell).
- **Size:** 1 surface body; 16 faces (bilinear B-spline patches), 40 edges (cubic B-spline curves),
  25 vertices. 26 KB.
- **SHA-256:** `6ae8ac2b1a9c7878552708c5c913376f3cd59c5b8bbcc8fceb4984234c400a92`

## Shape

A 200 × 200 mm sheet on a 5 × 5 grid of points, raised to `8 sin(πx/200) sin(πy/200)` mm. Each
face is the bilinear patch through its four corner points. Each edge is a cubic through four points
on the true edge, except that its two end points are moved 0.19 mm sideways (in the XY plane), so
every curve ends 0.19 mm beside the vertex it starts or ends at. Shared edges are written once and
used by both faces.

## Why it is interesting

Surface exports do contain such edges: the vertex and the curve disagree by many times the declared
accuracy, but by little next to the model (here 0.1 % of its size). A reader that refuses an edge
whose vertices are off its curve by more than the declared accuracy leaves faces out, and in a
surface model, where a body is made of these faces, it can lose the whole body. A reader that snaps
the curve's ends onto the vertices keeps all 16 faces.

## Check values

| | |
|---|---|
| Bodies | 1 open surface body |
| Faces | 16 |
| Area | about 40,000 mm²: 40,135.0 for the untrimmed patches; the trimmed faces differ a little, since the edges run up to 0.19 mm beside the patch borders |
| Bounding box | x 0 … 200, y 0 … 200, z 0 … 8 mm, within 0.19 mm |
