"""
digitise_paper.py -- read the paper's curves off the PDF's vector paths (Part 3).

Figures 4, 5, 6, 7, 9 and 10 of Fuchs et al. 2024 (arXiv:2405.02709) are embedded as vector graphics, so
every curve is a path of line segments in page coordinates. For each panel the axes are calibrated
by least squares from the positions of its tick labels (the numbers to the left of and below the
axes box), and each coloured path is mapped to (r, value). The result is the paper's own numbers to
about a tenth of a percent of the axis range, instead of a reading by eye. Figure 8 is a raster
image in the PDF and is compared by eye only.

Writes `paper_curves.csv` (every digitised point) and prints the extrema next to ours from
`numbers.csv` (made by side_by_side.py).

Usage: python digitise_paper.py [--pdf path]
"""
import argparse
import csv
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

# figure -> page, band (between captions), panels: name -> (white axes rect x0, y0 approx) and the curves in it
# curve colours: blue (0,0,1), green (0,1,0), red (1,0,0); dashed red = the smoothed inputs
FIGS = {
    4: dict(page=13, band=(400, 637), scale=1e39, panels={
        "energy density": dict(box=(105, 423), curves={"blue": "rho_smoothed_c2", "red": "rho_unsmoothed_c2"}),
        "pressure": dict(box=(344, 423), curves={"blue": "P_smoothed", "red": "P_unsmoothed"}, scale=1e38)}),
    5: dict(page=14, band=(60, 318), scale=1.0, panels={
        "g00": dict(box=(94, 104), curves={"blue": "g00", "red": "g00_schwarzschild"}),
        "g22": dict(box=(340, 104), curves={"blue": "g22", "red": "g22_schwarzschild"})}),
    6: dict(page=14, band=(366, 607), scale=1e39, panels={
        "energy density": dict(box=(105, 393), curves={"blue": "rho", "red": "rho_smoothed_c2"}),
        "pressure": dict(box=(344, 393), curves={"blue": "P_2 (radial)", "green": "P_1 = P_3 (tangential)", "red": "P_smoothed"})}),
    7: dict(page=16, band=(60, 525), scale=1e39, panels={
        "null": dict(box=(105, 102), curves={"blue": "null"}), "weak": dict(box=(344, 102), curves={"blue": "weak"}),
        "strong": dict(box=(105, 321), curves={"blue": "strong"}), "dominant": dict(box=(344, 321), curves={"blue": "dominant"})}),
    9: dict(page=19, band=(150, 587), scale=1e39, panels={
        "energy density": dict(box=(105, 164), curves={"blue": "rho"}),
        "pressure": dict(box=(344, 164), curves={"blue": "P_2", "green": "P_1", "red": "P_3"}),
        "momentum": dict(box=(105, 383), curves={"blue": "p_1", "green": "p_2 = p_3"}),
        "shears": dict(box=(344, 383), curves={"blue": "sigma_12"}, scale=1e38)}),
    10: dict(page=20, band=(60, 525), scale=1e39, panels={
        "null": dict(box=(105, 102), curves={"blue": "null"}), "weak": dict(box=(344, 102), curves={"blue": "weak"}),
        "strong": dict(box=(105, 321), curves={"blue": "strong"}), "dominant": dict(box=(344, 321), curves={"blue": "dominant"})}),
}
COLOURS = {"blue": (0.0, 0.0, 1.0), "green": (0.0, 1.0, 0.0), "red": (1.0, 0.0, 0.0)}
NUM = re.compile(r"^-?\d+(\.\d+)?$")


def panel_rect(page, box, band):
    """The white axes-background rectangle whose top-left is near `box`."""
    for d in page.get_drawings():
        r = d["rect"]
        if d.get("fill") == (1.0, 1.0, 1.0) and abs(r.x0 - box[0]) < 6 and abs(r.y0 - box[1]) < 12 and r.width > 100 and band[0] < r.y0 < band[1]:
            return r
    raise RuntimeError(f"no axes rect near {box}")


def calibrate(page, rect):
    """Linear maps from page x to r and page y to value, fitted to the tick labels around the axes box."""
    xs, ys = [], []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip().replace("−", "-")
                if not NUM.match(t):
                    continue
                x0, y0, x1, y1 = s["bbox"]
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                if s["size"] < 10:                                                          # superscripts, legend subscripts
                    continue
                if rect.x0 - 12 < x1 <= rect.x0 + 1 and rect.y0 - 8 < cy < rect.y1 + 8:      # y tick labels, right-aligned left of the box
                    ys.append((cy, float(t)))
                if rect.y1 - 1 <= y0 < rect.y1 + 10 and rect.x0 - 8 < cx < rect.x1 + 8:       # x tick labels, just below the box
                    xs.append((cx, float(t)))
    if len(xs) < 2 or len(ys) < 2:
        raise RuntimeError(f"not enough tick labels for {rect}: x {xs} y {ys}")
    # The labels give the values; the tick marks (short segments in the axes colour on the left and
    # bottom edges) give the positions exactly. Label boxes sit about 0.2 pt below their ticks in this
    # PDF, which put a 0.1 % offset on every panel until 27 October; the marks remove it.
    tx, ty = tick_marks(page, rect)
    xs = sorted(xs); ys = sorted(ys, key=lambda t: -t[0])          # y labels from the bottom up, like the marks' values
    if len(tx) == len(xs) and max(abs(t - p) for t, (p, _) in zip(tx, xs)) < 2.5:
        xs = [(t, v) for t, (_, v) in zip(tx, xs)]
    ty_desc = sorted(ty, reverse=True)                               # page y grows downwards: bottom tick first
    if len(ty_desc) == len(ys) and max(abs(t - p) for t, (p, _) in zip(ty_desc, ys)) < 2.5:
        ys = [(t, v) for t, (_, v) in zip(ty_desc, ys)]
    ax, bx = np.polyfit([p for p, _ in xs], [v for _, v in xs], 1)
    ay, by = np.polyfit([p for p, _ in ys], [v for _, v in ys], 1)
    resx = max(abs(ax * p + bx - v) for p, v in xs); resy = max(abs(ay * p + by - v) for p, v in ys)
    return (ax, bx), (ay, by), (len(xs), len(ys), resx, resy)


def tick_marks(page, rect):
    """Positions of the tick marks: single short segments in the axes colour, horizontal on the left edge
    of the box (y positions) and vertical on the bottom edge (x positions)."""
    xs, ys = [], []
    for d in page.get_drawings():
        col = d.get("color")
        if col is None or len(d["items"]) != 1 or d["items"][0][0] != "l" or not all(abs(c - 0.149) < 0.05 for c in col):
            continue
        p1, p2 = d["items"][0][1], d["items"][0][2]
        if abs(p1.y - p2.y) < 0.05 and abs(min(p1.x, p2.x) - rect.x0) < 1.5 and 0.5 < abs(p2.x - p1.x) < 6 and rect.y0 - 1 <= p1.y <= rect.y1 + 1:
            ys.append(round(p1.y, 3))
        if abs(p1.x - p2.x) < 0.05 and abs(max(p1.y, p2.y) - rect.y1) < 1.5 and 0.5 < abs(p2.y - p1.y) < 6 and rect.x0 - 1 <= p1.x <= rect.x1 + 1:
            xs.append(round(p1.x, 3))
    return sorted(set(xs)), sorted(set(ys))


def curve_points(page, rect, colour, band):
    pts = []
    for d in page.get_drawings():
        r = d["rect"]
        if d.get("color") != colour or not (band[0] < r.y0 and r.y1 < band[1]) or len(d["items"]) < 20:   # short paths: legend samples
            continue
        if not (rect.x0 - 3 <= r.x0 and r.x1 <= rect.x1 + 3 and rect.y0 - 3 <= r.y0 and r.y1 <= rect.y1 + 3):
            continue
        for it in d["items"]:
            if it[0] == "l":
                pts.append((it[1].x, it[1].y)); pts.append((it[2].x, it[2].y))
            elif it[0] == "c":
                pts.append((it[1].x, it[1].y)); pts.append((it[4].x, it[4].y))
    return np.array(pts) if pts else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default=str(ROOT / "sources/papers/2024_fuchs_constant_velocity_physical_warp_drive_2405.02709.pdf"))
    args = ap.parse_args()
    import pymupdf
    doc = pymupdf.open(args.pdf)
    ours = {}
    if (HERE / "numbers.csv").exists():
        with open(HERE / "numbers.csv", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                ours[row["curve"]] = row
    OURS_KEY = {("static", "rho"): "static.rho", ("static", "rho_smoothed_c2"): "profile.rho_smoothed_c2", ("static", "P_2 (radial)"): "static.P_yy",
                ("static", "rho_unsmoothed_c2"): "profile.rho_unsmoothed_c2", ("static", "P_unsmoothed"): "profile.P_unsmoothed",
                ("static", "g00"): "static.g00", ("static", "g22"): "static.g22",
                ("static", "P_1 = P_3 (tangential)"): "static.P_xx", ("static", "P_smoothed"): "profile.P_smoothed",
                ("static", "null"): "static.null", ("static", "weak"): "static.weak", ("static", "strong"): "static.strong", ("static", "dominant"): "static.dominant",
                ("warp", "rho"): "warp.rho", ("warp", "P_2"): "warp.P_yy", ("warp", "P_1"): "warp.P_xx", ("warp", "P_3"): "warp.P_zz", ("warp", "p_1"): "warp.p_x",
                ("warp", "p_2 = p_3"): "warp.p_y", ("warp", "sigma_12"): "warp.P_xy", ("warp", "null"): "warp.null", ("warp", "weak"): "warp.weak",
                ("warp", "strong"): "warp.strong", ("warp", "dominant"): "warp.dominant"}
    out = open(HERE / "paper_curves.csv", "w", encoding="utf-8")
    out.write("figure,panel,curve,r_m,value\n")
    cmp = open(HERE / "comparison.csv", "w", encoding="utf-8")
    cmp.write("figure,panel,curve,paper_max,paper_r_of_max_m,paper_min,paper_r_of_min_m,ours_max,ours_r_of_max_m,ours_min,ours_r_of_min_m,paper_over_ours_max\n")
    print(f"{'fig':>3s} {'panel':<15s} {'curve':<24s} | {'paper max':>11s} {'at r':>6s} {'paper min':>11s} {'at r':>6s} | {'ours max':>11s} {'at r':>6s} {'ours min':>11s} {'at r':>6s} | {'max ratio':>9s}")
    for n, F in FIGS.items():
        page = doc[F["page"] - 1]
        case = "static" if n in (4, 5, 6, 7) else "warp"
        for pname, P in F["panels"].items():
            rect = panel_rect(page, P["box"], F["band"])
            (ax, bx), (ay, by), info = calibrate(page, rect)
            scale = P.get("scale", F["scale"])
            for col, cname in P["curves"].items():
                pts = curve_points(page, rect, COLOURS[col], F["band"])
                if pts is None:
                    print(f"{n:3d} {pname:<15s} {cname:<24s} | no path found"); continue
                r = ax * pts[:, 0] + bx
                v = (ay * pts[:, 1] + by) * scale
                order = np.argsort(r); r, v = r[order], v[order]
                for ri, vi in zip(r, v):
                    out.write(f"{n},{pname},{cname},{ri:.4f},{vi:.6e}\n")
                i, j = int(np.argmax(v)), int(np.argmin(v))
                o = ours.get(OURS_KEY.get((case, cname), ""))
                os_ = f"{float(o['max']):+11.3e} {float(o['r_of_max_m']):6.2f} {float(o['min']):+11.3e} {float(o['r_of_min_m']):6.2f} | {v[i] / float(o['max']) if float(o['max']) else float('nan'):9.4f}" if o else "(no counterpart)"
                print(f"{n:3d} {pname:<15s} {cname:<24s} | {v[i]:+11.3e} {r[i]:6.2f} {v[j]:+11.3e} {r[j]:6.2f} | {os_}   [{len(pts)} pts; ticks {info[0]}x {info[1]}y, residual {info[2]:.2g} m, {info[3]:.2g}]")
                if o:
                    cmp.write(f"{n},{pname},{cname},{v[i]:.6e},{r[i]:.2f},{v[j]:.6e},{r[j]:.2f},{float(o['max']):.6e},{float(o['r_of_max_m']):.2f},{float(o['min']):.6e},{float(o['r_of_min_m']):.2f},"
                              f"{v[i] / float(o['max']) if float(o['max']) else float('nan'):.4f}\n")
    out.close(); cmp.close()
    print("written:", HERE / "paper_curves.csv", "and", HERE / "comparison.csv")


if __name__ == "__main__":
    main()
