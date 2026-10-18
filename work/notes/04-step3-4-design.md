# Note 04: design facts for Steps 3 and 4 (gathered 18 October, not yet executed)

## warpax side

- `warpax.metrics.fuchs_default(v_s=0.02, R_1=10.0, R_2=20.0, R_b=1.0, r_s_param=6.668692,
  n_grid=2048, kernel_type="moving_average")` builds Le's reimplementation at the paper's
  parameters. `r_s_param` is 2GM/c^2 for M = 4.49e27 kg. `kernel_type="moving_average"` is the
  published boxcar, four passes, width ratio about 1.72; `"gaussian"` is his variance-matched
  substitute. `build_fuchs_construction(...)` returns a `FuchsConstructionResult` with the 1D
  profiles; read its fields before use (`src/warpax/metrics/fuchs_construction.py` line 259).
- `warpax.tov.residuals.tov_residual(r, rho, p_r, p_t, Phi_prime)` and
  `tov_residual_from_metric(...)` give the anisotropic equilibrium residual.
- `warpax.constraints.source_consistency.stress_energy_residual(metric_fn, coords, T_input)` gives
  Delta T at a point.
- The importer `warpax.io.warpfactory.load_warpfactory` expects a `.mat` with `metric.tensor` as a
  single array of shape (4, 4, Nt, Nx, Ny, Nz) and `metric.coords` with 1D arrays `t, x, y, z`.
  **WarpFactory's native struct has `tensor` as a 4x4 cell and no `coords` field**, so the export
  script in Step 3 must convert: stack the cell into a 6D array and write the coordinate vectors
  from `gridSize`, `worldCenter` and `gridScaling`. Save with `-v7.3`; the importer then needs
  `pip install "warpax[interop]"` for `mat73`.

## WarpFactory side (for `matlab/build_shell.m`)

- Build with `metricGet_WarpShellComoving(gridSize, worldCenter, m, R1, R2, Rbuff, sigma,
  smoothFactor, vWarp, doWarp, gridScaling)`. The paper's parameters: R1 = 10, R2 = 20,
  m = 4.49e27, vWarp = 0.02. `Rbuff`, `sigma` and `smoothFactor` for Figs 6-10 are not stated in
  the paper's text; the live script `Examples/4 Warp Shell/W1_Warp_Shell.mlx` should hold them.
  Reading a `.mlx` needs MATLAB: do it in the CI job with `matlab.internal.liveeditor.openAndConvert`
  or by unzipping the `.mlx` (it is a zip with `matlab/document.xml` inside) and grepping.
- Export `Metric.params` (`rVec`, `rho`, `rhosmooth`, `P`, `Psmooth`, `M`, `A`, `B`) as the 1D
  profiles for the hoop-stress identity, plus the 3D `tensor` and `getEnergyTensor` output, plus
  `evalMetric` energy conditions, to `results/shell/*.mat` and small `.csv` files for the 1D data.
- Grid: the paper does not state it; start at 1 m spacing on a box that clears R2 by a few cells
  (a 61^3 grid at 1 m with the shell centred), then 0.5 m.

## The 1D identity (Step 4 core)

With rho~ and P~ the smoothed inputs, m from rho~, b from m, and a from (m, P~):

- G_tt gives rho = rho~ exactly; G_rr gives P_r = P~ exactly (both up to the radial quadrature
  error of `cumtrapz` and the interpolation onto the grid).
- The angular components give P_t = P_r + (r/2)[dP_r/dr + (rho + P_r) da/dr].

So the profile of P_t, its peak over rho c^2, its sign at the inner wall, and the sweep over
`smoothFactor` can all be computed in NumPy from the exported 1D arrays, independently of any 3D
finite differencing. The 3D runs then test the solvers against this, not the other way round.

## Open parameters to pin down before computing

`Rbuff`, `sigma`, `smoothFactor`, the grid spacing and box of the paper's figures; whether the
paper's "iterated until the energy conditions are satisfied at the boundaries" was done by hand.
These are the questions 2 and 3 for Fuchs and Helmerich in `01-reading.md` §7.
