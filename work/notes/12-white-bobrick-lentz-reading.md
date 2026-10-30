# Note 12: White 2011, Bobrick and Martire 2021, Lentz 2021: anything usable on the energy source?

> **Addendum, 30 October 2026.** At Carlos's request the published version of Lentz's paper (Class.
> Quantum Grav. 38, 075015; received 26 August 2020, revised 29 January 2021, published 9 March 2021,
> 14 pages) was looked at in his DeepDyve rental through Chrome DevTools. The viewer serves page images
> without a text layer and IOP reserves text and data mining and AI rights on it ("All rights,
> including for text and data mining, AI training, and similar technologies, are reserved", page 1
> footer), so no text was extracted; pages 1 and 2 were read as a reader would and compared with the
> arXiv text in `sources/papers-text/`: identical apart from copy-editing (title case, hyphenation,
> the v_s^2/c^2 factors that the arXiv HTML extraction flattens). Carlos: "if the first 2 pages of
> this are the same as arXiv you don't need to screenshot them all." Nothing new; the arXiv version
> and the three refutations of section 2.3 and 2.4 stand as the record.

27 October 2026, afternoon. Carlos asked, after note 11: "What about from these papers below? Anything we
can use if we didn't already?" with three links: NASA NTRS 20110015936, arXiv:2102.06824 and
arXiv:2006.07125. The first is Harold White's "Warp Field Mechanics 101" (NASA Johnson Space Center,
2011; the NTRS file holds the ten-page paper and the 23 slides of his 100 Year Starship Symposium talk of
2 September 2011). The other two were already in `sources/` from 18 October: Bobrick and Martire,
"Introducing Physical Warp Drives" (the framework the Fuchs paper builds on, `INDEX.md` B1) and Lentz,
"Breaking the Warp Barrier" (`INDEX.md` B6). Neither had been read closely here; the index rows came
from the critiques. A fourth paper was fetched because Le cites it against Lentz: Celmaster and Rubin,
"Violations of the Weak Energy Condition for Lentz Warp Drives" (arXiv:2511.18251, November 2025).

Fetching: the NASA PDF is not on arXiv, so `tools/fetch_sources.py` gained a `PDFS` list (url, stem) with
a PyMuPDF text extraction, one `=== page N ===` marker per page; Celmaster and Rubin is a manifest row.
Text files are in `sources/papers-text/`; "l. N" is a line of the named file, "p. N" a page of the NASA
PDF. The slides (pp. 11-33) extract as unmapped glyphs; they were read from rendered page images and are
cited by slide number. Judgements are marked **[mine]**. The question is the one of note 11: could the
stress-energy the Fuchs shell needs (rho0 = 1.3585e40 J/m^3, M = 4.49e27 kg; `REPORT.md` section 3) be
supplied by something other than that much matter in orbit, and does anything here lower the mass?

## 1. The answer for Carlos

Nothing here lowers the mass, and nothing names a source we had not already weighed. White's paper is
about the Alcubierre bubble, whose energy is negative; his finding is that a thicker bubble wall lowers
the peak and total negative energy, and his experiment aims to detect a tiny version of the field with an
interferometer around a ring of capacitors. Bobrick and Martire is the parent of the Fuchs paper: it says
that warp drives are shells of material, that a positive-energy spherical shell can only slow the clocks
inside it, and that "the mass requirements ... are still enormous"; its energy savings are for the
Alcubierre bubble (flatten it, or choose a slower fall-off), not for a massive shell. Lentz is the one
paper in the literature that names a concrete source, a plasma with electromagnetic fields, for a warp
geometry claimed to need only positive energy. Three groups have since shown that the geometry is not a
solution of Einstein's equations with that source and that its energy density is negative in places; the
most recent, Celmaster and Rubin, computed it directly. So the one "field plus matter" proposal on the
table does not stand, and the authors of all three papers put the energy of their objects at a star's or
a planet's mass.

For our shell specifically: White's thick-wall remedy is our smoothing width, and we have already swept
it (`REPORT.md` section 4.2): thicker walls cut the hoop stress but add mass, because the mass is fixed by
the compactness the shift requires, 0.1 of the compactness per unit shift. Bobrick and Martire's
spherical result, that positive energy buys only time dilation, is the qualitative form of that same
finding, and Santiago et al. point out that their own spherical example assumes a pressure-free hollow
fluid shell, the configuration note 02 shows cannot be static. The only thing I would take from this
reading is one sentence for the report: the warp-drive literature's single attempt at an ordinary-matter
source, Lentz's plasma, has been checked by three independent groups and found not to be a solution.

## 2. The papers

### 2.1 White, "Warp Field Mechanics 101" (`2011_white_warp_field_mechanics_101_ntrs_20110015936.txt`)

NASA Johnson Space Center, Eagleworks laboratory (p. 1, p. 8); ten pages of text plus the slide deck.

**Claim.** A review of the Alcubierre metric (eq. 1, p. 2) with three additions. (i) Wall thickness: for a
fixed velocity and radius, "as the warp bubble is allowed to get thicker, the required density is
drastically greatly reduced" and "the integration of the total energy density for the right-most field is
orders of magnitude less that the left-most field" (p. 3); the conclusion calls this "A significant
finding from this effort new to the literature" (p. 9) and adds that the SI conversion "still show[s] that
the idea will not be an easy task" (p. 10); slide 9 qualifies it: "the total energy ... is also reduced,
but to a point. Early indications suggest there is an optimal thickness". (ii) The "canonical form" of the
metric (eq. 4, p. 4) and a boost gamma = cosh(phi) with phi = 1/2 ln|1 - v_s^2 f^2| (p. 5), read as the
driving mechanism: a craft at 0.1 c with a boost of 100 would show "an apparent speed of 10c" (p. 5).
(iii) Mission planning with "an effective negative mass" (p. 7), and the White-Juday interferometer: a
1 cm toroidal test article, "something as simple as a very high-voltage capacitor ring", with "a boost on
the order of 1.0000001" (p. 8); slide 21: "this equates to a velocity of ~0.0004c which could be achieved
potentially with a toroidal ring of plasma", or "a ring of capacitors driven at high voltage". The paper
states plainly that the metric "violates all three energy conditions (strong, weak, and dominant) because
of the need for negative energy density" (p. 9). The Jupiter-to-Voyager energy figures sometimes
attributed to White are not in this document; it gives no total-energy numbers.

**Scale [mine].** The energy is negative, so no comparison of magnitude with our positive shell is
meaningful; the thick-wall scaling is the Alcubierre integral E ∝ v_s^2 R^2/w (Bobrick and Martire eq. 28,
Lentz eq. 23). The laboratory target: by White's own canonical form a boost of 1.0000001 is a metric shift
v_s f = sqrt(1 - e^(2 phi)) = 0.03 inside the centimetre (slide 21 converts the same boost to "0.0004c" by
the rapidity instead). A positive-mass shell carrying a shift of 0.03 needs a compactness of about 0.3
(`REPORT.md` section 4.4, shift at most 0.1 of the compactness), which at a radius of 0.5 cm is
M = 0.3 x 0.005 m x c^2/(2G) = 1e24 kg; the Alcubierre route needs a comparable magnitude of negative
energy. A capacitor ring stores kilojoules, 1e-14 kg. The device is short by about 38 orders of magnitude
on either accounting.

**Relevance.** The thick-wall finding transfers to our shell only as the smoothing width we have swept:
walls from 0.7 to 8.5 m cut the hoop stress from 1.28 to 0.15 rho0 and add mass, 0.03 % to 7.5 %
(`REPORT.md` section 4.2); the mass itself is set by the compactness the shift needs and does not fall. The
source White names, a capacitor ring, is field energy of the kind note 11 section 3 priced. Not usable.

### 2.2 Bobrick and Martire, "Introducing Physical Warp Drives" (`2021_bobrick_martire_introducing_physical_warp_drives_2102.06824.txt`)

Applied Physics (l. 48-50); CQG 38, 105009 (2021) per `INDEX.md` B1. Authors two and six of the Fuchs
paper.

**Claim.** Any warp drive "may be seen as a shell of ordinary or exotic material which fills region D_warp
and moves with some constant velocity" (l. 98); "Warp drives are inertially moving shells of positive or
negative energy material which enclose a 'passenger' region with a flat metric" (l. 219). Section 3 solves
the spherically symmetric case: positive energy forces a Schwarzschild exterior (l. 126); with an
isotropic fluid, P = 0 at both faces and a barotropic equation of state, N(r_in) = N(r_out) (l. 127-134),
so "for a subluminal warp drive based on non-exotic matter, the time inside the drive can only pass more
slowly than it does for a remote Minkowski observer comoving with the drive. For scale, an Earth-mass
shell of 10 meter radius will slow down the rate of time by a small fraction of 4e-4" (l. 135); "the only
type of modification to the internal spacetime that is achievable with purely positive energy for
spherically symmetric warp drives is slowing down the rate of time inside the craft" (l. 227). Energy
savings, all for the Alcubierre bubble's negative energy: flattening by a factor alpha_X divides the
energy by alpha_X (l. 176, 230); the shape function min(r_0/r, 1) saves "about a factor of three"
(l. 231, 277). On sources: propulsion "by an interaction with a bosonic field, or regular gaseous or
plasma material" (l. 224); speculation on ergoregions as "an efficient energy storage" and black-hole-like
regions for "accretion power" (l. 232-233); and the summary "While the mass requirements needed for such
modifications are still enormous at present, our work suggests a method of constructing such objects"
(l. 235). On Lentz: "without providing means to reproduce the study" (l. 76); "Our conclusions do not
support the recent claim" (l. 228).

**What the critiques say.** Santiago et al. Appendix A: "under the set of assumptions they are imposing
(zero pressure at the inner edge of the bubble wall, zero pressure at the outer edge of the bubble wall,
non-negative energy density within the bubble wall, and a barotropic equation of state) the unique
solution to the TOV is the trivial solution p(r) = 0 = rho(r), and the mass of the exterior region must be
zero" (`2022_santiago_...2105.03079.txt` l. 737); their Appendix D calls the one WEC-satisfying case "a
static spherically symmetric spacetime, therefore being reduced to either Minkowski or Schwarzschild"
(l. 799). Barzegar et al. list it under Errors 4, 10, 12, 14 and 27 (`INDEX.md` B1).

**Scale [mine].** The 4e-4 for an Earth mass at 10 m is GM/(c^2 R) = 4.4e-4, consistent. Our shell has
GM/(c^2 R2) = 1/6 and a cavity clock rate of 0.762 (`REPORT.md` section 4.2): the same effect, 400 times
larger, which is what two Jupiter masses in 20 m buy.

**Relevance.** This is where the Fuchs construction's premise comes from, and the hollow-shell point of
note 02 (and warpax's documentation) applies to its section 3 as Santiago et al. state it. The paper's
statement that positive energy buys only time dilation is the qualitative form of our shift ceiling, 0.1
of the compactness, for the one positive-energy shell that has been built numerically [mine]. Its energy
savings are for negative-energy bubbles. Whether flattening would change the shift ceiling of a
positive-mass shell is untested; the mechanism we found, momentum density reaching the energy density in
the inner wall at right angles to the motion (`REPORT.md` section 4.4), does not depend on the shape in
an obvious way, so I would not expect it to, but that is a computation, not a result. Nothing on sources
beyond matter, and no number for the mass other than "enormous".

### 2.3 Lentz, "Breaking the Warp Barrier: Hyper-Fast Solitons in Einstein-Maxwell-Plasma Theory" (`2021_lentz_breaking_the_warp_barrier_2006.07125.txt`)

Göttingen (l. 34); CQG 38, 075015 (2021) per `INDEX.md` B6; arXiv v2 of 10 August 2020 (l. 30).

**Claim.** A class of solitons with flat spatial slices, unit lapse and a shift that is the gradient of a
potential obeying a spatial wave equation, "hyperbolic" rather than Alcubierre's linear or Natário's
elliptic relation (eqs 12-15, l. 85-98). With sources arranged as rhomboids (Fig. 1, l. 121-123) the
Eulerian energy density is "everywhere positive" (l. 125, 132) and the momentum density vanishes (eq. 24,
l. 135-136). The source: "The multi-species stress-energy source of choice in this paper is an electric
plasma consisting of a massive fluid and electromagnetic fields" (l. 138), eq. 26 (l. 144); the trace of
Einstein's equation is used to bound the fluid's equation of state (l. 157); and the paper stops there:
"To further identify a solution of the more than dozen degrees of freedom of the plasma that satisfy the
example soliton ... would require computation beyond the scope of this paper. What can be said here is
that the conditions of the plasma are consistent with the soliton geometry. It is now a matter of finding
the right configuration" (l. 159). Energy: E_tot ~ C v_s^2 R^2/w (eq. 23, l. 129); "for a positive-energy
soliton with central regions radius R = 100 m and average source thickness along the z-axis w = 1 m
approaches a mass equivalent of E_tot ~ (few) x 10^-1 M_sun v_s" (l. 131, repeated l. 163); the Alcubierre
figure quoted for comparison is "-6 x 10^62 v_s/c kg" (l. 41). "The next challenge is to bring the energy
requirements of the positive-energy soliton to the human technological scale" (l. 163).

**What the critiques say.** Santiago et al.: "the author of [1] has not actually solved the Einstein
equations, he has only solved part of the Einstein equations, for the density, flux, and trace of the
stress" (Appendix C, l. 793); "they haven't only not found a solution which satisfies the WEC, they
haven't found a solution at all" (Appendix D, l. 798); and the general theorem that any Natário-class
drive, "yes, it even applies to Lentz/Fell-Heisenberg", violates the null energy condition (l. 699).
Barzegar et al.: "the proposal ('hyperbolic-shift-vector-plasma construction') by Lentz [24] is not a
solution to Einstein's equations" (`2026_barzegar_...2602.16495.txt` l. 1097); the metric "is clearly
below C^2", so "the classical energy conditions have no meaning in this situation" (l. 1187); "Lentz [24]
offers no proof for the claim that the WEC is not violated" (l. 1229). Le: the soliton "was proposed as a
positive-energy alternative but was subsequently shown to violate the NEC [2] and the WEC in the Eulerian
frame [22]" (`2026_le_...2602.18023.txt` l. 272-274). Celmaster and Rubin (section 2.4) computed it.

**Scale [mine].** A few tenths of a solar mass is 2e29 to 6e29 kg for v_s = c, at R = 100 m: one to three
hundred times the Fuchs shell's mass at five times its radius. Lentz's own scaling at the shell's numbers,
v_s = 0.02, R = 20 m, w = 10 m, gives C x 0.016 m, 2e25 kg for C = 1 (times c^2/G = 1.35e27 kg/m), and
5e28 kg at v_s = c. The comparison means little: the energy of an Alcubierre-type bubble falls as v^2
where the shell's mass is fixed by its compactness, and the construction it belongs to is not a solution.

**Relevance.** The one proposal in the literature that names an ordinary source, plasma and fields, for
a positive-energy warp geometry, and so the one paper directly on Carlos's question. Its own text leaves
the plasma configuration to be found (l. 159); three groups find that the geometry is not a solution with
that source and that its energy density goes negative. Not usable as a source; usable as the citation for
"this has been tried".

### 2.4 Celmaster and Rubin, "Violations of the Weak Energy Condition for Lentz Warp Drives" (`2025_celmaster_rubin_wec_violations_lentz_warp_drives_2511.18251.txt`)

arXiv:2511.18251, 23 November 2025 (l. 82); two authors with no institutional address (l. 85-88); no
journal reference. Fetched because Le's reference [22] is this paper.

**Claim.** "We begin with a direct calculation of the energy-momentum tensor of Lentz's warp drive in a
Eulerian reference frame, and show that there are spacetime regions where the energy density is negative.
We then examine the theoretical basis of Lentz's investigation and identify several derivation errors"
(l. 97-101); a modified geometry that respects Lentz's own inequalities "still violates the WEC even in
the Eulerian reference frame" (l. 104-105); for Lentz's original potential "the total energy of the phi_L
warp-spacetime is infinite" (l. 954). Conclusion: "The Lentz warp drive violates the WEC. We have shown
this directly by the numerical computation of the energy density" (l. 1170-1171); "None of this should be
surprising, given that there are no-go theorems ... which state the impossibility of WEC-compliant warp
drives" (l. 1176-1178).

**Relevance.** Closes the Lentz question from a third direction (direct computation, after Santiago's
theorem and Barzegar's analysis). Nothing on sources for our shell. It is the reference to give if the
report mentions the plasma proposal.

## 3. What can be used, what cannot

**Can be used.** One sentence in `REPORT.md` section 4.3 or 5, if Carlos wants it: the literature's one
attempt at an ordinary-matter source for a warp geometry, Lentz's plasma, has been found not to be a
solution by Santiago et al. (2022), Barzegar et al. (2026) and Celmaster and Rubin (2025); our swarm and
the elastic shell remain the only matter models on the table for a positive-energy shell. Also, Bobrick
and Martire's l. 227 as the published statement our shift ceiling quantifies.

**Cannot be used, and why.** White's thick-wall and Bobrick-Martire's flattening and shape savings are
for the Alcubierre bubble's negative energy; for our shell the only analogous knob, the wall width, is
already swept and does not touch the mass. White's capacitor ring and Lentz's plasma are field-energy
sources at 1e-14 kg and an unsolved configuration respectively, against 4.5e27 kg. Bobrick and Martire's
positive-energy spherical example rests on a pressure-free hollow fluid shell, which cannot be static.

## 4. Open questions

- Whether a flattened (oblate) positive-mass shell carries a larger shift than 0.1 of its compactness;
  untested, and a cheap matrix run in WarpFactory's framework if the shell builder allowed it (it does not;
  it would need a new metric function).
- Whether White's later "Warp Field Mechanics 102" (2013) and the Eagleworks interferometer results carry
  numbers worth recording; not fetched. Carlos's "Jupiter" figure may come from there, not from this paper.
- Whether to add Fell and Heisenberg 2021 to the "tried and refuted" sentence; it is in `sources/` and
  treated with Lentz by Santiago et al. (l. 699, 800), not re-read here.
