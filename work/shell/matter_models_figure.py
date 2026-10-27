"""
matter_models_figure.py -- the two matter models that could hold the shell up, as a picture.

Left: an elastic shell, a solid hollow ball whose inner wall carries a hoop compression (arrows along
the circumference) of 0.19 rho0 c^2 and a radial pressure of 0.077 rho0 c^2, the numbers of
work/shell/RESULTS.md section 3 at the authors' setting. Right: the swarm (Einstein cluster) of
work/notes/06-counter-rotation.md: particles on circular orbits through the centre of mass, orbital
planes in every direction, half each way, nothing touching; orbital speed set by the enclosed mass,
from near zero at the inner wall to 0.46 c at the outer one (note 06 section 2). Both drawn in
cross-section at the paper's geometry, R1 = 10 m, R2 = 20 m.

Usage: python matter_models_figure.py [--png out.png]
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, FancyArrowPatch, Ellipse

R1, R2 = 10.0, 20.0
png = sys.argv[sys.argv.index("--png") + 1] if "--png" in sys.argv else str(Path(__file__).parent / "matter_models.png")

fig, ax = plt.subplots(1, 2, figsize=(13, 6.6))
for a in ax:
    a.set_aspect("equal"); a.set_xlim(-26, 26); a.set_ylim(-26, 26); a.axis("off")

# --- left: the elastic shell
a = ax[0]
a.add_patch(Wedge((0, 0), R2, 0, 360, width=R2 - R1, facecolor="#c9c2b8", edgecolor="#6b6259", lw=1.2))
a.add_patch(Wedge((0, 0), R1 + 2.2, 0, 360, width=2.2, facecolor="#a8402f", alpha=0.55, edgecolor="none"))
# hoop compression: arrows pointing along the circumference toward each other at the inner wall
for k in range(8):
    th = 2 * np.pi * k / 8
    r = R1 + 1.1
    p0 = np.array([r * np.cos(th - 0.28), r * np.sin(th - 0.28)]); p1 = np.array([r * np.cos(th - 0.05), r * np.sin(th - 0.05)])
    q0 = np.array([r * np.cos(th + 0.28), r * np.sin(th + 0.28)]); q1 = np.array([r * np.cos(th + 0.05), r * np.sin(th + 0.05)])
    a.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=12, color="#5a1d12", lw=1.6))
    a.add_patch(FancyArrowPatch(q0, q1, arrowstyle="-|>", mutation_scale=12, color="#5a1d12", lw=1.6))
# radial pressure: short arrows across the wall at 12 m
for k in range(6):
    th = 2 * np.pi * k / 6 + 0.3
    r = 13.5
    p0 = np.array([(r + 1.4) * np.cos(th), (r + 1.4) * np.sin(th)]); p1 = np.array([(r - 1.4) * np.cos(th), (r - 1.4) * np.sin(th)])
    a.add_patch(FancyArrowPatch(p0, p1, arrowstyle="<|-|>", mutation_scale=9, color="#3a3a3a", lw=1.0))
a.text(0, 0, "empty\ncavity", ha="center", va="center", fontsize=11, color="#444")
a.text(0, 23.8, "An elastic shell: a solid hollow ball", ha="center", fontsize=13, fontweight="bold")
a.text(0, -22.8, "Inner wall: hoop compression of 0.19 of the energy density\n(2.6e39 Pa), like the hoop of a barrel.\nRadial pressure 0.077. No known material comes within\na factor of a billion of the strength-to-energy ratio needed.",
       ha="center", va="top", fontsize=9.5, color="#333")

# --- right: the swarm
a = ax[1]
a.add_patch(Wedge((0, 0), R2, 0, 360, width=R2 - R1, facecolor="#dfe8ee", edgecolor="#8aa0ad", lw=1.0, ls="--"))
rng = np.random.default_rng(3)
cmap = plt.get_cmap("viridis")
for k in range(16):
    r = R1 + 0.6 + (R2 - R1 - 1.2) * k / 15
    v = 0.46 * ((r - R1) / (R2 - R1)) ** 0.8          # illustrative: slow inside, 0.46 c at the outer wall
    incl = rng.uniform(0.15, 1.0)                      # projected great circle: an ellipse of axis ratio incl
    ang = rng.uniform(0, 180)
    col = cmap(v / 0.46)
    a.add_patch(Ellipse((0, 0), 2 * r, 2 * r * incl, angle=ang, fill=False, edgecolor=col, lw=1.6, alpha=0.9))
    # a particle and its direction of travel, alternating sense
    t = rng.uniform(0, 2 * np.pi); s = 1 if k % 2 == 0 else -1
    ca, sa = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    x, y = r * np.cos(t), r * incl * np.sin(t)
    dx, dy = -r * np.sin(t) * s, r * incl * np.cos(t) * s
    X, Y = ca * x - sa * y, sa * x + ca * y
    DX, DY = ca * dx - sa * dy, sa * dx + ca * dy
    n = np.hypot(DX, DY); DX, DY = DX / n * 2.4, DY / n * 2.4
    a.plot(X, Y, "o", color=col, ms=5)
    a.add_patch(FancyArrowPatch((X, Y), (X + DX, Y + DY), arrowstyle="-|>", mutation_scale=11, color=col, lw=1.4))
a.text(0, 0, "empty\ncavity", ha="center", va="center", fontsize=11, color="#444")
a.text(0, 23.8, "A swarm: particles in orbit, nothing touching", ha="center", fontsize=13, fontweight="bold")
a.text(0, -22.8, "Every particle on a circular orbit through the centre, planes in all\ndirections, half each way. Orbital speed from near zero at the inner\nwall (dark) to 0.46 c at the outer wall (yellow). Needs no strength;\nneeds two Jupiter masses in orbit inside 20 m.",
       ha="center", va="top", fontsize=9.5, color="#333")
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 0.46))
cb = fig.colorbar(sm, ax=a, fraction=0.04, pad=0.01); cb.set_label("orbital speed, fraction of c")

fig.suptitle("Two ways to hold up the Fuchs shell (R1 = 10 m, R2 = 20 m, 4.5e27 kg), in cross-section", fontsize=13)
fig.tight_layout(); fig.savefig(png, dpi=140)
print("figure written:", png)
