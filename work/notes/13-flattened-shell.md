# Note 13: the two open items of note 12, tested: a flattened shell, and White 2013

27 October 2026, evening. Carlos: "Can you test both?", meaning the two open questions at the end of
note 12: whether a flattened shell carries more shift than 0.1 of its compactness, and whether White's
2013 follow-up has numbers worth recording. Both done; the first is a computation
(`work/oblate-shell/`, write-up in its `RESULTS.md`), the second a fetch and a reading. Judgements are
marked **[mine]**.

## 1. The answer for Carlos

**Flattening does not buy much, and it cannot buy mass.** Bobrick and Martire flatten the Alcubierre
bubble and divide its (negative) energy by the flattening factor; they guess the same holds for
positive-energy drives. For a massive shell the whole object cannot be flattened by reshaping
coordinates, because the empty space outside a mass has a fixed form and squashing it fills it with
matter; a truly oblate shell is a problem in Einstein's equations nobody has solved, Bobrick and
Martire included. What can be done is to flatten the hole and the inner wall while the outside stays
as it is, and then the mass stays exactly what it was. Doing that, with the paper's own numerical
method, the energy conditions allow the cavity to be flattened or stretched by about 15 to 20 %
before the wall at the poles would have to carry pressure above its energy density. Within that
range a 15 % flattening raises the allowed shift from 0.030-0.032 to 0.033-0.035, about 10 %, and a
15 % stretch lowers it by the same amount; flattening by 20 % brings no further gain because a
second part of the wall fails first. Every reshaped shell also breaks the trace condition at the
polar wall, so none can be held up by the swarm of orbiting particles of note 06; only a material
carrying pressures near its own energy density could. The result of Part 1, a shift of about a
tenth of the compactness, stands within one step.

**White 2013 is a slide deck, and the famous numbers are on one slide.** "Warp Field Mechanics 102:
Energy Optimization" (NASA, 2013; 32 slides, no paper) has the chart behind the "Jupiter to Voyager"
story: for a 10 m bubble at an apparent 10 c, the negative mass the Alcubierre metric needs falls from
about Jupiter's mass at the thinnest wall to about the mass of the asteroid Vesta, 1e20 kg, at the
thickest, within general relativity; the further fall to about a tonne needs "hyperspace
oscillations", an extra-dimensional model White himself introduces with "space-time is really stiff
... Can we further reduce the energy required by reducing the stiffness? Maybe ... but we need to
engage higher dimensional models to do so". Neither step applies to our shell: thickening its walls
is the smoothing we swept (less hoop stress, more mass, never less), and a static shell has nothing
to oscillate. Nothing to use.

## 2. The flattened shell: what was built and what came out

Details and tables in `work/oblate-shell/RESULTS.md`; the log entry:

- The spherical shell was rebuilt in NumPy from the validated profile replica, assembled exactly as
  WarpFactory's `metricGet_WarpShellComoving.m` does (its cubic radial interpolation, its Cartesian
  form, its shift), fed to the ported solver and WarpFactory's Eulerian tetrad: against the CI export
  the metric agrees to 2e-13, the stress-energy to 3e-11 of rho0, and the Part 1 numbers reproduce to
  the printed digits. Each case costs about a minute on the laptop; 40 cases were run.
- The reshaping: the spherical radius in lapse, radial stretch and shift profile replaced by an
  ellipsoidal one inside the shell, axis ratio alpha along the shift for s <= 10 m, returning to 1 by
  20 m, exterior untouched. A first version with the ratio a function of the spherical radius folded
  along the squash axis and produced caustics (energy densities of -200 to -2000 rho0); the ratio
  must be a function of the ellipsoidal radius itself, solved implicitly, which cannot fold. The
  trap and the fix are recorded in `RESULTS.md` §1 and the script's docstring.
- At zero shift: ratios 0.8 to 1.15 pass the four pointwise conditions; 0.7, 0.5 and 1.25 fail the
  dominant condition at the polar inner wall (by 0.18, 0.90 and 3.25 rho0); every reshaped case fails
  the trace condition there (by 0.1 to 1.1 rho0). Moving the transition into the outer wall, so that
  the whole wall is reshaped, gives negative energy density in the equatorial outer wall at zero
  shift (-0.09 rho0 at ratio 0.85), so that family is dead on arrival.
- The ceiling: sphere pass 0.0300 / fail 0.0317; ratio 0.92 pass 0.0300 / fail 0.0333; ratio 0.85
  pass 0.0333 / fail 0.0350; ratio 0.80 pass 0.0300 / fail 0.0333; ratio 1.15 pass 0.0267 / fail
  0.0300. warpax's exact margins confirm the pass and fail at the sphere's and the 0.85 case's
  brackets. The shift adds the same momentum density at every ratio (0.150 rho0 per 0.01 of shift);
  the flattening changes the energy density at the critical site, the equatorial inner wall, by
  about 15 %, which is the whole effect.
- Register: row C11 added to `CLAIMS.md` for Bobrick and Martire's §5.3 conjecture, status result.

## 3. What I would and would not do with it [mine]

- Worth one sentence in the report's section 4.4 or 9: the ceiling is robust to reshaping the cavity
  by ±15 %, and flattening at fixed mass gains about 10 % at most. Not worth a figure there; the
  figure `work/oblate-shell/ceiling_vs_ratio.png` can go to the wiki if Carlos wants it.
- Not worth pursuing further with these tools: the interesting version of the question, an oblate
  shell with its own quadrupolar exterior and possibly less mass, needs a solver for the static
  axisymmetric Einstein equations with a prescribed source, which is a project of its own.

## 4. White 2013, the record (`2013_white_warp_field_mechanics_102_energy_optimization_ntrs_20130011213.txt`)

NTRS 20130011213, fetched through the `PDFS` list of `tools/fetch_sources.py`; 32 pages, all slides;
the formula and chart slides (6, 11, 16, 17) are images whose text does not extract and were read
from rendered pages (`p. N` below is the PDF page).

- Slides 2-5: the interstellar-flight framing of the 2011 paper, repeated.
- Slide 8 (p. 8): "Surface plots of York Time & T00, <v> = 10c, 10 meter diameter volume, variable
  warp 'bubble' thickness ... HOPE: Bubble Topology Optimization".
- Slide 9 (p. 9), read from the image: "As bubble thickness increases, York Time intensity
  decreases", "Changing topology greatly reduces the energy required", "But space-time is really
  stiff: c^4/8 pi G", "Can we further reduce the energy required by reducing the stiffness?
  Maybe... but we need to engage higher dimensional models to do so."
- Slides 11-14 (pp. 11-14): the Chung-Freese brane metric and its null geodesics, as in 2011, and
  the new step: "'Hyperspace' Oscillations ... higher dimensional space-time model can be used to
  alleviate this using the following trick: dU/dt => 1, U = 0, therefore dX/dt => 0 ... Reduces
  stiffness of spacetime!", "if there needs to be large dU/dt with U = 0, then there needs to be
  oscillation in d phi/dt so this will occur repeatedly" (p. 14, image); slide 15: "Oscillate the
  bubble intensity".
- Slide 16 (p. 16), the chart, read from the image: "Exotic Mass Warp Requirements, 10m diameter,
  v_apparent = 10c"; x-axis "Shell Thickness Fraction (2*R/S)" from 1e-5 ("THINNER BUBBLE/RING") to
  1e0 ("THICKER BUBBLE/RING ... no flat space left in bubble"); y-axis "Total exotic mass (kg)" from
  1e0 to 1e28, with reference marks Jupiter 1.9e27, Earth 6.0e24, Moon 7.4e22, 4 Vesta 2.6e20, Nimitz
  carrier 9.1e7, ISS 4.0e5, Dragon, Voyager. Six curves labelled "Bulk Velocity, dU/dt" = 0c, 0.9c,
  0.999c, 0.99999c, 0.9999999c, 0.999999999c, annotated "FASTER HYPERSPACE VELOCITY/OSCILLATIONS".
  The dU/dt = 0 curve, the general-relativity case, runs from about 1e27 kg at the left to about 1e20
  kg at the right; the lowest curve from about 1e10 kg to about 1e3 kg. The credit line reads "graph
  by Dr. Harold 'Sonny' White".
- Slide 17 (p. 17): the White-Juday interferometer, "Generate microscopic warp bubble that perturbs
  optical index by 1 part in 10,000,000"; slides 21-22 an artist's starship and acknowledgements;
  slides 23-31 are excerpts from the 2011 talk.

**Scale [mine].** The general-relativity reduction on the chart, seven orders of magnitude from a
thin to a thick wall, is the E proportional to 1/w of the Alcubierre integral (Bobrick and Martire
eq. 28; Lentz eq. 23); the remaining 17 orders are the extra-dimensional conjecture, for which the
deck gives no equation beyond the Chung-Freese null geodesic. For our shell the same "stiffness"
c^4/(8 pi G) is what converts the construction's curvature into 1.4e40 J/m^3; its wall-thickness knob
is the smoothing width, swept in `work/shell/sweep_smoothing.py`: wider walls lower the hoop stress
and raise the mass (REPORT §4.2), never the reverse, because the mass is fixed by the compactness the
shift needs. There is no oscillation to perform on a static shell.

**Relevance.** The "Jupiter to Voyager" figure is a statement about the Alcubierre bubble's negative
energy under a speculative extra-dimensional mechanism; it has no bearing on the positive mass of
this shell. Not usable. The index row (B6) says where the numbers are.

## 5. Open questions

- The one left open by this test is the one that cannot be done here: a self-consistent oblate shell
  with a quadrupolar vacuum exterior. Carlos could ask Le whether warpax's elastic-shell solver could
  be extended to axisymmetry; that is a question for the comment-window correspondence, not for us.
- The second failure site at |y| = 17.7 m that limits the gain below ratio 0.85 was not mapped in
  detail (which component of the stress-energy loses the dominant condition there); a half-hour with
  the slices if anyone wants it.
