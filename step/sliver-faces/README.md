# sliver-faces

One solid, a 60 × 40 × 10 mm block whose side carries four sliver faces 1 µm, 10 nm, 0.1 nm and
0.01 nm wide, while the file declares a distance accuracy of 1e-6 mm (1 nm): two slivers are wider
than the accuracy and two are narrower.

- **File:** `sliver-faces.step`
- **Author:** raykholo
- **Made with:** `scripts/generators/sliver_faces.py` (Python 3, standard library only; shared code
  in `scripts/generators/prism.py`). It writes STEP AP214 (`AUTOMOTIVE_DESIGN`) directly, in
  millimetres, with a distance accuracy of 1e-6 mm. Run
  `python3 scripts/generators/sliver_faces.py step/sliver-faces` to reproduce the file byte for
  byte.
- **Application protocol:** AP214.
- **Size:** 1 solid; 14 planar faces, 36 edges, 24 vertices. 17 KB.
- **SHA-256:** `366d369d959049f085c1d7954a7c4cee7b7c077df73f36d4177a4b04ed3777a3`

## Shape

The block's outline runs along y = 0 and steps up at x = 10, 20, 30 and 40 mm by 1e-3, 1e-5,
1e-7 and 1e-8 mm. Each step is a side face that wide and 10 mm tall; the top and bottom faces
each have 12 edges, four of them that short.

## Why it is interesting

Exports from many systems carry faces and edges near or below their stated accuracy. A reader
must keep the solid closed while edges are shorter than its tolerance: merging such vertices can
leave faces without area or split the shell, and keeping them strains meshing and sewing. The
four widths show where a reader's limit lies.

## Check values

| | |
|---|---|
| Solids | 1, closed |
| Faces | 14 |
| Volume | 23,999.496 mm³ |
| Bounding box | x 0 … 60, y 0 … 40, z 0 … 10 mm |
