# instanced-assembly-subfigures

An IGES assembly in which every part is placed by a subfigure instance: five solids, defined once
each, placed 23 times through three levels of nested subfigure definitions, with rotations about
every axis.

- **File:** `instanced-assembly-subfigures.igs`
- **Author:** raykholo
- **Made with:** `scripts/generators/instanced_assembly_subfigures.py` (Python 3, standard library only;
  shared code in `scripts/generators/prism.py`). It writes IGES 5.3 directly, in millimetres. Run
  `python3 scripts/generators/instanced_assembly_subfigures.py iges/instanced-assembly-subfigures`
  to reproduce the file byte for byte.
- **Content:** solids only. Each part is a manifold solid B-rep (186) with planar faces
  (190 plane surfaces, 110 lines, 502/504/508/510/514 topology).
- **Size:** 23 solid instances of 5 distinct solids; 166 faces, 360 edges and 240 vertices
  over all instances (38 faces in the distinct solids). Entities: 5 manifold solid B-reps (186),
  7 subfigure definitions (308), 13 singular subfigure instances (408), 8 transformation
  matrices (124). 1,016 lines, 81 KB.
- **SHA-256:** `8457accbaed7d2b99f4e0afc6ad99db976249cadb4f37ba7e667644e07107a4a`

## Structure

| Level | Subfigure definition | Placed in it |
|---|---|---|
| 1 (the file) | independent 408 instances | a base plate; four corner modules turned 0, 90, 180 and 270 degrees about Z; a fifth corner module tipped 120 degrees about the (1, 1, 0) axis after a 30 degree turn about Z; two pins tilted 30 degrees about X and about Y |
| 2 | `corner-module` (depth 2) | an L-section bracket, and a capped post leaning 15 degrees about X |
| 3 | `capped-post` (depth 1) | a hexagonal post with a square cap on each end, the lower cap turned 45 degrees about Z |

Every solid sits in its own one-member subfigure definition, so every placement in the file is a
408. Unrotated placements use the 408's own X, Y, Z translation; rotated ones carry rotation and
translation in a transformation matrix (124) on the 408's directory entry.

## Why it is interesting

Readers that take each 186 solid where it is defined, and skip the subfigure instances, import
5 solids stacked near the origin instead of 23 placed ones. It stresses:

- subfigure definitions nested three deep (308 containing 408s of other 308s);
- the same definition placed several times at different levels (the square cap appears 10 times);
- transformation matrices composed through the nesting, including non-axis rotations;
- both placement mechanisms of a 408 (its X, Y, Z parameters and its directory entry's matrix).

## Check values

Exact values from the generator, for checking a reader:

| | |
|---|---|
| Solids | 23 |
| Faces | 166 |
| Total volume | 396,937.070 mm³ (the solids overlap; this is the sum of their volumes) |
| Bounding box | x −100 … 100, y −70 … 70, z −8 … 145.095 mm |
