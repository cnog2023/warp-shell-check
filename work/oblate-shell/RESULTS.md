# Results: does a flattened shell carry more shift?

27 October 2026. Script `oblate_shell.py` (commands in `README.md`); logs and csv files in `run/`,
`run-static2/`, `run-static/`. Margins are fractions of rho0 = 1.3585e40 J/m^3, the peak smoothed
energy density of the static spherical shell (`work/matrix/RESULTS.md`); the numerical noise floor is
about 1e-6 and a margin counts as a violation below 1e-4, as in Part 1. Two edge cells are dropped.
C = 1/3 is the compactness of the spherical shell the profiles come from.

## 1. The question, and what could be tested

Bobrick and Martire 2021 §4.2 flatten the Alcubierre bubble along its direction of motion by a factor
alpha_X and find its negative energy divided by alpha_X, and in §5.3 write that this "conclusion
likely holds for the, more physical, purely positive energy subluminal warp drives as well"
(`sources/papers-text/2021_bobrick_martire_introducing_physical_warp_drives_2102.06824.txt` l. 176,
230; register row C11). For the Fuchs shell the quantity that matters is not the mass of a given
geometry but the shift it can carry, 0.09 to 0.10 times its compactness (`work/matrix/RESULTS.md`
§1). So the question is: does a flattened shell carry more shift than the spherical one?

What can be built. The Alcubierre metric has one function, the shape function, so flattening it is
one substitution. The shell has a mass, and a mass has an exterior field: squashing the whole metric,
exterior included, makes the exterior non-vacuum (a squashed Schwarzschild metric is not a solution
of the vacuum equations), and the object stops being a shell in empty space. A genuinely oblate shell
with the quadrupolar vacuum exterior it would have is a boundary-value problem in Einstein's
equations that neither toolkit solves; Bobrick and Martire defer the same problem themselves ("we
leave generalizing the positive energy spherically symmetric warp drive solutions to the axisymmetric
case to future studies", l. 140). What can be built by reverse engineering, in the paper's own
sense of prescribing a metric and reading the matter off it, is a shell whose cavity and inner wall
are reshaped while the exterior stays exactly Schwarzschild: the spherical radius r in the lapse
A(r), the radial stretch B(r) and the shift profile S(r) is replaced by an ellipsoidal radius s,
with the surfaces s = const ellipsoids of axis ratio a(s) (semi-axis along the shift direction x
over the semi-axis across it) equal to alpha inside s = 10 m and rising smoothly to 1 at s = 20 m,
and the radial direction replaced by the normal to those surfaces. The mass is then fixed by the
exterior (Birkhoff) and does not change; only the shape of the hole and of the wall around it does.
A second family, with the transition moved out into the outer wall (16 to 26 m) so that the whole
wall is reshaped, was also built; it fails at zero shift (§2).

Two technicalities. (i) The axis ratio must be a function of the ellipsoidal radius s itself, found
by solving s^2 = (x/a(s))^2 + y^2 + z^2 per point (bisection; the function is monotonic for any
flattening, §`squash` in the script). The first attempt took a(r), a function of the spherical
radius; then s stalls and, for strong flattening, folds along the squash axis, and the metric has
caustics: alpha = 0.7 gave an energy density of -220 rho0 and alpha = 0.5 of -2100 rho0 on the
x-axis in the squash transition (`run-static/log.txt`). Those numbers describe the fold, not a
shell, and are kept only as a record of the trap. (ii) The spherical case of the NumPy assembly was
compared with WarpFactory's own CI export on the same grid (`--validate`): metric components agree
to 2e-13, the Eulerian stress-energy to 3e-11 of rho0, and the Part 1 checks reproduce (null minimum
-2.411e-7, Type I fraction 1, momentum density 0.3031 rho0 at the paper's shift; at the first failing
shift 0.0333: null minimum -0.0968, Type I fraction 0.99207, momentum 0.505, exactly Part 1's
numbers in `work/matrix/run-fine/analysis_cases.csv`).

## 2. Which reshaped shells satisfy the energy conditions at all (zero shift)

| Axis ratio | Transition | Energy density, min | Null, 4000 directions, min | Dominant margin at Type I points, min | Trace margin, min; where; rest-frame rho and pressures there | Verdict |
|---|---|---|---|---|---|---|
| 0.50 | 10-20 m | -6.7e-6 | -6.6e-6 | **-0.905** at (-4.9, -0.1) | -2.23 at (-4.9, -0.7); rho 0.34, p 0.085 to 1.24 | fails: pressure above energy density in the polar inner wall |
| 0.70 | 10-20 m | -1.8e-6 | -1.8e-6 | **-0.184** at (-6.9, -0.1) | -0.83 at (6.9, -0.7); rho 0.39, p 0.073 to 0.57 | fails, same place |
| 0.80 | 10-20 m | -1.1e-6 | -1.1e-6 | -2.0e-6 | -0.44 at (7.9, -0.1); rho 0.42, p 0.063 to 0.40 | passes, dominant margin 0.02 at the polar inner wall |
| 0.85 | 10-20 m | +8.2e-7 | -2.4e-7 | -2.4e-7 | -0.29 at (-8.5, -0.1); rho 0.45, p 0.063 to 0.34 | passes |
| 0.92 | 10-20 m | +8.2e-7 | -2.4e-7 | -2.4e-7 | -0.11 at (9.1, -0.1); rho 0.46, p 0.051 to 0.26 | passes |
| 1.00 (the paper) | - | +8.2e-7 | -2.4e-7 | -2.4e-7 | +3.3e-7 | passes (Part 1) |
| 1.15 | 10-20 m | +8.2e-7 | -2.4e-7 | -2.4e-7 | -1.06 at (16.1, -0.1); rho 1.03, p 0.20 to 0.95 | passes, pressure at 0.92 of the energy density in the polar inner wall |
| 1.25 | 10-20 m | +8.2e-7 | **-1.69** at (17.7, 0.1) | **-3.25** at (16.9, -0.1) | -7.9; rho 0.96, p 0.47 to 4.2 | fails everything |
| 0.85 | 16-26 m | **-0.094** | -0.100 at (-0.9, -22.9) | -0.35 at (-0.1, 22.1) | -0.36 | fails: negative energy density in the equatorial outer wall |
| 0.70 | 16-26 m | **-0.39** | -0.42 at (-0.1, -21.5) | -1.17 | -1.14 | fails, same place |

Coordinates are (x, y) in metres on the central plane, x along the shift. The mass from the plane
integral of the Eulerian energy density is 4.5731e27 kg, the smoothed mass of the spherical shell,
for every reshaping, as the fixed exterior requires.

Two readings. The pointwise energy conditions allow the cavity to be reshaped by about 15 to 20 %
either way at this compactness; beyond that the polar inner wall (the part of the wall the squash
moves) has to carry pressure above its energy density. And every reshaped shell, however mild, fails
the trace condition rho > P_r + 2 P_t at that polar wall, so none of them is realisable by the swarm
of `work/notes/06` (which needs the trace condition everywhere); reshaping is available only to a
material that can hold pressures of 0.75 to 0.9 of its energy density.

## 3. The shift ceiling against the axis ratio

Shifts scanned at each ratio; "fails" is the first shift at which the null condition is violated
beyond the noise band or a point loses its rest frame (Type I fraction below 1), which happen together,
as in Part 1. Figure: `ceiling_vs_ratio.png`.

| Axis ratio | Last passing shift (in units of C) | First failing shift (in units of C) | Null minimum and Type I fraction at the first failure | Where it fails first (x, y) | Momentum density at the last pass [rho0] |
|---|---|---|---|---|---|
| 0.80 | 0.0300 (0.090) | 0.0333 (0.100) | -0.018, 0.99847 | (-0.1, -17.7): outer part of the equatorial wall | 0.447 |
| 0.85 | 0.0333 (0.100) | 0.0350 (0.105) | -0.015, 0.99854 | (0.1, 17.7): outer part of the equatorial wall | 0.499 |
| 0.92 | 0.0300 (0.090) | 0.0333 (0.100) | -0.013, 0.99896 | (0.1, -12.3): equatorial inner wall | 0.452 |
| 1.00 (the paper) | 0.0300 (0.090) | 0.0317 (0.095) | -0.043, 0.99659 | (0.1, -12.3): equatorial inner wall | 0.455 |
| 1.15 | 0.0267 (0.080) | 0.0300 (0.090) | -0.102, 0.98508 | (-0.1, 12.3): equatorial inner wall | 0.407 |

The shifts 0.0317 and 0.035 refine Part 1's brackets, which were in steps of 0.01 C: the sphere's
ceiling lies between 0.0300 and 0.0317 (0.090 to 0.095 C); the 15 % flattened cavity carries 0.0333
and fails at 0.0350 (0.100 to 0.105 C). The momentum density the shift adds is the same for every
ratio (0.150 rho0 per 0.01 of shift, within 1 %); what moves is the energy density against which it
is measured at the critical site, the inner wall at right angles to the motion: at the shift 0.0333
the largest ratio of momentum density to local energy density is 0.581 for the sphere, 0.530 at
ratio 0.92, 0.491 at 0.85 (which therefore passes), 0.518 at 0.80 and 0.672 at 1.15. Below 0.85 a
second site, the outer part of the same equatorial wall at |y| = 17.7 m, takes over and fails
first, so the gain peaks: flattening by 15 % buys about one step, flattening by 20 % buys nothing,
and elongating by 15 % loses one step.

warpax's exact margins (S-lemma, every observer; route A of `work/matrix/exact_conditions.py`) at the
pass/fail pairs agree with the sampled reading: sphere at 0.0300, dominant margin -2.2e-7 and null
deficit -2.4e-7 (noise; passes); sphere at 0.0333, dominant -0.048, null deficit -0.0968 (fails; the
dense check gives -0.0968); ratio 0.85 at 0.0333, dominant -2.2e-7, null deficit -2.4e-7 (passes);
ratio 0.85 at 0.0367, dominant -0.026, null deficit -0.0521 (fails; the dense check gives -0.0518).
Two implementations, one verdict at each bracket (`run/log_exact.txt`, `run/exact_alpha_*.csv`).

## 4. What it means [ours]

- At fixed mass, flattening the cavity along the direction of motion raises the shift ceiling by
  about 10 % at best (from 0.090-0.095 C to 0.100-0.105 C at an axis ratio of 0.85), and elongating
  it lowers the ceiling by the same amount. The energy conditions cap the reshaping at about 15 to
  20 % either way at this compactness, and any reshaping takes the shell out of reach of the swarm
  model. Nothing here resembles Bobrick and Martire's factor 1/alpha for the Alcubierre bubble, whose
  energy is a volume integral of a wall-local density that flattening simply shrinks; the shell's
  mass is fixed by its exterior field, and its ceiling by a wall-local ratio that the reshaping
  changes only through the curvature coupling, by about 15 % at the critical site.
- Whether a shell flattened as a whole, with a quadrupolar vacuum exterior, could carry less mass for
  the same shift is not answered here and cannot be with these tools; the only version that can be
  built by reverse engineering, the transition in the outer wall, fails the energy conditions at
  zero shift because the thin outer wall cannot absorb the stresses the reshaping demands.
- For the report: the conjecture in Bobrick and Martire §5.3 is not borne out for the one
  positive-energy warp shell that exists numerically, within the reshapings available to it; the
  ceiling 0.09-0.10 C of Part 1 is robust to ±15 % reshaping of the cavity within ±one step.

## 5. Caveats

- One construction, the paper's grid (0.2 m, central plane) and smoothing; the transition function
  of the axis ratio (quintic step from 10 to 20 m) is a choice; other choices move the numbers in
  §2 and §3 by amounts not explored.
- The verdicts are pointwise energy conditions, as everywhere in this project; the reshaped shells
  are not fluid solutions and no claim is made that a material could realise their stress state
  beyond what the dominant and trace margins say.
- The ceiling brackets are one grid step of shift wide (0.0017 to 0.0033); the gain at 0.85 is one
  to two such steps.
