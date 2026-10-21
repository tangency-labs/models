# tessellated-brep-mix

An AP242 assembly of three parts side by side: two exact B-rep solids (a block and a hexagonal
post) and one part given only as a tessellation (a closed, faceted dome, as a triangulated surface
set).

- **File:** `tessellated-brep-mix.step`
- **Author:** raykholo
- **Made with:** `scripts/generators/tessellated_brep_mix.py` (Python 3, standard library only;
  shared code in `scripts/generators/prism.py`). It writes STEP AP242
  (`AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF`) directly, in millimetres. Run
  `python3 scripts/generators/tessellated_brep_mix.py step/tessellated-brep-mix` to reproduce the
  file byte for byte.
- **Application protocol:** AP242, with tessellated geometry (`TESSELLATED_SHAPE_REPRESENTATION`,
  `TRIANGULATED_SURFACE_SET`, `COORDINATES_LIST`) alongside B-rep (`ADVANCED_BREP_SHAPE_REPRESENTATION`).
- **Size:** 3 parts in one assembly. B-rep: 2 solids, 14 planar faces. Tessellation: 290 vertices,
  576 triangles. 36 KB.
- **SHA-256:** `068e1d22b2e237930c66a773ce862ff67d45888c9a07b1935926b43dfbfec92a`

## Structure

| Part | Geometry | Placed at |
|---|---|---|
| `block` | B-rep box, 40 × 30 × 12 mm, centred on its axis | x = 0 |
| `hex-post` | B-rep hexagonal prism, 10 mm corner radius, 35 mm tall | x = 60 |
| `faceted-dome` | a closed hemisphere of radius 20 mm, 12 rings of 24 facets and a flat bottom, as one triangulated surface set without normals | x = 120 |

Each part is a product placed in the root assembly by a next-assembly-usage occurrence with an
item-defined transformation.

## Why it is interesting

AP242 lets a file carry faceted geometry where exact geometry is missing or not needed: scanned
parts, purchased parts, simplified fasteners. A reader that only takes B-rep loses those parts,
and the assembly comes in with gaps. Whether it warns about it is part of the test.

## Check values

| | |
|---|---|
| Parts | 3 (2 B-rep solids, 1 tessellated) |
| Volumes | block 14,400 mm³; hex-post 9,093.267 mm³; faceted dome 16,493.563 mm³ (of its facets) |
| Bounding box | x −20 … 140, y −20 … 20, z 0 … 35 mm |
