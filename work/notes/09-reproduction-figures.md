# Note 09: Part 3 (27 October 2026)

Log entry; the write-up is `work/wf-reproduction/RESULTS.md`.

- The paper's Figures 4 to 10 are y-axis line plots at the paper's point, which the Part 1 slices
  hold (f1_b1 static, f1_b5 at shift 0.02); ours were drawn on the same axes from the grid column at
  x = -0.1 m, the line the earlier shell export used. Seven pairs, all the same picture.
- The arXiv version is CC BY 4.0, so the paper's panels sit in the committed composites with
  attribution. PyMuPDF was installed into `.venv` to clip them; it also exposed the curves as vector
  paths, so the paper's values were digitised exactly (tick-label calibration, residuals 1e-6)
  rather than read by eye. Figure 8 is a raster image, compared by eye.
- Every amplitude in the paper sits 1 to 11 % above ours, more where the feature is sharper. The
  paper's smoothed inputs, its own curves, are narrower than the live script's (inner wall 4.65 m
  against 5.36 m). Fitting the two smoothing spans with the replica gives 6100 and 3540 samples,
  ratio 1.723, the paper's "~1.72", where the code has 1.79 x 4000 and 4000; Figures 4 and 6 give the
  same spans independently. At the fitted spans the replica predicts the hoop-stress spike to 0.14 %,
  the wall width to 3 mm and the g22 peak to 1e-4. The figures' lines carry 14,988 segments from
  r = 0.01 m, so they were sampled every 2 mm through the centre; the script's grid is 0.2 m with no
  centre cell. New register row C10; C8 confirmed from Figure 4 (the closed-form pressure step).
- Carlos asked for the numbers behind the figures in a spreadsheet rather than a visual verdict,
  which a non-physicist cannot give; `comparison.xlsx` holds them. Reading it, he spotted the
  paper's unsmoothed density at 1.7e37 outside the shell where it must be zero: the digitiser's
  tick-label calibration sat 0.2 pt below the tick marks. Recalibrated on the marks, baselines are
  zero to 1e-4 of the axis and the fit misfits dropped from 0.2-0.6 % to 0.02 %. The verdict per
  pair is now numerical, recorded in RESULTS.md section 1.
- Consequence: the hoop stress is 0.211 rho0 c^2 at the figures' smoothing, 0.194 at the script's;
  the shift ceiling was not recomputed at the figures' smoothing (a matrix rerun with smoothFactor
  3540 and a 1.72 shadow of `metricGet_WarpShellComoving.m` would do it).
- A slip on the way: a Python patch applied through a heredoc turned `\tilde` into a tab, the
  backslash trap from the notes in a new form; the editor tool is the right instrument for such
  edits.

Open after Part 3: Carlos's verdict per pair (a column in RESULTS.md); Part 4, the write-up, the
e-mails and the upstream issues, now with C10 as a third question for the authors.
