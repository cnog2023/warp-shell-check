"""
verify_null_bug.py -- why WarpFactory's sampled Null and Weak maps go negative before the Dominant
and Strong maps and before a direct null check do.

Reading Analyzer/getEnergyConditions.m: after doFrameTransfer the stress-energy is in the orthonormal
Eulerian frame, flagged contravariant. The Null and Weak branches then call
changeTensorIndex(energyTensor, "covariant", metric) with the COORDINATE metric, whereas the
Dominant and Strong branches use a Minkowski metric for the same step. Lowering the indices of a
frame tensor with the coordinate metric is only harmless where that metric is Minkowski; inside the
shell wall (g_rr differs from 1) and wherever the shift makes g_01 nonzero it mixes components.

This script replicates their Null evaluation in NumPy on one exported slice, first with the
coordinate metric (should reproduce their map), then with Minkowski (the consistent version), and
compares both with the dense null check. Usage: python verify_null_bug.py run-fine 1 7
(compactness index, beta index; defaults to C = 1/3, beta/C = 0.08).
"""
import sys
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from analyse_matrix import eulerian_tensor, fibonacci_sphere, nec_dense

run = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("run-fine")
a = int(sys.argv[2]) if len(sys.argv) > 2 else 1
b = int(sys.argv[3]) if len(sys.argv) > 3 else 7
s = loadmat(run / f"slice_f{a}_b{b}.mat")
rho0 = float(np.squeeze(s["rho0"])); beta = float(np.squeeze(s["beta"])); C = 2 * 6.67430e-11 * float(np.squeeze(s["M_kg"])) / (20.0 * 2.99792458e8**2)
print(f"slice f{a}_b{b}: compactness {C:.4f}, beta = {beta:.4f} (beta/C = {beta / C:.3f}), rho0 = {rho0:.3e} J/m^3")

edge = 2; sl = slice(edge, -edge)
T = eulerian_tensor(s)                       # (N,4,4) orthonormal Eulerian frame, contravariant
n = T.shape[0]
# coordinate metric on the central plane: g02 = g03 = g13 = g23 = 0 there by symmetry
g = np.zeros((n, 4, 4))
for (i, j, key) in [(0, 0, "g00"), (0, 1, "g01"), (1, 1, "g11"), (1, 2, "g12"), (2, 2, "g22"), (3, 3, "g33")]:
    v = np.asarray(s[key])[sl, sl].ravel()
    g[:, i, j] = v; g[:, j, i] = v
eta = np.diag([-1.0, 1.0, 1.0, 1.0])

# WarpFactory's null observers: getEvenPointsOnSphere golden-ratio spiral, 100 points, k = (1, n)/sqrt(2)
N = 100; i = np.arange(N); gr = (1 + 5 ** 0.5) / 2
theta = 2 * np.pi * i / gr; phi = np.arccos(1 - 2 * (i + 0.5) / N)
k = np.stack([np.ones(N), np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)], axis=1) / np.sqrt(2)

def their_null(Tup, metric):
    Tdown = np.einsum("nac,ncd,nbd->nab", metric, Tup, metric)      # T_ab = g_ac g_bd T^cd
    vals = np.einsum("nab,ka,kb->nk", Tdown, k, k)
    return vals.min(axis=1)

wf = np.asarray(s["null"])[sl, sl].ravel()                            # WarpFactory's exported map
mine_g = their_null(T, g)
mine_eta = their_null(T, np.broadcast_to(eta, (n, 4, 4)))
dense = nec_dense(T, fibonacci_sphere(4000))

print(f"WarpFactory's Null map, min over plane            : {wf.min() / rho0:+.4e} rho0")
print(f"replica with the coordinate metric, min           : {mine_g.min() / rho0:+.4e} rho0   max |replica - WarpFactory| / rho0 = {np.max(np.abs(mine_g - wf)) / rho0:.2e}")
print(f"same evaluation with the Minkowski metric, min    : {mine_eta.min() / rho0:+.4e} rho0")
print(f"dense null check (4000 directions, Minkowski), min: {dense.min() / rho0:+.4e} rho0")
act = np.abs(T).reshape(n, -1).max(axis=1) > 1e-6 * rho0
print(f"points where the coordinate-metric version is below -1e-4 rho0: {int((mine_g < -1e-4 * rho0).sum())}; Minkowski version: {int((mine_eta < -1e-4 * rho0).sum())}; dense: {int((dense < -1e-4 * rho0).sum())}  (of {int(act.sum())} active points)")
