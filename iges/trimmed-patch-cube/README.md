# trimmed-patch-cube

A closed 100 mm cube given only as trimmed surfaces: 54 B-spline patches, nine per side, each
trimmed by a composite curve. Some trims have pieces written end to start, and some pieces stop
0.02 mm short of the next.

- **File:** `trimmed-patch-cube.igs`
- **Author:** raykholo
- **Made with:** `scripts/generators/trimmed_patch_cube.py` (Python 3, standard library only;
  shared code in `scripts/generators/prism.py`). It writes IGES 5.3 directly, in millimetres. Run
  `python3 scripts/generators/trimmed_patch_cube.py iges/trimmed-patch-cube` to reproduce the file
  byte for byte.
- **Content:** trimmed surfaces only, no solids. Entities: 54 trimmed surfaces (144), 54 rational
  B-spline surfaces (128, bilinear patches), 54 curves on surface (142, model-space curve only),
  54 composite curves (102), 108 lines (110) and 108 B-spline curves (126, degree 1).
- **Size:** 54 faces, which sew into one closed shell with 108 edges and 56 vertices. 1,539
  lines, 125 KB.
- **SHA-256:** `8911254f16a31835597448f2420f9a604defb151e32e947c7dd901adc7dd3da8`

## Shape

Each side of the cube is split into 3 × 3 square patches, 33.3 mm across. Each patch is a degree
1 × 1 B-spline surface whose normal points out of the cube, trimmed by a curve on surface whose
model-space curve is a composite of four straight pieces round the patch, alternately lines and
degree-1 B-spline curves. Of the 216 pieces:

- 43 are written end to start (their direction runs against the loop); in 10 trims that is the
  first piece;
- 36 stop 0.02 mm before the corner where the next piece starts, so the loop has a gap there.

## Why it is interesting

A reader must turn each composite curve into a closed trim loop, then sew 54 separate faces into
one closed shell to get a solid. Readers that take pieces in the direction they are written, or
that need every piece to meet the next exactly, leave faces out, and the cube does not close.
The defects are mixed on purpose; each one alone is enough to drop faces.

## Check values

| | |
|---|---|
| Faces | 54 |
| Sewn result | 1 closed solid |
| Volume | 1,000,000 mm³ |
| Area | 60,000 mm² |
| Bounding box | x 0 … 100, y 0 … 100, z 0 … 100 mm |
