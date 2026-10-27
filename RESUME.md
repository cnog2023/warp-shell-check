# Resume here

**Last session: 26 October 2026.** Part 1 of `PLAN.md` section 7a is closed: `work/matrix/RESULTS.md`,
`work/notes/07-shift-vs-compactness.md`, register rows C4 (partial), C5 and C9 in `CLAIMS.md`, wiki
updated (Findings section 9). Tree clean at commit 620dfed.

**Next, only on Carlos's word: Part 2.** warpax's exact (S-lemma) energy conditions on the same cases
WarpFactory sampled, closing C4 and C5. Carlos's standing rules are in `PLAN.md` section 7a: one part
per session, each approved separately, no contact with anyone until Part 4, e-mails in
`work/notes/03-email-drafts.md` stay unsent.

## Inputs already on this machine, not in the repository

The slices are gitignored and the GitHub artifacts expire, so these folders are the only copies:

- `work/matrix/run-fine/slice_f<a>_b<b>.mat`: a = 1..4 over compactness {1/3, 1/10, 1/30, 1/100},
  b = 1..11 over shift/compactness {0, 0.02, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.12, 0.15}.
  Saved with `-v7`, so `scipy.io.loadmat` reads them; warpax's `io/warpfactory.py` reads v7 and v7.3.
  Each holds the central-plane Eulerian stress-energy components (`rho`, `p_x`, `p_y`, `p_z`, `P_xx`,
  `P_yy`, `P_zz`, `P_xy`, `P_xz`, `P_yz`), WarpFactory's four condition maps (`null`, `weak`, `strong`,
  `dominant`) and the metric components `g00`, `g01`, `g11`, `g12`, `g22`, `g33`. Grid 300 x 300 at 0.2 m.
  Producer: `matlab/shift_matrix.m` (lines 44-45 name the components, 105-114 save them).
- `work/matrix/run-coarse/`: the earlier, coarser shift set, same format.
- `work/matrix/run-fine/analysis_brackets.csv`: Part 1's pass/fail bracket per compactness and per
  reading. These are the numbers Part 2 compares against. `work/matrix/analyse_matrix.py` produced it.
- `.venv`: numpy 2.5.4, scipy 1.18.1, warpax 1.5.1 (JAX: pin float64 before anything else).
- `wiki/`: a clone of the GitHub wiki, its own git repository on branch `master`; edit, commit and push
  there. The main repository ignores it.

## Traps a fresh session would otherwise rediscover

- WarpFactory's `null` and `weak` maps lower indices with the coordinate metric; `strong` and `dominant`
  use Minkowski (`work/matrix/verify_null_bug.py`, wiki Findings section 8). Compare warpax against the
  dominant and strong maps, or against the replica run with Minkowski, never against the raw null and
  weak maps.
- The eleven shifts per compactness were chosen to bracket the threshold. A finer warpax threshold
  needs new shift values, which means a new run of the `matrix` job in `.github/workflows/matlab.yml`
  (free, but minutes of wall time and a new download: `work/matrix/README.md`).
- The two outermost cells on every grid line are stencil artefacts in vacuum; drop them, as the
  paper does.
- Same object, same points: the slices are the authors' construction at their settings. warpax's
  native `FuchsMetric` carries Le's own regularisation (`INDEX.md`, warpax entry) and is a second,
  separate comparison, not a substitute.

## What Part 2 must leave behind

Per case, warpax's exact verdict and its minimum margin; the fraction of exact violations the sampled
check missed (C4); the exact threshold bracket per compactness next to Part 1's (C5); one new
section in `work/matrix/RESULTS.md`; `CLAIMS.md` rows C4 and C5 closed; wiki Findings section 10,
the C4 and C5 rows in What-We-Are-Probing, one line on Home; `PLAN.md` status block; this file.
