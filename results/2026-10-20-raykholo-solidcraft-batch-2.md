# SolidCraft 0.18.1 on a 6-core laptop, second batch

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
| `step/nested-rotated-assembly/nested-rotated-assembly.step` | `f2f9c489c820` | 0.02 | 0.02 | 0.10 | 25 | 32 of 32 solids; volume and bounding box match the README |
| `step/component-tree-650/component-tree-650.step` | `8a839fc172a0` | 0.35 | 0.34 | 0.36 | 48 | 500 of 500 solids; volume and bounding box match the README |
| `step/untrimmed-surface-body/untrimmed-surface-body.step` | `2decd6561114` | < 0.01 | < 0.01 | < 0.01 | 21 | 1 open body, area 26,000 mm²; bounding box 100 × 80 × 50 mm, the trimmed faces' |
| `step/spline-profile-prism/spline-profile-prism.step` | `368194202b0b` | 0.12 | 0.11 | 0.13 | 36 | 1 solid, 82,529.6 mm³; the nine spline side faces are joined into one |
| `step/twisted-sweep-tube/twisted-sweep-tube.step` | `7bf831029603` | 0.20 | 0.20 | 0.24 | 51 | 1 solid, 90,194.5 mm³ |
| `step/coil-flush-cylinder/coil-flush-cylinder.step` | `937a3c96a7f1` | 2.46 | 2.09 | 2.93 | 67 | 1 solid, 28,880.9 mm³ (FreeCAD 1.1.4 gives 28,966.9) |

## Notes

- The machine was shared with other jobs (load average 10 to 20 on 12 threads), so the times
  include some contention. All runs at nice 10.
- Times under 0.01 s are below what `/usr/bin/time` resolves.
- Peak memory is the process's maximum resident set size.
