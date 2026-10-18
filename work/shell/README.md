# work/shell: what matter the Fuchs shell requires

Pipeline for Steps 3 and 4 of `PLAN.md`. Everything here is reproducible from the repository root.

| File | What it does |
|---|---|
| `../../matlab/build_shell.m` | Runs in the CI job `shell` (`.github/workflows/matlab.yml`). Builds the shell with WarpFactory exactly as the authors' example `W1_Warp_Shell.mlx` does, static and with the 0.02 shift, and exports the 1D construction profiles, the Eulerian stress-energy along the x and y axes through the centre, and central-plane slices. Artifact `shell-results`, downloaded into `ci-artifacts/` |
| `replicate_profiles.py` | The same 1D construction in NumPy, step for step, including MATLAB's moving-average edge rule. Writes `replica/profiles_static.csv` in the artifact's format |
| `compare_profiles.py` | MATLAB profiles against the replica, column by column |
| `hoop_stress.py` | The measurement. Route 1D: the equilibrium identity P_t = P_r + (r/2)[dP_r/dr + (rho + P_r) da/dr] on the construction's own smoothed profiles. Route 3D: WarpFactory's solver read on the y-axis, where P_yy is radial and P_xx = P_zz tangential. Prints both, their pointwise difference, and the warp-minus-static changes; `--png` draws the figure |

## Regenerate

```
.venv\Scripts\python work\shell\replicate_profiles.py
gh run download <run-id> -n shell-results -D work\shell\ci-artifacts
.venv\Scripts\python work\shell\compare_profiles.py work\shell\ci-artifacts\profiles_static.csv work\shell\replica\profiles_static.csv
.venv\Scripts\python work\shell\hoop_stress.py work\shell\ci-artifacts --png work\shell\hoop_stress.png
```

## Configuration under test

Copied from the authors' live script, not chosen by us: R1 = 10 m, R2 = 20 m, 2GM/(R2 c^2) = 1/3
(M = 4.49e27 kg), Rbuff = 0, sigma = 0, smoothFactor = 4000 (four passes of a moving average over
4000 radial samples for the pressure and 7160 for the density, with the radial sample spacing
5.07e-4 m), shift 0.02, grid 300 x 300 x 5 cells at 0.2 m. The 5-cell depth is the authors'
"cartoon" method: only the central z-plane has a complete fourth-order stencil, and that is the
plane we read. Results are in `RESULTS.md` once the CI artifact has been analysed.
