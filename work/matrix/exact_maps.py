"""
exact_maps.py -- the central plane at two shifts, seen by the exact check and by the sampled one (Part 2).

Two cases from the refined matrix at the paper's compactness (C = 1/3): the paper's own shift
(beta = 0.02, beta/C = 0.06, slice f1_b5) and the first failing shift of Part 1 (beta/C = 0.10,
slice f1_b9). For each, three maps on the central plane, edge cells dropped, in units of rho0:
the Eulerian momentum density |j| (what the shift adds and what breaks the conditions), warpax's
exact DEC margin from the S-lemma LMI (certify_point_lmi on the frame tensor, as in
exact_conditions.py route A), and WarpFactory's sampled Dominant map as exported, with the cells
the exact check finds violated but the sampled map does not marked on top.

Usage: python exact_maps.py <run_dir> [--cases 5,9] [--png out.png]   (default cases: 5 and 9 of compactness 1)
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
import numpy as np
from scipy.io import loadmat

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyse_matrix import ETA, NOISE as TAU, eulerian_tensor
from exact_conditions import ACTIVE, EDGE, in_chunks, warpax_functions


def case_maps(path, rho0, fx):
    jax, jnp, cert_eta, *_ = fx
    s = loadmat(path)
    beta = float(np.squeeze(s["beta"]))
    sl = slice(EDGE, -EDGE)
    x = np.asarray(s["x"]).ravel()[sl]
    y = np.asarray(s["y"]).ravel()[sl]
    T = eulerian_tensor(s, EDGE)
    n = T.shape[0]
    act = np.abs(T).reshape(n, -1).max(axis=1) > ACTIVE * rho0
    That = np.einsum("ij,njk,kl->nil", ETA, T[act], ETA)
    ex = in_chunks(cert_eta, jnp, That)
    dec = np.full(n, np.nan)
    dec[act] = ex["dec"] / rho0
    mom = np.sqrt(T[:, 0, 1] ** 2 + T[:, 0, 2] ** 2 + T[:, 0, 3] ** 2) / rho0
    dom = np.asarray(s["dominant"])[sl, sl].ravel() / rho0
    shape = (len(x), len(y))
    missed = (dec < -TAU) & ~(dom < -TAU)
    found = (dec < -TAU) & (dom < -TAU)
    return dict(beta=beta, x=x, y=y, dec=dec.reshape(shape), mom=mom.reshape(shape), dom=dom.reshape(shape),
                missed=missed.reshape(shape), found=found.reshape(shape), n_viol=int((dec < -TAU).sum()), n_missed=int(missed.sum()))


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--cases", default="5,9", help="shift indices b of compactness 1 to draw (default 5 = the paper's shift 0.02, 9 = the first failing one, beta/C = 0.10)")
    ap.add_argument("--png", default=None)
    a = ap.parse_args()
    run = Path(a.run)
    png = a.png or str(run.parent / "exact_maps.png")
    cases = [int(c) for c in a.cases.split(",")]
    rho0 = float(np.squeeze(loadmat(run / "slice_f1_b1.mat")["rho0"]))
    comp = 1 / 3
    fx = warpax_functions()
    rows = [case_maps(run / f"slice_f1_b{b}.mat", rho0, fx) for b in cases]
    for r in rows:
        print(f"beta {r['beta']:.4f} (beta/C {r['beta']/comp:.3f}): exact DEC min {np.nanmin(r['dec']):+.3e} rho0, violating cells {r['n_viol']}, missed by the sampled Dominant map {r['n_missed']}; max |j| {np.nanmax(r['mom']):.3f} rho0")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(len(rows), 3, figsize=(15, 4.6 * len(rows)), squeeze=False)
    for i, r in enumerate(rows):
        ext = [r["x"][0], r["x"][-1], r["y"][0], r["y"][-1]]
        boc = r["beta"] / comp
        tag = " (the paper's point)" if abs(r["beta"] - 0.02) < 1e-6 else (" (first failing shift)" if abs(boc - 0.10) < 1e-3 else "")
        lab = f"beta = {r['beta']:.4f}, beta / C = {boc:.2f}{tag}"
        im = ax[i, 0].imshow(r["mom"].T, origin="lower", extent=ext, cmap="viridis", vmin=0, vmax=0.5)
        ax[i, 0].set_title(f"Eulerian momentum density |j| / rho0\n{lab}", fontsize=9)
        fig.colorbar(im, ax=ax[i, 0], fraction=0.046)
        lim = 0.06
        im = ax[i, 1].imshow(r["dec"].T, origin="lower", extent=ext, cmap="RdBu", vmin=-lim, vmax=lim)
        ax[i, 1].set_title("exact DEC margin / rho0 (warpax, all observers)\nblue: satisfied, red: violated", fontsize=9)
        fig.colorbar(im, ax=ax[i, 1], fraction=0.046)
        im = ax[i, 2].imshow(r["dom"].T, origin="lower", extent=ext, cmap="RdBu", vmin=-lim, vmax=lim)
        if r["n_viol"]:
            X, Y = np.meshgrid(r["x"], r["y"], indexing="ij")
            ax[i, 2].scatter(X[r["found"]], Y[r["found"]], s=2, color="k", label=f"violation found by both ({int(r['found'].sum())})")
            ax[i, 2].scatter(X[r["missed"]], Y[r["missed"]], s=6, color="yellow", edgecolor="k", linewidth=0.3, label=f"found by the exact check only ({r['n_missed']})")
            ax[i, 2].legend(fontsize=7, loc="upper right")
        ax[i, 2].set_title("WarpFactory's sampled Dominant map / rho0 (100 directions)\ndots: cells violated at the 1e-4 rho0 threshold", fontsize=9)
        fig.colorbar(im, ax=ax[i, 2], fraction=0.046)
        for a in ax[i]:
            a.set_xlabel("x [m] (shift direction)"); a.set_ylabel("y [m]")
            for R in (10, 20):
                a.add_patch(plt.Circle((0, 0), R, fill=False, color="w", lw=0.5, ls="--"))
    fig.tight_layout(); fig.savefig(png, dpi=130)
    print(f"figure written: {png}")


if __name__ == "__main__":
    main()
