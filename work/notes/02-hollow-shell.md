# Note 02: the hollow shell on paper (Step 2)

18 October 2026. Script: `work/hollow-shell/tov_hollow.py` (NumPy, RK4 with 200,000 steps; the
exact identity (B.5) is reproduced to 1e-14, so the integration error is negligible). Units: G = c = 1,
lengths in metres. Statements marked **[mine]** are my reading, to be put to the authors.

## 1. The object

The paper's shell (Fuchs et al. 2024 §3-4): constant density between R1 = 10 m and R2 = 20 m, total
mass M = 4.49e27 kg, vacuum inside and outside. In geometric units M = 3.334 m, so the compactness
2GM/(R2 c^2) is 0.3334 and the shell density is 1.5e23 kg/m^3.

Everyone agrees on the first step: pick the density, assume isotropic pressure, integrate the TOV
equation. The question is what that step gives at the inner face, and what follows.

## 2. Three answers for the pressure at the inner face

| Route | P(R1) / rho c^2 | What it is |
|---|---|---|
| (1) TOV inward from P(R2) = 0, shell's own m(r), lapse matched to Schwarzschild at R2 | **+0.073** | What the paper's text, eq. (21), describes |
| (2) `TOVconstDensity.m`, the uniform solid-sphere closed form evaluated at R1 | **+0.095** | What WarpFactory's code actually computes (29% above route 1) |
| (3) Barzegar et al. (B.6): sqrt(1 - 2GM/R2) - 1 | **-0.184** | What the critique derives, imposing a(R1) = 0 as well as the match at R2 |

Routes (1) and (2) give compression at the inner face; route (3) gives tension. The sign matters:
the critique says (B.6) "not only violates the SEC ... but also contradicts their assumption of
positive pressure". With route (1) the pressure is positive and the strong energy condition is not
in question.

## 3. The elementary argument, which stands

A fluid face against vacuum must carry zero pressure, or something other than the fluid must hold
it. TOV makes nonnegative pressure fall outward, so integrating from P(R2) = 0 inward gives
P(R1) > 0: here +0.073 rho c^2. An isotropic hollow fluid shell with a free inner face therefore
cannot be static. This is the statement in warpax's documentation, and it is the statement the
paper itself concedes in §3.1 step 3 ("the isotropic pressure assumption is not valid for the R1
boundary to maintain a stable shell"). The paper's answer is hoop stress: an anisotropic shell.

## 4. Where (B.6) comes from, and why it does not describe the construction **[mine]**

The critique's (B.5), ln[rho/(rho + P(r))] = a(r) - a(R2), is exact for constant density and
isotropic pressure; the script confirms it to fourteen digits along route (1). To get (B.6) one
must set a(R1) = 0, their (B.3), "to match the Minkowski metric at r = R1".

But the lapse of a static spacetime can be normalised once. Their (B.2) normalises it at infinity,
through the Schwarzschild match at R2, and then the cavity's lapse is whatever the shell makes it:
a(R1) = -0.273, a clock rate of 0.761 relative to infinity. The cavity is still flat, since a
constant lapse over a flat spatial metric is Minkowski in rescaled time; the junction condition
asks for continuity of the induced metric, which a constant interior lapse equal to e^{a(R1)}
satisfies. Imposing a(R1) = 0 as well over-determines the problem: with route (1)'s pressure,
(B.5) at R1 would demand a(R2) = -0.071, while the Schwarzschild match fixes a(R2) = -0.203. The
two agree only for M = 0.

WarpFactory's `alphaNumericSolver.m` matches the lapse at the outer edge of its radial sample and
lets the cavity fall where it falls. It never imposes a(R1) = 0. So (B.6) describes neither the
paper's text nor its code. The critique's broader point in Error 18, that the final object is
defined by reading matter off a metric and carries no constitutive law, is a different argument
and is not touched by this.

## 5. The code against the text (claim C8)

The paper says the initial pressure comes from integrating eq. (21) with the shell's enclosed mass.
The code uses the closed-form pressure of a uniform solid sphere of radius R2 and mass M, masked to
the shell. At the inner face the two differ by a factor 1.29. Since the profile is then smoothed
four times and only serves as a starting point, this is a discrepancy between text and code, not
an error in what is finally analysed. It belongs in the report as a factual note.

## 6. What this settles and what it opens

Settled: the isotropic trial shell is not an equilibrium, by everyone's account including the
paper's; the critique's specific derivation of that fact uses a boundary condition the method does
not use and gets the sign of the inner pressure wrong; the code's pressure step is not the one
described.

Open, and now the whole project: the anisotropic shell that the smoothed profiles imply. Its
energy density and radial pressure are the smoothed inputs by construction; its tangential pressure
is fixed by the equilibrium identity P_t = P_r + (r/2)[dP_r/dr + (rho + P_r) da/dr]. Nobody has
published that profile, its peak relative to rho c^2, or how it scales with the smoothing width.
That is Step 4.

## 7. Questions this note raises for the authors

1. Barzegar, Buchert, Vigneron: is (B.3) a normalisation or a junction condition? With the lapse
   normalised at infinity the cavity lapse is 0.761; what remains of (B.6)?
2. Fuchs, Helmerich: `TOVconstDensity.m` is the solid-sphere closed form rather than an integration
   of eq. (21). Intended as an equivalent initial guess?
3. Le: the four-sentence argument in the warpax documentation is the sound form of the objection;
   may we quote it, and has the anisotropy of `FuchsMetric` been computed with `tov/residuals.py`?
