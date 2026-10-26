# Results: the allowed shift against compactness (Part 1A), and what fails first

26 October 2026. Data: CI runs 40406621961 (coarse: shifts 0 to 0.16 at every compactness) and
40411091447 (refined: shifts in units of the compactness C, 0 to 0.15 C) of `matlab/shift_matrix.m`,
WarpFactory 03b10cb under MATLAB R2026b with `matlab/shadow/generateUniformField.m` on the path (see
section 5). Analysis: `analyse_matrix.py`, `verify_null_bug.py`. Geometry, smoothing and grid are
the authors' (`W1_Warp_Shell.mlx`); only the mass and the shift vary. Margins are fractions of
rho0, the peak Eulerian energy density of the static shell at each compactness. Two edge cells are
dropped on every side. Figure: `matrix_fine.png`; coarse pass `matrix_coarse.png`.

## 1. The shell carries a shift proportional to its compactness

First failing shift per compactness, as a bracket between the largest passing and the smallest
failing value tested. "Sampled dominant" is WarpFactory's own check (100 directions x 10 speeds).
"Null, 4000 directions" is a direct minimisation of the null contraction in the Eulerian frame.
"Swarm" is the largest shift at which every active point is still Hawking-Ellis Type I with the
trace condition satisfied, the condition for the matter to be a swarm of subluminal particles.

| Compactness 2GM/(R2 c²) | M [kg] | Sampled dominant: passes / fails | Null, 4000 directions | Swarm-realisable everywhere | In units of C (all three) |
|---|---|---|---|---|---|
| 0.3333 (the paper) | 4.49e27 | 0.0300 / 0.0333 | 0.0300 / 0.0333 | 0.0300 / 0.0333 | 0.09 / 0.10 |
| 0.1 | 1.35e27 | 0.0090 / 0.0100 | 0.0090 / 0.0100 | 0.0090 / 0.0100 | 0.09 / 0.10 |
| 0.0333 | 4.49e26 | 0.0030 / 0.0033 | 0.0030 / 0.0033 | 0.0030 / 0.0033 | 0.09 / 0.10 |
| 0.01 | 1.35e26 | 0.0009 / 0.0010 | 0.0009 / 0.0010 | 0.0009 / 0.0010 | 0.09 / 0.10 |

Three independent readings put the ceiling in the same place at every compactness:

**beta_max = (0.09 to 0.10) x compactness**, over a range of 33 in compactness, for this geometry
and smoothing.

The margins themselves collapse onto one curve when plotted against shift over compactness
(left panel of the figure). The mechanism is visible in the raw numbers: the Eulerian momentum
density grows as 0.303 rho0 per 0.02 of shift at C = 1/3 and scales as beta / C, because the shift
profile and its gradients are fixed by the geometry while the energy density is fixed by the mass.
At the threshold the largest momentum density is 0.40 to 0.45 rho0 at every compactness, which is
where it reaches the local energy density in the wall; there the stress-energy loses its timelike
eigenvector (the Type I fraction drops below 100 % at exactly the failing shift) and the dominant
condition's flux bound, the null condition and swarm realisability all fail together.

## 2. The paper's own point

At the paper's compactness the published shift of 0.02 (beta / C = 0.06) passes every check with
every margin at the numerical noise floor, about 1e-6 rho0, which is the "10^34 J/m^3" floor the
paper states. The paper's footnote that 0.02 "is likely not an upper limit" is correct: the ceiling
is between 0.030 and 0.033, a factor 1.5 to 1.65 above it. Claim C5 is closed from WarpFactory's
side; warpax's reading is Part 2.

## 3. Combined with the strength scaling: what a real material allows

`work/shell/RESULTS.md` section 6 found the hoop stress the shell needs to be 0.76 x compactness in
units of the local energy density. Combining the two measured laws, a shell whose material can
sustain a strength-to-energy ratio s has compactness at most s / 0.76 and therefore

**beta_max = about 0.13 x s.**

For graphene, s = 6.4e-10, that is a shift of 8e-11, about 2.5 centimetres per second. For the swarm
model of `work/notes/06`, which needs no strength, the compactness is bounded instead by orbital
stability near 1/3, so the swarm ceiling is the paper's: about 0.03, at the paper's two Jupiter
masses. Within this construction there is no corner in which a shell made of anything real carries
a shift worth the name.

## 4. WarpFactory's Null and Weak maps use the wrong metric for the index change

In `Analyzer/getEnergyConditions.m` the stress-energy is transformed to the orthonormal Eulerian
frame and flagged contravariant; the Null and Weak branches then lower its indices with the
coordinate metric (`changeTensorIndex(energyTensor, "covariant", metric)`), while the Dominant and
Strong branches do the same step with a Minkowski metric. For a frame tensor only the Minkowski
choice is consistent. The error is invisible where the metric is Minkowski, small where only
g_rr differs from one (the static shell), and grows with the shift, which makes g_01 nonzero.

`verify_null_bug.py` replicates their Null evaluation in NumPy on exported slices at C = 1/3:

| beta / C | WarpFactory's Null map, min | Replica with the coordinate metric | Same with Minkowski | Null, 4000 directions |
|---|---|---|---|---|
| 0 | -1.08e-6 | -1.08e-6 (agrees to 1.8e-16) | -2.8e-7 | -5.6e-7 |
| 0.08 | -0.0493 | -0.0493 (agrees to 1.3e-16) | -3.0e-7 | -6.0e-7 |
| 0.10 | -0.114 | -0.114 (agrees to 1.6e-16) | -0.045 | -0.097 |

So the sampled Null and Weak maps report violations from beta / C = 0.07 that do not exist, and
would have put the paper's ceiling at 0.020 to 0.023 instead of 0.030 to 0.033. At the paper's own
point they show none, so the published conclusion is unaffected. Candidate upstream issue, with the
one-line fix: use `metricMinkowski` in those two branches as the other two already do.

A second, smaller point for claim C4: 100 directions find the threshold where 4000 do, but above
it they underestimate the depth of the violation by about a factor two (-0.045 against -0.097 at
beta / C = 0.10). The sampling is adequate for pass or fail at this resolution, not for magnitudes.

## 5. Incidental: the sampling needs a GPU unless shimmed

`generateUniformField.m` calls `getEvenPointsOnSphere(..., 1)` with the GPU flag hard-coded, so
`getEnergyConditions` fails with "Error using gpuArray" on any machine without one, whatever the
caller's `tryGPU`. `matlab/shadow/generateUniformField.m` is a copy that passes the flag through;
it is placed after WarpFactory on the path. With it, the four sampled conditions on the three
central planes take about 9 s per case on the runner's CPU; the authors' live script uses a GPU.

## 6. Caveats

- One geometry (R1 = 10 m, R2 = 20 m), one shift profile, the authors' smoothing. The constant
  0.09 to 0.10 belongs to that construction; the proportionality to compactness is structural.
- The central plane of the authors' 5-cell cartoon grid, at 0.2 m. Finer grids were not run.
- The null check is a dense sampling, not an exact certificate; warpax's matrix inequalities in
  Part 2 are the exact version.
- Linearity of the warp metric in the shift was verified exactly (max difference 0) against a
  direct build, so forming all shifts from one unit-shift build introduces nothing.
