"""
analyse_matrix.py -- the allowed shift against compactness (PLAN Part 1A), from the CI export.

Inputs (ci-artifacts/, written by matlab/shift_matrix.m):
  summary.csv            per (compactness, beta): WarpFactory's sampled energy-condition minima on the
                         central plane (100 directions x 10 speeds), Eulerian extremes, timings
  slice_f<a>_b<b>.mat    central-plane Eulerian stress-energy (10 components), the four sampled
                         condition maps, metric components, coordinates (MATLAB v7, read by SciPy)

Two readings of the energy conditions at every grid point, both with two edge cells dropped:
  sampled   WarpFactory's own maps, the paper's method;
  exact     the eigen-decomposition of the Eulerian stress-energy. For Hawking-Ellis Type I points
            (one timelike eigenvector) the rest-frame energy density rho and principal pressures p_i
            give the conditions in closed form: NEC min(rho + p_i), WEC rho and NEC, DEC min(rho - |p_i|),
            SEC rho + sum p_i and NEC, and the trace condition rho - sum p_i, which is the condition for
            the matter to be a swarm of subluminal particles (Part 1B).
Margins are reported as fractions of rho0, the peak Eulerian energy density of the static shell at
that compactness. The first failing shift per compactness is found by linear interpolation of each
margin in beta between the last non-negative and the first negative value.

Usage: python analyse_matrix.py [artifact_dir] [--png out.png]
"""
import sys
from pathlib import Path

import numpy as np
from scipy.io import loadmat

ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
NOISE = 1e-4      # fraction of rho0 below which a negative margin is treated as numerical noise


def load_summary(path):
    with open(path, encoding="utf-8") as f:
        header = f.readline().strip().split(",")
    data = np.loadtxt(path, delimiter=",", skiprows=1, ndmin=2)
    return [dict(zip(header, row)) for row in data]


def eulerian_tensor(s, edge=2):
    """(N, 4, 4) contravariant Eulerian T at interior points, plus flattened masks."""
    sl = slice(edge, -edge)
    g = lambda k: np.asarray(s[k])[sl, sl]
    rho, px, py, pz = g("rho"), g("p_x"), g("p_y"), g("p_z")
    Pxx, Pyy, Pzz, Pxy, Pxz, Pyz = g("P_xx"), g("P_yy"), g("P_zz"), g("P_xy"), g("P_xz"), g("P_yz")
    T = np.empty(rho.shape + (4, 4))
    T[..., 0, 0] = rho
    T[..., 0, 1] = T[..., 1, 0] = px
    T[..., 0, 2] = T[..., 2, 0] = py
    T[..., 0, 3] = T[..., 3, 0] = pz
    T[..., 1, 1] = Pxx
    T[..., 2, 2] = Pyy
    T[..., 3, 3] = Pzz
    T[..., 1, 2] = T[..., 2, 1] = Pxy
    T[..., 1, 3] = T[..., 3, 1] = Pxz
    T[..., 2, 3] = T[..., 3, 2] = Pyz
    return T.reshape(-1, 4, 4), rho.shape


def exact_conditions(T, rho0):
    """Rest-frame conditions at Type I points. Returns dict of per-point margins (NaN where not Type I)."""
    n = T.shape[0]
    M = T @ ETA                                   # T^a_b = T^{ac} eta_{cb}
    lam, vec = np.linalg.eig(M)
    out = {k: np.full(n, np.nan) for k in ("nec", "wec", "dec", "sec", "tec", "rho", "v2")}
    typeI = np.zeros(n, dtype=bool)
    real = np.all(np.abs(lam.imag) < 1e-9 * (np.abs(lam.real).max(axis=1, keepdims=True) + 1e-300), axis=1)
    norms = np.einsum("nij,jk,nik->ni", vec.real.transpose(0, 2, 1), ETA, vec.real.transpose(0, 2, 1))  # v^T eta v per eigenvector
    tl = norms < 0
    one_tl = tl.sum(axis=1) == 1
    typeI = real & one_tl
    idx = np.where(typeI)[0]
    lam_r = lam.real[idx]
    t_col = np.argmax(tl[idx], axis=1)
    rho = -lam_r[np.arange(len(idx)), t_col]
    p = np.array([np.delete(lam_r[i], t_col[i]) for i in range(len(idx))]) if len(idx) else np.zeros((0, 3))
    out["rho"][idx] = rho
    out["nec"][idx] = np.min(rho[:, None] + p, axis=1)
    out["wec"][idx] = np.minimum(rho, out["nec"][idx])
    out["dec"][idx] = np.min(rho[:, None] - np.abs(p), axis=1)
    out["sec"][idx] = np.minimum(rho + p.sum(axis=1), out["nec"][idx])
    out["tec"][idx] = rho - p.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        out["v2"][idx] = np.where(rho > 0, p.sum(axis=1) / rho, np.nan)
    for k in ("nec", "wec", "dec", "sec", "tec", "rho"):
        out[k] = out[k] / rho0
    return out, typeI


def first_failure(betas, margins):
    """Linear interpolation of the first zero crossing of margin(beta); None if never negative."""
    b = np.asarray(betas)
    m = np.asarray(margins)
    for i in range(1, len(b)):
        if m[i] < -NOISE and m[i - 1] >= -NOISE:
            if m[i - 1] == m[i]:
                return b[i]
            return b[i - 1] + (b[i] - b[i - 1]) * (m[i - 1] + NOISE) / (m[i - 1] - m[i])
    if m[0] < -NOISE:
        return 0.0
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    art = Path(args[0]) if args else Path(__file__).parent / "ci-artifacts"
    png = sys.argv[sys.argv.index("--png") + 1] if "--png" in sys.argv else None

    rows = load_summary(art / "summary.csv")
    factors = sorted({r["factor"] for r in rows}, reverse=True)
    betas = sorted({r["beta"] for r in rows})
    print(f"artifacts: {art}; compactness values {len(factors)}, shifts {betas}\n")

    results = []
    for a, f in enumerate(factors, start=1):
        static = [r for r in rows if r["factor"] == f and r["beta"] == 0.0][0]
        rho0 = static["rho0_J_m3"]
        comp = static["compactness"]
        print(f"=== compactness {comp:.4f} (M = {static['M_kg']:.3e} kg, rho0 = {rho0:.3e} J/m^3) ===")
        print(f"{'beta':>6s} | {'sampled (WarpFactory) min/rho0':^44s} | {'exact (eigen) min/rho0':^48s} | {'nonTypeI':>8s} {'max|p|/rho0':>11s}")
        print(f"{'':>6s} | {'null':>10s} {'weak':>10s} {'strong':>10s} {'dom':>10s} | {'nec':>9s} {'wec':>9s} {'dec':>9s} {'sec':>9s} {'tec':>9s} | {'':>8s}")
        per_beta = []
        for b, beta in enumerate(betas, start=1):
            r = [x for x in rows if x["factor"] == f and x["beta"] == beta][0]
            s = loadmat(art / f"slice_f{a}_b{b}.mat")
            T, shape = eulerian_tensor(s)
            scale = np.abs(T).reshape(T.shape[0], -1).max(axis=1)
            active = scale > 1e-6 * rho0          # ignore numerically empty points (cavity, far field)
            ex, typeI = exact_conditions(T[active], rho0)
            mins = {k: np.nanmin(ex[k]) if np.any(~np.isnan(ex[k])) else np.nan for k in ("nec", "wec", "dec", "sec", "tec")}
            non_typeI = int((~typeI).sum())
            v2max = np.nanmax(ex["v2"]) if np.any(~np.isnan(ex["v2"])) else np.nan
            rec = dict(factor=f, compactness=comp, beta=beta, rho0=rho0,
                       s_null=r["minNull"] / rho0, s_weak=r["minWeak"] / rho0, s_strong=r["minStrong"] / rho0, s_dom=r["minDominant"] / rho0,
                       e_nec=mins["nec"], e_wec=mins["wec"], e_dec=mins["dec"], e_sec=mins["sec"], e_tec=mins["tec"],
                       non_typeI=non_typeI, active=int(active.sum()), v2max=v2max, maxp=r["maxAbsMomentum"] / rho0,
                       t_ec=r["tEC_s"])
            per_beta.append(rec)
            results.append(rec)
            print(f"{beta:6.3f} | {rec['s_null']:+10.3e} {rec['s_weak']:+10.3e} {rec['s_strong']:+10.3e} {rec['s_dom']:+10.3e} | "
                  f"{rec['e_nec']:+9.2e} {rec['e_wec']:+9.2e} {rec['e_dec']:+9.2e} {rec['e_sec']:+9.2e} {rec['e_tec']:+9.2e} | {non_typeI:8d} {rec['maxp']:11.3f}")
        bl = [x["beta"] for x in per_beta]
        ff = {k: first_failure(bl, [x[k] for x in per_beta]) for k in ("s_null", "s_weak", "s_strong", "s_dom", "e_nec", "e_wec", "e_dec", "e_sec", "e_tec")}
        fmt = lambda v: "> %.2f" % bl[-1] if v is None else f"{v:.4f}"
        print(f"  first failing shift: sampled null {fmt(ff['s_null'])}, weak {fmt(ff['s_weak'])}, strong {fmt(ff['s_strong'])}, dominant {fmt(ff['s_dom'])};"
              f"  exact nec {fmt(ff['e_nec'])}, wec {fmt(ff['e_wec'])}, dec {fmt(ff['e_dec'])}, sec {fmt(ff['e_sec'])}, swarm/tec {fmt(ff['e_tec'])}")
        print(f"  sampled-condition time per case: {np.mean([x['t_ec'] for x in per_beta]):.0f} s\n")
        for x in per_beta:
            x.update({f"ff_{k}": (np.nan if v is None else v) for k, v in ff.items()})

    keys = list(results[0].keys())
    np.savetxt(Path(__file__).parent / "matrix_results.csv", np.array([[x[k] for k in keys] for x in results], dtype=float),
               delimiter=",", header=",".join(keys), comments="", fmt="%.10g")
    print("written: matrix_results.csv")

    if png:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(13, 4.8))
        for f in factors:
            sub = [x for x in results if x["factor"] == f]
            bl = [x["beta"] for x in sub]
            ax[0].plot(bl, [x["e_dec"] for x in sub], "o-", label=f"DEC exact, C = {sub[0]['compactness']:.3g}")
            ax[0].plot(bl, [x["s_dom"] for x in sub], "x:", color=ax[0].lines[-1].get_color(), label=f"dominant sampled, C = {sub[0]['compactness']:.3g}")
        ax[0].axhline(0, color="k", lw=0.8)
        ax[0].set_xlabel("shift beta"); ax[0].set_ylabel("minimum margin / rho0"); ax[0].set_title("Dominant energy condition against shift")
        ax[0].legend(fontsize=7); ax[0].grid(alpha=0.3)
        comps, ffs = [], []
        for f in factors:
            sub = [x for x in results if x["factor"] == f]
            v = sub[0].get("ff_e_dec", np.nan)
            if not np.isnan(v):
                comps.append(sub[0]["compactness"]); ffs.append(v)
        if len(comps) >= 2:
            ax[1].loglog(comps, ffs, "o-", label="first DEC failure (exact)")
            k = np.polyfit(np.log(comps), np.log(ffs), 1)[0]
            ax[1].set_title(f"First failing shift against compactness, slope {k:.2f}")
        else:
            ax[1].set_title("First failing shift against compactness (not reached in range)")
        ax[1].set_xlabel("compactness 2GM/(R2 c^2)"); ax[1].set_ylabel("first failing shift"); ax[1].grid(alpha=0.3, which="both"); ax[1].legend(fontsize=8)
        fig.tight_layout(); fig.savefig(png, dpi=130)
        print(f"figure written: {png}")


if __name__ == "__main__":
    main()
