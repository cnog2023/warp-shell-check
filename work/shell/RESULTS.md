# Results: what matter the Fuchs shell requires (static shell, authors' own configuration)

18 October 2026. Data: CI run 39152018476 of `matlab/build_shell.m` (WarpFactory 03b10cb, MATLAB
R2026b, artifact in `ci-artifacts/`), the NumPy replica (`replicate_profiles.py`), the identity
(`hoop_stress.py`) and the smoothing sweep (`sweep_smoothing.py`). Configuration: the authors' live
script `W1_Warp_Shell.mlx`, unchanged: R1 = 10 m, R2 = 20 m, M = 4.4886e27 kg (2GM/R2c^2 = 1/3),
smoothFactor = 4000, grid 300 x 300 x 5 at 0.2 m. All pressures and densities are quoted as
fractions of the peak smoothed energy density rho0 c^2 = 1.3585e40 J/m^3 unless stated.

## 1. The 1D construction: MATLAB against the NumPy replica

Column by column, over all 100,000 radial samples and inside the shell alike:

| Column | max difference / max value |
|---|---|
| rho (unsmoothed) | 0 |
| rhosmooth | 4.0e-13 |
| P (unsmoothed) | 2.2e-15 |
| Psmooth | 3.5e-14 |
| M (from smoothed density) | 3.4e-13 |
| A = g00 | 1.2e-13 |
| B = grr | 1.3e-13 |

The replica reproduces the construction, including MATLAB's moving-average edge rule, to round-off.
The static and warp exports have byte-identical 1D profiles: the shift touches g01 only, as the
paper states.

## 2. The 1D identity against WarpFactory's 3D solver

On the y-axis through the centre (y radial, so P_yy is the radial pressure and P_xx = P_zz the
tangential one), two edge cells dropped at each end:

| Quantity | 1D identity | WarpFactory 3D |
|---|---|---|
| Peak rho c^2 [J/m^3] | 1.3585e40 | 1.3583e40 |
| Radial pressure, peak | +0.0767 at r = 12.06 m | +0.0767 at r = 12.10 m |
| Tangential pressure, peak | +0.1937 at r = 10.31 m | +0.1937 at r = 10.30 m |
| Tangential pressure, minimum | -0.0089 at r = 19.08 m | -0.0089 at r = 19.10 m |

Largest pointwise difference between the two routes, as a fraction of rho0 c^2: energy density
9.7e-5, radial pressure 2.9e-5, tangential pressure 4.1e-5. P_xx and P_zz agree to 1.4e-5. These
sit where the solver's error budget (`../precision-probe/RESULTS.md`) puts a fourth-order stencil at
0.2 m spacing on walls several metres wide. Figure: `hoop_stress.png`.

Edge note: the two outermost cells on each side of every line carry rho = 0.41 rho0 and
P_xx = -0.21 rho0 c^2 in what is vacuum. They are the stencil's edge-fill artefacts, the reason the
authors recommend excluding two cells, and they are excluded everywhere here. Taken at face value
they would be the largest "stresses" in the data set.

## 3. The measurement

What the smoothed construction demands of its material, at the authors' setting:

| | Fraction of rho0 c^2 | Where |
|---|---|---|
| Radial pressure, peak | +0.077 | r = 12.1 m |
| Tangential pressure, peak (hoop compression) | +0.194 | r = 10.3 m, the inner wall |
| Tangential pressure, minimum (slight tension) | -0.009 | r = 19.1 m, the outer wall |
| Largest tangential pressure relative to the local energy density | 0.385 | r = 9.6 m, where rho is 0.5 rho0 |
| Cavity clock rate relative to infinity | 0.7617 | |
| Mass of the smoothed shell relative to M | 1.0188 | smoothing moves density outward |

In SI the hoop compression peaks at 2.6e39 Pa. The dominant energy condition, every pressure below
the local energy density, holds with a factor of 2.6 to spare; the paper's statement that "these
pressures are all lower in magnitude than the value of the energy density" is true in this
configuration, and this is its margin.

The warp modification (shift 0.02) changes, along the same lines, the energy density by at most
1.9e-3, the pressures by at most 1.5e-2, and adds a momentum density along the direction of motion
of up to 0.30 rho0 c^2 on the y-axis and 0.10 on the x-axis, the circulation the paper describes.
Its energy conditions over all observers are not yet evaluated here (CLAIMS C4, C5).

## 4. The free parameter: smoothing width

Everything above depends on the one knob the construction has. Rebuilding with the validated replica
for other `smoothFactor` values, holding R1, R2 and M fixed:

| smoothFactor | inner-wall width, 10-90% [m] | P_r peak | P_t peak | r of P_t peak [m] | P_t min | max P_t / rho(r) | mass / M |
|---|---|---|---|---|---|---|---|
| 250 | 0.34 | 0.093 | 2.53 | 10.00 | -0.017 | 5.70 | 1.0000 |
| 500 | 0.68 | 0.092 | 1.28 | 10.01 | -0.016 | 2.86 | 1.0003 |
| 1000 | 1.37 | 0.089 | 0.66 | 10.02 | -0.014 | 1.44 | 1.0011 |
| 2000 | 2.74 | 0.085 | 0.35 | 10.08 | -0.012 | 0.74 | 1.0047 |
| 3000 | 4.11 | 0.080 | 0.24 | 10.18 | -0.010 | 0.50 | 1.0106 |
| **4000** | **5.36** | **0.077** | **0.19** | **10.31** | **-0.009** | **0.39** | **1.0188** |
| 6000 | 7.11 | 0.077 | 0.16 | 10.62 | -0.008 | 0.27 | 1.0424 |
| 8000 | 8.51 | 0.080 | 0.15 | 10.89 | -0.010 | 0.21 | 1.0752 |
| 12000 | 9.05 | 0.086 | 0.14 | 11.11 | -0.014 | 0.17 | 1.1658 |
| 16000 | 9.28 | 0.091 | 0.13 | 11.07 | -0.013 | 0.16 | 1.2782 |

Reading: the hoop stress scales as the inverse of the wall width while the wall is thin, and the
dominant energy condition fails once the inner wall is sharper than about two metres. The smoothing
in the paper's step 5 is therefore not a numerical nicety; it is what buys the energy conditions,
and it does so by thickening the walls and adding mass. The authors' setting sits at a margin of
about 2.6 with 1.9 % extra mass.

## 5. What this does and does not say

- It confirms the paper's own description of the final matter (§3.2) and puts numbers on it: the
  shell is held up by a tangential compression of about a fifth of its peak energy density,
  concentrated in the inner wall.
- It does not show that any material can supply that. For scale, the ratio of strength to energy
  density is about 6e-10 for graphene and the pressure at the centre of a heavy neutron star is
  about 1e35 Pa, against 2.6e39 Pa here. Step 6 puts this properly, with Le's elastic-shell results.
- "Stable" in the paper means in equilibrium by construction; nothing here, or in the paper,
  addresses stability against perturbations.
- All of it is the static shell at one configuration, plus the warp shell's Eulerian components.
  The observer-robust energy conditions of the warp shell and the warpax-native comparison are the
  next computations.

## 6. The paper's remedy, made quantitative (compactness scan, `compactness_scan.py`)

The paper's answer to limited material strength is to make the shell large and less compact.
Holding the geometry and smoothing at the authors' values and scaling the mass down:

| 2GM/(R2 c^2) | M [kg] | rho0 [kg/m^3] | P_t peak / rho0 c^2 | max P_t / rho(r) | P_t peak [Pa] |
|---|---|---|---|---|---|
| 0.333 | 4.5e27 | 1.5e23 | 0.194 | 0.385 | 2.6e39 |
| 0.1 | 1.3e27 | 4.5e22 | 0.043 | 0.085 | 1.7e38 |
| 0.01 | 1.3e26 | 4.5e21 | 0.0039 | 0.0077 | 1.6e36 |
| 0.001 | 1.3e25 | 4.5e20 | 0.0004 | 0.0008 | 1.6e34 |
| 0.0001 | 1.3e24 | 4.5e19 | 0.00004 | 0.00008 | 1.6e32 |

In the weak-field limit the required strength-to-energy ratio settles at 0.76 times the
compactness. Reference ratios of strength to rho c^2: steel 7e-13, carbon fibre 4e-11, graphene
6e-10, diamond 4e-10. A graphene-strength shell therefore needs compactness below about 8e-10. At
the paper's 20 m radius that is still a mass of 1e19 kg at 3.7e14 kg/m^3 (corrected 27 Oct 2026:
"at nuclear density" here was loose; it is a thousandth of nuclear density); bringing the density
down to graphene's own requires an Earth-sized, Earth-mass shell. The same shell scaled to R2 = 0.5 m
at the same compactness has 2.7e17 kg at 5.9e17 kg/m^3, nuclear density, with the same ratios. What the warp shift can be at
such compactness is the next question (the paper's "mass-to-velocity ratio"), not yet computed.
