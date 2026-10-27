# Results: the paper's figures next to ours (Part 3, Step 3)

27 October 2026. The paper: Fuchs, Helmerich, Bobrick, Sellers, Melcher, Martire, "Constant Velocity
Physical Warp Drive Solution", CQG 41 (2024), arXiv:2405.02709, CC BY 4.0. Its Figures 4 to 10 are
"for a slice along the y-axis" at the authors' configuration, static (Figures 4 to 7) and with the
0.02 shift (Figures 8 to 10). Ours come from the Part 1 CI export at the same configuration
(`matlab/shift_matrix.m`, WarpFactory 03b10cb, MATLAB R2026b): the central-plane slices
`work/matrix/run-fine/slice_f1_b1.mat` (static) and `slice_f1_b5.mat` (shift 0.02, formed by linearity,
verified exact), read on the grid column at x = -0.1 m, which is the line `matlab/build_shell.m`
exported and which the two neighbouring columns reproduce to 8e-12; the smoothed inputs from
`profiles_f1.csv` of the same run. The paper's curves were read off the PDF's vector paths
(`digitise_paper.py`): each panel calibrated on its tick marks (a first pass used the tick-label boxes,
which sit 0.2 pt below the marks and put a 0.1 % offset on every panel; Carlos spotted it in the
workbook), 14,988 segments per curve; baselines that must be zero read zero to 1e-4 of the axis range,
and the radius is read to 0.1 mm. The pairs are `pairs/fig04_pair.png` to `pairs/fig10_pair.png`.

## 1. Verdict per pair

The form of every curve is the same: the same features at the same radii, in every panel. The
amplitudes differ by a few percent, most in the sharpest features, and section 3 traces all of it to
one cause. "Paper / ours" is the ratio of peak values from `comparison.csv`.

The verdict was planned as Carlos's visual "same picture / not the same" per pair (PLAN Step 3), a
sanity gate from an independent eye before the measurement steps. With the curves digitised to a
part in ten thousand and every difference accounted for, the gate is decided by the numbers, and on
27 October Carlos declined the visual verdict as a judgement a non-physicist cannot make. The
verdict below is therefore numerical, and the last column says what each difference is.

| Figure | What it shows | Same picture? | Peak values, paper against ours | What the difference is |
|---|---|---|---|---|
| 4 | The construction's inputs: density and pressure before and after smoothing | Yes | rho' 1.376e40 vs 1.376e40; P' at R1 1.300e39 vs 1.299e39; rho~ 1.373e40 vs 1.358e40; P~ 1.069e39 vs 1.042e39 | The unsmoothed inputs agree to 1e-4: same mass, radii and pressure step. The smoothed ones are narrower in the paper by 12 % of the wall width (section 3); that is the one real difference, and it is a setting |
| 5 | Static metric g00, g22 along y with the Schwarzschild reference | Yes | cavity g00 -0.5795 vs -0.5802; g22 peak 1.431 at 21.4 m vs 1.421 at 21.7 m | 0.1 % in the cavity lapse and 0.7 % in the g22 peak, both reproduced by the fitted smoothing; the metric is set by the mass, which is the same |
| 6 | Static stress-energy: energy density with rho~; P_2 radial, P_1 = P_3 tangential with P~ | Yes | rho 1.373e40 vs 1.358e40; P_2 1.069e39 vs 1.042e39; P_1 = P_3 2.903e39 at 10.25 m vs 2.631e39 at 10.30 m | 1 %, 2.5 % and 10 %: the sharper the feature, the larger; all three follow from the smoothing (section 3) |
| 7 | Static energy conditions, four sampled maps | Yes, including the low Null and Weak plateaus (section 2) | Null, Weak 2.802e39 vs 2.769e39; Strong 7.146e39 vs 7.056e39; Dominant 9.697e39 vs 9.591e39 | 1 %, the smoothing; no violation in either |
| 8 | Warp-shell metric g00, g01, g22 | Yes (raster in the PDF; by eye) | g01 -0.02 inside, 0 outside, transition 11 to 19 m in both | none visible |
| 9 | Warp-shell stress-energy: energy density, pressures, momentum, shears | Yes | rho 1.371e40 vs 1.356e40; P_1, P_3 2.876e39 vs 2.592e39; p_1 +4.376e39 at 12.4 m vs +4.119e39 at 12.5 m, -3.228e39 at 17.6 m vs -3.032e39 at 17.5 m | 1 %, 11 % and 6 %, the smoothing; our shear panel has a 1.9e37 bump (0.14 % of rho0) from our line's 0.1 m offset from the axis (section 5), the paper's line is on the axis |
| 10 | Warp-shell energy conditions | Yes | Null, Weak 2.808e39 vs 2.748e39; Strong 7.120e39 vs 6.907e39; Dominant 9.675e39 vs 9.486e39 | 2 to 3 %, the smoothing; no violation in either |

Whether a difference "matters" depends on what it is used for. For the project's conclusions, that
the shell needs a hoop stress of about a fifth of its energy density and can carry a shift of about a
tenth of its compactness, a 10 % change in the sharpest feature changes nothing; for the record, the
hoop stress at the paper's own setting is 0.211 rho0 c^2 rather than the 0.194 of the live script
(section 4). What does matter is that the published script and the figures differ, because anyone
rerunning the script, as we did, gets the script's numbers, not the paper's.

## 2. What the pairs establish

- The configuration is the one we copied: R1, R2 and M agree (the unsmoothed density plateau
  1.376e40 against our 1.376e40, the unsmoothed pressure step 1.300e39 against 1.299e39, the
  half-maximum radii of the smoothed density 10.01 and 20.01 m in both).
- Claim C8 from the paper's own Figure 4: the unsmoothed pressure at R1 is 0.0945 rho0 c^2, the
  uniform-solid-sphere closed form the code applies (0.0944), not the 0.073 of the inward integration
  the text describes (`work/notes/02-hollow-shell.md`).
- The paper's Null and Weak panels (Figures 7 and 10) plateau at 2.8e39 where their Strong panel
  reaches 7.1e39; our exported maps do the same (2.77e39), and the Minkowski-consistent evaluation of
  the same observer set gives 7.06e39 (dashed in our panels). The published Null and Weak maps carry
  the index inconsistency of claim C9 (`work/matrix/RESULTS.md` section 4): inside the shell they read
  low by about g00^2. No violation either way.
- Every solver output in the paper sits 1 to 11 % above ours, and the excess grows with the
  sharpness of the feature: 1.1 % on the energy density peak, 2.5 % on the radial pressure, 10 % on
  the hoop-stress spike, 6 % on the momentum lobes, 1 to 3 % on the energy-condition maps.

## 3. The difference is the smoothing behind the figures

The paper's smoothed inputs are its own curves, not solver output, and they are sharper than the
live script's: the inner wall is 4.65 m wide from 10 to 90 % of the plateau against 5.36 m, and the
plateau keeps nearly its full unsmoothed height (1.373e40 of 1.376e40) where the live script's
smoothing rounds it to 1.358e40. At fixed geometry and mass the construction has two free numbers, the moving-average spans
of density and pressure (four passes each; paper footnote 7: "a ratio between the span of density and
pressure s_rho / s_P ~ 1.72"; `metricGet_WarpShellComoving.m`: 1.79 x smoothFactor and smoothFactor,
with smoothFactor = 4000 in `W1_Warp_Shell.mlx`). `fit_smoothing.py` fits each span to the digitised
curves with the NumPy replica of the construction (`work/shell/replicate_profiles.py`, validated
against WarpFactory's export to 1e-13):

| | Density span | Pressure span | Ratio | Misfit, rho~ | Misfit, P~ |
|---|---|---|---|---|---|
| Live script (smoothFactor 4000) | 7160 samples, 3.63 m per pass | 4000, 2.03 m | 1.79 | 2.5 % | 1.3 % |
| Fitted to Figure 6 | 6100, 3.10 m | 3540, 1.80 m | **1.723** | 0.00 % | 0.02 % |
| Fitted to Figure 4, independently | 6100 | 3540 | 1.723 | 0.01 % | 0.02 % |

Both spans were free; their ratio came out at the paper's stated 1.72. Rebuilding the construction at
the fitted spans predicts the paper's solver outputs that depend only on the 1D profiles:

| | Live script | Fitted spans | Paper, digitised |
|---|---|---|---|
| Inner wall, 10 to 90 % of the plateau | 5.362 m | 4.649 m | 4.646 m |
| Radial pressure, peak | 1.042e39 | 1.069e39 | 1.069e39 |
| Tangential pressure (hoop stress), peak, by the equilibrium identity | 2.632e39 at 10.31 m | 2.907e39 at 10.25 m | 2.903e39 at 10.25 m |
| g22 peak | 1.4206 at 21.67 m | 1.4307 at 21.36 m | 1.4307 at 21.36 m |
| Cavity g00 | -0.5802 | -0.5796 | -0.5795 |
| Smoothed mass / M | 1.0188 | 1.0136 | |

The hoop-stress spike, the figure's sharpest feature, is reproduced to 0.14 %, the wall width to
3 mm, the g22 peak to a part in ten thousand. The figures were made
with a smoothing about 12 % narrower than the published live script's, at the ratio the paper states
rather than the one the code carries. A second difference of the same kind: each of the paper's
curves is a path of 14,988 segments starting at r = 0.01 m, so its line was sampled about every 2 mm
through the centre, while the live script's grid has 150 cells per half-axis at 0.2 m and no cell at
r = 0. Which grid produced the figures, and whether the 1.72 was a parameter of an earlier code
version, are questions for the authors (register row C10).

## 4. What this changes in Parts 1 and 2

Nothing in form; the numbers that scale with the wall sharpness move by up to a tenth. The hoop
stress the shell requires is 0.194 rho0 c^2 at the live script's smoothing (`work/shell/RESULTS.md`)
and 0.211 rho0 c^2 at the smoothing behind the paper's figures (2.903e39 over the paper's own peak
energy density 1.373e40); the strength a material would need follows it. The shift ceiling of
0.09 to 0.10 times the compactness and the exact energy-condition verdicts were obtained at the live
script's smoothing and were not recomputed; the momentum density at the paper's shift is 6 to 7 %
higher in the paper's figure, so the ceiling at the figures' smoothing would be slightly lower, which
a rerun of the matrix with smoothFactor 3540 and a shadow copy of `metricGet_WarpShellComoving.m`
carrying 1.72 can settle (not done; `.github/workflows/matlab.yml`, job `matrix`).

## 5. Caveats

- Our line sits at x = -0.1 m, the grid's nearest column to the axis; the paper's passes through
  r = 0. The one visible consequence is the shear panel of Figure 9: at x = -0.1 m the off-diagonal
  stress sigma_12 = x y (P_r - P_t)/r^2 is 1.9e37 at 9.9 m (0.14 % of rho0, the same value in the
  static slice), while on the axis it vanishes, as the paper's flat line shows.
- Figure 8 is a raster image in the PDF and is judged by eye; the vector figures are digitised on
  their tick marks, and baselines that must be zero (the unsmoothed inputs outside the shell, every
  map beyond 26 m) read zero to 1e-4 of the axis range, which is the accuracy of a paper value.
- The paper's Figure 4 legend labels the smoothed curves rho' and P' and the unsmoothed ones rho~
  and P~, the reverse of its own equation (22) and caption; our panel labels them as drawn.
- The energy-condition panels are WarpFactory's sampled maps (100 directions, 10 speeds), the
  paper's method, as exported from the same code; the exact (warpax) verdict on these slices is
  Part 2, `work/matrix/RESULTS.md` section 7.
