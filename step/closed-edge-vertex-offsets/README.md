# closed-edge-vertex-offsets

Five open surface bodies side by side, each a 20 mm square face bounded by a single closed edge,
whose one vertex sits on the edge's curve a tiny parameter step past the curve's start: 1e-9, 3e-8,
2e-7, 8e-7 and 5e-6.

- **File:** `closed-edge-vertex-offsets.step`
- **Author:** raykholo
- **Made with:** `scripts/generators/closed_edge_vertex_offsets.py` (Python 3, standard library only;
  number formatting from `scripts/generators/prism.py`). It writes STEP AP214
  (`AUTOMOTIVE_DESIGN`) directly, in millimetres, with a distance accuracy of 1e-6 mm. Run
  `python3 scripts/generators/closed_edge_vertex_offsets.py step/closed-edge-vertex-offsets` to
  reproduce the file byte for byte.
- **Application protocol:** AP214, as a manifold surface shape representation holding five
  shell-based surface models.
- **Size:** 5 surface bodies; 5 planar faces, 5 edges (closed degree-1 B-spline curves), 5
  vertices. 5 KB.
- **SHA-256:** `1da4947a2ff86d12785affb9c1b5eb3a271c094987be5965968d92271792da58`

## Shape

Each body is a square face on z = 0, 20 mm across, the five 30 mm apart along X. Its boundary is
one closed edge whose curve is a degree-1 B-spline through the square's corners, back to the
start, with parameter range 0 … 1 (a quarter per side). The edge's only vertex is the curve's
point at parameter 1e-9, 3e-8, 2e-7, 8e-7 or 5e-6 (the body names say which): at most 0.4 µm
along the first side from the corner where the curve starts.

## Why it is interesting

A reader splits a closed edge at its vertex. When the vertex sits a hair past the curve's start,
one piece is tiny: between a reader's "this is the start" tolerance and the point where its
curve evaluation gives up, that piece can be degenerate. Readers then drop the face, the body or
the whole file, or get the face's area wrong. Each body here holds one offset, so the result shows
exactly which offsets a reader handles.

## Check values

| | |
|---|---|
| Bodies | 5 open surface bodies |
| Area | 400 mm² each, 2,000 mm² in all |
| Bounding box | x 0 … 140, y 0 … 20, z 0 mm |
