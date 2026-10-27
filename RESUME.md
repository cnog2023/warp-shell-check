# Resume here

**Last session: 27 October 2026.** Parts 2 and 3 of `PLAN.md` section 7a are closed and Part 4 is
begun. State:

- `REPORT.md` at the root is the draft report for the two-week comment window (PLAN section 2 and
  Step 7). It is a draft: Carlos has not yet read it end to end.
- Letters to An T. Le and to Barzegar, Buchert and Vigneron were **sent on 27 October** (note 03 has
  the texts as sent and the Gmail ids), from cmnogueira@heimhero.de through the Gmail connector.
  Carlos had wanted them from cmnogueira@gmail.com and said so minutes after; they cannot be
  recalled. **Rule from now on: nothing outward goes without Carlos naming the sending address, and
  only he sends from gmail.com** (the connector cannot). Replies land in the heimhero.de mailbox; an
  optional two-line note from his personal address is drafted in note 03.
- The letter to Applied Physics (Fuchs, Helmerich) is drafted in note 03 for Carlos to send from
  cmnogueira@gmail.com with `REPORT.md` attached and linked.
- The two WarpFactory issues are drafted in note 10, to be posted by Carlos once the authors have
  answered question 3 of that letter (or declined to).
- Everything else of Parts 1 to 3 is in the three RESULTS files, the register, the wiki and
  `work/wf-reproduction/comparison.xlsx` (the numbers behind the figure pairs).

**Next, on Carlos's word:** his read of `REPORT.md`; the Applied Physics letter sent by him; then
the waiting. When replies arrive (heimhero.de mailbox, or wherever he moves the threads): record each
in the report's appendix, verbatim only with permission; change the text where a reply is right; say
where we disagree and why. After the window: Zenodo DOI (his account), the issues posted, a short
note where the field reads.

## Inputs already on this machine, not in the repository

- `work/matrix/run-fine/slice_f<a>_b<b>.mat` and `run-coarse/`: the Part 1 CI export, gitignored,
  the only copies (artifacts expire). a = 1..4 over compactness {1/3, 1/10, 1/30, 1/100}; fine
  b = 1..11 over shift/compactness {0, 0.02, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.12, 0.15},
  coarse b = 1..6 over shift {0, 0.01, 0.02, 0.04, 0.08, 0.16}. The paper's point is `f1_b5`. Saved
  with `-v7` (SciPy reads them); the y-axis line is column 150 (1-based), x = -0.1 m; `beta` and
  `g33` are uint8 where integral. `profiles_f<a>.csv` next to them are the 1D construction.
- `sources/papers/*.pdf`: local only; Part 3 reads the Fuchs PDF's vector paths with PyMuPDF.
- `.venv`: numpy 2.5.4, scipy 1.18.1, jax 0.10.2, warpax 1.5.1, pymupdf 2.0, openpyxl (JAX: pin
  float64 first; `JAX_PLATFORMS=cpu`).
- `wiki/`: clone of the GitHub wiki, own git repository on `master`; push main first, the figures
  are linked from raw.githubusercontent.
- The Gmail connector: signed into cmnogueira@heimhero.de (business), not his personal address.

## Traps a fresh session would otherwise rediscover

- WarpFactory's `null` and `weak` maps lower indices with the coordinate metric; `strong` and `dominant`
  use Minkowski (C9). Compare against the latter, or the consistent replicas in `exact_conditions.py`.
- WarpFactory's null vectors are k = (1, n)/sqrt 2, so its Null map is half the contraction at the
  normalisation the dense check and warpax's `null_deficit` use (mistaken for a factor two on 26 Oct).
- warpax's `certify_point_lmi` DEC margin is tetrad-dependent in magnitude; compare it by sign.
- The published live script is not the configuration behind the paper's figures (C10): spans 6100
  and 3540 (ratio 1.72) against 7160 and 4000 (1.79); lines sampled every 2 mm through r = 0. Parts 1
  and 2 are at the script's setting; the hoop stress is 0.194 rho0 c^2 there and 0.211 at the figures'.
- Digitising a MATLAB PDF figure: calibrate on the tick marks (short segments in the axes colour),
  not the label boxes, which sit 0.2 pt below them.
- Patching Python through a bash heredoc eats backslashes; use the editor tool or `Write`.
- The two outermost cells on every grid line are stencil artefacts; drop them.
- Same object, same points: the slices are the authors' construction at the script's settings;
  warpax's native `FuchsMetric` is a separate comparison, not a substitute.
- Carlos does not give verdicts that need physics judgement; give him the numbers (a workbook) and
  my judgement with the scale, and ask him only for decisions that are his.
