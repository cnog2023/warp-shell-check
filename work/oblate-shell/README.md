# work/oblate-shell: does a flattened shell carry more shift?

Question (Carlos, 27 October 2026, after Bobrick and Martire 2021 §4.2): flattening the Alcubierre
bubble along the direction of motion divides its negative energy by the flattening factor; does
flattening the Fuchs shell raise its shift ceiling, 0.09 to 0.10 times the compactness
(`work/matrix/RESULTS.md` §1)? Write-up: `RESULTS.md`; log entry: `work/notes/13-flattened-shell.md`.

| File | What |
|---|---|
| `oblate_shell.py` | Builds the shell metric in NumPy exactly as `metricGet_WarpShellComoving.m` does (1D profiles from the validated replica `work/shell/replicate_profiles.py`, WarpFactory's cubic Legendre radial interpolation, the twice-smoothed compact sigmoid for the shift), optionally with the spherical radius replaced by an ellipsoidal one inside the shell; computes the stress-energy with WarpFactory's solver arithmetic (`work/precision-probe/precision_probe.py`) on the authors' 300 x 300 x 5 grid at 0.2 m; transforms to the Eulerian frame through WarpFactory's tetrad (`work/matrix/exact_conditions.py`); runs the Part 1 checks (`work/matrix/analyse_matrix.py`: null condition over 4000 directions, Hawking-Ellis type, dominant and trace margins, momentum density) and, with `--exact`, warpax's S-lemma margins |
| `run/alpha_<a>.csv`, `run/log_alpha_<a>.txt` | One row per shift for each axis ratio; the logs are the console lines |
| `run-static2/` | Zero-shift cases over a wider range of axis ratios (which reshapings satisfy the energy conditions at all) |
| `run-static/` | First attempt with the axis ratio a function of the spherical radius; kept because it shows the caustics that construction produces (see `RESULTS.md` §1) |

## The flattened shell

The spherical metric is g_tt = A(r), spatial metric delta_ij + (B(r) - 1) n_i n_j with n the unit
radial vector, shift g_tx = -beta S(r). The flattened one replaces r by the ellipsoidal radius s,
defined implicitly by s^2 = (x/a(s))^2 + y^2 + z^2 with the axis ratio a(s) equal to alpha for
s <= r_a, rising by a quintic step to 1 for s >= r_b (defaults r_a = R1 = 10 m, r_b = R2 = 20 m), and
takes n normal to the surfaces s = const. Outside r_b the metric is the spherical one, so the
exterior stays exactly Schwarzschild and the mass is unchanged; the cavity and inner wall are
flattened along x, the direction of the shift, for alpha < 1 and elongated for alpha > 1. The matter
is whatever Einstein's equations demand of that metric, read off it as the paper itself does.

## Regenerate

```
.venv\Scripts\python work\oblate-shell\oblate_shell.py --validate
.venv\Scripts\python work\oblate-shell\oblate_shell.py --alpha 1.0  --betas 0,0.02,0.02667,0.03,0.03333,0.03667,0.04,0.045,0.05 --out work\oblate-shell\run\alpha_1.0.csv
.venv\Scripts\python work\oblate-shell\oblate_shell.py --alpha 0.85 --betas 0,0.02,0.02667,0.03,0.03333,0.03667,0.04 --out work\oblate-shell\run\alpha_0.85.csv
.venv\Scripts\python work\oblate-shell\oblate_shell.py --alpha 1.15 --betas 0,0.02,0.02667,0.03,0.03333,0.03667,0.04 --out work\oblate-shell\run\alpha_1.15.csv
.venv\Scripts\python work\oblate-shell\oblate_shell.py --summarise work\oblate-shell\run
```

`--validate` rebuilds the spherical shell at the paper's point and compares it with WarpFactory's
own CI export (`work/matrix/run-fine/slice_f1_b1.mat`, `slice_f1_b5.mat`): metric components agree
to 2e-13, the Eulerian stress-energy to 3e-11 of rho0, and the checks reproduce Part 1's numbers
(null minimum, Type I fraction, momentum density) to the printed digits. Each case takes about a
minute on a laptop; `--exact` adds warpax's margins (about a minute more per case; JAX in float64,
`JAX_PLATFORMS=cpu`). The static sweep: `--alpha <a> --betas 0 --out run-static2\alpha_<a>_10_20.csv`,
and `--ra 16 --rb 26` for the variant with the transition in the outer wall.
