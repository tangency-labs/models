# large-assembly-700

A flat STEP assembly of 700 simple solids: 35 distinct parts, each placed many times, in 20
row sub-assemblies of 35 parts. The same layout at another size: [large-assembly-1200](../large-assembly-1200/).

- **File:** `large-assembly-700.step`
- **Author:** raykholo
- **Made with:** `scripts/generators/large_assembly.py` (Python 3, standard library only; shared
  code in `scripts/generators/prism.py`). It writes STEP AP214 (`AUTOMOTIVE_DESIGN`) directly, in
  millimetres, with a distance accuracy of 1e-6 mm. Run
  `python3 scripts/generators/large_assembly.py 700 step/large-assembly-700` to reproduce the file
  byte for byte.
- **Application protocol:** AP214.
- **Size:** 700 solid instances of 35 distinct solids; 5,360 faces, 11,880 edges and
  7,920 vertices over all instances. Product structure: 56 products, 720
  next-assembly-usage occurrences, 20 sub-assemblies under one root. 0.7 MB.
- **SHA-256:** `58674bbadbef6b4941c206f1e70f2af2a43415f5d469010ca6d2ef0a93b2ceb3`

## Structure

The root assembly places 20 row sub-assemblies, 30 mm apart along Y. Each row places 35 parts,
30 mm apart along X, each turned about Z by a multiple of 15 degrees. The parts are planar
prisms: regular polygons of 3 to 12 sides, rectangular blocks and L-sections, 4 to 26 mm tall.
Placements are next-assembly-usage occurrences with item-defined transformations, as the CAx-IF
recommends for AP214 assemblies.

## Why it is interesting

The geometry is trivial, so the load time measures the assembly: reading 720
occurrences, placing 700 instances of 35 shared shapes, and building a model tree of that size.
Readers that copy each instance's geometry instead of sharing it, or cap the number of bodies or
occurrences, show it here first.

## Check values

Exact values from the generator, for checking a reader:

| | |
|---|---|
| Solids | 700 |
| Faces | 5,360 |
| Total volume | 1,559,917.795 mm³ |
| Bounding box | x -22 … 1036, y -18.163 … 587.088, z 0 … 26 mm |
