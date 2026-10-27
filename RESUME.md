# Resume here

**Last session: 27 October 2026.** Parts 2 and 3 of `PLAN.md` section 7a are closed. Part 2:
`work/matrix/RESULTS.md` section 7, note 08, C4 and C5 closed. Part 3: `work/wf-reproduction/RESULTS.md`,
note 09, the paper's Figures 4 to 10 next to ours (`pairs/`), register rows C2 and C8 extended and
C10 added. Wiki updated with figures for both (Findings sections 10 and 11). The "same picture" verdict per
pair is numerical (Carlos declined a visual one as beyond a non-physicist; he wants numbers and my
judgement with the reasoning): `work/wf-reproduction/RESULTS.md` section 1 and `comparison.xlsx`.

**Next, only on Carlos's word: Part 4.** The write-up (PLAN section 2: about ten pages from the
notes and the three RESULTS files), the e-mails (drafts in `work/notes/03-email-drafts.md`, to be
revised with Parts 1 to 3: the shift ceiling, the exact check, the figures' smoothing), the two
WarpFactory issues (GPU flag in `generateUniformField.m`; Null and Weak maps lowered with the
coordinate metric, with `work/matrix/verify_null_bug.py` as the replica), and the question C10 to the
authors (which smoothing and grid produced Figures 4 to 10). Carlos's standing rules are in `PLAN.md`
section 7a: one part per session, each approved separately, everything outward in his name and sent
by him, illustrations in the wiki with each part.

## Inputs already on this machine, not in the repository

The slices are gitignored and the GitHub artifacts expire, so these folders are the only copies:

- `work/matrix/run-fine/slice_f<a>_b<b>.mat`: a = 1..4 over compactness {1/3, 1/10, 1/30, 1/100},
  b = 1..11 over shift/compactness {0, 0.02, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.12, 0.15}.
  The paper's own point is `f1_b5` (beta = 0.02), the first failing shift `f1_b9`. Saved with `-v7`,
  so `scipy.io.loadmat` reads them. Each holds the central-plane Eulerian stress-energy components
  (`rho`, `p_x`, `p_y`, `p_z`, `P_xx`, `P_yy`, `P_zz`, `P_xy`, `P_xz`, `P_yz`; contravariant, orthonormal
  Eulerian frame, `Analyzer/doFrameTransfer.m`), WarpFactory's four condition maps (`null`, `weak`,
  `strong`, `dominant`) and the metric components `g00`, `g01`, `g11`, `g12`, `g22`, `g33`. Grid
  300 x 300 at 0.2 m; the y-axis line is column 150 (1-based), x = -0.1 m. `beta` and `g33` are
  stored as uint8 where integral; cast before arithmetic. `profiles_f<a>.csv` next to them are the
  1D construction (r, rho, rhosmooth, P, Psmooth, M, A, B).
- `work/matrix/run-coarse/`: the earlier, coarser shift set {0, 0.01, 0.02, 0.04, 0.08, 0.16}.
- `sources/papers/*.pdf`: the papers, local only (gitignored); `sources/papers-text/` the greppable
  text. Part 3 reads the Fuchs PDF's vector paths with PyMuPDF.
- `.venv`: numpy 2.5.4, scipy 1.18.1, jax 0.10.2, warpax 1.5.1, pymupdf 2.0 (JAX: pin float64 before
  anything else; `JAX_PLATFORMS=cpu`).
- `wiki/`: a clone of the GitHub wiki, its own git repository on branch `master`; edit, commit and push
  there. The main repository ignores it. Figures are linked as
  `https://raw.githubusercontent.com/cnog2023/warp-shell-check/main/work/...`, so the main repository
  must be pushed before the wiki page that shows them.

## Traps a fresh session would otherwise rediscover

- WarpFactory's `null` and `weak` maps lower indices with the coordinate metric; `strong` and `dominant`
  use Minkowski (`work/matrix/verify_null_bug.py`, wiki Findings section 8). The paper's Figures 7
  and 10 carry the same inconsistency (their Null plateau is 2.8e39 where Strong reaches 7.1e39).
  Compare against the dominant and strong maps, or against the consistent replicas in
  `exact_conditions.py` (`wf_observers`, `sampled_min`), never against the raw null and weak maps.
- WarpFactory's null vectors are k = (1, n)/sqrt 2, so its Null map is half the contraction at the
  k = (1, n) normalisation that the dense check and warpax's `null_deficit` use. Its timelike vectors
  are Euclidean-normalised at ten speeds (`generateUniformField.m`), so Weak and Strong are comparable
  by sign only.
- warpax's `certify_point_lmi` NEC, WEC and SEC margins are tetrad-invariant; the DEC value is not
  (flux margin divided by `max |T_hat|`). Compare DEC by sign.
- **The published live script is not the configuration behind the paper's figures** (C10): the
  figures' smoothing spans are 6100 and 3540 samples (ratio 1.72) against the script's 7160 and
  4000 (1.79), and their lines are sampled every 2 mm through r = 0. Everything in Parts 1 and 2 is
  at the script's setting; the hoop stress is 0.194 rho0 c^2 there and 0.211 at the figures'. A
  matrix rerun at the figures' smoothing needs smoothFactor 3540 and a shadow copy of
  `metricGet_WarpShellComoving.m` with 1.72 in place of 1.79.
- The two outermost cells on every grid line are stencil artefacts in vacuum; drop them. The
  remaining noise is about 1e-7 rho0 and sits outside the shell (r = 27 m).
- Patching Python through a bash heredoc eats backslashes (`\tilde` became a tab on 27 October); use
  the editor tool or `Write` for such edits.
- Same object, same points: the slices are the authors' construction at the script's settings.
  warpax's native `FuchsMetric` carries Le's own regularisation (`INDEX.md`, warpax entry) and is a
  second, separate comparison, not a substitute.

## What Part 4 must leave behind

The report (`docs/` or the repository root, Markdown, about ten pages, every number sourced), the
revised e-mails in `work/notes/03-email-drafts.md` for Carlos to send from his own mailbox, the two
upstream issue texts with the replica script, `CLAIMS.md` with every row's final status, the wiki's
Home and The-Question brought to the report's state, `PLAN.md` Step 7 status, this file, and the
Zenodo step for Carlos once the comment window closes.
