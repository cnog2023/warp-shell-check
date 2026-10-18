"""
replicate_profiles.py -- WarpFactory's 1D shell construction re-done in NumPy, step for step.

Replicates Metrics/WarpShell/metricGet_WarpShellComoving.m up to the radial profiles it stores in
Metric.params (rVec, rho, rhosmooth, P, Psmooth, M, A, B) for the W1 example configuration, so that
(a) hoop_stress.py can be exercised before the CI artifact exists and (b) the MATLAB profiles can be
checked against an independent implementation when it does.

MATLAB semantics reproduced:
  smooth(y, span)   Curve Fitting Toolbox moving average: even span reduced by one; near the ends
                    the window shrinks symmetrically (yy(1) = y(1), yy(2) = mean(y(1:3)), ...).
  cumtrapz(x, y)    cumulative trapezoid starting at 0.
  TOVconstDensity   closed-form uniform-sphere pressure, masked by the density array.
  alphaNumericSolver trapezoid integral of da/dr from r = 0, offset to Schwarzschild at r(end).

Usage: python replicate_profiles.py [out_dir]   (writes profiles_static.csv in the same format as build_shell.m)
"""
import sys
from pathlib import Path
import numpy as np

G = 6.67430e-11
c = 2.99792458e8


def matlab_smooth(y, span):
    span = int(span)
    if span % 2 == 0:
        span -= 1
    half = (span - 1) // 2
    n = y.size
    cs = np.concatenate([[0.0], np.cumsum(y)])
    yy = np.empty_like(y)
    idx = np.arange(n)
    h = np.minimum(half, np.minimum(idx, n - 1 - idx))
    lo = idx - h
    hi = idx + h + 1
    yy[:] = (cs[hi] - cs[lo]) / (hi - lo)
    return yy


def cumtrapz(x, y):
    out = np.zeros_like(y)
    out[1:] = np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x))
    return out


def build(R1=10.0, R2=20.0, spaceScale=5, cartoonThickness=5, smoothFactor=4000, factor=1.0 / 3.0):
    gridSize = np.ceil([1, 2 * (R2 + 10) * spaceScale, 2 * (R2 + 10) * spaceScale, cartoonThickness]).astype(int)
    gridScaling = np.array([0.0, 1 / spaceScale, 1 / spaceScale, 1 / spaceScale])
    worldCenter = np.array([(cartoonThickness + 1) / 2, (2 * (R2 + 10) * spaceScale + 1) / 2,
                            (2 * (R2 + 10) * spaceScale + 1) / 2, (cartoonThickness + 1) / 2]) * np.array([1, *gridScaling[1:]])
    m = R2 / (2 * G) * c**2 * factor
    worldSize = np.sqrt(sum((gridSize[k] * gridScaling[k] - worldCenter[k])**2 for k in (1, 2, 3)))
    r = np.linspace(0, worldSize * 1.2, 10**5)
    rho = m / (4 / 3 * np.pi * (R2**3 - R1**3)) * ((r > R1) & (r < R2))
    M = cumtrapz(r, 4 * np.pi * rho * r**2)
    Mend = M[-1]
    R = R2
    # MATLAB's sqrt of a negative argument (r beyond ~34.6 m here) is complex, and the (r < R) mask
    # then zeroes it; NumPy would give NaN, so the argument is clipped where the mask is zero anyway.
    arg = np.maximum(R**3 - 2 * G * Mend * r**2 / c**2, 0.0)
    num = R * np.sqrt(R - 2 * G * Mend / c**2) - np.sqrt(arg)
    den = np.sqrt(arg) - 3 * R * np.sqrt(R - 2 * G * Mend / c**2)
    P = c**2 * rho * (num / den) * (r < R)
    rhos = rho.copy()
    for _ in range(4):
        rhos = matlab_smooth(rhos, 1.79 * smoothFactor)
    Ps = P.copy()
    for _ in range(4):
        Ps = matlab_smooth(Ps, smoothFactor)
    Ms = cumtrapz(r, 4 * np.pi * rhos * r**2)
    Ms[Ms < 0] = Ms.max()
    B = (1 - 2 * G * Ms / r / c**2)**(-1)
    B[0] = 1.0
    with np.errstate(invalid="ignore", divide="ignore"):
        dalpha = (G * Ms / c**2 + 4 * np.pi * G * r**3 * Ps / c**4) / (r**2 - 2 * G * Ms * r / c**2)
    dalpha[0] = 0.0
    aT = cumtrapz(r, dalpha)
    C = 0.5 * np.log(1 - 2 * G * Ms[-1] / r[-1] / c**2)
    a = aT + (C - aT[-1])
    A = -np.exp(2 * a)
    return dict(r_m=r, rho_kg_m3=rho, rhosmooth_kg_m3=rhos, P_Pa=P, Psmooth_Pa=Ps, M_kg=Ms, A_g00=A, B_grr=B,
                m=m, worldSize=worldSize, gridSize=gridSize)


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "replica"
    out.mkdir(parents=True, exist_ok=True)
    d = build()
    cols = ["r_m", "rho_kg_m3", "rhosmooth_kg_m3", "P_Pa", "Psmooth_Pa", "M_kg", "A_g00", "B_grr"]
    data = np.column_stack([d[k] for k in cols])
    np.savetxt(out / "profiles_static.csv", data, delimiter=",", header=",".join(cols), comments="", fmt="%.17g")
    print(f"M = {d['m']:.6g} kg; worldSize = {d['worldSize']:.4f} m; r in [0, {d['r_m'][-1]:.4f}] m, dr = {d['r_m'][1]:.4e} m; grid {d['gridSize']}")
    r = d["r_m"]
    i1 = np.argmin(np.abs(r - 10.0)); i2 = np.argmin(np.abs(r - 20.0)); i5 = np.argmin(np.abs(r - 5.0))
    rho0 = d["rho_kg_m3"].max()
    print(f"unsmoothed P at R1 / rho c^2 = {d['P_Pa'][i1 + 2] / (rho0 * c**2):.5f} (solid-sphere closed form)")
    print(f"smoothed: rhosmooth(R1)/rho0 = {d['rhosmooth_kg_m3'][i1] / rho0:.4f}, Psmooth(R1)/rho0 c^2 = {d['Psmooth_Pa'][i1] / (rho0 * c**2):.5f}")
    print(f"cavity lapse exp(a) at r = 5 m: {np.sqrt(-d['A_g00'][i5]):.5f}; g00 at R2: {d['A_g00'][i2]:+.5f}; total smoothed mass / m = {d['M_kg'][-1] / d['m']:.6f}")
    print(f"written: {out / 'profiles_static.csv'}")


if __name__ == "__main__":
    main()
