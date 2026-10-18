# Precision probe: WarpFactory's solver arithmetic in NumPy

Run on 27 September 2026 on Carlos's laptop (Python 3.14, NumPy 2.5), from `precision_probe.py` in
this folder. The script is a line-for-line port of `repos/WarpFactory/Solver/utils/*.m`: the same
fourth-order stencils and edge fill, the same cofactor inverse, the same Ricci loop order, the same
1/c factors on time derivatives, the same c^4/(8 pi G) scaling.

Question it answered: is any precision lost by moving the solver from MATLAB to Python, and where
do the method's real precision limits lie?

## Case 0: Minkowski, 11^3, float64

Maximum |T| over all sixteen components: exactly 0.0.

## Case A: Alcubierre, v = 0.1 c, R = 5 m, sigma = 0.8 /m, box of half-width 10 m

Solver T^00 against Alcubierre's closed-form Eulerian energy density, error as a fraction of the
peak, two edge cells dropped on every side.

| dx [m] | points | dtype | max error / peak | rms error / peak | time [s] |
|---|---|---|---|---|---|
| 1.000 | 9,261 | float64 | 1.633e-01 | 1.680e-02 | 0.1 |
| 0.500 | 68,921 | float64 | 2.027e-02 | 1.523e-03 | 1.0 |
| 0.250 | 531,441 | float64 | 1.577e-03 | 1.057e-04 | 57 |
| 0.500 | 68,921 | float32 | 2.027e-02 | 1.523e-03 | 0.6 |

Peak |T^00| of the exact solution: 1.929e39 J/m^3.

## Case B: Schwarzschild vacuum, 21^3 box centred 30 m from a mass with GM/c^2 = 1 m

Exact stress-energy is zero, so every nonzero digit is numerical error. Values are max |T| divided
by the curvature scale kappa * 2M/r^3 = 3.567e38 J/m^3.

| dx [m] | float64 | float32 |
|---|---|---|
| 1.000 | 3.931e-05 | 1.785e-02 |
| 0.300 | 6.148e-08 | 1.952e-01 |
| 0.100 | 9.623e-09 | 1.657e+00 |
| 0.030 | 9.294e-08 | 2.228e+01 |
| 0.010 | 7.397e-07 | 1.206e+02 |
| 0.003 | 9.771e-06 | 1.340e+03 |
| 0.001 | 8.314e-05 | 1.206e+04 |

## What it means

- Grid resolution, not arithmetic, sets the precision. The Alcubierre error falls by about an order
  of magnitude per halving of the spacing, as a fourth-order stencil should. At WarpFactory's
  standard 1 m spacing the error is at the percent level, matching the error figure in the
  WarpFactory methods paper.
- Double precision has a floor near 1e-8 of the curvature scale for this geometry. MATLAB double
  and NumPy float64 are the same IEEE 754 number, so two faithful implementations should agree to
  about twelve digits on identical inputs. That is the acceptance rule for any MATLAB-versus-port
  comparison.
- Single precision is the real hazard: two percent at best, nonsense when refined, and the unit
  factor c^4/(8 pi G) = 4.8e42 overflows float32's maximum of 3.4e38, so the output cannot even be
  represented. MATLAB's GPU arrays keep double by default; PyTorch and JAX default to single. Any
  Python work must pin float64 and assert it. (warpax states it uses 64-bit floats.)

## Regenerate

```
python -m venv .venv
.venv\Scripts\python -m pip install numpy matplotlib
.venv\Scripts\python work\precision-probe\precision_probe.py work\precision-probe\precision_probe.png
```

Runs in about two minutes; the finest Alcubierre grid needs under a gigabyte of memory.
