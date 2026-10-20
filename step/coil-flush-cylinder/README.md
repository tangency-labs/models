# coil-flush-cylinder

A cylinder with a square-section coil joined round it, the coil's ends flush with the cylinder's end faces.

- **File:** `coil-flush-cylinder.step`
- **Author:** raykholo
- **Made with:** SolidCraft 0.18.1 (`solidcraft-cli`), from the command script
  `scripts/generators/coil_flush_cylinder.json`, exported with SolidCraft's default STEP writer: AP242
  (`AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF`), millimetres. Reproduce it with
  `solidcraft-cli run scripts/generators/coil_flush_cylinder.json --out step/coil-flush-cylinder/coil-flush-cylinder.step`; the file is the
  same byte for byte when written under this name.
- **Application protocol:** AP242.
- **Size:** 1 solid; 18 faces (13 B-spline surfaces, 5 planes), 48 edges, 32 vertices in the file. 1.6 MB.
- **SHA-256:** `937a3c96a7f1adf87afe21106371d0b0dfc13ab0519d5292fff023d5417b72ec`

## Shape

A cylinder, radius 15 mm and 40 mm long, with a coil joined round it: coil diameter 30.8 mm, a
4 mm square section inside that diameter, pitch 9 mm, 36 mm of height starting 2 mm up, so the
section spans z 0 to 40 and the coil's two end faces lie in the cylinder's end planes. The coil's
walls are B-spline surfaces; the coil overlaps the cylinder by 0.4 mm, as a hose thread does.

## Why it is interesting

The coil's ends lie exactly in the cylinder's end planes, so free-form edges of one body lie in
plane faces of the other. Making it is a hard boolean case, and reading it back stresses
tessellation and mass properties of long, twisting B-spline faces that meet planes edge to edge.
Readers agree on the box but not exactly on the volume (see below).

## Check values

| | |
|---|---|
| Solids | 1 |
| Bounding box | x −15.4 … 15.4, y −15.4 … 15.4, z 0 … 40 mm |
| Volume | 28,880.9 mm³ (SolidCraft 0.18.1); 28,966.9 mm³ (FreeCAD 1.1.4). No analytic value. |
