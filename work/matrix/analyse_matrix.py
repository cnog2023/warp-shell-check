"""
analyse_matrix.py -- the allowed shift against compactness (PLAN Part 1A), from the CI export.

Inputs (a run folder written by matlab/shift_matrix.m and downloaded with gh run download):
  summary.csv            per (compactness, beta): WarpFactory's sampled energy-condition minima on the
                         central plane (100 directions x 10 speeds, the paper's setting), Eulerian
                         extremes, timings
  slice_f<a>_b<b>.mat    central-plane Eulerian stress-energy (10 components), the four sampled
                         condition maps, metric components, coordinates (MATLAB v7, read by SciPy)

Three readings at every interior grid point (two edge cells dropped):
  sampled    WarpFactory's own maps, the paper's method, read from summary.csv;
  null-dense the null energy condition minimised over 4000 null directions per point. A negative
             value is a definite violation of the null condition, and with it of the weak, strong
             and dominant ones, since all of them imply it. It needs no assumption about the
             algebraic type of the stress-energy;
  type       the Hawking-Ellis type from the eigen-decomposition of the Eulerian stress-energy.
             Type I points (one timelike eigenvector) have a rest frame with energy density rho and
             principal pressures p_i, and are realisable by a swarm of subluminal particles iff
             rho > 0 and rho - sum p_i > 0, the trace condition (Part 1B). Points that are not Type I
             cannot be a swarm; their fraction is reported.
Margins are fractions of rho0, the peak Eulerian energy density of the static shell at that
compactness. The first failing shift is reported as a bracket: the largest shift that passes and the
smallest that fails, per criterion.

Usage: python analyse_matrix.py <run_dir> [--png out.png]
"""
import sys
from pathlib import Path

import numpy as np
from scipy.io import loadmat

ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
NOISE = 1e-4          # fraction of rho0 below which a negative margin counts as numerical noise
N_DIRS = 4000


def load_summary(path):
    with open(path, encoding="utf-8") as f:
        header = f.readline().strip().split(",")
    data = np.loadtxt(path, delimiter=",", skiprows=1, ndmin=2)
    return [dict(zip(header, row)) for row in data]


def eulerian_tensor(s, edge=2):
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
    return T.reshape(-1, 4, 4)


def fibonacci_sphere(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    theta = np.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)], axis=1)


def nec_dense(T, dirs, chunk=4000):
    """min over null k = (1, n) of T^{ab} k_a k_b = T00 - 2 T0i n_i + Tij n_i n_j, per point."""
    out = np.empty(T.shape[0])
    for s in range(0, T.shape[0], chunk):
        t = T[s:s + chunk]
        f = (t[:, 0, 0][:, None]
             - 2.0 * (t[:, 0, 1:] @ dirs.T)
             + np.einsum("nij,di,dj->nd", t[:, 1:, 1:], dirs, dirs))
        out[s:s + chunk] = f.min(axis=1)
    return out


def type_and_swarm(T, rho0):
    """Hawking-Ellis Type I test and, at Type I points, rest-frame rho, pressures and the trace condition."""
    M = T @ ETA                                   # T^a_b = T^{ac} eta_{cb}
    lam, vec = np.linalg.eig(M)
    scale = np.abs(lam.real).max(axis=1) + 1e-300
    real = np.all(np.abs(lam.imag) < 1e-8 * scale[:, None], axis=1)
    V = vec.real.transpose(0, 2, 1)               # (n, 4 eigenvectors, 4 components)
    norms = np.einsum("nki,ij,nkj->nk", V, ETA, V)
    timelike = norms < 0
    typeI = real & (timelike.sum(axis=1) == 1)
    idx = np.where(typeI)[0]
    rho = np.full(T.shape[0], np.nan)
    tec = np.full(T.shape[0], np.nan)
    dec = np.full(T.shape[0], np.nan)
    if len(idx):
        lam_r = lam.real[idx]
        tcol = np.argmax(timelike[idx], axis=1)
        r = -lam_r[np.arange(len(idx)), tcol]
        mask = np.ones_like(lam_r, dtype=bool)
        mask[np.arange(len(idx)), tcol] = False
        p = lam_r[mask].reshape(len(idx), 3)
        rho[idx] = r / rho0
        tec[idx] = (r - p.sum(axis=1)) / rho0
        dec[idx] = (r - np.abs(p).max(axis=1)) / rho0
    return typeI, rho, tec, dec


def bracket(betas, margins):
    """(largest passing beta, smallest failing beta); None where not reached."""
    b = np.asarray(betas); m = np.asarray(margins)
    ok = m >= -NOISE
    last_pass = b[ok].max() if ok.any() else None
    fails = b[~ok]
    first_fail = fails.min() if fails.size else None
    return last_pass, first_fail


def fmt_bracket(br, scale=1.0):
    lp, ff = br
    a = "none" if lp is None else f"{lp / scale:.4f}"
    c = "none in range" if ff is None else f"{ff / scale:.4f}"
    return f"pass <= {a}, fail >= {c}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit("usage: analyse_matrix.py <run_dir> [--png out.png]")
    art = Path(args[0])
    png = sys.argv[sys.argv.index("--png") + 1] if "--png" in sys.argv else None
    dirs = fibonacci_sphere(N_DIRS)

    rows = load_summary(art / "summary.csv")
    factors = sorted({r["factor"] for r in rows}, reverse=True)
    print(f"run folder: {art}; {len(factors)} compactness values, {len(rows)} cases\n")

    results = []
    brackets = []
    for a, f in enumerate(factors, start=1):
        sub = sorted([r for r in rows if r["factor"] == f], key=lambda r: r["beta"])
        static = [r for r in sub if r["beta"] == 0.0][0]
        rho0 = static["rho0_J_m3"]; comp = static["compactness"]
        print(f"=== compactness {comp:.4f} (M = {static['M_kg']:.3e} kg, rho0 = {rho0:.3e} J/m^3) ===")
        print(f"{'beta':>7s} {'beta/C':>7s} | {'sampled min/rho0 (WarpFactory)':^44s} | {'null-dense':>10s} {'TypeI%':>7s} {'swarm%':>7s} {'TECmin':>9s} | {'max|p|/rho0':>11s}")
        print(f"{'':>7s} {'':>7s} | {'null':>10s} {'weak':>10s} {'strong':>10s} {'dom':>10s} | {'':>10s} {'':>7s} {'':>7s} {'':>9s} |")
        per = []
        for r in sub:
            b = int(round(sub.index(r))) + 1
            s = loadmat(art / f"slice_f{a}_b{b}.mat")
            T = eulerian_tensor(s)
            active = np.abs(T).reshape(T.shape[0], -1).max(axis=1) > 1e-6 * rho0
            Ta = T[active]
            nd = nec_dense(Ta, dirs) / rho0
            typeI, rho_r, tec, dec = type_and_swarm(Ta, rho0)
            swarm = typeI & (rho_r > 0) & (tec >= -NOISE)
            rec = dict(factor=f, compactness=comp, beta=r["beta"], beta_over_C=r["beta"] / comp, rho0=rho0,
                       s_null=r["minNull"] / rho0, s_weak=r["minWeak"] / rho0, s_strong=r["minStrong"] / rho0, s_dom=r["minDominant"] / rho0,
                       nec_dense=nd.min(), typeI_frac=typeI.mean(), swarm_frac=swarm.mean(),
                       tec_min=np.nanmin(tec) if np.any(~np.isnan(tec)) else np.nan,
                       dec_typeI_min=np.nanmin(dec) if np.any(~np.isnan(dec)) else np.nan,
                       maxp=r["maxAbsMomentum"] / rho0, n_active=int(active.sum()), t_ec=r["tEC_s"])
            per.append(rec); results.append(rec)
            print(f"{rec['beta']:7.4f} {rec['beta_over_C']:7.3f} | {rec['s_null']:+10.3e} {rec['s_weak']:+10.3e} {rec['s_strong']:+10.3e} {rec['s_dom']:+10.3e} | "
                  f"{rec['nec_dense']:+10.3e} {100 * rec['typeI_frac']:7.1f} {100 * rec['swarm_frac']:7.1f} {rec['tec_min']:+9.2e} | {rec['maxp']:11.3f}")
        bl = [x["beta"] for x in per]
        br = {k: bracket(bl, [x[k] for x in per]) for k in ("s_null", "s_weak", "s_strong", "s_dom", "nec_dense")}
        br["swarm"] = bracket(bl, [0.0 if x["swarm_frac"] >= 0.999 else -1.0 for x in per])
        print(f"  first failing shift, in units of beta:   sampled dominant {fmt_bracket(br['s_dom'])}; sampled null {fmt_bracket(br['s_null'])}; null-dense {fmt_bracket(br['nec_dense'])}; swarm-realisable everywhere {fmt_bracket(br['swarm'])}")
        print(f"  the same in units of beta / C:            sampled dominant {fmt_bracket(br['s_dom'], comp)}; null-dense {fmt_bracket(br['nec_dense'], comp)}; swarm {fmt_bracket(br['swarm'], comp)}\n")
        brackets.append(dict(compactness=comp, **{f"{k}_pass": (np.nan if v[0] is None else v[0]) for k, v in br.items()},
                             **{f"{k}_fail": (np.nan if v[1] is None else v[1]) for k, v in br.items()}))

    keys = list(results[0].keys())
    np.savetxt(art / "analysis_cases.csv", np.array([[x[k] for k in keys] for x in results], dtype=float), delimiter=",", header=",".join(keys), comments="", fmt="%.10g")
    bkeys = list(brackets[0].keys())
    np.savetxt(art / "analysis_brackets.csv", np.array([[x[k] for k in bkeys] for x in brackets], dtype=float), delimiter=",", header=",".join(bkeys), comments="", fmt="%.10g")
    print(f"written: {art / 'analysis_cases.csv'}, {art / 'analysis_brackets.csv'}")

    if png:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(13, 4.8))
        for f in factors:
            sub = sorted([x for x in results if x["factor"] == f], key=lambda x: x["beta"])
            x = [s["beta_over_C"] for s in sub if s["beta"] > 0]
            ax[0].plot(x, [s["s_dom"] for s in sub if s["beta"] > 0], "o-", label=f"sampled dominant, C = {sub[0]['compactness']:.3g}")
            ax[0].plot(x, [s["nec_dense"] for s in sub if s["beta"] > 0], "x--", color=ax[0].lines[-1].get_color(), label=f"null, 4000 directions, C = {sub[0]['compactness']:.3g}")
        ax[0].axhline(0, color="k", lw=0.8)
        ax[0].set_xscale("log")
        ax[0].set_xlabel("shift / compactness"); ax[0].set_ylabel("minimum margin / rho0")
        ax[0].set_title("Energy-condition margins collapse when the shift is scaled by compactness")
        ax[0].legend(fontsize=7); ax[0].grid(alpha=0.3, which="both")
        cs = [b["compactness"] for b in brackets]
        lo = [b["s_dom_pass"] for b in brackets]; hi = [b["s_dom_fail"] for b in brackets]
        ax[1].loglog(cs, lo, "v", color="C0", label="largest passing shift (sampled dominant)")
        ax[1].loglog(cs, hi, "^", color="C3", label="smallest failing shift (sampled dominant)")
        for c_, l_, h_ in zip(cs, lo, hi):
            if not (np.isnan(l_) or np.isnan(h_)):
                ax[1].plot([c_, c_], [l_, h_], "k-", lw=1)
        cc = np.array([min(cs), max(cs)])
        ax[1].loglog(cc, 0.07 * cc, "k:", lw=1, label="0.07 x compactness")
        ax[1].set_xlabel("compactness 2GM/(R2 c^2)"); ax[1].set_ylabel("shift beta")
        ax[1].set_title("The allowed shift against compactness"); ax[1].grid(alpha=0.3, which="both"); ax[1].legend(fontsize=8)
        fig.tight_layout(); fig.savefig(png, dpi=130)
        print(f"figure written: {png}")


if __name__ == "__main__":
    main()
