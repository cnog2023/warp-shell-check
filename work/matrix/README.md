# work/matrix: the allowed shift against compactness (Part 1A)

| File | What |
|---|---|
| `../../matlab/shift_matrix.m` | CI job `matrix`: for each compactness builds the static and the unit-shift shell once, forms every shift by linearity (verified exactly), computes the stress-energy, its Eulerian frame and WarpFactory's sampled energy conditions on the three central planes, exports slices and a summary |
| `../../matlab/shadow/generateUniformField.m` | One-token shim so the sampling honours the CPU flag (WarpFactory hard-codes the GPU) |
| `analyse_matrix.py` | Sampled minima from the summary, a dense null check (4000 directions), Hawking-Ellis type and swarm realisability from the slices; brackets of the first failing shift; figure |
| `verify_null_bug.py` | Replicates WarpFactory's Null evaluation on one slice with the coordinate metric (reproduces its map to 1e-16) and with Minkowski (no spurious violations) |
| `exact_conditions.py` | Part 2: warpax's exact S-lemma margins for all four conditions at every active point of every slice, by two routes (frame tensor with Minkowski; coordinate tensor through WarpFactory's own tetrad, rebuilt and checked); warpax's Hawking-Ellis census and algebraic Type I margins; WarpFactory's sampled maps, with the Null and Weak maps re-evaluated with the consistent metric; per case the miss fraction of the sampled check and the exact threshold bracket next to Part 1's; figure |
| `exact_maps.py` | Part 2 illustration: the central plane at the paper's shift and at the first failing one, as momentum density, exact DEC margin and WarpFactory's sampled Dominant map with the cells only the exact check catches marked |
| `run-coarse/`, `run-fine/` | Downloaded artifacts; `summary.csv` and the analysis csv files (`analysis_*.csv`, `exact_*.csv`) are committed, the slices and profiles are not (`gh run download <id> -n matrix-results -D work/matrix/run-fine`) |
| `RESULTS.md` | The write-up |

Regenerate the analysis (Part 1):

```
.venv\Scripts\python work\matrix\analyse_matrix.py work\matrix\run-fine --png work\matrix\matrix_fine.png
.venv\Scripts\python work\matrix\verify_null_bug.py work\matrix\run-fine 1 7
```

Part 2 (about 30 s per case alone on a laptop CPU; the factors can run as separate processes):

```
.venv\Scripts\python work\matrix\exact_conditions.py work\matrix\run-fine --factors 1,2,3,4
.venv\Scripts\python work\matrix\exact_conditions.py work\matrix\run-fine --summarise --png work\matrix\exact_fine.png
.venv\Scripts\python work\matrix\exact_conditions.py work\matrix\run-coarse --factors 1,2,3,4
.venv\Scripts\python work\matrix\exact_conditions.py work\matrix\run-coarse --summarise
.venv\Scripts\python work\matrix\exact_maps.py work\matrix\run-fine --png work\matrix\exact_maps.png
```

Runs: coarse 40406621961, refined 40411091447.
