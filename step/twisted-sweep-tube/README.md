# twisted-sweep-tube

A tube cut along its whole length by a rectangle swept with a 30° twist.

- **File:** `twisted-sweep-tube.step`
- **Author:** raykholo
- **Made with:** SolidCraft 0.18.1 (`solidcraft-cli`), from the command script
  `scripts/generators/twisted_sweep_tube.json`, exported with SolidCraft's default STEP writer: AP242
  (`AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF`), millimetres. Reproduce it with
  `solidcraft-cli run scripts/generators/twisted_sweep_tube.json --out step/twisted-sweep-tube/twisted-sweep-tube.step`; the file is the
  same byte for byte when written under this name.
- **Application protocol:** AP242.
- **Size:** 1 solid; 10 faces (5 B-spline surfaces, 2 cylinders, 3 planes), 27 edges, 18 vertices in the file. 0.4 MB.
- **SHA-256:** `7bf83102960361bd57070358b9cef5f8f237a839a5f8340ab61db41f51a29731`

## Shape

A tube, outer diameter 30 mm, inner diameter 20 mm and 250 mm long, cut by a 9 × 6 mm rectangle
centred on the wall (12.5 mm from the axis) and swept 250 mm along the tube with a 30° twist. The
cut goes through both walls, so a twisted slot runs the whole length.

## Why it is interesting

The slot's walls are twisted B-spline surfaces that cross both cylinders along long space
curves. It stresses intersection curves between free-form and cylindrical faces, and their
tessellation, over a long thin part.

## Check values

| | |
|---|---|
| Solids | 1 |
| Bounding box | x −15 … 15, y −15 … 15, z 0 … 250 mm |
| Volume | 90,194.5 mm³ (SolidCraft 0.18.1); 90,204.5 mm³ (FreeCAD 1.1.4). Uncut tube: 98,174.8 mm³. |
