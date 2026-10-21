# filleted-boss-grid

A plate with an 8 × 8 grid of round bosses, every boss filleted where it meets the plate and round
its top: 128 small fillets on one solid.

- **File:** `filleted-boss-grid.step`
- **Author:** raykholo
- **Made with:** SolidCraft 0.18.1 (`solidcraft-cli`), from the command script
  `scripts/generators/filleted_boss_grid.json`, exported with SolidCraft's default STEP writer:
  AP242 (`AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF`), millimetres. Reproduce it with
  `solidcraft-cli run scripts/generators/filleted_boss_grid.json --out step/filleted-boss-grid/filleted-boss-grid.step`;
  the file is the same byte for byte when written under this name.
- **Application protocol:** AP242.
- **Size:** 1 solid; 390 faces, 844 edges, 520 vertices in the file. 911 KB.
- **SHA-256:** `842505915f16ab26d83cf85c16a58f5fdbdaf255aa859934fb739a7ac8696efa`

## Shape

A 120 × 120 × 10 mm plate. On its top, 64 cylindrical bosses, radius 4 mm and 6 mm tall, on a
13.5 mm grid. Each boss has a 1 mm concave fillet where it meets the plate and a 0.5 mm convex
fillet round its top edge.

## Why it is interesting

Many small fillets on one part, as on cast or moulded parts: 128 toroidal blends, each tangent to
a plane and a cylinder. They stress tessellation at small radii (and any measuring that refines
with the smallest radius), face count in the viewer, and picking small faces.

## Check values

| | |
|---|---|
| Solids | 1 |
| Volume | 163,582.520 mm³ (exact: plate + bosses + 64 × (base fillet − top fillet), by Pappus's theorem) |
| Bounding box | x 0 … 120, y 0 … 120, z 0 … 16 mm |
