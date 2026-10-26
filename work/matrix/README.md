# work/matrix: the allowed shift against compactness (Part 1A)

| File | What |
|---|---|
| `../../matlab/shift_matrix.m` | CI job `matrix`: for each compactness builds the static and the unit-shift shell once, forms every shift by linearity (verified exactly), computes the stress-energy, its Eulerian frame and WarpFactory's sampled energy conditions on the three central planes, exports slices and a summary |
| `../../matlab/shadow/generateUniformField.m` | One-token shim so the sampling honours the CPU flag (WarpFactory hard-codes the GPU) |
| `analyse_matrix.py` | Sampled minima from the summary, a dense null check (4000 directions), Hawking-Ellis type and swarm realisability from the slices; brackets of the first failing shift; figure |
| `verify_null_bug.py` | Replicates WarpFactory's Null evaluation on one slice with the coordinate metric (reproduces its map to 1e-16) and with Minkowski (no spurious violations) |
| `run-coarse/`, `run-fine/` | Downloaded artifacts; `summary.csv` and the analysis csv files are committed, the slices and profiles are not (`gh run download <id> -n matrix-results -D work/matrix/run-fine`) |
| `RESULTS.md` | The write-up |

Regenerate the analysis:

```
.venv\Scripts\python work\matrix\analyse_matrix.py work\matrix\run-fine --png work\matrix\matrix_fine.png
.venv\Scripts\python work\matrix\verify_null_bug.py work\matrix\run-fine 1 7
```

Runs: coarse 40406621961, refined 40411091447.
