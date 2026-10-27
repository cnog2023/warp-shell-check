"""
side_by_side.py -- the paper's Figures 6 to 10 next to ours from the exported slices (PLAN Step 3, Part 3).

The paper (Fuchs et al. 2024, arXiv:2405.02709, CC BY 4.0) plots, "for a slice along the y-axis" at
the authors' configuration (R1 = 10 m, R2 = 20 m, M = 4.49e27 kg, shift 0.02 along +x, smoothFactor
4000, 300 x 300 x 5 grid at 0.2 m):
  Fig 4   the 1D construction: density and pressure before (red) and after (blue) smoothing  (page 13)
  Fig 5   static shell: metric g00 and g22 along the y-axis with the Schwarzschild reference (page 14)
  Fig 6   static shell: Eulerian energy density with the smoothed input rho~ c^2; pressures P_2 (radial
          on this axis), P_1 = P_3 (tangential) with the smoothed input P~        (page 14)
  Fig 7   static shell: the four sampled energy-condition maps, Null, Weak, Strong, Dominant (page 16)
  Fig 8   warp shell: metric components g00, g01, g22 along the y-axis                   (page 18)
  Fig 9   warp shell: energy density; pressures P_2, P_1, P_3; momentum p_1, p_2 = p_3; shears (page 19)
  Fig 10  warp shell: the four sampled energy-condition maps                              (page 20)

Ours come from the Part 1 CI export at the same configuration (`matlab/shift_matrix.m`): the central
plane slices `work/matrix/run-fine/slice_f1_b1.mat` (static) and `slice_f1_b5.mat` (shift 0.02, formed
by linearity, verified exact), read on the grid column at x = -0.1 m, the one `matlab/build_shell.m`
exported as the y-axis line (the grid has no x = 0 column; the two neighbours differ by 8e-12). The
smoothed inputs come from `profiles_f1.csv` of the same run. The two outermost cells are stencil
artefacts and are dropped, as the paper does. Energy conditions are WarpFactory's own exported maps,
the paper's method (100 directions x 10 speeds); for Null and Weak the consistent Minkowski
evaluation (claim C9, `work/matrix/RESULTS.md` section 4) is drawn dashed on top, since the exported
maps lower indices with the coordinate metric and read low by about g00^2 inside the shell.

Outputs, in this folder: `paper/figNN.png` (the paper's panels, clipped from the PDF at 200 dpi),
`ours/figNN.png`, and `pairs/figNN_pair.png` with the two side by side. `numbers.csv` lists the
extrema of every curve we draw, with their radii, for the record.

Usage: python side_by_side.py [--pdf path] [--run work/matrix/run-fine]
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from scipy.io import loadmat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "work" / "matrix"))
from exact_conditions import sampled_min, wf_observers  # noqa: E402

C_SI = 2.99792458e8
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
COL = 149           # 0-based grid column at x = -0.1 m, as in build_shell.m (i0 = 150, 1-based)
EDGE = 2            # outermost cells dropped
PAGES = {4: 13, 5: 14, 6: 14, 7: 16, 8: 18, 9: 19, 10: 20}
G_SI = 6.67430e-11
M_KG = 4.488636405000363e27   # the slices' mass (profiles_f1.csv run, factor 1/3)
R_S = 2 * G_SI * M_KG / C_SI ** 2
BLUE, RED, GREEN = "#0000ff", "#ff0000", "#00c000"


# ---------------------------------------------------------------- the paper's panels
def clip_paper_figures(pdf, out):
    import pymupdf
    doc = pymupdf.open(str(pdf))
    out.mkdir(parents=True, exist_ok=True)
    for n, p in PAGES.items():
        page = doc[p - 1]
        cap = [b for b in page.get_text("blocks") if b[4].strip().startswith(f"Figure {n}")][0]
        prev_caps = [b for b in page.get_text("blocks") if b[4].strip().startswith("Figure ") and b[3] < cap[1]]
        top = max([b[3] for b in prev_caps] + [60.0, {4: 405.0, 5: 95.0}.get(n, 0.0)])   # below the running header / the text above
        # the figure is whatever is drawn (vector paths) or placed (raster images) between the previous
        # caption and this one; some pages carry the MATLAB figure as an embedded image
        rects = [d["rect"] for d in page.get_drawings()] + [pymupdf.Rect(i["bbox"]) for i in page.get_image_info()]
        rects = [r for r in rects if r.y0 > top and r.y1 < cap[1] and r.width > 20 and r.height > 20]
        if rects:
            x0 = min(r.x0 for r in rects) - 30; x1 = max(r.x1 for r in rects) + 12
            y0 = max(min(r.y0 for r in rects) - 14, top + 1); y1 = max(r.y1 for r in rects) + 30
        else:
            x0, x1, y0, y1 = 72, 540, top + 4, cap[1]
        clip = pymupdf.Rect(max(x0, 72), max(y0, 0), min(x1, page.rect.width - 60), min(y1, cap[1]))
        pix = page.get_pixmap(dpi=200, clip=clip)
        pix.save(str(out / f"fig{n:02d}.png"))
        print(f"paper Figure {n}: page {p}, clip {clip}, {pix.width} x {pix.height} px")


# ---------------------------------------------------------------- our lines
def line(slice_, key):
    v = np.asarray(slice_[key], dtype=float)[COL, :]
    return v


def load_case(run, b):
    s = loadmat(run / f"slice_f1_b{b}.mat")
    y = np.asarray(s["y"]).ravel()
    keep = (y > 0) & (np.arange(len(y)) < len(y) - EDGE)
    d = {k: line(s, k)[keep] for k in ("rho", "p_x", "p_y", "p_z", "P_xx", "P_yy", "P_zz", "P_xy", "P_xz", "P_yz",
                                         "null", "weak", "strong", "dominant", "g00", "g01", "g11", "g22", "g33")}
    d["r"] = y[keep]
    # the Eulerian frame tensor on the line, for the consistent Null and Weak evaluation
    n = keep.sum()
    T = np.zeros((n, 4, 4))
    T[:, 0, 0] = d["rho"]
    for i, k in enumerate(("p_x", "p_y", "p_z"), start=1):
        T[:, 0, i] = T[:, i, 0] = d[k]
    T[:, 1, 1], T[:, 2, 2], T[:, 3, 3] = d["P_xx"], d["P_yy"], d["P_zz"]
    T[:, 1, 2] = T[:, 2, 1] = d["P_xy"]; T[:, 1, 3] = T[:, 3, 1] = d["P_xz"]; T[:, 2, 3] = T[:, 3, 2] = d["P_yz"]
    null_vecs, time_vecs = wf_observers()
    eta = np.broadcast_to(ETA, T.shape)
    d["null_fix"] = sampled_min(T, eta, null_vecs)
    d["weak_fix"] = sampled_min(T, eta, time_vecs)
    d["beta"] = float(np.squeeze(s["beta"]))
    return d


def load_profiles(run):
    p = np.loadtxt(run / "profiles_f1.csv", delimiter=",", skiprows=1)
    return dict(r=p[:, 0], rho_s=p[:, 2] * C_SI ** 2, P_s=p[:, 4], rho_u=p[:, 1] * C_SI ** 2, P_u=p[:, 3])


# ---------------------------------------------------------------- drawing, in the paper's layout
def style(ax, title, ylim, ylabel="[J/m$^3$]"):
    ax.set_title(title, fontweight="bold")
    ax.set_xlim(0, 30); ax.set_ylim(*ylim)
    ax.set_xlabel("r [m]"); ax.set_ylabel(ylabel)
    ax.grid(False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(True)


def sci(ax, power):
    import matplotlib.ticker as mt
    f = mt.ScalarFormatter(useMathText=True)
    f.set_powerlimits((power, power))
    ax.yaxis.set_major_formatter(f)
    ax.yaxis.get_offset_text().set_fontsize(9)


def draw_fig4(prof, plt):
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].plot(prof["r"], prof["rho_s"], color=BLUE, lw=2, label=r"$\tilde\rho$ (smoothed)")
    ax[0].plot(prof["r"], prof["rho_u"], color=RED, lw=1.5, label=r"$\rho'$ (before smoothing)")
    style(ax[0], "Energy Density", (0, 15e39)); sci(ax[0], 39); ax[0].legend(loc="upper right")
    ax[1].plot(prof["r"], prof["P_s"], color=BLUE, lw=2, label=r"$\tilde P$ (smoothed)")
    ax[1].plot(prof["r"], prof["P_u"], color=RED, lw=1.5, label=r"$P'$ (before smoothing)")
    style(ax[1], "Pressure", (0, 15e38)); sci(ax[1], 38); ax[1].legend(loc="upper right")
    return fig


def draw_fig5(st, plt):
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    r = np.linspace(0.05, 30, 3000)
    with np.errstate(divide="ignore"):
        g00_s = -(1 - R_S / r); g22_s = 1 / (1 - R_S / r)
    ax[0].plot(st["r"], st["g00"], color=BLUE, lw=2, label="Shell")
    ax[0].plot(r, g00_s, color=RED, lw=1.5, ls="--", label="Sch.")
    style(ax[0], r"$g_{00}$", (-1, -0.3), ""); ax[0].legend(loc="upper right")
    ax[1].plot(st["r"], st["g22"], color=BLUE, lw=2, label="Shell")
    ax[1].plot(r[r > R_S], g22_s[r > R_S], color=RED, lw=1.5, ls="--", label="Sch.")
    ax[1].axvline(R_S, color=RED, lw=1.2, ls="--")
    style(ax[1], r"$g_{22}$", (1, 2), ""); ax[1].legend(loc="upper right")
    return fig


def draw_fig6(st, prof, plt):
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].plot(st["r"], st["rho"], color=BLUE, lw=2, label=r"$\rho$")
    ax[0].plot(prof["r"], prof["rho_s"], color=RED, lw=1.5, ls="--", label=r"$\tilde\rho$")
    style(ax[0], "Energy Density", (0, 15e39)); sci(ax[0], 39); ax[0].legend(loc="upper right")
    ax[1].plot(st["r"], st["P_yy"], color=BLUE, lw=2, label=r"$P_2$")
    ax[1].plot(st["r"], st["P_xx"], color=GREEN, lw=2, label=r"$P_1 = P_3$")
    ax[1].plot(prof["r"], prof["P_s"], color=RED, lw=1.5, ls="--", label=r"$\tilde P$")
    style(ax[1], "Pressure", (-0.5e39, 5e39)); sci(ax[1], 39); ax[1].legend(loc="upper right")
    return fig


def draw_ec(d, plt, title_suffix=""):
    fig, ax = plt.subplots(2, 2, figsize=(9, 6.8))
    for a, (key, name) in zip(ax.ravel(), (("null", "Null"), ("weak", "Weak"), ("strong", "Strong"), ("dominant", "Dominant"))):
        a.plot(d["r"], d[key], color=BLUE, lw=2, label=name)
        if key in ("null", "weak"):
            a.plot(d["r"], d[key + "_fix"], color=BLUE, lw=1.2, ls="--", label=name + ", Minkowski index change (C9)")
        style(a, name, (-0.5e39, 15e39)); sci(a, 39); a.legend(loc="upper right", fontsize=8)
    return fig


def draw_fig8(w, plt):
    fig, ax = plt.subplots(2, 2, figsize=(9, 6.8))
    ax[0, 0].plot(w["r"], w["g00"], color=BLUE, lw=2); style(ax[0, 0], r"$g_{00}$", (-1, -0.5), "")
    ax[0, 1].plot(w["r"], w["g01"], color=BLUE, lw=2); style(ax[0, 1], r"$g_{01}$", (-0.025, 0.0), "")
    ax[1, 0].plot(w["r"], w["g22"], color=BLUE, lw=2); style(ax[1, 0], r"$g_{22}$", (1, 1.5), "")
    ax[1, 1].axis("off")
    return fig


def draw_fig9(w, plt):
    fig, ax = plt.subplots(2, 2, figsize=(9, 6.8))
    ax[0, 0].plot(w["r"], w["rho"], color=BLUE, lw=2, label=r"$\rho$")
    style(ax[0, 0], "Energy Density", (0, 15e39)); sci(ax[0, 0], 39); ax[0, 0].legend(loc="upper right")
    ax[0, 1].plot(w["r"], w["P_yy"], color=BLUE, lw=2, label=r"$P_2$")
    ax[0, 1].plot(w["r"], w["P_xx"], color=GREEN, lw=2, label=r"$P_1$")
    ax[0, 1].plot(w["r"], w["P_zz"], color=RED, lw=2, label=r"$P_3$")
    style(ax[0, 1], "Pressure", (-0.5e39, 5e39)); sci(ax[0, 1], 39); ax[0, 1].legend(loc="upper right")
    ax[1, 0].plot(w["r"], w["p_x"], color=BLUE, lw=2, label=r"$p_1$")
    ax[1, 0].plot(w["r"], w["p_y"], color=GREEN, lw=2, label=r"$p_2 = p_3$")
    style(ax[1, 0], "Momentum", (-7.5e39, 7.5e39)); sci(ax[1, 0], 39); ax[1, 0].legend(loc="upper right")
    ax[1, 1].plot(w["r"], w["P_xy"], color=BLUE, lw=2, label=r"$\sigma_{12} = \sigma_{13} = \sigma_{23}$")
    style(ax[1, 1], "Shears", (-2e38, 2e38)); sci(ax[1, 1], 38); ax[1, 1].legend(loc="upper right")
    return fig


def compose(paper_png, ours_png, out_png, n):
    from PIL import Image, ImageDraw, ImageFont
    a = Image.open(paper_png).convert("RGB"); b = Image.open(ours_png).convert("RGB")
    h = 1100
    a = a.resize((int(a.width * h / a.height), h)); b = b.resize((int(b.width * h / b.height), h))
    gap, top = 40, 70
    canvas = Image.new("RGB", (a.width + b.width + 3 * gap, h + top + gap), "white")
    canvas.paste(a, (gap, top)); canvas.paste(b, (2 * gap + a.width, top))
    d = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except OSError:
        font = ImageFont.load_default()
    d.text((gap, 18), f"Fuchs et al. 2024, Figure {n} (arXiv:2405.02709, CC BY 4.0)", fill="black", font=font)
    d.text((2 * gap + a.width, 18), f"Ours: WarpFactory at the authors' configuration, Part 1 export (work/matrix)", fill="black", font=font)
    canvas.save(out_png)


def extrema(name, r, v, rows):
    i, j = int(np.argmax(v)), int(np.argmin(v))
    rows.append((name, v[i], r[i], v[j], r[j]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default=str(ROOT / "sources/papers/2024_fuchs_constant_velocity_physical_warp_drive_2405.02709.pdf"))
    ap.add_argument("--run", default=str(ROOT / "work/matrix/run-fine"))
    args = ap.parse_args()
    run = Path(args.run)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10, "axes.titlesize": 12, "legend.frameon": True})

    clip_paper_figures(Path(args.pdf), HERE / "paper")
    st, w, prof = load_case(run, 1), load_case(run, 5), load_profiles(run)
    print(f"static beta {st['beta']}, warp beta {w['beta']}; r from {st['r'][0]:.1f} to {st['r'][-1]:.1f} m, {len(st['r'])} points")
    (HERE / "ours").mkdir(exist_ok=True); (HERE / "pairs").mkdir(exist_ok=True)
    figs = {4: draw_fig4(prof, plt), 5: draw_fig5(st, plt), 6: draw_fig6(st, prof, plt), 7: draw_ec(st, plt), 8: draw_fig8(w, plt), 9: draw_fig9(w, plt), 10: draw_ec(w, plt)}
    for n, fig in figs.items():
        fig.tight_layout(); fig.savefig(HERE / "ours" / f"fig{n:02d}.png", dpi=160); plt.close(fig)
        compose(HERE / "paper" / f"fig{n:02d}.png", HERE / "ours" / f"fig{n:02d}.png", HERE / "pairs" / f"fig{n:02d}_pair.png", n)

    rows = []
    for case, d in (("static", st), ("warp", w)):
        for k in ("rho", "P_xx", "P_yy", "P_zz", "p_x", "p_y", "P_xy", "null", "weak", "strong", "dominant", "null_fix", "weak_fix", "g00", "g01", "g22"):
            extrema(f"{case}.{k}", d["r"], d[k], rows)
    extrema("profile.rho_smoothed_c2", prof["r"], prof["rho_s"], rows); extrema("profile.P_smoothed", prof["r"], prof["P_s"], rows)
    extrema("profile.rho_unsmoothed_c2", prof["r"], prof["rho_u"], rows); extrema("profile.P_unsmoothed", prof["r"], prof["P_u"], rows)
    with open(HERE / "numbers.csv", "w", encoding="utf-8") as f:
        f.write("curve,max,r_of_max_m,min,r_of_min_m\n")
        for row in rows:
            f.write(f"{row[0]},{row[1]:.6e},{row[2]:.2f},{row[3]:.6e},{row[4]:.2f}\n")
            print(f"{row[0]:28s} max {row[1]:+.4e} at {row[2]:5.2f} m   min {row[3]:+.4e} at {row[4]:5.2f} m")
    print("written:", HERE / "numbers.csv", "and the figures under paper/, ours/, pairs/")


if __name__ == "__main__":
    main()
