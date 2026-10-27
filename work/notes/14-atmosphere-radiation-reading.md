# Note 14: Fell and Loeb 2026, "Radiative Signatures from Warp Drives Traveling Through the Earth's Atmosphere": anything on stability?

27 October 2026, evening. Request from the main session on Carlos's behalf: Carlos read in `REPORT.md` that
the paper under test calls its shell "stable" while no stability analysis exists on either side (register
row C7), recalled arXiv:2608.10800 as possibly relevant, and asked whether anything in it bears on the
Fuchs shell's stability or on anything else the project could use. Fetched the project's way (manifest
row, `tools/fetch_sources.py`); text in
`sources/papers-text/2026_fell_loeb_radiative_signatures_warp_drives_atmosphere_2608.10800.txt`, "l. N"
below is a line of that file. The id resolves to the stated title: Shaun David Brocus Fell (Applied
Physics, PBC; the Fell of Fell and Heisenberg 2021) and Abraham Loeb (Applied Physics and Harvard),
arXiv v1 of 11 August 2026, 16 pages, gr-qc, no journal reference, CC BY-NC-SA 4.0. Judgements are
marked **[mine]**.

## 1. The answer for Carlos

The paper does not touch the stability of a warp shell, ours or anyone's. It asks a different question:
if a warp bubble of the Alcubierre kind, the one with no mass at all, flew through the upper atmosphere at
a tenth to three quarters of the speed of light, what would we see? The authors take the Alcubierre
metric as a fixed background, ignore the matter that would be needed to produce it, and simulate air
flowing past it with a relativistic shock-capturing fluid code. The bubble piles the air up into a bow
shock in front of it; the air in the stagnation zone is heated to tens or hundreds of MeV per nucleon;
the shocked gas radiates gamma rays at ten to ten million terawatts, and the atmosphere below re-emits a
glow that for the fastest and largest bubbles would outshine the Sun on the ground. The point of the
paper, stated in its introduction and conclusion, is to constrain the "warp drive" interpretation of
unidentified anomalous phenomena: anything aircraft-sized moving relativistically through air would be
unmistakable. The word "stability" occurs only for the numerical scheme and for a simulation reaching a
steady state. Nothing in it is a dynamical analysis of a shell, and the authors say explicitly that their
results are "strictly for zero ADM mass warp drives" and that a massive one like the Fuchs shell "would
behave differently"; they leave that for future work.

So it offers nothing for C7, and nothing for the report beyond one line of context: the Applied Physics
line is still producing warp-drive papers in 2026, this one cites the Barzegar critique and the
Celmaster-Rubin refutation of Lentz in its first paragraph, and it treats the Fuchs shell as one of a
list of constructions rather than as the physical drive. The regimes do not even overlap: the paper's
slowest bubble moves at 0.1 c, five times the largest shift the Fuchs shell can carry, and a shell of
two Jupiter masses in 20 m would interact with an atmosphere through its gravity, not through a shock.

## 2. What the paper does

**Setup.** "As a representative embodiment, the metric of a warp drive spacetime is taken to be the
Alcubierre metric" (l. 66), eq. 1-2 (l. 74-83), with "the only nonzero metric derivatives" in the wall of
thickness 1/sigma (l. 83). "The metric is assumed static over the course of the simulation. Moreover, the
spacetime source term is ignored. This implies that components of the atmospheric fluid can pass cleanly
through the highly nonlinear volumes of the region, which would normally not occur in a physical setup
... the matter sector consists solely of the interacting fluid without any backreaction" (l. 84). The
fluid is a perfect fluid in the Valencia formulation with a Taub-Mathews equation of state and a
two-temperature electron-ion model (l. 67, 87-123), run in Athena++ with adaptive refinement pinned to
the bubble wall and the shock (l. 87, 213-216). The paper is careful about the numerics: the
conservative-to-primitive inversion fails in cold cells and is replaced by an entropy-advection branch
(l. 125-154); convergence is checked with a mass-flux residual and the Bernoulli invariant (l. 319-337).

**Parameters.** Upstream temperature Theta_1 from 1e-3 to 1e-6 (as a proxy for the real 1e-13, justified
by the high-Mach limit, l. 203-212), bubble speeds v_s of 0.1, 0.25, 0.5 and 0.75 c, bubble radii R of
25, 50 and 100 m with sigma = 5/R (l. 293); "code units are taken to be meters" (l. 293).

**Central result.** A detached bow shock with a stagnation zone between the wall and the shock nose
(l. 294); the stagnation temperature k_B T ~ (W_1 - 1) m_u c^2, 144 MeV per nucleon at 0.5 c, "well above
the electron pair production threshold" (l. 160-162); the standoff distance and compression ratio from
the Rankine-Hugoniot conditions, matching the runs with one calibrated constant (l. 167-177, 301, 317).
Luminosity from bremsstrahlung within 15 R: "from 10^13 to 10^19 watts, or 10's of terawatts to tens of
exawatts" (l. 303), mostly gamma rays (l. 307); the re-radiated stratospheric glow "ranges from 0.007 W/m^2
for v_s = 0.1 c and R = 25 m up to 7460 W/m^2 at v_s = 0.75 c and R = 100 m" (l. 314), the latter several
times the solar constant; "These numbers are all order-of-magnitude" (l. 314).

**Conclusions.** "The inferred luminosities exceed by many orders of magnitude the values detected for
UAP ... These results further constrain warp drive interpretations of UAP within the terrestrial
environment" (l. 341). "The results of this study are strictly for zero ADM mass warp drives, such as the
Alcubierre metric, the Van den Broeck metric, and the Lentz metric. It has been shown in Bobrick and
Martire [8] that generic warp drive spacetimes have non-zero ADM mass ... Non-zero ADM mass spacetimes
would behave differently from those in the current study ... Future studies will explore this region of
the parameter space, including sub-relativistic velocities" (l. 342). Scaling L proportional to rho_1^2
R^3 and to v_s^3 above a 0.2 MeV knee (l. 343); a floor near 1e3 W for the mechanism, and "a sufficiently
compact or slow warp drive would therefore not shock the atmosphere, and would not glow by this mechanism
at all" (l. 344). Framing: "Reports on Unidentified Anomalous Phenomena (UAP) near Earth triggered
speculations that they might be associated with warp drives. The present study is performed with this
association in mind" (l. 65); supported by the Galileo Project at Harvard; Bobrick and Martire thanked
for comments (l. 346).

**Where "stability" occurs.** "The EoS therefore doesn't just set the physics, it also determines the
stability of the simulation" (l. 113); "Snapshot of a stabilized simulation" (figure captions, l. 295,
298). That is all. The paper does not define, discuss or test the dynamical stability of any spacetime,
and does not mention the Fuchs shell beyond listing it among recent constructions in the first paragraph
(l. 62, reference [17]).

## 3. Claim and scale

- Claim, in one sentence: a zero-mass Alcubierre bubble crossing the upper atmosphere at 0.1 to 0.75 c
  would be a gamma-ray source of 1e13 to 1e19 W with a visible stratospheric glow, so relativistic
  warp-drive interpretations of aerial phenomena are excluded; slow or compact bubbles are not addressed.
- Scale against the project [mine]: the paper's objects have zero mass and radii of 25 to 100 m; the
  Fuchs shell has M = 4.49e27 kg in R2 = 20 m (`REPORT.md` section 3) and a maximum shift of 0.030 to
  0.033 c (`work/matrix/RESULTS.md` section 1), below the paper's slowest case by a factor of three to
  five. Its surface gravity, G M/R2^2 = 7.5e14 m/s^2, would govern any encounter with air long before a
  shock did. The paper's own caveat (l. 342) says the same from the other side: a massive drive has
  curvature everywhere, and their standoff estimate does not apply.
- On the energy conditions, the paper is silent by construction: with the source term dropped there is
  no matter sector for the bubble, only the air.

## 4. Verdict

- For C7 (stability): nothing. The claim register's statement stands: no stability analysis of the shell
  exists on either side, and this paper is not one.
- For the report: at most one sentence in the related-work paragraph, if Carlos wants it, noting that
  the 2026 Applied Physics and Harvard paper on atmospheric signatures treats zero-mass bubbles only and
  defers massive shells to future work. Not needed for any claim.
- For the index: filed under the 27 October readings (`INDEX.md` B7), with its real content in the row.
- Method note [mine]: the paper is a clean example of the reverse-engineering stance taken to its limit,
  a prescribed metric with its matter not merely unspecified but removed ("the spacetime source term is
  ignored", l. 84); the authors say so plainly, which is more than the 2024 paper did about its own
  stress-energy.

## 5. Open questions

- None for the project. The paper's promised follow-up on non-zero ADM mass drives would be the first
  dynamical study of anything like the Fuchs shell in a medium; if it appears, it belongs in `INDEX.md`
  B4 next to Clough et al.
