# SolidCraft 0.18.1 on a 6-core laptop

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
| `iges/instanced-assembly-subfigures/instanced-assembly-subfigures.igs` | `8457accbaed7` | 0.02 | 0.02 | 0.10 | 21 | 5 of 23 solids: subfigure instances (408) not read |
| `step/large-assembly-700/large-assembly-700.step` | `58674bbadbef` | 1.09 | 1.06 | 1.10 | 58 | 700 of 700 solids; volume and bounding box match the README |
| `step/large-assembly-1200/large-assembly-1200.step` | `673e5c8bba06` | 1.97 | 1.62 | 2.03 | 75 | 1,200 of 1,200 solids; volume and bounding box match the README |

## Notes

- The machine was shared with other jobs (load average 10 to 13 on 12 threads), so the times
  include some contention. All runs at nice 10.
- `instanced-assembly-subfigures.igs`: SolidCraft 0.18.1 imports each solid once, where its
  subfigure definition puts it (5 solids, 258,632.559 mm³, z 0 to 70 mm), instead of the 23
  placed instances. An unreleased build with subfigure support (pull request #1609 on
  tangency-labs/solidcraft) reads all 23 solids with the README's volume and bounding box.
- Peak memory is the process's maximum resident set size.
