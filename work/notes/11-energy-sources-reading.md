# Note 11: could the shell's stress-energy come from something other than orbiting matter? Seven papers read

27 October 2026. Carlos's question, in his words: "we claim we would need 2 jupiters spinning at 0.42c to
generate the warp bubble... but what if theoretically there is other way to 'generate' this mass?" He gave
seven arXiv ids with one-line descriptions from an AI summary and asked whether anything in them could
advance the project. The project's own numbers behind his sentence: the shell is R1 = 10 m to R2 = 20 m,
M = 4.4886e27 kg, peak smoothed energy density rho0 = 1.3585e40 J/m^3 (`REPORT.md` section 3); the swarm
that holds that density up without material strength needs orbital speeds up to 0.46 c at the outer wall,
and reproducing the construction's own stress state needs rms speeds of 0.92 c at the inner wall
(`work/notes/06-counter-rotation.md` section 2; `REPORT.md` section 4.3). Mean density M/V with
V = 4/3 pi (20^3 - 10^3) m^3 = 2.93e4 m^3: 1.53e23 kg/m^3, 1.38e40 J/m^3 [mine, arithmetic].

How the papers were fetched: seven rows added to `sources/papers/MANIFEST.tsv`, `tools/fetch_sources.py`
run; PDFs in `sources/papers/`, text in `sources/papers-text/` (arXiv's HTML, tag-stripped; both
gitignored). Below, "l. N" is line N of the named text file. Quotes are copied from those files. Every
judgement is marked **[mine]**. Each id was checked against arxiv.org (API listing, 27 October 2026):

- 2502.14535 now resolves to "Observation of quantum free fall and the consistency with the equivalence
  principle" (v4, 7 Dec 2025); versions 1-3 carried the title on Carlos's list, "Observation of the quantum
  equivalence principle for matter-waves". Same paper.
- 2502.17575 resolves to "On the quantum mechanics of entropic forces" (Carney et al., one version). The
  title on the list, "Emergent Gravity in the Thermodynamic Limit", is not this paper's title in any
  version; the list's description does fit its content, so the id was used and the title recorded here.
- 1401.3164 is as titled, but its method is the generalised uncertainty principle, not loop quantum
  gravity as the list's description said (section 2.2).
- The other four resolve to the listed titles (1212.0426's title is longer than the list's version).

## 1. The answer for Carlos

No. None of the seven papers describes a way to produce the stress-energy the shell needs without putting
that much mass-energy there. Four are about measuring gravity or measuring with it: how precisely a quantum
particle's mass can be read off its fall (Seveso, Peri and Paris), what quantum phase a free-falling atom
picks up (Dobkowski et al.), how faint a gravitational-wave background can be detected (Guo et al.), and how
Planck-scale corrections to the metric around the Sun would show up in light bending and Mercury's orbit
(Ali, Khalil and Vagenas). Two are about limits: a heuristic cap on how much energy a region can hold
(Kauffmann) and Planck-scale limits on measurable energy and time (Abou El Dahab and Tawfik). One, Carney
et al., is about where gravity comes from: it builds toy quantum models in which Newton's attraction
between two masses comes out of the heat and entropy of a hidden medium instead of from gravitons. But in
those models the force is still between masses that are already there, with the same G and the same masses;
the medium supplies the law of attraction, not the mass. In relativity's language, all seven take the
stress-energy as given and ask what gravity does with it or how to detect it. None asks how to make it.

The scales say the same thing. The shell needs about 1.4e40 joules per cubic metre, which is 1.5e23 kg per
cubic metre over 29,000 cubic metres. The vacuum ("dark") energy density Kauffmann's bound estimates is
1.7e-9 J/m^3, 49 orders of magnitude smaller. The gravitational-wave backgrounds Guo et al. call detectable
carry about 2e-18 J/m^3, 58 orders smaller. The quantum-gravity correction to empty space that Ali et al.
parametrise is, even at the loosest bound their own table allows, a thousand times too small at the shell's
radius and of the wrong sign; at the size theory expects it is 38 orders too small. The laboratory masses
are single atoms, 1e-25 kg, against 4.5e27 kg. General relativity does allow, in principle, any
stress-energy with the right pattern, and field energy counts as much as matter. But field energy at the
shell's density means magnetic fields of 2e17 tesla or electric fields of 6e25 volts per metre, millions of
times beyond where the vacuum itself breaks down (the Schwinger limit), and a pure field's pressures always
add up to its energy density where the shell's add up to at most 0.85 of it, so a field alone cannot even
reproduce the shell's stress state [mine]. The honest position after this reading is the one in note 06:
within known physics, the material-free way to hold this shell up is matter in orbit, and these papers
change nothing about the mass. What they add is a sharper way to say why: emergent-gravity models change
the explanation of attraction, not the accounting of energy.

## 2. The papers, one by one

### 2.1 Kauffmann, "A Self-Gravitational Upper Bound on Localized Energy ..." (`2012_kauffmann_self_gravitational_upper_bound_1212.0426.txt`)

Posted in physics.gen-ph, v5 of 26 January 2014 (l. 21); the author gives no institution ("Retired,
American Physical Society Senior Life Member", l. 25-26); no journal reference in the text; 12 pages.

**Claim.** A Newtonian model with energy feedback: the energy of a static lump is reduced by its own
gravitational potential, and the potential is computed from the reduced energy (eqs 2a-2c, l. 87-100), the
author's "energetically self-consistent upgraded Newtonian gravitational theory" (l. 29). The reduction
factor stays between 0 and 1 (eq. 4a, l. 164), hence "0 <= (G E_G)/(c^4 r_s) < 1" (eq. 4b, l. 168): a
sphere of radius r cannot hold more effective energy than c^4 r/G, horizons never form, and "nonzero
effective static point energies indeed don't exist" (l. 214-215). A quantum field has infinite zero-point
energy; fed into the model, any infinite energy inside radius r_s comes out as exactly E_G = (c^4/G) r_s
(eq. 8a, l. 309), mean density 3 c^4/(4 pi G r_s^2) (eq. 8b, l. 319). With r_s = 1.3e26 m, the age of the
universe times c, that is "about 1.7 x 10^-9 joules per cubic meter" (l. 325), "the same order of magnitude
as what is yielded by observations" (l. 327-328). The author argues quantising gravity is irrelevant to
this ("Gravitational radiation doesn't physically enter into self-gravitational correction", l. 375-376).

**Scale [mine].** The cap at r = 20 m: E_max = c^4 (20 m)/G = 2.4e45 J, 2.7e28 kg; the shell's 4.49e27 kg
is one sixth of it (G M/(c^2 R2) = 0.167; the paper's inequality is this ratio < 1). General relativity's
own bound for a fluid sphere, Buchdahl's 2GM/(c^2 R) < 8/9, is also met: the shell has 1/3 (`REPORT.md`
section 3). The vacuum-energy estimate, 1.7e-9 J/m^3, is 8e48 times below rho0.

**Relevance.** A cap on energy, not a source of it; not binding on the shell; the vacuum energy it
estimates is 49 orders of magnitude too small; and the model is not general relativity. Nothing to use.
The list's description is a fair paraphrase of the abstract.

### 2.2 Abou El Dahab, Tawfik, "Measurable Maximal Energy and Minimal Time Interval" (`2014_aboueldahab_tawfik_measurable_maximal_energy_1401.3164.txt`)

gr-qc, 14 January 2014 (l. 37); 16 pages; a Canadian Journal of Physics DOI per the arXiv listing.

**Claim.** The generalised uncertainty principle (GUP) is Heisenberg's relation with an extra Planck-scale
term (eq. 1, l. 58-62). The paper asks what largest energy and smallest time interval can be measured under
it. The linear GUP gives an infinite maximal energy and a negative minimal time, "obviously non-physical"
(l. 108); the quadratic GUP gives Delta E_max = E_Pl/(2 alpha_0) and Delta t_min = alpha_0 hbar/(M_Pl c^2)
(eqs 13-14, l. 123-127); combined with Itzhaki's clock argument on a Schwarzschild background, "both
maximal energy and minimal time have the order of the Planck time" (l. 49; eqs 16-27, l. 163-221). Section
IV.4 (l. 268-286) reviews minimum-mass bounds from a positive cosmological constant (Böhmer and Harko's
M >= Lambda c^2 R^3/(12 G), eq. 35, l. 277-283) and Wesson's "mass quanta". Loop quantum gravity appears
in one sentence of the discussion, as one approach among others (l. 252); the list's description, "loop
quantum gravity's discrete structure dictates a minimum mass quantum", does not describe this paper.

**Scale [mine].** The Planck energy is 1.96e9 J, so Delta E_max for alpha_0 near 1 is about 1e9 J, the
energy of a few hundred kilowatt-hours. The shell's rest energy M c^2 is 4.0e44 J, 2e35 Planck energies.
The minimum-mass bound is a lower bound at cosmological density, far below anything here.

**Relevance.** About the smallest and largest things a single measurement can resolve at the Planck scale.
Nothing about sourcing stress-energy. Not usable.

### 2.3 Ali, Khalil, Vagenas, "Minimal Length in quantum gravity and gravitational measurements" (`2015_ali_khalil_vagenas_minimal_length_gravitational_measurements_1510.06365.txt`)

gr-qc, v2 of 4 November 2015 (l. 33); 7 pages; "to appear in EPL" per the arXiv listing.

**Claim.** A GUP changes Hawking's black-hole temperature (eq. 10, l. 131). The paper asks which modified
Schwarzschild metric reproduces that temperature, takes F(r) = (1 - 2GM/r)(1 + eta (2GM/r)^n) (eq. 15,
l. 147), fixes n = 2 by matching the short-distance Newton law of the Randall-Sundrum model (l. 197-205),
and arrives at F(r) = (1 - 2GM/r)(1 - l_p alpha_0 GM/(2 pi r^2)) (eq. 29, l. 206). It then computes the
corrections to light deflection, Shapiro delay, Mercury's perihelion and gravitational redshift and turns
the measurement accuracies into upper bounds on alpha_0: 1.4e41, 5.8e40, 1.6e35, 2.5e38 (Table 1,
l. 339-349). It notes the modified metric is "a solution of the Einstein equations in a perturbative sense"
(l. 217) with a non-zero right-hand side: "we keep the LHS of the Einstein equations as it is and we assign
the QG corrections to the RHS" (l. 208), G^t_t = G^r_r = +eps GM (4GM - r)/r^5, G^th_th = G^ph_ph =
-eps GM (6GM - r)/r^5, eps = l_p alpha_0/(2 pi) (l. 211-216, c = 1).

**Scale [mine].** This is the one place in the seven where an effective stress-energy is written down. At
the shell's own mass (GM/c^2 = 3.33 m) and r = 20 m, restoring units, rho_eff = (c^4/(8 pi G)) eps
(GM/c^2) (4GM/c^2 - r)/r^5. At the loosest bound in Table 1 (alpha_0 = 1.6e35, eps = 0.41 m) that is
-1.4e37 J/m^3: a thousandth of rho0, and negative everywhere outside r = 4GM/c^2 = 13.3 m. At the
electroweak-scale bound the paper quotes (alpha_0 ~ 1e17, l. 248-249) it is -8.6e18 J/m^3, 21 orders
below; at alpha_0 ~ 1 it is -86 J/m^3. And it presupposes the mass M.

**Relevance.** Tests of quantum-gravity corrections against solar-system data; the effective source is a
correction around a mass that must already exist, and it is far too small. Not usable. One observation
[mine]: reading a stress-energy off a prescribed metric is the same operation the paper under test
performs (`CLAIMS.md` C1, Error 18); here too the authors call the result perturbative rather than matter.

### 2.4 Seveso, Peri, Paris, "Quantum limits to mass sensing in a gravitational field" (`2016_seveso_peri_paris_quantum_limits_mass_sensing_1603.09559.txt`)

gr-qc, v4 of 19 December 2016 (l. 38); "Journal: J. Phys. A" (l. 40); 18 pages.

**Claim.** How precisely can the mass of a quantum particle be estimated from its motion under gravity?
Classically the mass drops out (equivalence principle); quantum mechanically "the Schrödinger equation for
a particle of mass m in an external gravitational field depends parametrically on the ratio hbar/m"
(l. 51), so the mass leaves a trace, and the quantum Fisher information sets the ultimate precision (eq. 8,
l. 80). Results: for free fall the information grows as t^4 (eq. 16, l. 115-118), but position
measurements of the trajectory carry no gravitational information at all (l. 122), "in accordance with the
equivalence principle" (l. 138, 256); coherent superpositions of energy levels (a neutron bouncing on a
mirror, a trapped particle) beat mixtures (l. 159, 255); "More intense gravitational fields allow to
extract, in general, a greater amount of information" (l. 256). "The purpose of the present paper is thus
not to discuss any realistic implementation" (l. 53).

**Scale.** A neutron, 1.7e-24 g (l. 145); nanomechanical oscillators of 1e-21 kg to 1e-12 g (l. 201, 204);
for 1 kg at 1 Hz the quantum enhancement would take "the age of the Universe" (l. 201). The shell:
4.5e27 kg. The list's description matches l. 138 (position measurements of a falling packet).

**Relevance.** Measuring a mass, not making one. Not usable.

### 2.5 Dobkowski et al., "Observation of quantum free fall and the consistency with the equivalence principle" (`2025_dobkowski_quantum_free_fall_equivalence_principle_2502.14535.txt`)

quant-ph, v4 of 7 December 2025 (l. 52); Folman's group at Ben-Gurion with Marletto, Fuentes, Penrose,
Vedral and Schleich (l. 54-80); 58 pages with supplement; CC BY-NC-ND 4.0 (l. 51).

**Claim.** A cloud of about 2e4 rubidium-87 atoms (l. 131) is split into two wave packets: one held still
against gravity by a magnetic gradient, one in free fall for up to 2 ms, up to 7.5 micrometres apart
(l. 97), then recombined. The predicted phase difference is -(m/3 hbar) g^2 T^3 (eq. 2, l. 112), the
quantum phase of a free-falling object predicted since 1927 (l. 91) and equal to the "gauge phase" obtained
by assuming the equivalence principle holds for the wavefunction (eq. 1, l. 102). They see 13 oscillations,
about 80 rad (l. 140), with the cubic law and its prefactor confirmed to a few percent (l. 146): "we have
measured for the first time the quantum phase of a freely-falling object, and at the same time we have
confirmed the phase predicted if the EP is applied to a freely-falling WP" (l. 155). Supplement N: "the
considerations of this paper refer to the gravitational field as a 'passive' background, namely the
Earth's gravitational field, which is not being actively affected by the quantum-mechanical constituents
of the atom" (l. 628); tests of mass as an active gravitational source need "10^9 to 10^10 atomic masses"
in superposition, "six to seven orders of magnitude" beyond today's record (l. 632).

**Scale [mine].** 2e4 Rb-87 atoms are 2.9e-21 kg; one atom is 1.4e-25 kg; the shell is 3e52 atoms. The
phase prefactor m g^2/(6 hbar) for one atom is 2.2e10 rad/s^3.

**Relevance.** A test of how matter waves fall in Earth's field, with gravity as a passive background by
the authors' own statement. Not usable. The list's description is accurate.

### 2.6 Carney, Karydas, Scharnhorst, Singh, Taylor, "On the quantum mechanics of entropic forces" (`2025_carney_quantum_mechanics_entropic_forces_2502.17575.txt`)

hep-th, 24 February 2025 (l. 40); Phys. Rev. X 15, 031038 (2025) per the arXiv listing; CC BY 4.0 (l. 39).

**Claim.** Following Jacobson 1995 and Verlinde 2011 (refs [1], [2], l. 412-414), explicit quantum models in
which "Newton's law of gravity arises from extremization of the free energy of a collection of qubits or
oscillators, rather than from the exchange of virtual quanta of a fundamental field" (l. 56). The guiding
analogy is the ideal gas: the pressure on two pistons is an entropic force mediated by the gas, not by a
field (l. 78-84). Non-local model: qubits whose frequencies depend on the distance between two masses;
with 1/f(x) = lambda + l^2/|x| the thermal force is -(pi^2/12) T^2 l^2 x/|x|^3, and "to match to Newton's
law, we take pi^2 T^2 l^2/12 == G_N m_1 m_2" (eqs 15-17, l. 139-147); "The ontological status of the
identification in Eq. (17) is somewhat uncertain" (l. 148). Local model: a lattice of qubits that a mass
slightly polarises (l. 174-213). Central result: a Lindblad equation for the masses, a coherent Newtonian
interaction plus noise (eq. 40, l. 247; "the central result of this paper", l. 269). Consequences: force
noise of order 1e-24 N/sqrt(Hz) for milligram masses a millimetre apart (l. 301); decoherence of spatial
superpositions, with the lambda = 0 case already excluded by atom interferometers (l. 344); reduced
gravitational entanglement, so that any detection of it "would rule out the entire remaining parameter
space of the local spin entropic model" (l. 400). The construction is "non-relativistic" (l. 85); "Another
[direction] is to find a relativistic version" (l. 406); and "for certain values of the free parameters ...
this kind of entropic interaction can also reproduce the predictions of ordinary virtual graviton exchange,
at least in the non relativistic limit" (l. 403).

**Scale.** Masses in the experiments discussed: 1e-13 kg (l. 391), caesium atoms (l. 318), 1 kg at
cryogenic temperatures (l. 317). The Planck density is quoted as "10^104 J/cm^3" (l. 402).

**Relevance.** The one paper on Carlos's list about where gravity comes from, and its answer bears on his
question in the negative. In every version of the model the force is between masses m_1 and m_2 that are
already present; the medium fixes G_N through its temperature and a length (eqs 17, 23, 33) and supplies
the law, not the mass. Nothing in it lets a region acquire stress-energy, and in Jacobson's relativistic
antecedent, where Einstein's equations themselves emerge, they emerge as equations between geometry and
T_mu_nu, which still has to be there [mine]. Not usable as a source. Usable as a quotable, peer-reviewed
statement for a reader who asks whether the shell's mass could be "emergent": the programme changes the
explanation of attraction, not the accounting of energy.

### 2.7 Guo, Miao, Wang, Yang, Zhou, "Fundamental quantum limits for detecting ultrahigh frequency gravitational waves" (`2026_guo_quantum_limits_ultrahigh_frequency_gw_2501.18146.txt`)

gr-qc, v2 of 26 February 2026 (l. 43); Phys. Rev. D 113, 044020 (2026) per the arXiv listing; 21 pages.

**Claim.** Above 10 kHz there is no astrophysical gravitational-wave foreground (l. 64), and primordial
backgrounds from phase transitions, domain walls and cosmic strings are predicted there. The paper derives
a universal quantum limit for any detector: the wave couples to the detector's stored electromagnetic
energy, H_int = a h E_EM (eq. 2, l. 75-77), and the gain is bounded by the vacuum energy fluctuations of
that stored energy, the "energetic quantum limit" (eq. 3, l. 78-80). Minimum detectable strains follow for
interferometers, microwave cavities and levitated spheres (Table 1, l. 85-138; Fig. 1). "backgrounds in the
kHz-MHz range are in principle observable, whereas higher-frequency signals lie below the quantum limit"
(l. 59), "with all classical noises excluded" (l. 65). Grand-unified phase transitions up to about
1e10 GeV are testable in principle, above that not (l. 195).

**Scale [mine].** A background's energy density is Omega_GW rho_crit, with Omega_GW = 2 pi^2 f^2 h_c^2/
(3 H_0^2) (l. 146). The benchmark peak amplitude is h^2 Omega_p ~ 1.19e-9 (eq. 7, l. 190-191); with
rho_crit/h^2 = 3 H_0^2 c^2/(8 pi G) = 1.69e-9 J/m^3 (H_0 = 100 h km/s/Mpc, l. 146) that is 2.0e-18 J/m^3,
58 orders below rho0. The other way round, not from this paper: for a monochromatic wave's averaged energy
density pi c^2 f^2 h^2/(8 G) (Isaacson) to equal rho0 the strain would be 0.17 at a 10 m wavelength and 5
at 300 m, so no longer a wave on a background; and averaged wave stress-energy is that of radiation,
which is neither static nor a hoop stress.

**Relevance.** Detection limits, not production; the "energy" in it is the detector's stored field energy
and the background's. Not usable.

## 3. What can be used, what cannot, and why

**Can be used, modestly.**

- Carney et al. as the reference for one sentence in the report's interpretation, if a reader asks whether
  the mass could be emergent: current emergent-gravity models reproduce Newton's law between given masses
  in the non-relativistic limit and say nothing about producing stress-energy (section 2.6).
- Two context numbers for the compactness: the shell sits at one sixth of Kauffmann's heuristic cap and at
  3/8 of Buchdahl's bound (2GM/(c^2 R) = 1/3 against 8/9) [mine]. Not needed for any claim.
- Ali et al. as a worked example of reading an effective stress-energy off a prescribed metric and calling
  it a perturbation rather than matter, the move at issue in C1 (section 2.3). A footnote at most.

**Cannot be used, and why.** Seveso et al., Dobkowski et al. and Guo et al. measure gravity or measure with
it; Abou El Dahab and Tawfik bound what one measurement can resolve at the Planck scale; Kauffmann caps
energy rather than supplying it, in a model that is not general relativity; the only effective source any
of them writes down (Ali et al.) is a quantum-gravity correction around an existing mass, at least a
thousand times too small here. The scale gaps are 49 to 58 orders of magnitude for the vacuum and
gravitational-wave densities, and 52 orders in mass for the atoms.

**What general relativity does allow, for orientation; not from these papers and not checked here
[mine].** Einstein's equations accept any stress-energy with rho ~ 1.4e40 J/m^3 and the anisotropy of
`work/shell/RESULTS.md`. The known material-free candidates:

- Pure field energy: B = sqrt(2 mu_0 rho0) = 1.9e17 T or E = sqrt(2 rho0/epsilon_0) = 5.5e25 V/m, against
  magnetar fields of 1e11 T and the Schwinger limit of 4.4e9 T, 1.3e18 V/m. A pure Maxwell field is also
  trace-free, so its pressures sum to its energy density, where the shell's sum to at most 0.85 of the local
  density (note 06 section 2, the trace margin 0.15): a field alone cannot supply the shell's stress state.
- Field plus matter: Bonnor's electrically counterpoised dust (the Majumdar-Papapetrou class), in which
  charge balances gravity with zero pressure at any density. For this shell q/m = sqrt(4 pi epsilon_0 G) =
  8.6e-11 C/kg gives Q = 3.9e17 C and a surface field of 8.7e24 V/m, 7e6 times the Schwinger limit.
- Wheeler's geon, electromagnetic waves held together by their own gravity, known to be unstable.
- The Einstein cluster, done in note 06: two Jupiter masses in orbit at up to 0.46 c.

Each of the first three is my recollection of a standard result, with the shell's numbers put in by hand;
none has been read or computed here. They are reading items if Carlos wants the question pursued, and the
numbers say in advance that none lowers the mass: they only change what the mass is made of.

## 4. Open questions

- Whether a mixed configuration, charged particles in orbit, would lower the orbital speeds of note 06 at
  the price of charge; not computed, and the field strengths above make it a curiosity.
- Whether anyone has published energy-condition results for an electromagnetically supported shell at
  compactness 1/3; not searched.
- Where Carlos's list came from: two of its seven titles do not match the ids, and two descriptions
  do not match the papers (1401.3164's method; 1510.06365 "sets the minimum energy scales for probing
  gravity", where the paper sets upper bounds on a quantum-gravity parameter from classical tests). Lists
  of this kind should be checked id by id, as here, before anything is cited from them.
- Whether to fetch the three candidates in section 3 (Majumdar 1947, Papapetrou 1947, Bonnor 1960s;
  Wheeler 1955) for a short section of the report on what else could, in principle, hold the shell up.
  My recommendation [mine]: not for the comment-window draft; a sentence pointing to note 06 suffices.
