"""
precision_probe.py

WarpFactory's solver arithmetic (Solver/utils/*.m) ported line for line to NumPy,
then run against cases with a known exact answer, so numerical error can be measured.

  Case 0  Minkowski            exact T = 0, must come out exactly zero
  Case A  Alcubierre           T^00 vs Alcubierre's closed-form energy density, three grid spacings
  Case B  Schwarzschild vacuum exact T = 0, so every nonzero digit is numerical error;
                               swept over grid spacing in float64 and float32

Faithful to the MATLAB: same 4th-order stencils and boundary fill, same cofactor inverse,
same Ricci loop structure and operation order, same 1/c factors on time derivatives,
same c^4/(8 pi G) scaling to J/m^3.

Usage:  python precision_probe.py [output.png]
"""
import sys
import time
import numpy as np

c = 2.99792458e8            # Units/Universal Constants/c.m
G = 6.67430e-11             # Units/Universal Constants/G.m
KAPPA = c**4 / (8 * np.pi * G)   # einE.m: J/m^3 per unit Einstein tensor (1/m^2)


# ---------------------------------------------------------------- takeFiniteDifference1.m
def fd1(A, k, delta):
    B = np.zeros_like(A)
    if A.shape[k] >= 5:
        Am = np.moveaxis(A, k, 0)
        Bm = np.moveaxis(B, k, 0)
        Bm[2:-2] = (-(Am[4:] - Am[:-4]) + 8 * (Am[3:-1] - Am[1:-3])) / (12 * delta[k])
        Bm[0] = Bm[2]
        Bm[1] = Bm[2]
        Bm[-2] = Bm[-3]
        Bm[-1] = Bm[-3]
    return B


# ---------------------------------------------------------------- takeFiniteDifference2.m
def fd2(A, k1, k2, delta):
    B = np.zeros_like(A)
    s = A.shape
    if s[k1] >= 5 and s[k2] >= 5:
        if k1 == k2:
            Am = np.moveaxis(A, k1, 0)
            Bm = np.moveaxis(B, k1, 0)
            Bm[2:-2] = (-(Am[4:] + Am[:-4]) + 16 * (Am[3:-1] + Am[1:-3]) - 30 * Am[2:-2]) / (12 * delta[k1] ** 2)
            Bm[0] = Bm[2]
            Bm[1] = Bm[2]
            Bm[-2] = Bm[-3]
            Bm[-1] = Bm[-3]
        else:
            kS, kL = min(k1, k2), max(k1, k2)
            Am = np.moveaxis(A, (kS, kL), (0, 1))
            Bm = np.moveaxis(B, (kS, kL), (0, 1))
            nS, nL = s[kS], s[kL]

            def X(i, j):
                return Am[2 + i:nS - 2 + i, 2 + j:nL - 2 + j]

            # mixed derivative: boundaries stay zero, exactly as in the MATLAB
            Bm[2:-2, 2:-2] = 1 / (12 ** 2 * delta[kL] * delta[kS]) * (
                -(-(X(2, 2) - X(-2, 2)) + 8 * (X(1, 2) - X(-1, 2)))
                + (-(X(2, -2) - X(-2, -2)) + 8 * (X(1, -2) - X(-1, -2)))
                + 8 * (-(X(2, 1) - X(-2, 1)) + 8 * (X(1, 1) - X(-1, 1)))
                - 8 * (-(X(2, -1) - X(-2, -1)) + 8 * (X(1, -1) - X(-1, -1))))
    return B


# ---------------------------------------------------------------- cDet.m / c4Inv.m
def cdet(M):
    h = len(M)
    if h == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    d = 0
    for i in range(h):
        sub = [row[:i] + row[i + 1:] for row in M[1:]]
        d = d + (1 if i % 2 == 0 else -1) * M[0][i] * cdet(sub)
    return d


def c4inv(g):
    det = cdet(g)
    inv = [[None] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            minor = [[g[r][col] for col in range(4) if col != i] for r in range(4) if r != j]
            inv[i][j] = 1 / det * ((-1) ** (i + j)) * cdet(minor)
    return inv


# ---------------------------------------------------------------- ricciT.m
MIRROR = [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)]


def ricci_tensor(gu, gl, delta):
    s = gl[0][0].shape
    dt = gl[0][0].dtype
    d1, d2 = {}, {}
    for i in range(4):
        for j in range(i, 4):
            for k in range(4):
                a = fd1(gl[i][j], k, delta)
                if k == 0:
                    a = 1 / c * a
                d1[(i, j, k)] = a
                for n in range(k, 4):
                    b = fd2(gl[i][j], k, n, delta)
                    if (n == 0 and k != 0) or (n != 0 and k == 0):
                        b = 1 / c * b
                    elif n == 0 and k == 0:
                        b = 1 / c ** 2 * b
                    d2[(i, j, k, n)] = b
                    if k != n:
                        d2[(i, j, n, k)] = b
    for k in range(4):
        for (i, j) in MIRROR:
            d1[(i, j, k)] = d1[(j, i, k)]
            for n in range(4):
                d2[(i, j, k, n)] = d2[(j, i, k, n)]

    R = [[None] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(i, 4):
            Rt = np.zeros(s, dtype=dt)
            for a in range(4):
                for b in range(4):
                    R2 = np.zeros(s, dtype=dt)
                    R2 = R2 - (d2[(i, j, a, b)] + d2[(a, b, i, j)] - d2[(i, b, j, a)] - d2[(j, b, i, a)])
                    for r in range(4):
                        R3 = np.zeros(s, dtype=dt)
                        R4 = np.zeros(s, dtype=dt)
                        R5 = np.zeros(s, dtype=dt)
                        for d in range(4):
                            R3 = R3 + d1[(b, d, j)] * gu[r][d]
                            R4 = R4 + (d1[(j, d, b)] - d1[(j, b, d)]) * gu[r][d]
                            R5 = R5 - (d1[(b, d, a)] + d1[(b, d, a)] - d1[(a, b, d)]) * gu[r][d]
                        R2 = R2 + R4 * d1[(i, r, a)] + 1 / 2 * (
                            R3 * d1[(a, r, i)] + R5 * (d1[(j, r, i)] + d1[(i, r, j)] - d1[(j, i, r)]))
                    Rt = Rt + gu[a][b] * R2
            R[i][j] = 1 / 2 * Rt
    for (i, j) in MIRROR:
        R[i][j] = R[j][i]
    return R


# ---------------------------------------------------------------- ricciS.m / einT.m / einE.m / met2den.m
def ricci_scalar(R, gu):
    Rs = 0
    for mu in range(4):
        for nu in range(4):
            Rs = Rs + gu[mu][nu] * R[mu][nu]
    return Rs


def einstein_tensor(R, Rs, gl):
    return [[R[m][n] - 0.5 * gl[m][n] * Rs for n in range(4)] for m in range(4)]


def energy_tensor(E, gu):
    """Contravariant T^{mu nu} in J/m^3.  In float64 the unit factor is applied first,
    exactly as einE.m does.  In float32 that factor (4.8e42) overflows float32's maximum
    of 3.4e38, so it is applied last, in float64, purely so the comparison can be made."""
    f32 = E[0][0].dtype == np.float32
    Ed = E if f32 else [[KAPPA * E[m][n] for n in range(4)] for m in range(4)]
    T = [[None] * 4 for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            acc = 0
            for al in range(4):
                for be in range(4):
                    acc = acc + Ed[al][be] * gu[al][mu] * gu[be][nu]
            T[mu][nu] = acc.astype(np.float64) * KAPPA if f32 else acc
    return T


def met2den(gl, delta):
    gu = c4inv(gl)
    R = ricci_tensor(gu, gl, delta)
    Rs = ricci_scalar(R, gu)
    E = einstein_tensor(R, Rs, gl)
    return energy_tensor(E, gu)


# ---------------------------------------------------------------- metrics
def zeros_metric(shape, dtype):
    return [[np.zeros(shape, dtype) for _ in range(4)] for _ in range(4)]


def minkowski_metric(n, dtype):
    g = zeros_metric((1, n, n, n), dtype)
    g[0][0][:] = -1
    for i in (1, 2, 3):
        g[i][i][:] = 1
    return g, [1.0, 1.0, 1.0, 1.0]


def alcubierre_metric(n, L, v, R, sigma, dtype):
    """metricGet_Alcubierre.m on one time slice, bubble centred on the grid; plus the exact
    Eulerian energy density from Alcubierre 1994, T^00 = -(1/8pi) v^2 rho^2/(4 r^2) f'(r)^2."""
    x = np.linspace(-L, L, n)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    f = (np.tanh(sigma * (R + r)) + np.tanh(sigma * (R - r))) / (2 * np.tanh(R * sigma))   # shapeFunction_Alcubierre.m
    beta_x = -v * f                                                                       # covariant shift, gamma = identity
    g = zeros_metric((1, n, n, n), dtype)
    g[0][0] = (-1 + beta_x * beta_x)[None].astype(dtype)   # threePlusOneBuilder.m: -alpha^2 + beta_k beta^k
    g[0][1] = beta_x[None].astype(dtype)
    g[1][0] = g[0][1]
    for i in (1, 2, 3):
        g[i][i][:] = 1
    dx = x[1] - x[0]

    def sech2(u):
        return 1 / np.cosh(u) ** 2

    fprime = sigma * (sech2(sigma * (R + r)) - sech2(sigma * (R - r))) / (2 * np.tanh(R * sigma))
    with np.errstate(invalid="ignore", divide="ignore"):
        T00_exact = -KAPPA * (v ** 2 * (Y ** 2 + Z ** 2) / (4 * r ** 2)) * fprime ** 2
    T00_exact = np.where(r == 0, 0.0, T00_exact)[None]
    return g, [1.0, dx, dx, dx], T00_exact, dx


def schwarzschild_metric(n, dx, centre, Mgeo, dtype):
    """Schwarzschild in isotropic Cartesian coordinates: exact vacuum, T = 0 everywhere.
    Mgeo = G M / c^2 in metres.  Keep the box away from the origin."""
    off = (np.arange(n) - (n - 1) / 2) * dx
    X, Y, Z = np.meshgrid(off + centre[0], off + centre[1], off + centre[2], indexing="ij")
    rho = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    A = 1 + Mgeo / (2 * rho)
    Bf = 1 - Mgeo / (2 * rho)
    g = zeros_metric((1, n, n, n), dtype)
    g[0][0] = (-(Bf / A) ** 2)[None].astype(dtype)
    psi4 = (A ** 4)[None].astype(dtype)
    for i in (1, 2, 3):
        g[i][i] = psi4.copy()
    return g, [1.0, dx, dx, dx]


def interior(a):
    """Drop 2 grid points at every spatial edge, as the WarpFactory paper recommends."""
    return a[:, 2:-2, 2:-2, 2:-2]


# ---------------------------------------------------------------- runs
def run():
    out = {}
    print("=" * 78)
    print("Case 0: Minkowski, 11^3, float64 -> max |T^{mu nu}| over all 16 components")
    g, delta = minkowski_metric(11, np.float64)
    T = met2den(g, delta)
    m = max(np.abs(T[a][b]).max() for a in range(4) for b in range(4))
    print(f"   max |T| = {m!r}  (must be exactly 0.0)")

    print("=" * 78)
    print("Case A: Alcubierre, v = 0.1 c, R = 5 m, sigma = 0.8 /m, box +-10 m, one time slice")
    print("   T^00 from the ported solver vs Alcubierre's closed-form energy density")
    print(f"   {'dx [m]':>7} {'points':>8} {'dtype':>8} {'max err / peak':>15} {'rms err / peak':>15} {'time [s]':>9}")
    out["alc"] = []
    for n, dtype in [(21, np.float64), (41, np.float64), (81, np.float64), (41, np.float32)]:
        g, delta, T00_exact, dx = alcubierre_metric(n, 10.0, 0.1, 5.0, 0.8, dtype)
        t0 = time.time()
        T = met2den(g, delta)
        el = time.time() - t0
        num = interior(T[0][0]).astype(np.float64)
        ex = interior(T00_exact)
        peak = np.abs(ex).max()
        err = num - ex
        mx = np.abs(err).max() / peak
        rms = np.sqrt(np.mean(err ** 2)) / peak
        print(f"   {dx:7.3f} {n**3:8d} {np.dtype(dtype).name:>8} {mx:15.3e} {rms:15.3e} {el:9.1f}")
        out["alc"].append((dx, n, np.dtype(dtype).name, mx, rms))
        if n == 81:
            out["alc_slice"] = (num[0, :, :, (n - 4) // 2], ex[0, :, :, (n - 4) // 2], dx)
    print(f"   peak |T^00| of the exact solution: {peak:.3e} J/m^3")

    print("=" * 78)
    print("Case B: Schwarzschild vacuum, 21^3 box centred 30 m from a mass with GM/c^2 = 1 m")
    print("   exact T = 0, so max |T| / (kappa * 2M/r^3) is pure numerical error")
    ref = KAPPA * 2 * 1.0 / 30.0 ** 3
    print(f"   reference curvature scale kappa*2M/r^3 = {ref:.3e} J/m^3")
    print(f"   {'dx [m]':>7} {'float64':>12} {'float32':>12}")
    out["sch"] = []
    for dx in [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]:
        row = [dx]
        for dtype in (np.float64, np.float32):
            g, delta = schwarzschild_metric(21, dx, (30.0, 0.0, 0.0), 1.0, dtype)
            T = met2den(g, delta)
            m = max(np.abs(interior(T[a][b])).max() for a in range(4) for b in range(4))
            row.append(m / ref)
        print(f"   {row[0]:7.3f} {row[1]:12.3e} {row[2]:12.3e}")
        out["sch"].append(row)
    return out


def plot(out, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    num, ex, dx = out["alc_slice"]
    vmax = np.abs(ex).max()
    im0 = axes[0].imshow(num.T, origin="lower", cmap="RdBu_r", vmin=-vmax, vmax=vmax,
                         extent=[-8, 8, -8, 8])
    axes[0].set_title(f"Alcubierre T$^{{00}}$, ported solver, dx = {dx:.2f} m")
    axes[0].set_xlabel("x [m]")
    axes[0].set_ylabel("y [m]")
    fig.colorbar(im0, ax=axes[0], label="J/m$^3$")
    im1 = axes[1].imshow((num - ex).T, origin="lower", cmap="PuOr",
                         vmin=-np.abs(num - ex).max(), vmax=np.abs(num - ex).max(), extent=[-8, 8, -8, 8])
    axes[1].set_title("solver minus exact (Alcubierre 1994, closed form)")
    axes[1].set_xlabel("x [m]")
    fig.colorbar(im1, ax=axes[1], label="J/m$^3$")

    sch = np.array(out["sch"])
    axes[2].loglog(sch[:, 0], sch[:, 1], "o-", label="float64 (MATLAB double / NumPy default)")
    axes[2].loglog(sch[:, 0], sch[:, 2], "s-", label="float32 (single)")
    xs = np.array([0.001, 1.0])
    axes[2].loglog(xs, 3.9e-5 * (xs / 1.0) ** 4, "k:", lw=1, label="slope dx$^4$ (truncation)")
    axes[2].loglog(xs, 8.3e-11 * (xs / 1.0) ** -2, "k--", lw=1, label="slope dx$^{-2}$ (round-off)")
    axes[2].set_xlabel("grid spacing dx [m]")
    axes[2].set_ylabel("max |T| / curvature scale   (exact answer is 0)")
    axes[2].set_title("Schwarzschild vacuum: error vs grid spacing")
    axes[2].legend(fontsize=8)
    axes[2].grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    print(f"plot written: {path}")


if __name__ == "__main__":
    out = run()
    if len(sys.argv) > 1:
        plot(out, sys.argv[1])
