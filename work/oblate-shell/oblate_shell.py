"""
oblate_shell.py -- does a flattened (oblate) shell carry more shift than the spherical one? (note 13)

Question (Carlos, 27 October 2026, after Bobrick and Martire 2021 section 4.2, where flattening the
Alcubierre bubble along the direction of motion divides its negative energy by the flattening factor):
does flattening the Fuchs shell raise its shift ceiling, 0.09 to 0.10 times the compactness
(work/matrix/RESULTS.md section 1)?

Construction. The spherical shell is WarpFactory's metricGet_WarpShellComoving.m, assembled here in
NumPy from the validated 1D replica (work/shell/replicate_profiles.py): g_tt = A(r), spatial metric
delta_ij + (B(r) - 1) n_i n_j with n the unit radial vector (what sph2cartDiag.m computes), the shift
g_tx = -beta S(r) with S the twice-smoothed compact sigmoid, radial values by WarpFactory's own cubic
Legendre interpolation on the 1e5-point profile. The flattened shell replaces r by the ellipsoidal
radius s = sqrt((x/a(r))^2 + y^2 + z^2) in A, B and S and takes n normal to the ellipsoids s = const,
with a(r) = alpha for r <= r_a rising smoothly (quintic step, C^2) to 1 for r >= r_b, so that outside
the shell the metric is exactly the spherical Schwarzschild one (a squashed exterior would not be
vacuum). alpha < 1 flattens the cavity and inner wall along x, the direction of the shift; alpha > 1
elongates them. The stress-energy follows from Einstein's equations by WarpFactory's own solver
arithmetic (work/precision-probe/precision_probe.py, fourth-order finite differences, the authors'
300 x 300 x 5 "cartoon" grid at 0.2 m), on the central plane with two edge cells dropped, then the
Eulerian frame through WarpFactory's tetrad (work/matrix/exact_conditions.py). This is reverse
engineering in the paper's own sense: the metric is prescribed and the matter is read off it.

Checks per case, as in work/matrix/analyse_matrix.py: the null condition minimised over 4000 null
directions; the Hawking-Ellis type and, at Type I points, the dominant-condition margin rho - max|p|
and the trace margin; the largest Eulerian momentum density; the energy density minimum. Optionally
(--exact) warpax's S-lemma margins for the four conditions at every active point.

Usage:
  python oblate_shell.py --validate                     # alpha = 1 against the CI slices f1_b1, f1_b5
  python oblate_shell.py --alpha 0.7 --betas 0,0.02,0.03 --out run/alpha_0.7.csv [--exact]
  python oblate_shell.py --summarise run                # brackets per alpha from the csv files
Options: --ra 10 --rb 20 (squash transition radii), --grid 300 (cells per side; 5 in z), --dx 0.2.
"""
import argparse
import csv
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
for sub in ("precision-probe", "shell", "matrix"):
    sys.path.insert(0, str(ROOT / "work" / sub))
import precision_probe as pp                                   # noqa: E402
import replicate_profiles as rp                                # noqa: E402
from analyse_matrix import ETA, NOISE, bracket, fibonacci_sphere, nec_dense, type_and_swarm   # noqa: E402
from exact_conditions import wf_eulerian_matrix                # noqa: E402

G, c = rp.G, rp.c
R1, R2 = 10.0, 20.0
SMOOTH = 4000
FACTOR = 1.0 / 3.0
EDGE = 2
N_DIRS = 4000
ACTIVE = 1e-6
RHO_FLOOR = 1e-2        # |j|/rho is reported where rho > RHO_FLOOR * rho0


# ---------------------------------------------------------------- WarpFactory's 1D pieces
def compact_sigmoid(r, R1, R2, sigma=0.0, Rbuff=0.0):
    """compactSigmoid.m: 1 inside R1 + Rbuff, 0 outside R2 - Rbuff, a smooth fall in between."""
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        expo = ((R2 - R1 - 2 * Rbuff) * (sigma + 2)) / 2 * (1.0 / (r - R2 + Rbuff) + 1.0 / (r - R1 - Rbuff))
        core = np.nan_to_num(1.0 / (np.exp(expo) + 1.0), nan=0.0)
    inside = (r > R1 + Rbuff) & (r < R2 - Rbuff)
    return np.abs(np.where(inside, core, 0.0) + (r >= R2 - Rbuff) - 1.0)


def legendre_interp(arr, idx):
    """legendreRadialInterp.m, vectorised: cubic Lagrange on the four samples around the fractional
    1-based index idx. At an integer idx MATLAB's formula is 0/0; the sample itself is returned there."""
    x0 = np.floor(idx - 1)
    x1 = np.floor(idx)
    x2 = np.ceil(idx)
    x3 = np.ceil(idx + 1)
    y = [arr[np.clip(xk, 1, arr.size).astype(int) - 1] for xk in (x0, x1, x2, x3)]
    x = idx
    with np.errstate(divide="ignore", invalid="ignore"):
        out = (y[0] * (x - x1) * (x - x2) * (x - x3) / ((x0 - x1) * (x0 - x2) * (x0 - x3))
               + y[1] * (x - x0) * (x - x2) * (x - x3) / ((x1 - x0) * (x1 - x2) * (x1 - x3))
               + y[2] * (x - x0) * (x - x1) * (x - x3) / ((x2 - x0) * (x2 - x1) * (x2 - x3))
               + y[3] * (x - x0) * (x - x1) * (x - x2) / ((x3 - x0) * (x3 - x1) * (x3 - x2)))
    return np.where(x1 == x2, y[1], out)


def fractional_index(rsample, r):
    """metricGet_WarpShellComoving.m: nearest sample at or below r, plus the linear fraction, 1-based."""
    dr = rsample[1] - rsample[0]
    n = np.clip(np.floor(r / dr).astype(int), 0, rsample.size - 2)
    return n + 1 + (r - rsample[n]) / (rsample[n + 1] - rsample[n])


class Profiles:
    def __init__(self, smooth=SMOOTH, factor=FACTOR):
        d = rp.build(smoothFactor=smooth, factor=factor)
        self.r = d["r_m"]
        self.A = d["A_g00"]
        self.B = d["B_grr"]
        S = compact_sigmoid(self.r, R1, R2)
        self.S = rp.matlab_smooth(rp.matlab_smooth(S, smooth), smooth)
        self.M = d["m"]
        self.rho_peak = d["rhosmooth_kg_m3"].max() * c ** 2
        self.M_smooth = d["M_kg"][-1]

    def at(self, s):
        idx = fractional_index(self.r, s)
        return legendre_interp(self.A, idx), legendre_interp(self.B, idx), legendre_interp(self.S, idx)


# ---------------------------------------------------------------- grid, squash, metric
def grid(n, nz, dx):
    centre = (n + 1) / 2 * dx
    cz = (nz + 1) / 2 * dx
    x = np.arange(1, n + 1) * dx - centre
    z = np.arange(1, nz + 1) * dx - cz
    X, Y, Z = np.meshgrid(x, x, z, indexing="ij")
    return x, z, X, Y, Z


def axis_ratio(s, alpha, ra, rb):
    """a(s): alpha for s <= ra, 1 for s >= rb, a quintic (C^2) step between; and da/ds."""
    t = np.clip((s - ra) / (rb - ra), 0.0, 1.0)
    w = t ** 3 * (10 - 15 * t + 6 * t ** 2)
    dw = 30 * t ** 2 * (1 - t) ** 2 / (rb - ra)
    return alpha + (1 - alpha) * w, (1 - alpha) * dw


def squash(X, Y, Z, alpha, ra, rb, iters=60):
    """Ellipsoidal radius s, defined implicitly by s^2 = (x/a(s))^2 + y^2 + z^2 with the axis ratio a
    a function of s itself, and the unit normal to the surfaces s = const. For alpha < 1 the function
    f(s) = s^2 - x^2/a(s)^2 - y^2 - z^2 is increasing (f' = 2s + 2x^2 a'/a^3 > 0), so the root is unique
    and the surfaces never fold; bisection on [r min(1, 1/alpha), r max(1, 1/alpha)]. (With the ratio
    taken as a function of the spherical radius r instead, s stalls or folds along the squash axis once
    (1 - alpha) is large, and the metric develops caustics: the first version of this script did that.)
    For alpha > 1 the sign of f' is checked and the number of points where it fails is returned."""
    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    lo = r * min(1.0, 1.0 / alpha)
    hi = r * max(1.0, 1.0 / alpha)
    yz2 = Y ** 2 + Z ** 2
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        a, _da = axis_ratio(mid, alpha, ra, rb)
        f = mid ** 2 - (X / a) ** 2 - yz2
        lo = np.where(f < 0, mid, lo)
        hi = np.where(f < 0, hi, mid)
    s = 0.5 * (lo + hi)
    a, da = axis_ratio(s, alpha, ra, rb)
    denom = s + X ** 2 * da / a ** 3                 # (1/2) df/ds at the root
    folds = int((denom <= 0).sum())
    gx = X / a ** 2 / denom
    gy = Y / denom
    gz = Z / denom
    norm = np.sqrt(gx ** 2 + gy ** 2 + gz ** 2)
    return s, gx / norm, gy / norm, gz / norm, folds


def metric(prof, X, Y, Z, alpha, ra, rb, beta):
    s, nx, ny, nz, folds = squash(X, Y, Z, alpha, ra, rb)
    if folds:
        print(f"WARNING: the ellipsoidal radius folds at {folds} grid points (alpha {alpha}); results there are meaningless", flush=True)
    A, B, S = prof.at(s)
    n = [nx, ny, nz]
    g = pp.zeros_metric(X.shape, np.float64)
    g[0][0] = A.copy()
    g[0][1] = -beta * S
    g[1][0] = g[0][1]
    for i in range(3):
        for j in range(i, 3):
            g[i + 1][j + 1] = (1.0 if i == j else 0.0) + (B - 1.0) * n[i] * n[j]
            g[j + 1][i + 1] = g[i + 1][j + 1]
    return [[gij[None] for gij in row] for row in g], s[None]


# ---------------------------------------------------------------- the plane, in the Eulerian frame
def plane_tensors(g, T, k, edge):
    sl = slice(edge, -edge)
    shape = g[0][0][0, sl, sl, k].shape
    n = shape[0] * shape[1]
    gl = np.empty((n, 4, 4))
    Tu = np.empty((n, 4, 4))
    for i in range(4):
        for j in range(4):
            gl[:, i, j] = g[i][j][0, sl, sl, k].ravel()
            Tu[:, i, j] = T[i][j][0, sl, sl, k].ravel()
    Tcov = np.einsum("nab,nbc,ncd->nad", gl, Tu, gl)
    M = wf_eulerian_matrix(gl)
    That_cov = np.einsum("nia,nij,njb->nab", M, Tcov, M)
    That_up = ETA @ That_cov @ ETA                       # doFrameTransfer.m: T^{0i} = -T_{0i}
    return gl, That_up, shape


def analyse(That, rho0, x, y, dirs):
    """The matrix analysis on one plane (contravariant frame tensor, points x points)."""
    n = That.shape[0]
    act = np.abs(That).reshape(n, -1).max(axis=1) > ACTIVE * rho0
    Ta = That[act]
    rho = Ta[:, 0, 0]
    j = np.sqrt((Ta[:, 0, 1:] ** 2).sum(axis=1))
    dense = nec_dense(Ta, dirs)
    typeI, rho_rest, tec, dec = type_and_swarm(Ta, rho0)
    with np.errstate(invalid="ignore", divide="ignore"):
        jr = np.where(rho > RHO_FLOOR * rho0, j / rho, np.nan)
    XX, YY = np.meshgrid(x, y, indexing="ij")
    xa, ya = XX.ravel()[act], YY.ravel()[act]

    def worst(v):
        """minimum of v over the active points and where it sits (x, y)."""
        if not np.isfinite(v).any():
            return np.nan, np.nan, np.nan, -1
        i = int(np.nanargmin(v))
        return float(v[i]), float(xa[i]), float(ya[i]), i

    nec_min, x_nec, y_nec, _ = worst(dense / rho0)
    dec_min, x_dec, y_dec, i_dec = worst(dec)
    tec_min, x_tec, y_tec, i_tec = worst(tec)
    rec = dict(n_active=int(act.sum()),
               rho_min=float(rho.min() / rho0), rho_max=float(rho.max() / rho0),
               nec_dense=nec_min, x_nec=x_nec, y_nec=y_nec,
               typeI_frac=float(typeI.mean()), n_not_typeI=int((~typeI).sum()),
               dec_typeI_min=dec_min, x_dec=x_dec, y_dec=y_dec,
               tec_min=tec_min, x_tec=x_tec, y_tec=y_tec,
               j_max=float(j.max() / rho0), j_over_rho_max=float(np.nanmax(jr)) if np.isfinite(jr).any() else np.nan)
    if (~typeI).any():
        k = int(np.argmax(~typeI))
        rec.update(x_not_typeI=float(xa[k]), y_not_typeI=float(ya[k]))
    # principal values (rest-frame energy density and pressures, in units of rho0) at the worst trace point
    if i_tec >= 0:
        lam = np.sort(np.linalg.eigvals(Ta[i_tec] @ ETA).real) / rho0
        rr = rho_rest[i_tec]
        p = np.delete(lam, int(np.argmin(np.abs(lam + rr))))
        rec.update(rho_at_tec=float(rr), p_min_at_tec=float(p.min()), p_max_at_tec=float(p.max()))
    # a point fails if it is not Type I (no rest frame) or its DEC margin is below the noise band
    fail = (~typeI) | (np.nan_to_num(dec, nan=-np.inf) < -NOISE)
    rec["n_fail_dec"] = int(fail.sum())
    dec_floor = dec_min if np.isfinite(dec_min) else -1.0
    rec["dec_margin"] = min(dec_floor, -1.0 if (~typeI).any() else 0.0)   # -1: some point has no rest frame
    return rec, act


def plane_mass(That, rho0, x, y, dx, act=None):
    """Mass from the Eulerian energy density on the central plane, using the axisymmetry about x:
    the plane z = 0 contains the symmetry axis and |y| is the cylindrical radius."""
    XX, YY = np.meshgrid(x, y, indexing="ij")
    rho = That[:, 0, 0].reshape(XX.shape)
    # the plane covers both half-planes y < 0 and y > 0, each a full set of meridional half-planes,
    # so the volume weight is pi |y|, not 2 pi |y|; at alpha = 1 this returns the smoothed mass
    return float((rho * np.pi * np.abs(YY)).sum() * dx * dx / c ** 2)


def exact_margins(That, rho0):
    from exact_conditions import in_chunks, warpax_functions
    jax, jnp, cert_eta, cert_g, floor_eta, classify, algebraic = warpax_functions()
    n = That.shape[0]
    act = np.abs(That).reshape(n, -1).max(axis=1) > ACTIVE * rho0
    That_cov = ETA @ That[act] @ ETA
    ex = in_chunks(cert_eta, jnp, That_cov)
    out = {f"ex_{k}": float(ex[k].min() / rho0) for k in ("nec", "wec", "sec", "dec")}
    out["ex_nulldef"] = 2 * out["ex_nec"]
    out["n_ex_dec_fail"] = int((ex["dec"] < -NOISE * rho0).sum())
    return out


# ---------------------------------------------------------------- runs
def run_case(prof, X, Y, Z, x, dx, alpha, ra, rb, beta, rho0, dirs, exact=False):
    t0 = time.time()
    g, s = metric(prof, X, Y, Z, alpha, ra, rb, beta)
    T = pp.met2den(g, [1.0, dx, dx, dx])
    k = X.shape[2] // 2
    gl, That, shape = plane_tensors(g, T, k, EDGE)
    xi = x[EDGE:-EDGE]
    rec, act = analyse(That, rho0, xi, xi, dirs)
    rec.update(alpha=alpha, ra=ra, rb=rb, beta=beta, beta_over_C=beta / FACTOR, rho0=rho0,
               mass_plane_kg=plane_mass(That, rho0, xi, xi, dx), t_s=time.time() - t0)
    if exact:
        rec.update(exact_margins(That, rho0))
    return rec, That, gl, shape


def write_rows(path, rows):
    keys = sorted({k for r in rows for k in r})
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def validate(args):
    """alpha = 1: the NumPy assembly and solver against WarpFactory's CI export on the same grid."""
    from scipy.io import loadmat
    prof = Profiles()
    x, z, X, Y, Z = grid(args.grid, 5, args.dx)
    dirs = fibonacci_sphere(N_DIRS)
    run = ROOT / "work" / "matrix" / "run-fine"
    for case, beta in (("slice_f1_b1.mat", 0.0), ("slice_f1_b5.mat", 0.02)):
        s = loadmat(run / case)
        rho0 = float(np.squeeze(s["rho0"]))
        rec, That, gl, shape = run_case(prof, X, Y, Z, x, args.dx, 1.0, args.ra, args.rb, beta, rho0, dirs)
        sl = slice(EDGE, -EDGE)
        print(f"== {case}: beta = {beta}, rho0 (export) = {rho0:.6e} J/m^3, replica peak {prof.rho_peak:.6e}")
        for key, (i, j) in (("g00", (0, 0)), ("g01", (0, 1)), ("g11", (1, 1)), ("g12", (1, 2)), ("g22", (2, 2)), ("g33", (3, 3))):
            ref = np.asarray(s[key], dtype=float)[sl, sl].ravel()
            d = np.abs(gl[:, i, j] - ref).max()
            print(f"   metric {key}: max |diff| = {d:.3e}")
        comp = {"rho": (0, 0), "p_x": (0, 1), "p_y": (0, 2), "P_xx": (1, 1), "P_yy": (2, 2), "P_zz": (3, 3), "P_xy": (1, 2)}
        for key, (i, j) in comp.items():
            ref = np.asarray(s[key], dtype=float)[sl, sl].ravel()
            d = np.abs(That[:, i, j] - ref).max() / rho0
            print(f"   frame {key}: max |diff| / rho0 = {d:.3e}   (export range {ref.min() / rho0:+.4f} .. {ref.max() / rho0:+.4f})")
        print(f"   checks: nec_dense {rec['nec_dense']:+.3e}, typeI {rec['typeI_frac']:.6f}, dec_typeI_min {rec['dec_typeI_min']:+.3e}, "
              f"j_max {rec['j_max']:.4f}, mass_plane {rec['mass_plane_kg']:.4e} kg (construction M {prof.M:.4e}, smoothed {prof.M_smooth:.4e}), {rec['t_s']:.0f} s")


def scan(args):
    prof = Profiles()
    n = args.grid if args.alpha <= 1 else int(np.ceil(2 * (args.alpha * R2 + 10) / args.dx))
    x, z, X, Y, Z = grid(n, 5, args.dx)
    dirs = fibonacci_sphere(N_DIRS)
    rho0 = args.rho0 if args.rho0 else prof.rho_peak
    rows = []
    for beta in [float(b) for b in args.betas.split(",")]:
        rec, That, gl, shape = run_case(prof, X, Y, Z, x, args.dx, args.alpha, args.ra, args.rb, beta, rho0, dirs, exact=args.exact)
        rec["grid"] = n
        rows.append(rec)
        print(f"alpha {args.alpha:.3f} ra {args.ra:.0f} rb {args.rb:.0f} beta {beta:.4f} (beta/C {rec['beta_over_C']:.3f}): rho_min {rec['rho_min']:+.2e} "
              f"nec {rec['nec_dense']:+.3e} at ({rec['x_nec']:+.1f},{rec['y_nec']:+.1f}) typeI {rec['typeI_frac']:.5f} "
              f"dec {rec['dec_typeI_min']:+.3e} at ({rec['x_dec']:+.1f},{rec['y_dec']:+.1f}) tec {rec['tec_min']:+.3e} at ({rec['x_tec']:+.1f},{rec['y_tec']:+.1f}) "
              f"[rho {rec.get('rho_at_tec', np.nan):.3f} p {rec.get('p_min_at_tec', np.nan):+.3f}..{rec.get('p_max_at_tec', np.nan):+.3f}] "
              f"j_max {rec['j_max']:.3f} j/rho {rec['j_over_rho_max']:.3f} mass {rec['mass_plane_kg']:.4e} "
              + (f"exact dec {rec['ex_dec']:+.3e} nec {rec['ex_nulldef']:+.3e} " if args.exact else "") + f"{rec['t_s']:.0f} s", flush=True)
        if args.out:
            write_rows(Path(args.out), rows)


def summarise(args):
    import glob
    rows = []
    for f in sorted(glob.glob(str(Path(args.summarise) / "*.csv"))):
        with open(f, encoding="utf-8") as fh:
            rows += [{k: (float(v) if v not in ("", "nan") else np.nan) for k, v in r.items()} for r in csv.DictReader(fh)]
    alphas = sorted({r["alpha"] for r in rows})
    print(f"{'alpha':>6} {'ra':>5} {'rb':>5} {'static rho_min':>14} {'static nec':>11} {'static dec':>11} {'mass/M':>7} "
          f"{'pass <= beta':>12} {'fail >= beta':>12} {'in units of C':>14} {'j_max at last pass':>18}")
    M = Profiles().M
    brackets = []
    for a in alphas:
        rs = sorted([r for r in rows if r["alpha"] == a], key=lambda r: r["beta"])
        st = [r for r in rs if r["beta"] == 0]
        st = st[0] if st else rs[0]
        betas = [r["beta"] for r in rs]
        margins = [min(r["nec_dense"], np.nan_to_num(r["dec_typeI_min"], nan=-1.0), 0.0 if r["typeI_frac"] == 1 else -1.0) for r in rs]
        lp, ff = bracket(betas, margins)
        jlp = [r["j_max"] for r in rs if r["beta"] == lp][0] if lp is not None else np.nan
        fmt = lambda v: "none" if v is None else f"{v:.4f}"
        units = (f"{fmt(lp / FACTOR if lp is not None else None)} / {fmt(ff / FACTOR if ff is not None else None)}")
        print(f"{a:6.3f} {st['ra']:5.1f} {st['rb']:5.1f} {st['rho_min']:+14.3e} {st['nec_dense']:+11.3e} {st['dec_typeI_min']:+11.3e} "
              f"{st['mass_plane_kg'] / M:7.4f} {fmt(lp):>12} {fmt(ff):>12} {units:>14} {jlp:18.3f}")
        brackets.append((a, lp, ff, rs))
    if args.png:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.3))
        for a, lp, ff, rs in brackets:
            rs2 = [r for r in rs if r["beta"] > 0]
            ax1.plot([r["beta"] / FACTOR for r in rs2], [r["nec_dense"] for r in rs2], "o-", ms=4, label=f"axis ratio {a:.2f}")
        ax1.axhline(0, color="k", lw=0.6)
        ax1.set_xlabel("shift / compactness")
        ax1.set_ylabel("null condition, minimum over 4000 directions  [rho0]")
        ax1.set_ylim(-0.5, 0.03)
        ax1.set_title("the worst point against the shift, per axis ratio")
        ax1.legend(fontsize=8)
        for a, lp, ff, rs in brackets:
            if lp is not None:
                ax2.plot(a, lp / FACTOR, "o", color="C0")
            if ff is not None:
                ax2.plot(a, ff / FACTOR, "x", color="C3")
            if lp is not None and ff is not None:
                ax2.plot([a, a], [lp / FACTOR, ff / FACTOR], color="C0", lw=1)
        ax2.axhline(0.09, color="0.7", lw=0.6, ls="--")
        ax2.axhline(0.10, color="0.7", lw=0.6, ls="--")
        ax2.set_xlabel("axis ratio of the cavity (semi-axis along the motion / across it)")
        ax2.set_ylabel("shift ceiling, in units of compactness")
        ax2.set_title("o last pass, x first fail; dashes: Part 1's spherical bracket")
        fig.tight_layout()
        fig.savefig(args.png, dpi=130)
        print("figure:", args.png)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--summarise", default=None)
    ap.add_argument("--alpha", type=float, default=1.0)
    ap.add_argument("--ra", type=float, default=R1)
    ap.add_argument("--rb", type=float, default=R2)
    ap.add_argument("--betas", default="0")
    ap.add_argument("--grid", type=int, default=300)
    ap.add_argument("--dx", type=float, default=0.2)
    ap.add_argument("--rho0", type=float, default=0.0, help="reference energy density; default: the replica's peak smoothed rho c^2")
    ap.add_argument("--exact", action="store_true", help="also run warpax's S-lemma margins")
    ap.add_argument("--out", default=None)
    ap.add_argument("--png", default=None, help="with --summarise: figure of the margins and the brackets")
    args = ap.parse_args()
    if args.validate:
        validate(args)
    elif args.summarise:
        summarise(args)
    else:
        scan(args)


if __name__ == "__main__":
    main()
