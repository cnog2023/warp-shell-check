# Note 06: could rotation hold the shell up? Counter-rotating rings and the Einstein cluster

26 October 2026. Prompted by Carlos: Sagan's machine in *Contact* has counter-rotating rings; could
counter-rotation remove the symmetry objection to rotational support? Script:
`work/shell/einstein_cluster.py`, on the validated 1D replica at the authors' configuration.

## 1. The physics

A single spinning shell is supported only at its equator, bulges, and carries net angular momentum,
so it is neither static nor spherically symmetric. Two rings spinning opposite ways cancel the net
angular momentum. Many rings on many axes, half of them running each way, cancel it and spread the
support over every direction. The continuum limit of that picture is a known exact configuration:
Einstein's 1939 cluster, a static, spherically symmetric swarm of particles on circular geodesics
with randomly oriented orbital planes.

Its properties are what this shell needs. Every particle is in free fall, so no material strength
is involved anywhere. The swarm's stress-energy has zero radial pressure and a tangential pressure
P_t = rho v^2 / 2, with the local orbital speed fixed by the enclosed mass, v^2 = m(r) / (r - 2m(r)).
Because it is a superposition of dust streams it satisfies every pointwise energy condition
automatically, with P_t / rho = v^2 / 2 never above one half. A hollow swarm with an empty cavity is
allowed: the inner particles orbit slowly because little mass lies inside them. The one geometric
constraint is r > 3 m(r) everywhere in the swarm, since circular orbits of massive particles exist
only outside the photon orbit.

So the honest answer to the question is yes, in principle, and with a pedigree: generalised
counter-rotation is the oldest material-free way to hold a shell up in general relativity. It
answers the critique's valid objection that the Fuchs construction names no matter model, with a
model that has no constitutive law to violate.

## 2. Numbers, authors' configuration

| | Fuchs shell as built | Einstein-cluster shell, same density profile |
|---|---|---|
| Radial pressure, peak | 0.077 rho0 c^2 | 0 |
| Tangential pressure, peak | 0.194 rho0 c^2 at r = 10.3 m | 0.066 rho0 c^2 at r = 18.1 m |
| Largest P_t relative to local rho | 0.385 | 0.105 |
| Support mechanism | material strength | orbital motion |
| Orbital speed needed | none | from near 0 at the inner wall to 0.46 c at the outer wall |
| Photon-orbit margin, min of r - 3m(r) in the material | | 5.3 m, comfortable |
| Mass | 4.57e27 kg | the same |

Two further results:

- **The Fuchs stress state itself can be realised by a swarm**, with radial and tangential velocity
  dispersions, if and only if (P_r + 2 P_t) / rho < 1, the trace energy condition, which is stricter
  than the dominant one. At the authors' smoothing the margin is 0.15, and it demands an rms particle
  speed of 0.92 c at the inner wall. For smoothFactor 3000 and below the Fuchs state is not
  realisable by any swarm, although the dominant energy condition still holds down to about 1500.
  The sweep is in the script's output.
- **The hoop-stress spike at the inner wall is a feature of the Fuchs construction, not of the
  problem.** A swarm shell with the same density spreads its support with the enclosed mass and
  needs a third of the peak tangential stress, with none of it radial. The construction's starting
  point, an isotropic-pressure guess, is what puts the stress where it is.

## 3. What it does not change, and what it opens

- The mass. The swarm has the same 4.6e27 kg within 10 to 20 m at 1.5e23 kg/m^3. Material strength
  was impossible; a swarm of two Jupiter masses orbiting at half light speed inside a 20 m shell is
  impossible logistics. The physics is now consistent; the engineering is not closer.
- Collisions. "Collisionless" at that density is a modelling assumption, not a description.
- Stability. Einstein clusters have a known stability literature (relativistic ones can be unstable
  to radial perturbations); not yet read. A reading item for the next part.
- The warp shift. The shift adds a circulating momentum density of up to 0.30 rho0 c^2 at beta =
  0.02. Whether the warp shell's full stress-energy is still swarm-realisable (Hawking-Ellis Type I,
  energy flux below the energy density, trace condition) is a direct check on the exported slices
  and is the second half of this line of work.
- Frame dragging. Counter-rotation cancels the net angular momentum; each ring still drags frames
  locally, and the random-axis average cancels that too. A single pair of rings, as in the novel,
  does not: it is a caricature of the swarm, not an instance of it.

## 4. Where this sits in the project

It is a candidate matter model for Step 6, alongside Le's elastic shell: strength-supported against
motion-supported. It is cheap to compute, entirely within the replica and the exported slices, and
it is the kind of thing the critique's authors would recognise as a legitimate response to Error 18
and the Synge-method objection. References to pull in the next part: Einstein 1939 (Ann. Math. 40,
922), Florides 1974 (Proc. R. Soc. A 337, 529), and a recent stability study of Einstein clusters.
