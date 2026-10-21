# SolidCraft 0.18.1 on a 6-core laptop, third batch

- **Submitted by:** raykholo
- **Date run:** 2026-10-20

## Machine

| | |
|---|---|
| CPU | Intel Core i7-9750H, 6 cores / 12 threads |
| RAM | 32 GB |
| GPU | not used (headless command-line import) |
| Storage | NVMe SSD |
| Operating system | Fedora-based Linux (kernel 7.0) |

## Software

| | |
|---|---|
| Software | SolidCraft 0.18.1 (`solidcraft-cli`, release build of commit 522ae775) |
| Import settings | defaults: millimetres, no healing options |
| What was timed | `solidcraft-cli eval <file>`: process start to exit, which reads the file, builds every body and measures it |
| Cache | warm (the file was read before the timed runs) |
| Runs per model | 3 |

## Results

| Model | SHA-256 | Median (s) | Min (s) | Max (s) | Peak memory (MB) | Notes |
|---|---|---|---|---|---|---|
| `step/vertices-off-curves/vertices-off-curves.step` | `6ae8ac2b1a9c` | 0.01 | < 0.01 | 0.01 | 12 | failed: no bodies; "edge vertices are 1.900e-1 mm off their curve" |
| `iges/trimmed-patch-cube/trimmed-patch-cube.igs` | `8911254f16a3` | 0.08 | 0.08 | 0.09 | 22 | 15 of 54 faces, an open body; faces with reversed first trim pieces or trim gaps left out |
| `step/tessellated-brep-mix/tessellated-brep-mix.step` | `068e1d22b2e2` | 0.02 | 0.02 | 0.04 | 22 | 2 of 3 parts: the tessellated dome is left out, with no warning |
| `step/toothed-plate-50k-faces/toothed-plate-50k-faces.step` | `9f59ade85de5` | 89.71 | 77.71 | 90.82 | 1,207 | 1 solid, 50,002 faces, volume and bounding box match the README |
| `stl/terrain-block-1m/terrain-block-1m.stl` | `2c5e4e39999a` | 7.90 | 7.88 | 7.96 | 487 | 988,880 triangles, volume matches the README |
| `obj/terrain-block-1m/terrain-block-1m.obj` | `1349cbb4d5ef` | 6.14 | 6.07 | 6.24 | 329 | 988,880 triangles, volume matches the README |
| `3mf/terrain-block-1m/terrain-block-1m.3mf` | `680fce128d2f` | 7.86 | 7.40 | 7.88 | 333 | 988,880 triangles, volume matches the README |
| `stl/defective-mesh/defective-mesh.stl` | `303238a59aaa` | < 0.01 | < 0.01 | < 0.01 | 15 | one mesh body, 97 triangles: the duplicate dropped, the flipped triangle turned back (62,666.667 mm³) |

## Notes

- The machine was shared with other jobs (load average 8 to 14 on 12 threads), so the times
  include some contention. All runs at nice 10.
- Times under 0.01 s are below what `/usr/bin/time` resolves.
- `toothed-plate-50k-faces`: opening the file without measuring takes 28 s (0.9 GB); the rest of
  the time is measuring the body.
- Peak memory is the process's maximum resident set size.
