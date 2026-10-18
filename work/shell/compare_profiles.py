"""
compare_profiles.py -- MATLAB's exported 1D construction against the NumPy replica, column by column.

    python compare_profiles.py ci-artifacts/profiles_static.csv replica/profiles_static.csv

Reports, for each column, the largest absolute difference divided by the column's largest absolute
value, and where it occurs. Identical algorithms should agree to round-off, about 1e-12 or better;
a larger difference localised near r = 0 or near the far end points at the moving-average edge
rule; a difference inside the shell points at a real discrepancy between the two implementations.
"""
import sys

import numpy as np


def load(path):
    with open(path, encoding="utf-8") as f:
        header = f.readline().strip().split(",")
    return header, np.loadtxt(path, delimiter=",", skiprows=1)


def main(a_path, b_path):
    ha, A = load(a_path)
    hb, B = load(b_path)
    assert ha == hb, f"column mismatch: {ha} vs {hb}"
    assert A.shape == B.shape, f"shape mismatch: {A.shape} vs {B.shape}"
    r = A[:, 0]
    print(f"{'column':18s} {'max|diff|/max|val|':>20s} {'at r [m]':>10s} {'max|val|':>14s}")
    for j, name in enumerate(ha):
        scale = np.max(np.abs(A[:, j])) or 1.0
        d = np.abs(A[:, j] - B[:, j])
        i = int(np.argmax(d))
        print(f"{name:18s} {d[i] / scale:20.3e} {r[i]:10.3f} {scale:14.6e}")
    # the same restricted to the shell region, where it matters
    m = (r > 4.0) & (r < 26.0)
    print("\nrestricted to 4 m < r < 26 m:")
    for j, name in enumerate(ha):
        scale = np.max(np.abs(A[m, j])) or 1.0
        d = np.abs(A[m, j] - B[m, j])
        i = int(np.argmax(d))
        print(f"{name:18s} {d[i] / scale:20.3e} {r[m][i]:10.3f}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
