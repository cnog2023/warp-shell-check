# Note 07: Part 1 (26 October 2026)

Log entry; the write-up is `work/matrix/RESULTS.md`.

- The matrix ran in CI on the authors' configuration with the mass scaled to four compactness
  values and the shift formed by linearity from one unit-shift build per compactness (verified
  exact against a direct build). Two slips on my side cost two failed runs: a variable defined
  after its first use, twice. The concurrency rule cancelled the stale run each time.
- WarpFactory's sampling needs a GPU as shipped (`getEvenPointsOnSphere(..., 1)` hard-coded); a
  one-token shadow copy on the path fixes it. With it the four sampled conditions take 9 s per
  case on the runner's CPU.
- Result: the first failing shift is between 0.09 and 0.10 times the compactness at every
  compactness from 1/3 to 1/100, by three independent readings (WarpFactory's dominant map, a
  dense null check, swarm realisability). The paper's 0.02 passes; its ceiling is 0.030 to 0.033.
  Combined with the strength law of `work/shell/RESULTS.md`, the shift a real material allows is
  about 0.13 times its strength-to-energy ratio: centimetres per second for graphene.
- Found on the way: WarpFactory's Null and Weak maps lower the frame tensor's indices with the
  coordinate metric instead of the Minkowski one its Dominant and Strong branches use. A NumPy
  replica reproduces its map to 1e-16 and the Minkowski version removes the spurious violations.
  At the paper's own point the maps show none, so the published figures stand; above it they fail
  about 1.5 times too early. Candidate upstream issue with a one-line fix. Also: 100 directions
  find the threshold where 4000 do, but underestimate the depth of a violation by about two.
- The wiki went live during the run (six pages); it needs the Part 1 result added, done in the
  same session.
- Part 1B's literature half: Einstein-cluster shells are radially stable where r > 6 m(r)
  (Ostrowski 2025, shell by shell) and in the halo regime (Böhmer and Harko 2007); the swarm on
  the authors' density is marginal only in its outermost skin. The swarm realisability of the warp
  shell's own stress-energy coincides with its Type I region, so the swarm ceiling on the shift is
  the same 0.09 to 0.10 C.

Open after Part 1: warpax's exact energy conditions on the same slices (Part 2), the side-by-side
figures (Part 3), the write-up and contact (Part 4). The Null/Weak finding should go to the
WarpFactory authors as an issue in Part 4, with the replica script.
