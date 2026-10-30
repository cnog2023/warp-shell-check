# Note 15: four papers checked for an explorable path beyond the elastic-shell session

30 October 2026. Request from the main session, in Carlos's words: "before we go there [the elastic-shell
session] anything we can use from the articles below ... Download the documents for reference and see if
any presents any explorable path beyond the elastic shell session to our current problem." The problem is
the one `REPORT.md` states: the shell needs a hoop stress of a fifth of its energy density that no material
supplies by nine orders of magnitude, the only material-free model is the orbiting swarm, the shift
ceiling is a tenth of the compactness, and the planned next computation is Le's elastic shell at our
parameters. Four ids, all resolved on arxiv.org on 30 October 2026 (API listing); manifest rows and the
fetch script as before; text in `sources/papers-text/`, "l. N" a line of the named file. One of the four
(2608.08213) was already in `sources/` from 18 October; the copy was already v2 (the HTML endpoint serves
the latest version), re-fetched anyway, and read closely now for the first time. One (2203.05989) has no
HTML version; the fetch script gained a fallback that extracts the PDF's text with PyMuPDF (page markers;
the equations come out as token soup, the prose is fine). Judgements are marked **[mine]**.

| arXiv id | Resolves to | Authors | Date, venue, category |
|---|---|---|---|
| 2608.08213v2 | "Exploring Particle Geodesics in a Warp Drive Spacetime" | Sanches, Morris, Brandt (LSU) | v2 12 Aug 2026; "Accepted for publication in Classical and Quantum Gravity"; gr-qc |
| 2302.13826v3 | "Influence of anisotropic matter on the Alcubierre metric and other related metrics: revisiting the problem of negative energy" | Abellán, Bolívar, Vasilev | v3 20 Apr 2023; Gen. Relativ. Gravit. 55:60 (2023); physics.gen-ph |
| 2205.02780v1 | "Alcubierre Warp Drive in Bohmian Quantum Gravity" | Sijo K. Joseph | 28 Apr 2022; no journal; physics.gen-ph |
| 2203.05989v2 | "Superluminal Geometrodynamics of Braneworld Hyperdrive via Brane-Bulk Interaction" | Alias, Jalar (UKM, Malaysia) | v2 5 Apr 2023; no journal; physics.gen-ph |

## 1. The answer for Carlos

None of the four opens a path. Two of them are not physics we could use at all: one rewrites the
Alcubierre bubble inside a "Bohmian quantum gravity" that changes Einstein's equations and ends with a
differential equation it does not solve; the other adds a fifth dimension to the Alcubierre bubble, drops
it again on the next page, and concludes that its "hyperdrive" needs more energy than a warp drive, not
less. The third is a symbolic study of what kind of fluid could sit behind the Alcubierre metric; it has
an error that a referee should have caught, it computes no number, and the one thing it gets right, that
the matter behind a warp metric must be anisotropic, is exactly what our measurement of the shell already
put a number on. The fourth is a careful and interesting paper, accepted by Classical and Quantum Gravity,
about what happens to dust, meteors and rogue planets that a sub-light Alcubierre bubble runs into, and
how a "deflector shield" could be added to the metric; but it deals with a massless bubble, computes no
matter at all, and says in one sentence that every metric it uses violates every energy condition. For
our shell, whose wall is solid matter at 1.5e23 kg/m^3 (`work/shell/RESULTS.md`, the table at l. 118), the
question of what passes through the bubble does not arise, and the shield idea would add momentum
density, which is the thing that caps the shift.

So the elastic-shell session stays the next step, and nothing here competes with it. If anything is to be
taken from these four, it is one cosmetic exercise, ranked last in section 3: the geodesic integrator the
LSU group published as open source could draw the paths of free particles around and inside our exported
shell metric; it would make a picture for the wiki and settle no claim. Cost half a day; what it needs is
in the repository; I do not recommend it before the elastic shell is done.

## 2. The papers

### 2.1 Sanches, Morris, Brandt, "Exploring Particle Geodesics in a Warp Drive Spacetime" (`2026_particle_geodesics_warp_drive_2608.08213.txt`)

**Claim.** "Although the Alcubierre Warp Drive is theoretically capable of providing faster-than-light
travel, it may be difficult to use for this purpose. But is it useful for slower-than-light travel?" (l. 45).
Massive-particle geodesics are integrated in the 3+1 form (l. 102-117) for the Natário class of metrics,
flat slices with a flow vector (eq. 4, l. 94), with a C^3 polynomial form function (eqs 10-11, l. 121-127).
Results at a bubble speed of 0.5 c (l. 155): stationary dust is "picked up" and dragged along with the
bubble (l. 152-153, read off eq. 18); dust moving toward the ship is focused behind it and accelerated
to 10 % of c (l. 194); dust moving away is reflected "as much as 80 % of light speed" (l. 217); "slippage"
(ship speed different from the drag speed, eq. 35-36, l. 251-258) and "negative slippage" to back away
from a rogue planet when the field shuts down (l. 277-279); a "deflector shield", transverse flow
components k rho_y phi, k rho_z phi on a shell outside the bubble (eqs 37-42, l. 285-306), which sweeps
particles aside but creates "co-moving points", a "ring-shaped region" in three dimensions, where
particles "accelerate without limit but stay in place" when k_0 > sqrt(1 - u^2) (l. 319, 352-354, 368),
cured by switching the deflector off behind the ship (eq. 53, l. 364-369). The paper is explicit about what it does not do: "we don't need to calculate the
distribution of matter to study geodesics ... Computing the matter configuration that makes this motion
possible is a separate calculation" (l. 130), and "the choice of flow vector made in Eqs. (37)-(39) still
represent a warp drive spacetime of the Natário class ... More specifically, the Stress-Energy-Momentum
tensor violates all the energy conditions" (l. 308). An open-source Rust integrator and visualiser are
published (l. 158, refs [11], [12]).

**Metric and matter model.** Alcubierre and Natário flow vectors on flat slices, unit lapse; no matter
model; zero ADM mass. On "stability": "attempts to simulate a superluminal Alcubierre Drive have met with
instability [4]" (Clough et al., numerical, l. 58-61) and "a quantum back-reaction would destabilize any
warp drive that attempts to exceed light speed" (l. 78-79, citing Hiscock and others); both concern
superluminal bubbles, not a static massive shell.

**Scale.** Units with the solar mass as 1: a unit length of 1.477 km, bubble inner radius R = 4 and width
sigma = 4, "approximately 6 km" (l. 156); dust of 1e-9 to 1e-6 kg (l. 51-52); bubble speed 0.5 c, debris
at 1 % of c (l. 155). No energy or mass of the bubble is computed. Against the shell: 20 m and 4.49e27 kg
(`REPORT.md` section 3), a shift of 0.02 c in the paper and 0.030 to 0.033 c at the ceiling
(`work/matrix/RESULTS.md` section 1).

**Relevance.** None for the mass, the stress or the ceiling. The one transferable idea, a transverse
shift to deflect matter, is a momentum density added to the cavity's edge, and momentum density reaching
the local energy density is what sets our ceiling (`work/matrix/RESULTS.md` section 1) [mine]. The
"bubble picks up debris" result has a trivial analogue in the shell: the cavity drags its contents at the
shift speed, and the wall is matter that nothing passes through. The integrator could be pointed at our
exported metric for a picture; see section 3.

### 2.2 Abellán, Bolívar, Vasilev, "Influence of anisotropic matter on the Alcubierre metric..." (`2023_abellan_bolivar_vasilev_anisotropic_matter_alcubierre_2302.13826.txt`)

**Claim.** "the issue of negative energy densities associated with the Alcubierre warp metric ... can be
addressed when the whole non-vacuum Einstein equations of the system are examined. To this end, we have
considered matter content in the form of anisotropic fluids" (l. 56); "in rectangular coordinates, the
energy density depends necessarily on the tangential pressures of the fluid. For matter such as dust or
isotropic fluids we find that density and other related quantities become identically zero. This makes
the negative energy problem spurious" (l. 57-58); "In all cases we determine that energy density is not
mandatory negative" (l. 60). Method: an anisotropic fluid with principal axes along x, y, z (eq. 10-12,
l. 109-118) is set equal to the Einstein tensor of the Alcubierre metric component by component
(eqs 13-22, l. 120-139); from the vanishing of the fluid's yz component they derive the "critical"
constraint that the shift can depend on y or on z but not both (eq. 21, 25, l. 136, 146, 152-154), and then
rho = (p_y - p_z)/2 and p_x = 3 rho (eqs 28-31, l. 156-168). The same is repeated for cylindrical warps
along z and along r and for a radial "spherical warp" (sections 3-5), with "no condition that requires the
energy to be negative" (l. 517) and the conclusion that "the assertion that the Alcubierre warp requires
by necessity negative energy density should be taken with caution" (l. 521).

**Metric and matter model.** The Alcubierre metric with a general shift; an anisotropic fluid without
shear stress, diagonal in a fixed Cartesian or cylindrical frame. No solution is attempted ("It is not the
purpose of this article to solve these equations", l. 140); no number appears anywhere in the paper.

**What is wrong with it [mine].** The "critical constraint" (eq. 25) is not a property of the geometry. It
comes from setting the yz component of the Einstein tensor equal to zero because the fluid the authors
chose has no yz stress; the Alcubierre metric's Einstein tensor has a yz component, so what the equation
says is that a shear-free fluid cannot source the metric unless the shift depends on one transverse
coordinate only, which no bubble does. The paper reads this as a constraint on the bubble and the zero
density of the dust and isotropic cases as the negative-energy problem being "spurious"; both say the
opposite, that those sources cannot produce the geometry at all. This is the move Santiago et al. describe
for Lentz, "imposing both sides of the Einstein equations"
(`2022_santiago_schuster_visser_generic_warp_drives_violate_nec_2105.03079.txt` l. 797-798), in the
paper's own symbols. Barzegar et al. file the group's papers under "a naive evaluation of the components
of the Einstein tensor is performed in these works without addressing the main pathologies of such models
while making various errors" (`2026_barzegar_buchert_vigneron_classification_demystification_2602.16495.txt`
l. 1307), note that they "take the WEC to be equivalent to the positivity of the Eulerian energy" (l. 1223),
and list them with the works that "rushed to plot some figures without an in-depth analysis" (l. 1113).

**Scale.** None given. The shell's anisotropy is a number we measured: a tangential pressure of 0.19 of
the peak energy density against a radial one of 0.077 (`REPORT.md` section 4.2), with the shear components
in the exported slices.

**Relevance.** The idea that the matter behind a warp metric must be anisotropic is right, and it is the
Fuchs construction's own starting point ("non-uniform pressure terms along the theta and phi directions,
akin to hoop stress", `work/notes/01-reading.md` section 1); our measurement quantified it. The paper adds
no method, no number and no model, and its central constraint is an error. Nothing to run.

### 2.3 Joseph, "Alcubierre Warp Drive in Bohmian Quantum Gravity" (`2022_joseph_alcubierre_bohmian_quantum_gravity_2205.02780.txt`)

**Claim.** "Alcubierre warp drive metric is coupled to quantum mechanical scalar matter field. The
requirement of the exotic matter for the warp drive is mapped into a conformal wave equation. This result
into a fourth order partial differential equation in terms of the quantum mechanical density. Finding a
proper quantum mechanical density obeying the proposed partial differential equation will be a resolution
to the exotic matter problem" (l. 34). The theory is a scalar-tensor theory in Weyl geometry in which the
conformal factor is the exponential of the de Broglie-Bohm quantum potential (eqs 1-10, l. 51-95), "gravity
is still treated as classical" (l. 49); the Alcubierre energy density is equated to the quantum part of the
stress tensor "ignoring other contributions (they are smaller due to the presence of kappa)" (l. 144), giving
a wave equation for the conformal factor (eqs 22-23, l. 159-163) and a fourth-order equation for the
density (eq. 28, l. 181); a flat-space toy version with a constant in place of the Alcubierre function is
separated into trigonometric and hyperbolic solutions (l. 194-197); "If one can find a viable distribution
of quantum mechanical density which obeys the wave equation ... we will resolve our problem of exotic
matter" (l. 199). Its reference list cites White's 2003 paper and "H. White, J. Br. Interplanet. Soc. 66,
242 (2011)" (l. 274-279), which locates the journal version of the 2011 NASA paper of note 12.

**Metric and matter model.** Alcubierre; a quantum scalar field in a modified theory of gravity. No number.

**Relevance.** A different theory of gravity, within which the paper itself reaches no solution. Outside
the project by its own rules ("Not new physics", `PLAN.md` section 8), and outside Applied Physics's own
grant rules (classical relativity, positive energy; `INDEX.md` C). Nothing to run.

### 2.4 Alias, Jalar, "Superluminal Geometrodynamics of Braneworld Hyperdrive via Brane-Bulk Interaction" (`2022_alias_jalar_braneworld_hyperdrive_2203.05989.txt`)

**Claim.** "we employ the concept of braneworld that naturally influence spacetime geometrodynamics.
Start from define and develop the spacetime metric of braneworld warp bubble, the expression for energy
densities as function of relevant parameters which contribute to the braneworld approach of superluminal
travel by hyperspace-drive were derive" (p. 1, l. 19-23). A metric with an extra coordinate Y is written
(eq. 1, p. 2); "the extradimensional term Y that represents the bulk space is negligible from the
perspective of a Eulerian observer inside the bubble. Therefore, as Y -> 0" (p. 3, l. 327-332) the metric
"can be deduced to the original Alqubierre metric" (p. 5, l. 1396-1398); the energy density is then
Alcubierre's, "which violates the energy condition" (p. 12, l. 3151), with its velocity term credited to
"Lobo and Visser's calculation" (p. 13, l. 3175); a "hyperdrive velocity" is defined as the sum of an
on-brane velocity and a "bulk velocity" (eq. 38, p. 10),
"analogically as if wind that represent bulk, push the kite surfing surfer that represents the warp
bubble" (p. 10, l. 2725-2727), and the energy density as a sum of a brane and a bulk term (eqs 49-51,
p. 13). Conclusion: "the hyperdrive requires much more energy than that of a warp drive" (p. 14, l. 3643).

**Metric and matter model.** Alcubierre, with a fifth coordinate introduced and discarded. No matter
model; no number; no journal.

**Relevance.** None. It is worth one remark for note 13's record: this is a second attempt to put an extra
dimension under the Alcubierre bubble, independent of White's, and it concludes that the extra dimension
costs energy rather than saving it. Neither has a calculation behind the sign [mine].

## 3. Explorable paths, ranked

1. **The elastic-shell session, as planned.** Nothing in these four papers competes with it or changes its
   brief. It is the only open question with a solver (Le's) and a defined input (our stress state).
2. **Geodesics of test particles in the exported shell metric** (from Sanches et al.). What the session
   would do: adapt the published 3+1 integrator, or write a short one of our own, to the metric of
   `work/matrix/run-fine/slice_f1_b5.mat` (the paper's point, shift 0.02) and draw the paths of particles
   released outside the shell and inside the cavity. What it needs: that slice, whose metric tensor gives
   the lapse, shift and spatial metric. Cost: half a day. What it would show: capture by the shell's
   gravity outside (surface acceleration G M/R2^2 = 7.5e14 m/s^2,
   `work/notes/14-atmosphere-radiation-reading.md` section 3), uniform drag at 0.02 c inside. A figure
   for the wiki; no register row moves. Ranked last because it answers nothing the report asks.
3. Nothing else. Abellán et al. offer a bookkeeping we have already done exactly; Joseph and Alias and
   Jalar offer other theories of gravity with no numbers.

## 4. Open questions

- Whether the LSU group's follow-up, if any, computes the stress-energy of the deflector metric; the
  paper defers it (l. 130). If it appears it belongs next to Clough et al. in `INDEX.md` B4.
- The JBIS 66, 242 reference for White's 2011 paper is a bibliographic pointer only; it was not fetched.
