# component-tree-650

A STEP product tree of 655 components, four levels deep and five wide at each assembly level,
every assembly a distinct product with its own name: 156 assemblies and 500 part occurrences of 16
small planar parts.

- **File:** `component-tree-650.step`
- **Author:** raykholo
- **Made with:** `scripts/generators/component_tree.py` (Python 3, standard library only; shared
  code in `scripts/generators/prism.py`). It writes STEP AP214 (`AUTOMOTIVE_DESIGN`) directly, in
  millimetres, with a distance accuracy of 1e-6 mm. Run
  `python3 scripts/generators/component_tree.py step/component-tree-650` to reproduce the file byte
  for byte.
- **Application protocol:** AP214.
- **Size:** 500 solid instances of 16 distinct solids; 3,657 faces, 7,971 edges and 5,314 vertices
  over all instances. Product structure: 172 products (156 assemblies, 16 parts), 655
  next-assembly-usage occurrences. 0.6 MB.
- **SHA-256:** `8a839fc172a0c2eeec3dec3e72675002be549cc2b1c6b32fab0fb99989ae752e`

## Structure

`component-tree-650` → 5 `group-G` → 5 `group-G-S` each → 5 `module-G-S-M` each → 4 parts each.
The 125 modules are distinct products (none is shared), so a model tree shows 655 components:
5 + 25 + 125 assemblies and 500 parts. The parts are 16 small prisms, reused across modules and
turned about Z in 30° steps inside each module.

## Why it is interesting

The geometry is small; the tree is not. It stresses a model browser: listing 655 nodes, expanding
and collapsing whole levels, hiding and showing a group of 100 parts at once, and selecting a
component deep in the tree. It also checks that a reader keeps every assembly a separate node
instead of merging the ones with the same shape.

## Check values

Exact values from the generator, for checking a reader:

| | |
|---|---|
| Components | 655 (156 assemblies, 500 part occurrences, under one root) |
| Solids | 500 |
| Faces | 3,657 |
| Total volume | 78,754.325 mm³ |
| Bounding box | x -6 … 330, y -7.5 … 335.5, z 0 … 6 mm |
