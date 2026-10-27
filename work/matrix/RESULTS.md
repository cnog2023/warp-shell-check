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

A second, smaller point for claim C4, **corrected 27 October 2026 (section 7.3)**: the replica
columns above are at WarpFactory's own normalisation, k = (1, n)/sqrt 2, which is half the
contraction the dense column reports, so -0.045 reads -0.090 on the dense column's scale and the
sampling shortfall at beta / C = 0.10 is 7 %, not a factor two. 100 directions find the threshold
where 4000 do and, at the paper's compactness, 93 % of the depth; the shortfall is large only where
the violation is shallow (section 7.3).

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

## 7. Part 2: the second toolkit on the same points (27 October 2026)

Same slices as sections 1 to 5 (runs 40411091447 and 40406621961), now read by warpax 1.5.1 (An T.
Le; `repos/warpax` at cb68eee, installed in `.venv`). Script `exact_conditions.py`, illustration
`exact_maps.py`; per-case data in `run-fine/exact_cases.csv`, `exact_miss.csv`, `exact_brackets.csv`
and the same three files in `run-coarse/`; figures `exact_fine.png` and `exact_maps.png`. Margins are
fractions of rho0 as above; a cell violates a condition when its margin is below -1e-4 rho0, Part 1's
threshold; the two edge cells per side are dropped; "active" cells are those with |T| > 1e-6 rho0,
57,292 to 57,476 per slice.

**What warpax adds.** WarpFactory tests a condition at a cell against a sample of observers, 100
directions at 10 speeds. warpax's `certify_point_lmi` decides it for every observer at once: with the
stress-energy in an orthonormal Eulerian tetrad, the null, weak and strong conditions are each
equivalent to the 4 x 4 matrix T_hat + sigma eta being positive semidefinite for some multiplier
sigma, and the dominant condition to two such tests (Le 2026, arXiv 2602.18023, Theorem 1, by the
S-lemma; `repos/warpax/src/warpax/energy_conditions/slemma.py`). The margin it returns is the best
smallest eigenvalue over sigma: positive, satisfied by all observers; negative, some observer sees a
violation. For the null condition twice the margin is the exact minimum of T(k,k) over null k = n + s,
|s| = 1 (`null_deficit`), the quantity Part 1 sampled over 4000 directions. "Exact" refers to the
observer problem only: the stress-energy is still WarpFactory's finite-difference result on its
0.2 m cartoon grid, with its noise of about 1e-7 rho0.

**Two routes into warpax, one answer.** Route A hands warpax the exported Eulerian frame tensor,
lowered (T_hat = eta T eta), with the Minkowski metric. Route B rebuilds the coordinate components
through WarpFactory's own transformation matrix (`Analyzer/utils/getEulerianTransformationMatrix.m`,
ported; its defining identity M^T g M = eta holds to 6.7e-16 on every slice) and hands warpax T_ab
and g_ab, so warpax constructs its own tetrad. The null, weak and strong margins agree to 3.8e-15
rho0 over the fine run and 7.1e-14 rho0 over the coarse one, whose margins reach 80 rho0; the
dominant margin agrees in sign at every point and differs in magnitude by up to 0.22 rho0 in the
coarse run, because warpax divides its flux margin by the largest frame component, which depends on
the spatial triad (its docstring: "not an invariant severity"). warpax's Hawking-Ellis
classification agrees with Part 1's NumPy eigen-reading at every cell of every case. Cost: 37 to 75 s
per case alone on a 16-thread laptop CPU, four matrix inequalities per cell.

### 7.1 Claim C5: the paper's shift passes every condition for every observer

| Case (C = 1/3) | NEC | WEC | SEC | DEC | Null deficit | Cells below warpax's floor | Cells below 1e-6 rho0 |
|---|---|---|---|---|---|---|---|
| Static shell, beta = 0 | -1.21e-7 | -1.21e-7 | -1.21e-7 | -2.16e-7 | -2.42e-7 | 812 | 0 |
| The paper's shift, beta = 0.02 | -1.21e-7 | -1.21e-7 | -1.21e-7 | -2.16e-7 | -2.42e-7 | 812 | 0 |
| Last passing shift, beta = 0.030 | -1.21e-7 | -1.21e-7 | -1.21e-7 | -2.16e-7 | -2.42e-7 | 812 | 0 |

The minima are the same numbers at every passing shift because the worst cell sits at r = 27.2 m,
outside the shell, where the stress-energy is pure stencil noise and the shift changes nothing.
warpax's own decision floor is 1e-12 of the tensor scale; the 748 to 812 cells per slice below it
are between 1e-12 and 1e-6 rho0, are there at beta = 0, and are WarpFactory's finite-difference noise.
The same holds at the other three compactnesses (minima -1.07e-7 to -1.10e-7 rho0). C5 is closed from
both sides: 0.02 satisfies all four conditions for every observer.

### 7.2 The exact threshold, next to Part 1's

| Compactness | Exact, each of the four conditions: passes / fails | In units of C | Part 1, sampled dominant | Part 1, null 4000 directions |
|---|---|---|---|---|
| 1/3 | 0.0300 / 0.0333 | 0.09 / 0.10 | 0.0300 / 0.0333 | 0.0300 / 0.0333 |
| 1/10 | 0.0090 / 0.0100 | 0.09 / 0.10 | 0.0090 / 0.0100 | 0.0090 / 0.0100 |
| 1/30 | 0.0030 / 0.0033 | 0.09 / 0.10 | 0.0030 / 0.0033 | 0.0030 / 0.0033 |
| 1/100 | 0.0009 / 0.0010 | 0.09 / 0.10 | 0.0009 / 0.0010 | 0.0009 / 0.0010 |

The bracket is unchanged at thresholds of 1e-5 and 1e-3 rho0 (`exact_brackets.csv`). The four
conditions fail at the same shift and, up to 0.12 C, with the same margin at the same cell: r = 12.3 m,
the inner wall at right angles to the shift direction, where the momentum density peaks at 0.50 rho0
(`exact_maps.png`); from 0.15 C the dominant margin drops below the others as its flux half takes
over. Every violating cell is Type IV in warpax's census (a complex eigenvalue pair, no rest frame):
at 0.10 C the Type IV counts are the violating counts, 456, 156, 96 and 76 cells; there are no Type II
or III cells anywhere, and no Type I cell violates, the algebraic Type I margins never falling below
-2.4e-7 rho0. The exact DEC minimum at 0.10 C is -0.0485, -0.0139, -0.0074 and -0.0054 rho0 for
C = 1/3, 1/10, 1/30 and 1/100: the violation at the first failing shift is shallower as the
compactness falls, so the threshold sits closer to 0.10 C there; at 0.12 C the minima are -0.158,
-0.106, -0.097 and -0.094.

### 7.3 Claim C4: what the sampled check misses

The sampled Dominant map is WarpFactory's as exported (100 null directions; it tests the flux half
of the condition only). The sampled Null and Weak maps lower indices with the coordinate metric
(section 4), so they are re-evaluated here with the same observer set and the Minkowski metric. The
Null maps are doubled to the dense check's normalisation, k = (1, n).

| C | beta / C | Exact DEC violations, cells | Missed by the sampled Dominant map | Missed by 100 null directions, consistent metric | Missed by 4000 directions | Depth seen by 100 directions / exact |
|---|---|---|---|---|---|---|
| 1/3 | 0.10 | 456 | 4.8 % | 8.8 % | 0 | 93 % |
| 1/3 | 0.12 | 1440 | 3.5 % | 6.7 % | 0.3 % | 97 % |
| 1/3 | 0.15 | 4032 | 1.2 % | 3.1 % | 0.1 % | 98 % |
| 1/10 | 0.10 | 156 | 20.5 % | 32.1 % | 0 | 78 % |
| 1/10 | 0.12 | 1196 | 3.8 % | 7.7 % | 0 | 97 % |
| 1/10 | 0.15 | 3760 | 1.2 % | 2.4 % | 0.05 % | 98 % |
| 1/30 | 0.10 | 96 | 27.1 % | 68.8 % | 0 | 59 % |
| 1/30 | 0.12 | 1196 | 5.2 % | 12.0 % | 0 | 96 % |
| 1/30 | 0.15 | 3776 | 1.7 % | 3.1 % | 0.2 % | 98 % |
| 1/100 | 0.10 | 76 | 65.8 % | 76.3 % | 0 | 44 % |
| 1/100 | 0.12 | 1188 | 5.4 % | 12.2 % | 0.5 % | 96 % |
| 1/100 | 0.15 | 3760 | 1.4 % | 3.1 % | 0.05 % | 98 % |

Pooled over the 12 violating cases of the fine run: 21,132 exact DEC violations, 564 missed by the
sampled Dominant map (2.7 %); 21,144 exact NEC violations, 1,144 missed by 100 consistent null
directions (5.4 %). Pooled over the 18 violating cases of the coarse run, shifts up to 16 C and
margins down to -80 rho0: 327,280 and 436 missed (0.13 %); 327,168 and 1,020 (0.31 %).

Reading. The sampled check never misses a failing case (section 7.2); it misses cells on the rim of
a violating region, where the margin is shallow, and the rim is most of the region at the first
failing shift. Adding the consistent Weak map to the Dominant flag recovers nothing: the weak half of
the dominant condition never fails where the flux half holds. The three consistent sampled maps,
Null, Weak and Strong, flag the same cells, because the minimum over WarpFactory's timelike set is
attained on its null members (speed index zero). The exported Null and Weak maps (claim C9) are not
usable for this count: at the first failing shift 88 % of the cells the Null map flags at C = 1/3 are
not violations, and at 0.09 C it flags cells where the exact check finds none.

**Correction to Part 1.** Section 4, note 07 and register row C4 said that 100 directions
underestimate a violation's depth "by about a factor two" (-0.045 against -0.097 at beta / C = 0.10).
The replica values were at WarpFactory's normalisation k = (1, n)/sqrt 2, half the contraction; on
the dense check's scale they read -0.090 against -0.097: 7 %. The real shortfall at the first
failing shift is 7 % at C = 1/3, 22 % at 1/10, 41 % at 1/30 and 56 % at 1/100, where the violation
is shallowest, and at most 4 % from 0.12 C on. 4000 directions are within 0.05 to 0.4 % of the exact
depth everywhere. The sampled check is adequate for the pass-or-fail verdict on a case at this
resolution and not for counting cells or sizing violations near the threshold, the same order of
shortfall Le reports for a Rodal case (93.4 % detection at 1000 directions, his section 3.4).

### 7.4 Caveats

- The exactness is in the observer problem. The inputs are WarpFactory's finite differences on the
  authors' cartoon grid, central plane, 0.2 m; a finer grid or a 3D export would change the noise
  floor and the cell counts, not the method.
- The miss fractions depend on the 1e-4 rho0 threshold through the shallow rim cells; the brackets do
  not (section 7.2).
- warpax's dominant margin is tetrad-dependent in magnitude; only its sign is used here.
- warpax's native `FuchsMetric` (Le's own regularisation of the construction) was not run; it is a
  second, separate object, not a substitute for the slices.
