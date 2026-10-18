# Note 05: the first measurement (Steps 3-4, static shell)

18 October 2026, evening. Full numbers and tables in `work/shell/RESULTS.md`; this note is the log
entry.

- The authors' own example configuration was read out of `W1_Warp_Shell.mlx` (the live script is a
  zip; `matlab/document.xml` holds the code), so no parameter had to be guessed or asked for:
  smoothFactor = 4000, a 300 x 300 x 5 "cartoon" grid at 0.2 m, M fixed by 2GM/R2c^2 = 1/3.
- WarpFactory built both shells on the GitHub runner in about a minute each; the energy tensor and
  Eulerian frame took six seconds. Two toolboxes are needed: Parallel Computing (`isgpuarray`) and
  Curve Fitting (`smooth`). Neither is in WarpFactory's README.
- A NumPy replica of the 1D construction matches MATLAB's export to 1e-13, including the
  moving-average edge rule. The warp and static 1D profiles are byte-identical.
- The equilibrium identity on those profiles and WarpFactory's finite-difference solver on the
  y-axis give the same tangential pressure to 4e-5 of rho0 c^2: peak +0.194 at r = 10.3 m. The
  radial pressure peaks at +0.077. The dominant energy condition holds with margin 2.6.
- The smoothing sweep shows the hoop stress scaling as one over the wall width while the wall is
  thin, and the dominant energy condition failing below about two metres. The smoothing is what
  buys the energy conditions.
- The two outermost grid cells on every line are stencil artefacts (rho = 0.41 rho0 in vacuum).
  Excluded, as the authors recommend; worth a sentence in the report because they are the largest
  numbers in the raw export.

Next computations: the all-observer energy conditions of the warp shell in WarpFactory (its sampled
check, on the runner; `evalMetric` with tryGPU = 0) and in warpax (matrix inequalities on the
exported slice or on the native `FuchsMetric`); the warpax-native 1D comparison; the side-by-side
figures against the paper's Figs 6, 8, 9.
