# spline-profile-prism

A prism whose outline is one closed, smooth spline through nine points.

- **File:** `spline-profile-prism.step`
- **Author:** raykholo
- **Made with:** SolidCraft 0.18.1 (`solidcraft-cli`), from the command script
  `scripts/generators/spline_profile_prism.json`, exported with SolidCraft's default STEP writer: AP242
  (`AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF`), millimetres. Reproduce it with
  `solidcraft-cli run scripts/generators/spline_profile_prism.json --out step/spline-profile-prism/spline-profile-prism.step`; the file is the
  same byte for byte when written under this name.
- **Application protocol:** AP242.
- **Size:** 1 solid; 11 faces (9 B-spline surfaces, 2 planes), 27 edges, 18 vertices in the file. 14 KB.
- **SHA-256:** `368194202b0b89ded73f055b09677533741441c2954bd1513bc74e3f06781ac4`

## Shape

A periodic cubic spline through nine points, an irregular lobed outline about 80 × 63 mm, extruded
25 mm. The side wall is written as nine B-spline faces, one per span between fit points, meeting
tangentially; the top and bottom are planes bounded by nine spline edges each.

## Why it is interesting

Every side edge is a spline, and neighbouring faces meet tangentially. It stresses blends and
offsets on spline edges, tessellation of tangent spline walls, and readers that join faces
across tangent edges.

## Check values

| | |
|---|---|
| Solids | 1 |
| Bounding box | x −40.02 … 40.05, y −28.07 … 31.75, z 0 … 25 mm |
| Volume | 82,529.6 mm³ (SolidCraft 0.18.1); 82,532.0 mm³ (FreeCAD 1.1.4) |
