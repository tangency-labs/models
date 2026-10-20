# toothed-plate-50k-faces

One solid of 50,002 planar faces: a 500 mm square plate, 5 mm thick, whose outline is 12,500
square teeth 0.08 mm wide and 0.5 mm deep.

- **File:** `toothed-plate-50k-faces.step`
- **Author:** raykholo
- **Made with:** `scripts/generators/toothed_plate.py` (Python 3, standard library only; number
  formatting from `scripts/generators/prism.py`). It writes STEP AP214 (`AUTOMOTIVE_DESIGN`)
  directly, in millimetres, with a distance accuracy of 1e-6 mm, writing each distinct point,
  direction, vector and placement once. Run
  `python3 scripts/generators/toothed_plate.py step/toothed-plate-50k-faces` to reproduce the file
  byte for byte.
- **Application protocol:** AP214.
- **Size:** 1 solid; 50,002 faces (all planes), 150,000 edges (all lines), 100,000 vertices.
  46.2 MB.
- **SHA-256:** `9f59ade85de592741a5436b086ff48397fb3ac7cad083fd96a3094e17db93047`

## Shape

The outline runs round a 500 × 500 mm square. Each side carries 3,125 teeth at a 0.16 mm pitch:
the outline steps out 0.5 mm, runs 0.08 mm, steps back and runs 0.08 mm. Extruded 5 mm, that gives
50,000 side faces, 0.08 × 5 or 0.5 × 5 mm each, and a top and a bottom face each bounded by one
loop of 50,000 edges.

## Why it is interesting

A single part with tens of thousands of faces, two of which have 50,000-edge boundaries. It
stresses B-rep building and topology lookups, tessellating a planar face with a very long, very
fine boundary, and picking and highlighting in a view where most faces are a fraction of a pixel.

## Check values

| | |
|---|---|
| Solids | 1 |
| Faces | 50,002 |
| Volume | 1,252,500 mm³ |
| Area | 573,500 mm² (the outline is 14,500 mm long) |
| Bounding box | x −0.5 … 500.5, y −0.5 … 500.5, z 0 … 5 mm |
