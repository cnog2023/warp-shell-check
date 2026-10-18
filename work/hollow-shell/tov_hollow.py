"""
tov_hollow.py -- the static hollow shell of isotropic fluid, done three ways, at the paper's numbers.

Paper's shell (Fuchs et al. 2024, §3-4): R1 = 10 m, R2 = 20 m, M = 4.49e27 kg, constant density in
the shell, vacuum inside and outside. Geometric units G = c = 1, lengths in metres, so M -> GM/c^2.

(1) Hollow-shell TOV, integrated inward from P(R2) = 0 with the shell's own enclosed mass m(r).
    This is what the paper's text (eq. 21) describes. Gives P(R1), and the lapse a(r) when a is
    matched to Schwarzschild at R2 (as WarpFactory's alphaNumericSolver.m does, at the outer edge).
(2) WarpFactory's actual pressure step, Metrics/utils/TOVconstDensity.m: the closed-form
    interior-Schwarzschild pressure of a uniform SOLID sphere of radius R2 and mass M, evaluated in
    the shell. Not the same as (1).
(3) Barzegar, Buchert, Vigneron 2026, Appendix B, eq. (B.6): P(R1)/rho = sqrt(1 - 2M/R2) - 1 < 0.
    Follows from their (B.5) only if one imposes a(R1) = 0 (their B.3) together with the
    Schwarzschild match at R2 (their B.2). Route (1) imposes only the latter.

Also checks the identity (rho + P) e^{a} = const through the shell, which is (B.5) in disguise, and
reports the cavity's clock rate exp(a(R1)) relative to infinity.

Usage: python tov_hollow.py
"""
import numpy as np

G = 6.67430e-11
c = 2.99792458e8

R1, R2 = 10.0, 20.0           # m
M_kg = 4.49e27                # kg, paper's value (2.365 Jupiter masses)
M = G * M_kg / c**2           # geometric mass in metres
rho = M / (4.0 / 3.0 * np.pi * (R2**3 - R1**3))   # geometric density, 1/m^2


def m_enclosed(r):
    return M * (r**3 - R1**3) / (R2**3 - R1**3)


def tov_rhs(r, P):
    """dP/dr for isotropic pressure with the shell's own m(r)."""
    m = m_enclosed(r)
    return -(rho + P) * (m + 4 * np.pi * r**3 * P) / (r * (r - 2 * m))


def dadr(r, P):
    m = m_enclosed(r)
    return (m + 4 * np.pi * r**3 * P) / (r * (r - 2 * m))


def integrate_inward(n=200000):
    """RK4 from R2 to R1 for P (with P(R2) = 0) and for a (with a(R2) = Schwarzschild)."""
    rs = np.linspace(R2, R1, n + 1)
    h = rs[1] - rs[0]           # negative
    P = np.zeros_like(rs)
    a = np.zeros_like(rs)
    a[0] = 0.5 * np.log(1 - 2 * M / R2)
    for i in range(n):
        r, p = rs[i], P[i]
        k1 = tov_rhs(r, p)
        k2 = tov_rhs(r + h / 2, p + h / 2 * k1)
        k3 = tov_rhs(r + h / 2, p + h / 2 * k2)
        k4 = tov_rhs(r + h, p + h * k3)
        P[i + 1] = p + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        # a uses the same stepping with P interpolated by the stage values
        l1 = dadr(r, p)
        l2 = dadr(r + h / 2, p + h / 2 * k1)
        l3 = dadr(r + h / 2, p + h / 2 * k2)
        l4 = dadr(r + h, p + h * k3)
        a[i + 1] = a[i] + h / 6 * (l1 + 2 * l2 + 2 * l3 + l4)
    return rs, P, a


def solid_sphere_pressure(r, R=R2):
    """TOVconstDensity.m, in geometric units: uniform sphere of radius R and mass M (the paper's M)."""
    num = R * np.sqrt(R - 2 * M) - np.sqrt(R**3 - 2 * M * r**2)
    den = np.sqrt(R**3 - 2 * M * r**2) - 3 * R * np.sqrt(R - 2 * M)
    return rho * num / den


def main():
    comp = 2 * M / R2
    print(f"paper's shell: R1 = {R1:g} m, R2 = {R2:g} m, M = {M_kg:.3g} kg = {M:.4f} m (geometric)")
    print(f"compactness 2GM/(R2 c^2) = {comp:.4f};  shell density rho = {rho * c**2 / G:.3e} kg/m^3 ({rho:.3e} 1/m^2)")
    print()

    rs, P, a = integrate_inward()
    P_R1 = P[-1]
    a_R1, a_R2 = a[-1], a[0]
    const = (rho + P) * np.exp(a)
    print("(1) hollow-shell TOV, inward from P(R2) = 0, lapse matched to Schwarzschild at R2")
    print(f"    P(R1)/rho c^2            = {P_R1 / rho:+.5f}   (positive: compression at the free inner face)")
    print(f"    a(R2) = {a_R2:+.5f}, a(R1) = {a_R1:+.5f};  cavity clock rate exp(a(R1)) = {np.exp(a_R1):.5f} of infinity")
    print(f"    identity (rho+P) e^a const:  max relative drift through the shell = {np.max(np.abs(const / const[0] - 1)):.2e}")
    print(f"    (B.5) check: ln[rho/(rho+P(R1))] = {np.log(rho / (rho + P_R1)):+.5f}  vs  a(R1) - a(R2) = {a_R1 - a_R2:+.5f}")
    print()

    P_ss = solid_sphere_pressure(np.array([R1, 0.5 * (R1 + R2), R2]))
    print("(2) WarpFactory's TOVconstDensity.m (uniform SOLID sphere of radius R2), evaluated in the shell")
    print(f"    P(R1)/rho c^2 = {P_ss[0] / rho:+.5f};  P(mid)/rho c^2 = {P_ss[1] / rho:+.5f};  P(R2)/rho c^2 = {P_ss[2] / rho:+.5f}")
    print(f"    ratio to the hollow-shell value at R1: {P_ss[0] / P_R1:.3f}")
    print()

    P_bbv = np.sqrt(1 - comp) - 1
    print("(3) Barzegar et al. (B.6), which assumes a(R1) = 0 as well as the match at R2")
    print(f"    P(R1)/rho c^2 = {P_bbv:+.5f}   (negative: tension)")
    print(f"    what a(R1) = 0 would require of the outer lapse: a(R2) = ln[rho/(rho+P(R1))] with the true P(R1) gives {np.log(rho / (rho + P_R1)):+.5f},")
    print(f"    but the Schwarzschild match fixes a(R2) = {a_R2:+.5f}; both cannot hold unless M = 0.")
    print()

    # a sampled profile for later plotting / for comparison with WarpFactory's Metric.params.P
    out = np.column_stack([rs[::-1], P[::-1] / rho, a[::-1]])
    np.savetxt("tov_hollow_profile.csv", out, delimiter=",", header="r_m,P_over_rho_c2,a", comments="")
    print("profile written: tov_hollow_profile.csv  (r, P/rho c^2, a)  from R1 to R2")


if __name__ == "__main__":
    main()
