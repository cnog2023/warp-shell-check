# What matter does the Fuchs et al. warp shell require? An independent, reproducible check

**Draft for comment, 27 October 2026.** Carlos Nogueira (Frankfurt) with Claude Code (Anthropic's
Fable model). Repository: github.com/cnog2023/warp-shell-check, MIT licence; wiki:
github.com/cnog2023/warp-shell-check/wiki. Every number in this report names the file it comes from,
and every claim tested is quoted and located in `CLAIMS.md` and `work/notes/01-reading.md`.

This draft goes to the authors of the paper, to the authors of the critique and to the author of
warpax before it is made public, with a two-week comment window. Replies are quoted verbatim only
with permission; an appendix will record them.

## Summary

In 2024 Fuchs, Helmerich, Bobrick, Sellers, Melcher and Martire published a warp-drive spacetime
they call physical: a shell of matter, R1 = 10 m to R2 = 20 m, M = 4.49e27 kg, with a shift of 0.02 c
inside it, satisfying all four pointwise energy conditions. In February 2026 Barzegar, Buchert and
Vigneron published a critique holding, among 37 points, that the construction "is not a solution to
Einstein's equations". Also in 2026 An T. Le released warpax, a toolkit with exact energy-condition
tests, and wrote that his tests "do not resolve" the question of what the shell's matter is.

We rebuilt the shell with the authors' own toolkit at the configuration of their published live
script, reproduced the construction step for step in NumPy to one part in 1e13, and measured what
nobody had published. The findings, each computed two ways:

| | Result | Where |
|---|---|---|
| The matter the construction requires | A tangential compression (hoop stress) peaking at **0.194 of the peak energy density** in the inner wall, 2.6e39 Pa, with the radial pressure at 0.077. The 1D identity and the 3D solver agree to 4e-5 | section 4.2 |
| The construction's one free parameter | The smoothing width. The hoop stress scales as its inverse; below a wall width of about 2 m the dominant energy condition fails. The paper's setting has a margin of 2.6 | section 4.2 |
| The paper's remedy, a larger and less compact shell, quantified | The strength-to-energy ratio required is **0.76 times the compactness**. Graphene's ratio, 6e-10, needs a compactness below 8e-10 | section 4.2 |
| How much shift the shell carries | **0.09 to 0.10 times the compactness**, at every compactness from 1/3 to 1/100, by WarpFactory's sampled check, a dense null check and warpax's exact check alike. The paper's 0.02 passes; the ceiling at its compactness is 0.030 to 0.033 | sections 4.4, 4.5 |
| Combined | A shell whose material sustains a strength-to-energy ratio s can carry a shift of about **0.13 s**: centimetres per second for graphene | section 4.4 |
| A matter model that needs no strength | A swarm of orbiting particles (Einstein's 1939 cluster) supports the same density with a third of the stress and none of it radial, at orbital speeds up to 0.46 c; it makes the physics consistent and the engineering no closer | section 4.3 |
| The critique's central derivation | Its Appendix B imposes a condition the construction never uses and gets the sign of the inner pressure wrong; its broader objection, that no constitutive law is named, stands | section 4.1 |
| The paper's own figures | Reproduced, same pictures; their amplitudes are 1 to 11 % above the published script's output because the figures were smoothed 12 % less, at the span ratio the paper states rather than the one the code carries | section 4.6 |
| Two defects in WarpFactory | Its energy-condition sampling demands a GPU as shipped; its Null and Weak maps lower indices with the wrong metric and fail about 1.5 times too early above the paper's point. The published figures are unaffected | section 4.7 |

In one sentence: the construction does what its authors say it does, the matter it requires is a
hoop stress of a fifth of its energy density that no material can supply by a factor of about a
billion, and the warp shift a real material could carry is a tenth of a compactness that would have
to be a billionth. Our judgements, where they go beyond the numbers, are labelled as such.

## 1. Who is writing, and how

Carlos Nogueira is a software engineer with no training in relativity; he gives the time, the
project planning and the compute budget, reads every result, and decides at every gate. Claude Code,
an AI model, did the reading, wrote and ran the code, and drafted this text. Neither has any
affiliation with Anthropic's research, with Applied Physics, with the critique's authors or with the
warpax project. It is a hobby, done carefully, and nothing here should be weighed by anything but
its reproducibility.

The rules we held ourselves to (`CLAUDE.md`, `PLAN.md`): a claim is quoted and located before it is
tested; every headline number is computed twice, by different means (WarpFactory and warpax, or an
analytic identity and a solver); every number names its source file; both sides of the dispute are
quoted the same way; and nothing is called finished before the people involved have seen it.

## 2. The question

The paper's construction (Fuchs et al. 2024, section 3.1) starts from a trial fluid: a constant
density between R1 and R2, an isotropic pressure from the TOV equation, both smoothed by a moving
average. The metric is built from the smoothed pair; Einstein's equations then "provide the true rho
and P_i that correspond to the metric obtained in this step". The paper says what to expect:
"non-uniform pressure terms along the theta and phi directions, akin to hoop stress in a cylinder",
and "a large spike on the inner bound of the shell" (section 3.2). It does not say how large.

The critique (Barzegar, Buchert and Vigneron 2026, Error 18 and Appendix B) holds that "the
construction proposed by Fuchs et al. is not a solution to Einstein's equations; ... the authors do
not solve the TOV equations", and derives in its equation (B.6) a negative pressure at the inner
face. Le (2026, section on related work) writes that "our pointwise tests of G/8 pi do not resolve
that source-consistency question".

So the question is: how far is the matter the metric actually requires from the trial fluid, where,
and what does the gap imply about the claim that the shell is made of ordinary, stable matter? It is
one measurement. It runs on a laptop, and the authors' toolkit is public.

## 3. Method

**The configuration.** The authors' live script `W1_Warp_Shell.mlx`, unchanged: R1 = 10 m,
R2 = 20 m, M = 4.4886e27 kg (compactness 2GM/(R2 c^2) = 1/3), smoothFactor 4000 (four passes of a
moving average over 4000 radial samples for the pressure and 7160 for the density), shift 0.02, a
300 x 300 x 5 grid at 0.2 m. The 5-cell depth is the authors' "cartoon" method: only the central
plane has a complete finite-difference stencil, and that is the plane we read. The two outermost
cells on every grid line are stencil artefacts in vacuum, the ones the authors say to drop, and are
dropped everywhere. rho0 is the peak smoothed energy density of the static shell, 1.3585e40 J/m^3;
pressures and margins are quoted as fractions of it unless stated.

**Three implementations.** (1) WarpFactory itself (MIT, MATLAB), run on GitHub's free MATLAB
runners for public repositories (`.github/workflows/matlab.yml`); its builds and exports are the
primary data. (2) A NumPy replica of the 1D construction (`work/shell/replicate_profiles.py`), which
reproduces every profile of the MATLAB export, including the smoothing's edge rule, to between 2e-15
and 4e-13 (`work/shell/RESULTS.md` section 1); it is what the parameter sweeps run on. (3) warpax
1.5.1 (Le; MIT, Python/JAX), whose S-lemma tests decide each energy condition for every observer at
once from a 4 x 4 matrix inequality, with no observer sample and no speed cap.

**The error budget.** Before measuring anything we ported WarpFactory's solver arithmetic to NumPy
and ran both on an Alcubierre bubble with a closed-form answer: MATLAB on the runner and the port
agree to the last digit, the method's error is percent-level at 1 m spacing and falls as the fourth
power of the spacing, and double precision gives a floor near 1e-8 (`work/precision-probe/RESULTS.md`).
On the authors' 0.2 m grid the solver's noise on a slice is about 1e-7 rho0, which is the
"10^34 J/m^3" floor the paper states.

**The measurement itself.** The construction fixes the energy density and the radial pressure to
its smoothed inputs by design (we confirm it: the derived radial pressure equals the input to
3e-5). The only new matter it demands is the tangential pressure, which the equilibrium identity
fixes from the same profiles, P_t = P_r + (r/2)[dP_r/dr + (rho + P_r) da/dr]. We computed it that way
on WarpFactory's own 1D profiles and, independently, read it off WarpFactory's 3D solver on the
y-axis of the exported slice (`work/shell/hoop_stress.py`).

## 4. Results

### 4.1 The hollow shell on paper, and the critique's Appendix B

Three values of the pressure at the inner face of the paper's trial shell, for the paper's numbers
(`work/hollow-shell/tov_hollow.py`, `work/notes/02-hollow-shell.md`):

| Route | P(R1) / rho c^2 |
|---|---|
| TOV integrated inward from P(R2) = 0 with the shell's own enclosed mass, lapse matched to Schwarzschild outside: what the paper's text, equation (21), describes | +0.073 |
| `TOVconstDensity.m`, the uniform-solid-sphere closed form masked to the shell: what the code does, and what the paper's Figure 4 shows (section 4.6) | +0.095 |
| The critique's equation (B.6), sqrt(1 - 2GM/R2) - 1 | -0.184 |

The critique's (B.5) is exact for constant density and isotropic pressure; we reproduce it to
1e-14. To reach (B.6) it imposes a(R1) = 0, its (B.3), alongside the Schwarzschild match at R2, its
(B.2). The lapse of a static spacetime can be normalised once; with (B.2) it is normalised at
infinity, and the cavity's clock then runs at 0.761 of the rate at infinity, the cavity still flat
in rescaled time. Imposing both over-determines the problem: they agree only for M = 0. WarpFactory's
`alphaNumericSolver.m` matches the lapse outside and never imposes a(R1) = 0. So (B.6) describes
neither the paper's text nor its code, and the sign it finds is not the construction's.

The elementary objection stands regardless: a fluid face against vacuum must carry zero pressure,
TOV makes nonnegative pressure fall outward, so an isotropic hollow fluid shell cannot be static.
The paper concedes exactly this ("the isotropic pressure assumption is not valid for the R1 boundary
to maintain a stable shell") and answers with hoop stress. warpax's documentation states the
objection in four sentences, the cleanest form we know. The critique's broader point in Error 18,
that the final object is read off a metric and carries no constitutive law, is a different argument
and is not touched by any of this. (Register rows C1, C8.)

### 4.2 The measurement: what the shell requires, and what sets it

At the authors' setting (`work/shell/RESULTS.md` sections 2 and 3):

| | Fraction of rho0 c^2 | Where |
|---|---|---|
| Radial pressure, peak | +0.077 | 12.1 m |
| Tangential pressure, peak (hoop compression) | +0.194 | 10.3 m, the inner wall |
| Tangential pressure, minimum (slight tension) | -0.009 | 19.1 m, the outer wall |
| Largest pressure relative to the local energy density | 0.385 | 9.6 m |
| Cavity clock rate relative to infinity | 0.762 | |
| Mass added by the smoothing | 1.9 % | |

The 1D identity and the 3D solver agree to 4e-5 of rho0 on the tangential pressure and to 1e-4 on
the energy density, inside the error budget. In SI the hoop compression peaks at 2.6e39 Pa. The
dominant energy condition, every pressure below the local energy density, holds with a factor 2.6
to spare, which is the margin behind the paper's statement that "these pressures are all lower in
magnitude than the value of the energy density". (C2, C3.)

**The one knob.** The paper says the smoothing "is iterated upon ... until we find a metric that
satisfies the energy conditions at the boundaries". Sweeping it with the replica, everything else
fixed (`work/shell/sweep_smoothing.py`):

| Inner wall, 10 to 90 % of the plateau | Hoop stress, peak | Largest pressure over local energy density | Mass added |
|---|---|---|---|
| 0.7 m | 1.28 | 2.86 | 0.03 % |
| 1.4 m | 0.66 | 1.44 | 0.1 % |
| 2.7 m | 0.35 | 0.74 | 0.5 % |
| 5.4 m (the paper) | 0.19 | 0.39 | 1.9 % |
| 8.5 m | 0.15 | 0.21 | 7.5 % |

The hoop stress scales as the inverse of the wall width while the wall is thin; the dominant
condition fails below about 2 m. The smoothing is not a numerical nicety: it is what buys the energy
conditions, by thickening the walls and adding mass.

**The paper's remedy, quantified.** "For realistic materials that may have a limited range of
pressures possible, this requirement can always be satisfied by making the shell large and modifying
the density profile." Scaling the mass down at fixed geometry and smoothing
(`work/shell/compactness_scan.py`), the required strength-to-energy ratio settles at **0.76 times the
compactness**. Reference ratios of strength to rho c^2: steel 7e-13, carbon fibre 4e-11, diamond
4e-10, graphene 6e-10. A graphene-strength shell therefore needs a compactness below about 8e-10,
which at the paper's 20 m radius is still 1e19 kg at nuclear density; at graphene's own density it
is an Earth-sized, Earth-mass shell. For scale the other way, the pressure at the centre of a heavy
neutron star is about 1e35 Pa, against 2.6e39 Pa here.

### 4.3 What could supply the stress: two matter models

The paper does not name a material, and "stable" in it means in equilibrium by construction; no
stability analysis appears in the paper, and we performed none. Two candidate models exist.

**An elastic shell.** Le's second paper solves the Einstein-elastic boundary-value problem for a
self-gravitating shell with two free faces; we have not reproduced it and cite it as the place where
the strength question is treated properly. The ratios above say what the elasticity would have to
be.

**A swarm, which needs no strength** (`work/shell/einstein_cluster.py`, `work/notes/06`). The
continuum limit of counter-rotating rings on random axes is Einstein's 1939 cluster: particles on
circular geodesics, zero radial pressure, tangential pressure rho v^2/2 with v set by the enclosed
mass. On the authors' density profile it needs a peak tangential stress of 0.066 rho0 at 18.1 m,
against 0.194 for the construction, none of it radial, and orbital speeds rising to 0.46 c at the
outer wall; the photon-orbit constraint is met with 5.3 m to spare. It satisfies every pointwise
energy condition automatically. The construction's own stress state can be produced by a swarm with
velocity dispersions if and only if (P_r + 2 P_t)/rho < 1, which it is at the authors' setting with
a margin of 0.15, at the price of rms particle speeds of 0.92 c at the inner wall; for walls a
quarter sharper it cannot be produced by any swarm. The literature's radial-stability criterion for
such clusters, r > 6 m(r) shell by shell (Ostrowski 2025; Böhmer and Harko 2007 for the halo regime),
makes the swarm on the authors' density marginal only in its outermost skin. Our reading [ours]: the
inner-wall spike is a feature of the construction's isotropic starting guess, not of the problem;
the swarm closes the physics, with two Jupiter masses orbiting at half light speed inside 20 m, and
brings the engineering no closer.

### 4.4 How much shift the shell carries, against compactness

With the shell built at four compactnesses (1/3, 1/10, 1/30, 1/100) and the warp metric formed at
eleven shifts each, in units of the compactness (`matlab/shift_matrix.m`, `work/matrix/RESULTS.md`),
three independent readings on every case: WarpFactory's own sampled dominant condition (100
directions, 10 speeds, the paper's setting), a direct null check over 4000 directions, and the
swarm-realisability test of section 4.3.

| Compactness | First failing shift, all three readings | In units of compactness |
|---|---|---|
| 1/3, the paper | 0.030 to 0.033 | 0.09 to 0.10 |
| 1/10 | 0.0090 to 0.0100 | 0.09 to 0.10 |
| 1/30 | 0.0030 to 0.0033 | 0.09 to 0.10 |
| 1/100 | 0.0009 to 0.0010 | 0.09 to 0.10 |

**The allowed shift is about a tenth of the compactness**, over a range of 33 in compactness, for
this geometry and smoothing. The mechanism is visible in the exported numbers: the Eulerian momentum
density that the shift adds grows as shift over compactness, 0.30 rho0 per 0.02 of shift at the
paper's compactness, because the shift profile is fixed by the geometry while the energy density is
fixed by the mass. Failure arrives where the momentum density reaches the local energy density, 0.40
to 0.45 rho0 at the threshold, in the inner wall at right angles to the direction of travel; there
the stress-energy loses its timelike eigenvector, and the dominant condition, the null condition and
swarm realisability fail together. The paper's 0.02 passes every check with every margin at the
noise floor; its footnote that 0.02 "is likely not an upper limit" is right by a factor of about
1.6. (C5.)

Put together with section 4.2: a shell whose material sustains a strength-to-energy ratio s has
compactness at most s/0.76 and therefore a shift of at most about **0.13 s**. For graphene that is
8e-11, about 2.5 centimetres per second. The swarm needs no strength and is limited instead by
orbital stability near compactness 1/3, so its ceiling is the paper's, about 0.03, at the paper's
two Jupiter masses.

### 4.5 The exact check: warpax on the same points

WarpFactory decides a condition at a cell by trying 100 directions at 10 speeds; warpax's
`certify_point_lmi` decides it for every observer at once (Le 2026, Theorem 1). We ran it on every
active cell of all 68 exported slices, by two routes that agree to 4e-15 rho0, and its algebraic
classification of every cell agrees with ours (`work/matrix/exact_conditions.py`,
`work/matrix/RESULTS.md` section 7).

The exact check puts the first failing shift in the same bracket, 0.09 to 0.10 times the
compactness, for each of the four conditions at every compactness, and passes the paper's 0.02 for
every observer with every margin at the noise floor (1.2e-7 to 2.2e-7 rho0). Every violating cell
has lost its rest frame (Hawking-Ellis Type IV); no cell that keeps one violates. (C4, C5 closed.)

What the sampled check misses: never a failing case, but cells on the shallow rim of a violating
region. At the first failing shift it misses 5 % of the violating cells at the paper's compactness
and 66 % at compactness 1/100, where the violation is shallowest; one step further up, 3 to 5 %;
pooled over the deep violations of the coarse scan, 0.13 %. One hundred directions see 93 % of the
exact depth of the violation at the paper's compactness and 44 % at 1/100 at that shift, 96 % or
more beyond it. This is the same order of shortfall Le reports for a Rodal case (93.4 % detection at
1000 directions). The sampled check is adequate for the pass-or-fail verdict on a case at this
resolution, and not for counting cells or sizing violations near the threshold.

### 4.6 The paper's own figures, reproduced

The paper's Figures 4 to 10 are line plots along the y-axis at its point. Ours from the same export
are the same pictures in every panel (`work/wf-reproduction/pairs/`). Reading the paper's curves off
the PDF's vector paths, calibrated on the tick marks, and comparing them with ours at every radius
(`work/wf-reproduction/comparison.xlsx`): the unsmoothed inputs agree to 1 part in 10,000, so it is
the same shell, but every amplitude in the paper sits 1 to 11 % above ours, the more the sharper the
feature. The cause is in the paper's own smoothed inputs, which are narrower than what the published
script produces (inner wall 4.65 m against 5.36 m). Fitting the construction's two smoothing spans to
them with the replica gives 6100 and 3540 samples, ratio 1.723, the "approximately 1.72" of the
paper's footnote 7, where the published code carries 1.79 and a span of 4000; Figures 4 and 6 give
the same spans independently, to 0.02 %. Rebuilt at those spans, the replica reproduces the paper's
hoop-stress spike to 0.14 %, its wall width to 3 mm and its g22 peak to 1 part in 10,000. The
figures' lines are also sampled every 2 mm through the centre, where the script has 0.2 m cells and
no cell at the centre. The published script is therefore not the exact configuration behind the
figures; at the figures' setting the hoop stress is 0.211 rho0 c^2 rather than 0.194, and nothing
else in this report changes. (C10; C8 confirmed from Figure 4.)

### 4.7 Two defects in WarpFactory

- `generateUniformField.m` passes a hard-coded GPU flag to `getEvenPointsOnSphere`, so
  `getEnergyConditions` fails on any machine without a GPU whatever the caller's `tryGPU`; a
  one-token shadow copy fixes it (`matlab/shadow/generateUniformField.m`).
- In `getEnergyConditions.m` the Null and Weak branches lower the indices of the Eulerian frame
  tensor with the coordinate metric, where the Dominant and Strong branches use Minkowski, the only
  consistent choice for a frame tensor. A NumPy replica reproduces the exported Null map to 1.3e-16
  and, with Minkowski, the spurious violations vanish (`work/matrix/verify_null_bug.py`). At the
  paper's own point the maps show none, so the published figures stand; above it the Null and Weak
  maps fail about 1.5 times too early (a ceiling of 0.020 to 0.023 instead of 0.030 to 0.033 at the
  paper's compactness), and in the paper's Figures 7 and 10 their panels plateau at 2.8e39 where the
  Strong panel reaches 7.1e39, by about the square of g00. (C9.) Both are to be reported upstream
  with the replica, if the authors agree.

## 5. Interpretation [ours]

Everything in this section is our judgement on the numbers above, labelled so that it can be
disagreed with separately.

- **The construction is self-consistent, in the sense that matters to the critique's Error 18 as
  stated.** The metric is built from smoothed inputs and the matter is read off it; Einstein's
  equations hold by construction, the energy density and the radial pressure equal the inputs, and
  the tangential pressure is whatever equilibrium demands. The phrase "not a solution to Einstein's
  equations" is not borne out; the phrase "the authors do not solve the TOV equations" is borne out
  in the sense that no equation of state or constitutive law is ever named, which is the critique's
  substantive point.
- **"Physical" holds at the level the paper checks and fails at the level it gestures at.** All
  four pointwise energy conditions are satisfied, exactly, for every observer, with a margin of 2.6
  on the dominant one. The matter that satisfies them must sustain a hoop stress of a fifth of its
  own energy density, which exceeds the strength-to-energy ratio of the strongest known material by
  about nine orders of magnitude; the paper's remedy of a less compact shell buys relief only in
  proportion to the compactness, and the shift the shell can carry falls with it.
- **The warp shift is small in the paper and smaller for anything real.** 0.02 is about 6000 km/s;
  the ceiling at the paper's compactness is 0.03; at the compactness a graphene shell could sustain
  it is centimetres per second. Within this construction there is no corner in which a shell made
  of anything real carries a shift worth the name. A swarm of orbiting particles removes the strength
  problem and leaves two Jupiter masses at half light speed inside 20 metres.
- **What the dispute looks like from the numbers.** The paper's descriptive claims about its own
  object are correct and understated; its word "stable" means equilibrium, and no stability analysis
  exists on either side. The critique's specific derivation does not describe the construction, and
  its general objection does. Le's toolkit decides the energy conditions where sampling could only
  estimate them, and the two agree on every verdict that matters here.

## 6. The claim register, in one table

| | Claim | Status |
|---|---|---|
| C1 | The critique: the construction is not a solution of Einstein's equations, by Appendix B | The derivation imposes a(R1) = 0, which neither the text nor the code does, and finds tension where integration finds compression; the elementary objection and the constitutive-law point stand. Awaiting the authors' reply |
| C2 | The paper: radial pressure equals the input; tangential pressure spikes at the inner wall | Confirmed and sized: 0.194 rho0 c^2 at the script's smoothing, 0.211 at the figures' |
| C3 | The paper: every pressure stays below the energy density | True at the authors' setting, margin 2.6; fails for walls sharper than about 2 m |
| C4 | WarpFactory's sampled observer check is sufficient | For the verdict on a case, yes; it misses 5 to 66 % of the violating cells at the first failing shift and almost none when the violation is deep |
| C5 | A shift of 0.02 satisfies all four energy conditions | Yes, for every observer, in both toolkits; the ceiling is 0.030 to 0.033 |
| C6 | The "comoving frame" obtained by a Galilean transformation is legitimate | Not tested here; interpretive |
| C7 | The shell is "stable" | Equilibrium by construction; no stability analysis exists; what could supply the stress is section 4.3 |
| C8 | The pressure step integrates the TOV equation | The code applies a solid-sphere closed form, and so does the paper's Figure 4; an initial guess, smoothed afterwards |
| C9 | WarpFactory's four condition maps are evaluated consistently | The Null and Weak maps use the coordinate metric where the Dominant and Strong use Minkowski; spurious violations above the paper's point, none at it |
| C10 | The published live script is the configuration behind the paper's figures | The figures were smoothed 12 % less, at ratio 1.72 against the code's 1.79, and sampled every 2 mm; every amplitude difference follows |

## 7. What we ask the people involved

- To Barzegar, Buchert and Vigneron: is (B.3) meant as a junction condition or as a normalisation?
  With the lapse normalised at infinity the cavity clock runs at 0.761; what remains of (B.6)?
- To Fuchs and Helmerich: is the closed-form pressure step intended as an equivalent initial guess?
  Which smoothing spans and grid produced Figures 4 to 10? May we open the two toolkit defects as
  issues, with the replica?
- To Le: may we quote the four-sentence statement of the hollow-shell impossibility? Have you
  computed the anisotropy of your own FuchsMetric? Would a comparison of WarpFactory's native
  profiles with FuchsMetric be welcome in warpax?

Letters to Le and to the critique's authors went on 27 October 2026; the letter to Applied Physics
goes with this draft. Every reply will be recorded in the appendix, verbatim with permission or
summarised without, and what is right in it will change this text.

## 8. Reproducibility

Everything is in the repository. `work/precision-probe/` holds the solver error budget;
`work/hollow-shell/` the TOV routes; `work/shell/` the replica, the identity, the smoothing sweep,
the compactness scan and the swarm; `work/matrix/` the shift matrix from CI, its analysis, the
Null/Weak replica and the exact warpax check; `work/wf-reproduction/` the figure pairs, the
digitised curves, the smoothing fit and the workbook. Each folder's `README.md` gives the commands;
`INDEX.md` lists the sources; `CLAIMS.md` the register. The MATLAB jobs run on GitHub Actions under
MathWorks' free licence for public repositories and export their artifacts; the central-plane slices
(gitignored, re-downloadable) are the inputs to every Python step. The paper's figures are
reproduced under its CC BY 4.0 licence with attribution.

## 9. Limitations

- One geometry (R1 = 10 m, R2 = 20 m), one shift profile, the authors' smoothing and grid. The
  constant 0.09 to 0.10 belongs to that construction; the proportionality to compactness is
  structural. The authors' cartoon grid at 0.2 m was kept so the numbers are theirs; finer grids
  were not run.
- The strength law and the shift ceiling were computed at the published script's smoothing; at the
  figures' smoothing the hoop stress is 9 % higher and the ceiling would be slightly lower, not
  recomputed.
- The energy-condition verdicts are pointwise. Averaged conditions, dynamics, acceleration and
  superluminal cases are outside this work; so is any stability analysis.
- The swarm model is a consistency check, not a design; collisionlessness at nuclear density is an
  assumption.
- The exactness of the warpax check is in the observer problem; the stress-energy it checks is still
  WarpFactory's finite-difference result, with its noise of about 1e-7 rho0.

## Appendix: responses received

None yet. The two-week comment window opens when this draft is sent.
