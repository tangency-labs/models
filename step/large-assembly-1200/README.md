# large-assembly-1200

A flat STEP assembly of 1,200 simple solids: 60 distinct parts, each placed many times, in 24
row sub-assemblies of 50 parts. The same layout at another size: [large-assembly-700](../large-assembly-700/).

- **File:** `large-assembly-1200.step`
- **Author:** raykholo
- **Made with:** `scripts/generators/large_assembly.py` (Python 3, standard library only; shared
  code in `scripts/generators/prism.py`). It writes STEP AP214 (`AUTOMOTIVE_DESIGN`) directly, in
  millimetres, with a distance accuracy of 1e-6 mm. Run
  `python3 scripts/generators/large_assembly.py 1200 step/large-assembly-1200` to reproduce the file
  byte for byte.
- **Application protocol:** AP214.
- **Size:** 1,200 solid instances of 60 distinct solids; 9,400 faces, 21,000 edges and
  14,000 vertices over all instances. Product structure: 85 products, 1,224
  next-assembly-usage occurrences, 24 sub-assemblies under one root. 1.2 MB.
- **SHA-256:** `673e5c8bba060eac270708dd6e5e0f50a1083825b4c9aadb9235b192e0d98828`

## Structure

The root assembly places 24 row sub-assemblies, 30 mm apart along Y. Each row places 50 parts,
30 mm apart along X, each turned about Z by a multiple of 15 degrees. The parts are planar
prisms: regular polygons of 3 to 12 sides, rectangular blocks and L-sections, 4 to 26 mm tall.
Placements are next-assembly-usage occurrences with item-defined transformations, as the CAx-IF
recommends for AP214 assemblies.

## Why it is interesting

The geometry is trivial, so the load time measures the assembly: reading 1,224
occurrences, placing 1,200 instances of 60 shared shapes, and building a model tree of that size.
Readers that copy each instance's geometry instead of sharing it, or cap the number of bodies or
occurrences, show it here first.

## Check values

Exact values from the generator, for checking a reader:

| | |
|---|---|
| Solids | 1,200 |
| Faces | 9,400 |
| Total volume | 2,817,664.542 mm³ |
| Bounding box | x -18.163 … 1490.1, y -19.053 … 709.053, z 0 … 26 mm |
