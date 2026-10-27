# work/wf-reproduction: the paper's figures next to ours (Step 3, Part 3)

| File | What |
|---|---|
| `side_by_side.py` | Clips Figures 4 to 10 of Fuchs et al. 2024 from the PDF (vector pages rendered at 200 dpi; the paper is CC BY 4.0 on arXiv) into `paper/`, draws ours from the Part 1 slices at the paper's point on the same axes into `ours/`, composes `pairs/figNN_pair.png`, and writes `numbers.csv` (extrema of every curve we draw) |
| `digitise_paper.py` | Reads the paper's curves off the PDF's vector paths, calibrating each panel from its tick labels; writes `paper_curves.csv` (every point, 21 MB, not committed) and `comparison.csv` (extrema, paper against ours). Figure 8 is a raster image in the PDF and is compared by eye only |
| `fit_smoothing.py` | Fits the two moving-average spans of the construction to the paper's digitised smoothed inputs (Figures 4 and 6) with the validated NumPy replica, then predicts the hoop stress and the metric at the fitted spans; writes `fit_smoothing.csv` |
| `make_workbook.py`, `comparison.xlsx` | The numbers behind every pair as a workbook: one sheet per figure with the paper's value and ours at every radius, difference and ratio as formulas, the replica at the fitted smoothing alongside; a Summary sheet; the smoothing fit; Part 2's exact-against-sampled cases. Excel evaluates the formulas on opening (no LibreOffice here to pre-compute them) |
| `RESULTS.md` | The write-up, the verdict per pair, and what the differences turned out to be |

Regenerate (the Fuchs PDF is in `sources/papers/`, local only; the slices and `profiles_f1.csv` in
`work/matrix/run-fine/` are the Part 1 download, `work/matrix/README.md`):

```
.venv\Scripts\python work\wf-reproduction\side_by_side.py
.venv\Scripts\python work\wf-reproduction\digitise_paper.py
.venv\Scripts\python work\wf-reproduction\fit_smoothing.py
```

```
.venv\Scripts\python work\wf-reproduction\make_workbook.py
```

`pymupdf` (PyMuPDF 2.0) and `openpyxl` were added to `.venv` on 27 October 2026 for the PDF and
workbook steps; nothing else needs them.
