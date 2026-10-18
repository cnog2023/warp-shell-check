# Note 01: close reading (Step 1)

18 October 2026. Quotes are copied from the text extractions in `sources/papers-text/`; locations
give section numbers and, where useful, character offsets into those files. Every statement marked
**[mine]** is my reading, not the source's.

## 1. Fuchs et al. 2024, the paper under test (`2024_fuchs_constant_velocity_physical_warp_drive_2405.02709.txt`)

Licence CC BY 4.0. Dated "August 2023" in the body; arXiv v1 4 May 2024.

**Abstract.** "we present a solution for a constant-velocity subluminal warp drive that satisfies
all of the energy conditions. The solution involves combining a stable matter shell with a shift
vector distribution that closely matches well-known warp drive solutions such as the Alcubierre
metric. We generate the spacetime metric numerically, evaluate the energy conditions, and confirm
that the shift vector distribution cannot be reduced to a coordinate transformation."

**§1.3, the "rule of thumb".** "As a rule of thumb, the Eulerian momentum flux and pressures should
be less than the energy density to satisfy the energy conditions [11]." Their three "key
ingredients": positive ADM mass; "much larger positive energy density than both pressure and
momentum flux in the non-vacuum warp bubble, as measured by Eulerian observers"; subluminal speeds.

**§2.1.** "we utilize a moving matter shell as the foundation metric ... This solution features a
flat interior with an asymptotically-flat Schwarzchild solution outside the shell. The shell
solution will be constructed in comoving coordinates in which the metric tensor does not depend on
time." The warp modification is "adding shift vector to the shell metric", eq. (6)-(7), g_01 only.

**§2.2.** Energy conditions sampled "with a spatial orientation density of 100 samples and for
timelike observers and an additional velocity magnitude density of 10 samples".

**§3.1, the construction.** Metric (16): ds^2 = -e^{2a} dt^2 + e^{2b} dr^2 + dOmega^2 (sic: the r^2
is missing in the printed form; Barzegar Error 33(iv) remarks it "is not spherically symmetric").
Then, decisive for our question:

> "However, for a stable shell the pressures P can not be assumed as isotropic since the interior
> radius must withstand the gravity inward pressure, resulting in non-uniform pressure terms along
> the theta and phi directions, akin to hoop stress in a cylinder. With non-isotropic pressure, the
> solution takes the form: T = diag(rho, P1, P2, P3). To solve for the non-isotropic shell solution,
> we will take an iterative approach to find a and b as modifications from the isotropic solution
> by changing the assumed pressure and density used to determine a and b in the isotropic case."

The five steps: (1) constant density rho' between R1 and R2; (2) "Solve for the initial guess
pressure profile P'(r) by assuming the pressure in the shell is isotropic and zero at r = R2 using
the Tolman-Oppenheimer-Volkoff (TOV) equation. After solving the differential equation with the
single boundary condition at r = R2, we are left with a constant pressure inside, this pressure is
set to zero for r < R1 to enforce a vacuum interior."; (3) "the isotropic pressure assumption is
not valid for the R1 boundary to maintain a stable shell. To address this issue, we soften the
boundary using radial smoothing applied to rho' and P'"; (4) "The smoothed rho~ and P~ are then
used to solve for the terms of a and b which build the actual metric. Solving the stress-energy
tensor using the Einstein field equations then provides the true rho and P_i that correspond to
the metric obtained in this step."; (5) "the smoothing function for pressure and density is
iterated upon ... until we find a metric that satisfies the energy conditions at the boundaries".
Eq. (21) writes the TOV equation with the shell's own m'(r).

**[mine]** So the paper does not claim the final shell is an isotropic fluid. The isotropic TOV
profile is an initial guess; the final matter is "the true rho and P_i" read off the metric, and
the paper expects hoop stress. The smoothing width is what keeps that hoop stress finite.

**§3.2, what the derived matter looks like.** "Along each of the principal coordinate directions,
the input pressure P~ used to solve for a from Eq. (25) is equal to the calculated stress-energy
pressure P along that direction since it is aligned with the radial direction. The pressures along
the x- and z- directions are equal and differ from the y-pressure, with a large spike on the inner
bound of the shell. The choice to smooth the pressure and density is made purposely to find a
solution with non-isotropic pressures ... For a static shell, the inner boundary at R1 requires a
difference in pressure between the radial pressures and the angular pressure to ensure the shell
is stable from gravitational collapse. This manifests as a kind of hoop stress around the inner
radius of the shell. It is also important that these pressures are all lower in magnitude than the
value of the energy density at that point to ensure that the shell is physical. For realistic
materials that may have a limited range of pressures possible, this requirement can always be
satisfied by making the shell large and modifying the density profile". And: "No energy condition
violations exist beyond the numerical precision limits that exist at 10^34 in this setup".

**[mine]** Three testable statements in one paragraph: derived radial pressure equals the input;
tangential pressure spikes at the inner wall; every pressure stays below the energy density. The
last is the dominant energy condition in words. "Stable from gravitational collapse" is equilibrium
by construction; no perturbative stability analysis appears anywhere in the paper.

**§4.1, the warp modification.** g_01^warp = g_01 - S_warp(r)(g_01 + beta_warp), eq. (26); S_warp
a compact sigmoid (27)-(28) with buffer R_b; "the addition of shift inside the shell is possible
for beta_warp = 0.02 without any energy condition violation" with footnote 9 "This is likely not
an upper limit". Constraint 1: "The interior region should remain flat, meaning all spatial
derivatives of the metric are zero" (Barzegar Error 33(vi) objects to this definition of flatness).

**§4.2.** "The energy density remains mostly unchanged compared to that of a standard moving shell,
but the modification of the shift vector causes a difference in the momentum and pressure values
for Eulerean observers ... both positive and negative momentum density around r ~ (R2 - R1)/2 ...
indicative of a circulation pattern".

**§5.1, the invariance test.** Light rays through the centre, forward and back: "the Warp Shell
(from Section 4) has delta t ~ 7.6 ns and the Matter Shell (from Section 3) has delta t = 0 ns ...
This experiment demonstrates a Lense-Thirring effect exists for warp drives with shift vectors,
creating a linear frame dragging ... Since the photon travel time is a measurable quantity, the
shift-vector modification of the shell metric cannot be reduced to a coordinate transformation."
Footnote 10: "Reference warp metrics are converted to a comoving frame using a Galilean
transformation to their coordinates."

**§6.** "the first constant velocity subluminal physical warp drive solution to date ... constructed
from a stable shell of matter with a modified shift vector on its interior". Future work: "a direct
1D optimization of the radial profiles for density, pressure, and shift vector, possibly reducing
required mass by orders of magnitude"; acceleration "a major direction of work".

**Appendix A.** Four error sources; "the double precision limit still restricts meaningful results
for the stress-energy tensor and energy condition violation to those of above 10^34 in magnitude".

## 2. What the code does (`repos/WarpFactory/Metrics/`)

- `WarpShell/metricGet_WarpShellComoving.m`: density array `rho = m/(4/3 pi (R2^3-R1^3))` masked
  to R1 < r < R2; `P = TOVconstDensity(R2, M, rho, rsample)`; then `rho = smooth(smooth(smooth(
  smooth(rho, 1.79*smoothFactor)...)))` and the same four passes on P with `smoothFactor`; mass
  recomputed by `cumtrapz` of the smoothed density; `B = (1 - 2GM/r)^-1`; `a = alphaNumericSolver`;
  `A = -exp(2a)`; interpolated onto the Cartesian grid by `legendreRadialInterp` and `sph2cartDiag`;
  warp: `g12 = g12 - g12.*S - S*vWarp` with `S` from `compactSigmoid(rsample, R1, R2, sigma, Rbuff)`
  smoothed twice.
- `utils/TOVconstDensity.m` is one line: `P = c^2*rho.*((R*sqrt(R-2GM/c^2) - sqrt(R^3-2GM r^2/c^2))
  ./ (sqrt(R^3-2GM r^2/c^2) - 3R sqrt(R-2GM/c^2))).*(r<R)` with `M = M(end)`, `R = R2`. That is the
  interior Schwarzschild solution of a uniform solid sphere, masked by the shell's density array.
  **[mine]** It is not an integration of eq. (21) with the shell's m'(r); the enclosed mass it
  implies is the solid sphere's. Treated by the paper as an initial guess, so this is a
  documentation discrepancy rather than an error in the final object, but it should be recorded.
- `utils/alphaNumericSolver.m`: `dalpha = (GM/c^2 + 4 pi G r^3 P/c^4) ./ (r^2 - 2GM r/c^2)`,
  `dalpha(1) = 0`, cumulative trapezoid from r = 0 outward, then `offset = C - alphaTemp(end)` with
  `C = 1/2 log(1 - 2GM(end)/r(end)/c^2)`: the lapse is matched to Schwarzschild at the outer edge of
  the radial sample. Inside the cavity `M = 0` and `P = 0`, so `dalpha = 0` and the cavity lapse is
  a constant below zero. **Nothing imposes a(R1) = 0.**

## 3. Barzegar, Buchert, Vigneron 2026 (`2026_barzegar_buchert_vigneron_classification_demystification_2602.16495.txt`)

- **Error 12.** "Helmerich et al. [30, Sections 4.1 & 4.2] made another wrong statement that the
  Alcubierre and Van Den Broeck metrics can be transformed to time-independent metrics, i.e.,
  admitting global timelike Killing vector field, by transforming to what they call 'constant
  velocity comoving frame' via a 'Galilean transformation,' hence dropping some time-derivatives in
  the calculation (cf. Section IV.7 below). Fuchs et al. [29] make the same mistake around which
  they build their central concept."
- **Error 13.** The 3+1 geodesic discussion of Fuchs §1.2: "the whole conceptualization of a
  'constant velocity warp drive' by Fuchs et al. [29] has no meaning as long as no distinction is
  made between u_i and u^i ... the shift vector is a choice of coordinate system."
- **Error 18 and Appendix B.** "The construction proposed by Fuchs et al. [29] is not a solution to
  Einstein's equations; indeed, as we showed in Appendix B, the authors do not solve the
  Tolman-Oppenheimer-Volkoff (TOV) equations resulting from the Einstein equation in the given
  context. Hence, the algorithm in Fuchs et al. [29, Figure 3] for 'metric creation' is flawed."
  Appendix B: metric (B.1); density profile; "they assume that the pressure P is positive and
  isotropic, and vanishes for r < R1 and r = R2"; e^{-2b} = 1 - 2Gm(r)/r; junction conditions
  e^{2a(R2)} = 1 - 2GM/R2 (B.2) and "it should match the Minkowski metric at r = R1, i.e.,
  a(R1) = 0" (B.3); TOV in the form dP/dr = -(rho + P) da/dr (B.4), integrated to
  ln[rho/(rho + P(r))] = a(r) - a(R2) (B.5); hence P(R1)/rho = sqrt(1 - 2GM/R2) - 1 < 0 (B.6),
  "which not only violates the SEC (and possibly other energy conditions), but also contradicts
  their assumption of positive pressure".
  **[mine]** (B.3) and (B.2) together fix the lapse at two radii. The lapse can be normalised once;
  the standard choice is unity at infinity, which (B.2) encodes, and then the cavity's lapse is
  below unity, not unity. WarpFactory does exactly that. The paper's step 2 integrates from R2
  only, which is route (1) of `work/hollow-shell/tov_hollow.py`, and gives positive pressure at
  R1, not negative. The physically valid objection is the one warpax's documentation states: a
  free inner face needs P(R1) = 0, TOV gives P(R1) > 0, so an isotropic hollow fluid shell cannot
  be static. The paper concedes exactly this in step 3 and answers with anisotropy. So Error 18 as
  derived appears to attack an initial guess with a boundary condition the method does not use,
  while its broader point, that the final object has no matter model, stands. To be checked
  against the authors.
- **Error 20.** Helmerich, Fuchs, Abellán "do not perform a proper 3+1-numerics ... they suffer from
  an unclear IVF". Remark IV.27: they "rushed to plot some figures without an in-depth analysis".
- **Error 31.** The "rule of thumb" "is a well-known fact just explained above".
- **Error 33.** Six items, among them: "(iii) ... a vector (or covector) is set to be equal to a
  scalar field (e.g., u_i/u^0 = v_s ...)", "(iv) the metric given by Fuchs et al. [29, Equation
  (16)] is not spherically symmetric", "(v) mixing the orthonormal and coordinate bases by Fuchs et
  al. [29, Equation (10)]", "(vi) identifying the flatness with vanishing of spatial derivatives of
  the metric".
- **Error 35.** Clough et al. is "the only sound numerical GR work" in the field, faulted only for
  the "mind projection fallacy" in its detection suggestion.
- **Error 37.** Fuchs et al. "call a solution to the 3+1-form of the geodesic equation warp drive,
  without exactly saying in what way it differs from the motion of a particle observed from a given
  reference frame".
- **Theorem IV.31 (Natário 2002).** R-Warp models violate either the WEC or the SEC. IV.32-33:
  zero-expansion drives violate the WEC.
- **Abstract.** "most claims regarding physical warp drives must be reassessed, and it becomes
  highly challenging to justify or support the viability of such models, not merely due to the
  violation of energy conditions."

## 4. Helmerich et al. 2024 (`2024_helmerich_warpfactory_cqg_2404.03095.txt`)

- **§4.1.** "To analyze the metric, the commonly used Galilean transformation is applied: x' = x -
  v_s t, t' = t. This makes the metric time-independent and amounts to an addition of the shift
  vector: beta_x' = beta_x + v_s. The metric being in a comoving frame removes the necessity for
  time derivatives and reduces the computation required."
  **[mine]** For constant v_s this is an exact coordinate change in which the Alcubierre metric is
  stationary; for subluminal v_s the Killing vector is timelike everywhere. What Error 12 objects
  to beyond the word "Galilean" needs the authors' clarification; to be asked.
- **§6.** "Traditionally, the analysis of physicality in these metrics has been limited to
  considering the energy density observed by Eulerian observers. However, this approach alone is
  insufficient for a thorough evaluation of the energy conditions. To overcome these limitations
  ... Warp Factory employs a numerical framework."

## 5. Le 2026 (`2026_le_observer_robust_energy_conditions_warpax_2602.18023.txt`)

- §1: "Prior warp-drive tooling (WarpFactory [13]) samples ~10^3 observer directions per point".
- §3.4: at 10^3 directions per point the sampled check "detects 93.4% of the 15,624 points whose
  Type-I algebraic DEC slack is below -10^-10" in a Rodal case.
- Related work: "They also question the consistency of the Fuchs shell's assumed matter source
  with its metric. Our pointwise tests of G_ab/8 pi do not resolve that source-consistency
  question."
- Table 9 (standardised kinematics, v_s = 0.02, R_c = 15 m, width 4.42 m): Fuchs row Type I 100%,
  Type IV 0%, R_c^2 min(rho + p_i) = 0.021 (a) and 0.022 (b); WEC/NEC miss columns blank.
- Appendix D, "Fuchs constant-velocity shell": eqs (53)-(55); "density and pressure are then
  smoothed by four passes of a moving average with width ratio s_rho/s_P ~ 1.72"; "with the
  Schwarzschild boundary condition ... outside the solved grid, which we impose analytically rather
  than by extrapolating the numerical solution"; "We replace the published buffered clamps by the
  natural-endpoint extension".
- `repos/warpax/docs/how-to/reproduce_warpshell_paper.md`: "An isotropic static shell with
  nonnegative density and pressure, a regular empty cavity, and no surface stress cannot satisfy
  its inner vacuum boundary. Vacuum matching requires p(a)=0, while the TOV equation makes
  nonnegative pressure nonincreasing outward. A nontrivial shell under these assumptions is
  impossible. Tangential stress or an elastic constitutive law changes the problem."

## 6. What this changes about the plan

The gap between "trial fluid" and "derived matter" is not in dispute: the paper states it and even
describes its shape (radial pressure equals input; tangential pressure spikes at the inner wall).
What nobody has published is its size, its dependence on the smoothing width, and what it implies.
And the gap is almost entirely one-dimensional: with b from the smoothed mass and a from the
smoothed pressure, the derived energy density and radial pressure equal the inputs by
construction, and the only new quantity is the tangential pressure, fixed by the anisotropic TOV
identity P_t = P_r + (r/2)[dP_r/dr + (rho + P_r) da/dr]. That can be computed exactly from
WarpFactory's own 1D profiles (`Metric.params`), then confirmed in 3D by both toolkits. Step 4 of
`PLAN.md` is revised accordingly.

## 7. Questions for the authors (for Step 2 and the first contact)

1. To Barzegar et al.: is (B.3) intended as a normalisation or as a junction condition? With the
   lapse normalised at infinity, the cavity lapse is below unity; what then remains of (B.6)?
2. To Fuchs et al.: `TOVconstDensity.m` is the uniform solid-sphere closed form rather than an
   integration of eq. (21); intended as an equivalent initial guess?
3. To Fuchs et al.: what smoothing widths and grid produced Figs 6-10, and is the `W1_Warp_Shell`
   live script the exact configuration?
4. To Le: has the anisotropy of the Fuchs shell been computed with `tov/residuals.py` on his
   `FuchsMetric`, and would he want the comparison with WarpFactory's native profiles in warpax?
