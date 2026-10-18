"""
hoop_stress.py -- what matter the Fuchs shell requires, from WarpFactory's own numbers.

Inputs: the CI artifact written by matlab/build_shell.m (default folder ci-artifacts/):
  profiles_<case>.csv   r, rho, rhosmooth, P, Psmooth, M, A = g00, B = grr        (1D construction)
  line_y_<case>.csv     Eulerian stress-energy along the y-axis through the centre  (3D solver)
  line_x_<case>.csv     the same along the x-axis
for case = static and warp.

Two independent routes to the tangential pressure of the static shell:
  (1D) the equilibrium identity on the construction's own smoothed profiles, in geometric units,
         P_t = P_r + (r/2) [ dP_r/dr + (rho + P_r) da/dr ],   a = (1/2) ln(-g00)
       with rho = rhosmooth and P_r = Psmooth, which the construction fixes by design;
  (3D) WarpFactory's finite-difference solver, read on the y-axis line where y is radial: there
       P_yy is the radial pressure and P_xx = P_zz the tangential one, and rho is the energy density.
Agreement between the two, within the solver's error budget, is the Step 4 check. The numbers that
matter are then: peak P_t / rho c^2, its sign and radius, and the same for P_r.

Usage: python hoop_stress.py [artifact_dir] [--png out.png]
"""
import sys
from pathlib import Path

import numpy as np

G = 6.67430e-11
c = 2.99792458e8


def load_csv(path):
    with open(path, encoding="utf-8") as f:
        header = f.readline().strip().split(",")
    data = np.loadtxt(path, delimiter=",", skiprows=1)
    return {h: data[:, i] for i, h in enumerate(header)}


def identity_tangential(prof):
    """P_t from the 1D identity, SI in and SI out. Returns r, rho c^2, P_r, P_t (all J/m^3)."""
    r = prof["r_m"]
    rho_g = G * prof["rhosmooth_kg_m3"] / c**2          # 1/m^2
    Pr_g = G * prof["Psmooth_Pa"] / c**4                 # 1/m^2
    a = 0.5 * np.log(-prof["A_g00"])
    dPr = np.gradient(Pr_g, r)
    da = np.gradient(a, r)
    Pt_g = Pr_g + 0.5 * r * (dPr + (rho_g + Pr_g) * da)
    k = c**4 / G
    return r, rho_g * k, Pr_g * k, Pt_g * k, a


def summarise(name, r, rho, Pr, Pt, mask):
    rho_peak = rho[mask].max()
    out = {}
    for label, arr in (("P_r", Pr), ("P_t", Pt)):
        i_max = np.argmax(arr[mask])
        i_min = np.argmin(arr[mask])
        rr = r[mask]
        out[label] = dict(max=arr[mask][i_max] / rho_peak, r_max=rr[i_max],
                          min=arr[mask][i_min] / rho_peak, r_min=rr[i_min])
    print(f"  [{name}] peak rho c^2 = {rho_peak:.4e} J/m^3")
    for label, d in out.items():
        print(f"  [{name}] {label}/rho c^2: max {d['max']:+.4f} at r = {d['r_max']:.2f} m; min {d['min']:+.4f} at r = {d['r_min']:.2f} m")
    return out, rho_peak


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    art = Path(args[0]) if args else Path(__file__).parent / "ci-artifacts"
    png = None
    if "--png" in sys.argv:
        png = sys.argv[sys.argv.index("--png") + 1]

    print(f"artifacts: {art}")
    prof = load_csv(art / "profiles_static.csv")
    r, rho1, Pr1, Pt1, a = identity_tangential(prof)
    shell = (r > 2.0) & (r < 28.0)          # exclude the origin and the far field
    print("\n(1D) identity on the construction's own smoothed profiles, static shell")
    s1, rho_peak = summarise("1D", r, rho1, Pr1, Pt1, shell)
    print(f"  [1D] cavity lapse exp(a) at r = 5 m: {np.exp(np.interp(5.0, r, a)):.5f}; a at r = 40 m: {np.interp(40.0, r, a):+.5f}")

    liney = load_csv(art / "line_y_static.csv")
    y = liney["coord_m"]
    ry = np.abs(y)
    print("\n(3D) WarpFactory solver on the y-axis line, static shell (P_yy radial, P_xx = P_zz tangential)")
    m3 = (ry > 2.0) & (ry < 28.0)
    s3, rho3_peak = summarise("3D", ry, liney["rho"], liney["P_yy"], liney["P_xx"], m3)
    print(f"  [3D] P_xx vs P_zz on the line: max |P_xx - P_zz| / rho peak = {np.max(np.abs(liney['P_xx'] - liney['P_zz'])[m3]) / rho3_peak:.2e}")

    # pointwise comparison of the two routes at the 3D sample radii (one side of the axis)
    side = (y > 2.0) & (y < 28.0)
    rho1_i = np.interp(y[side], r, rho1)
    Pr1_i = np.interp(y[side], r, Pr1)
    Pt1_i = np.interp(y[side], r, Pt1)
    d_rho = np.max(np.abs(liney["rho"][side] - rho1_i)) / rho_peak
    d_Pr = np.max(np.abs(liney["P_yy"][side] - Pr1_i)) / rho_peak
    d_Pt = np.max(np.abs(liney["P_xx"][side] - Pt1_i)) / rho_peak
    print("\n(1D vs 3D) largest pointwise difference on y > 0, as a fraction of peak rho c^2")
    print(f"  energy density     : {d_rho:.3e}")
    print(f"  radial pressure    : {d_Pr:.3e}")
    print(f"  tangential pressure: {d_Pt:.3e}")

    # the warp shell against the static one, along y (radial to the motion) and x (along the motion)
    try:
        liney_w = load_csv(art / "line_y_warp.csv")
        linex_s = load_csv(art / "line_x_static.csv")
        linex_w = load_csv(art / "line_x_warp.csv")
        print("\n(warp vs static) largest change along the lines, as a fraction of peak rho c^2")
        for comp in ("rho", "p_x", "p_y", "P_xx", "P_yy", "P_zz", "P_xy"):
            dy = np.max(np.abs(liney_w[comp] - liney[comp])[m3]) / rho3_peak
            mx = (np.abs(linex_s["coord_m"]) > 2.0) & (np.abs(linex_s["coord_m"]) < 28.0)
            dx = np.max(np.abs(linex_w[comp] - linex_s[comp])[mx]) / rho3_peak
            print(f"  {comp:5s}: y-line {dy:.3e}   x-line {dx:.3e}")
    except FileNotFoundError as e:
        print(f"(warp files missing: {e})")

    if png:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
        ax[0].plot(r[shell], rho1[shell] / rho_peak, label=r"$\rho c^2$ (smoothed input = derived)")
        ax[0].plot(r[shell], Pr1[shell] / rho_peak, label=r"$P_r$ (smoothed input = derived)")
        ax[0].plot(r[shell], Pt1[shell] / rho_peak, label=r"$P_t$ from the 1D identity")
        ax[0].plot(ry[m3 & (y > 0)], liney["P_xx"][m3 & (y > 0)] / rho_peak, "k.", ms=3, label=r"$P_{xx}$ on the y-axis, WarpFactory 3D")
        ax[0].axvline(10, color="grey", lw=0.5); ax[0].axvline(20, color="grey", lw=0.5)
        ax[0].set_xlabel("r [m]"); ax[0].set_ylabel(r"fraction of peak $\rho c^2$")
        ax[0].set_title("Static shell: what the smoothed construction requires")
        ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3)
        ax[1].plot(y[side], (liney["P_xx"][side] - Pt1_i) / rho_peak, label=r"$P_{xx}^{3D} - P_t^{1D}$")
        ax[1].plot(y[side], (liney["P_yy"][side] - Pr1_i) / rho_peak, label=r"$P_{yy}^{3D} - P_r^{1D}$")
        ax[1].plot(y[side], (liney["rho"][side] - rho1_i) / rho_peak, label=r"$\rho^{3D} - \rho^{1D}$")
        ax[1].set_xlabel("y [m]"); ax[1].set_ylabel(r"difference / peak $\rho c^2$")
        ax[1].set_title("3D solver minus 1D identity (solver error budget)")
        ax[1].legend(fontsize=8); ax[1].grid(alpha=0.3)
        fig.tight_layout(); fig.savefig(png, dpi=130)
        print(f"\nfigure written: {png}")


if __name__ == "__main__":
    main()
