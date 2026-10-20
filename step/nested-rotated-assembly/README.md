# nested-rotated-assembly

A STEP assembly four levels deep in which every placement, at every level, is rotated, most of them
about oblique axes: 32 solid instances of 4 small planar parts.

- **File:** `nested-rotated-assembly.step`
- **Author:** raykholo
- **Made with:** `scripts/generators/nested_rotated_assembly.py` (Python 3, standard library only;
  shared code in `scripts/generators/prism.py`). It writes STEP AP214 (`AUTOMOTIVE_DESIGN`)
  directly, in millimetres, with a distance accuracy of 1e-6 mm. Run
  `python3 scripts/generators/nested_rotated_assembly.py step/nested-rotated-assembly` to reproduce
  the file byte for byte.
- **Application protocol:** AP214.
- **Size:** 32 solid instances of 4 distinct solids; 208 faces, 432 edges and 288 vertices
  over all instances. Product structure: 8 products, 11 next-assembly-usage occurrences,
  52 component occurrences once expanded. 35 KB.
- **SHA-256:** `f2f9c489c8205b0a0bbb055a9e6d202f31ca04e3195098863d784a00a62ebbc6`

## Structure

| Level | Component | Placed in it |
|---|---|---|
| 1 (the file) | `nested-rotated-assembly` | two `ring`s: one turned 12° about Y, the other turned 180° about the (1, 2, 3) axis |
| 2 | `ring` | three `pair`s turned 10°, 130° and 250° about the (0.3, 0.2, 1) axis and stacked 15 mm apart; an `angle` turned 90° about X |
| 3 | `pair` | a `plate` turned 5° about Z; two `cell`s, turned 25° about (1, 1, 0) and −40° about (1, −1, 1) |
| 4 | `cell` | a `keyed-block` (an asymmetric outline, so a wrong rotation shows); a `tri-peg` turned 20° about Z |

Placements are next-assembly-usage occurrences with item-defined transformations.

## Why it is interesting

A reader must compose four rotations, in the right order, to place each solid. A reader that
applies them in the wrong order, transposes a rotation, or drops one level puts parts in visibly
wrong places, and the bounding box below no longer matches.

## Check values

Exact values from the generator, for checking a reader:

| | |
|---|---|
| Solids | 32 |
| Faces | 208 |
| Total volume | 148,313.074 mm³ (the solids overlap; this is the sum of their volumes) |
| Bounding box | x -32.883 … 196.564, y -36.186 … 75.997, z -17.911 … 102.505 mm |
