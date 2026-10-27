"""
exact_conditions.py -- warpax's exact (S-lemma) energy conditions on the exported slices (PLAN Part 2).

Same object, same points as Part 1: the central-plane slices that matlab/shift_matrix.m exported from
WarpFactory at the authors' configuration, read with SciPy. Part 1 read WarpFactory's own sampled
maps (100 directions x 10 speeds), a dense null check (4000 directions) and the Hawking-Ellis type
off these slices. This script adds the second toolkit: warpax 1.5.1 (An T. Le), whose
energy_conditions.slemma module decides each of the four conditions over EVERY observer at a point
from one 4x4 linear matrix inequality (Le 2026, arXiv 2602.18023, Theorem 1): no observer sample,
no rapidity cap, no type assumption. Its margins are signed, positive = satisfied; for the null
condition twice the margin is the exact minimum of T(k,k) over null k = n + s, |s| = 1
(warpax.energy_conditions.null_deficit), the quantity Part 1's dense check sampled.

Inputs per point. The slice holds WarpFactory's stress-energy in its orthonormal Eulerian frame,
contravariant (Analyzer/doFrameTransfer.m). warpax wants covariant tetrad components, so
That = eta T eta with eta = diag(-1, 1, 1, 1); That[0,0] = rho, That[0,i] = -j_i, That[i,j] = S_ij,
exactly Le's eq. (21)-(22). Route A feeds That with the Minkowski metric to certify_point_lmi. Route B
rebuilds the coordinate components T_ab = M^-T That M^-1 from WarpFactory's own transformation matrix
(Analyzer/utils/getEulerianTransformationMatrix.m, ported below and checked against M^T g M = eta)
and feeds those with the coordinate metric, so warpax builds its own tetrad; the two must agree to
roundoff, and the script prints by how much they do.

Sampled maps for the comparison (claim C4). WarpFactory's Null and Weak maps lower indices with the
coordinate metric (work/matrix/verify_null_bug.py, RESULTS.md section 4); the consistent versions are
replicated here with the Minkowski metric and the same observer set (getEvenPointsOnSphere spiral,
generateUniformField normalisation). The Strong and Dominant maps are taken as exported. The Dominant
map tests only the flux half of the condition (J = -T.k causal, null k); warpax's DEC is the smaller
of the WEC margin and the flux margin, so a "completed" sampled DEC flag (corrected Weak or exported
Dominant) is reported next to the Dominant-only one.

Thresholds. A point violates a condition when its margin is below -TAU rho0, TAU = 1e-4 as in Part 1
(analyse_matrix.NOISE), rho0 the peak Eulerian energy density of the static shell at that compactness.
WarpFactory's finite differences put noise of about 1e-6 rho0 on every slice; warpax's own decision
floor (noise_floor, 1e-12 of the tensor scale) is far below it, so counts at that floor are also
reported and read as the stencil noise they are. WarpFactory's null map is T(k,k) for k = (1, n)/sqrt 2,
half the normalised contraction, and is doubled before any comparison; its timelike maps mix
normalisations (Euclidean unit 4-vectors at ten speeds) and are compared by sign only.

Outputs, in the run folder: exact_cases_f<a>.csv per compactness index (one row per shift), then with
--summarise: exact_cases.csv, exact_brackets.csv (first failing shift per condition, exact, next to
Part 1's analysis_brackets.csv), exact_miss.csv, and the figure.

Usage:
  python exact_conditions.py <run_dir> --factors 1,2        # compute (one process per factor is fine)
  python exact_conditions.py <run_dir> --summarise [--png out.png]
"""
import argparse
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
import numpy as np
from scipy.io import loadmat

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyse_matrix import ETA, NOISE as TAU, N_DIRS, bracket, eulerian_tensor, fibonacci_sphere, load_summary, nec_dense, type_and_swarm

EDGE = 2            # edge cells dropped per side, as everywhere in work/matrix
ACTIVE = 1e-6       # |T| above this fraction of rho0 counts as a matter point (Part 1's mask)
CHUNK = 8192        # points per JIT call (padded, so the function compiles once)
ROUTE_B_STRIDE = 29 # route B runs on every 29th active point plus the worst point of each condition
G_SI, C_SI, R2 = 6.67430e-11, 2.99792458e8, 20.0
CONDS = ("nec", "wec", "sec", "dec")


# ---------------------------------------------------------------- slices and WarpFactory replicas
def coordinate_metric(s, n):
    """Covariant 4-metric on the central plane; g02 = g03 = g13 = g23 = 0 there by symmetry."""
    sl = slice(EDGE, -EDGE)
    g = np.zeros((n, 4, 4))
    for (i, j, key) in [(0, 0, "g00"), (0, 1, "g01"), (1, 1, "g11"), (1, 2, "g12"), (2, 2, "g22"), (3, 3, "g33")]:
        v = np.asarray(s[key], dtype=float)[sl, sl].ravel()
        g[:, i, j] = v
        g[:, j, i] = v
    return g


def wf_eulerian_matrix(g):
    """Port of getEulerianTransformationMatrix.m: lower-triangular M with M^T g M = eta, columns = tetrad legs."""
    G = lambda i, j: g[:, i - 1, j - 1]
    f0 = G(4, 4)
    f1 = -G(3, 4) ** 2 + G(3, 3) * f0
    f2 = 2 * G(2, 3) * G(2, 4) * G(3, 4) - G(4, 4) * G(2, 3) ** 2 - G(3, 3) * G(2, 4) ** 2 + G(2, 2) * f1
    f3 = (-2 * G(4, 4) * G(1, 2) * G(1, 3) * G(2, 3) + 2 * G(1, 3) * G(1, 4) * G(2, 3) * G(2, 4)
          + 2 * G(1, 2) * G(1, 3) * G(2, 4) * G(3, 4) + 2 * G(1, 2) * G(1, 4) * G(2, 3) * G(3, 4)
          - G(1, 2) ** 2 * G(3, 4) ** 2 - G(1, 3) ** 2 * G(2, 4) ** 2 - G(1, 4) ** 2 * G(2, 3) ** 2
          + G(3, 3) * (-2 * G(1, 2) * G(1, 4) * G(2, 4) + G(4, 4) * G(1, 2) ** 2)
          + G(2, 2) * (-2 * G(1, 3) * G(1, 4) * G(3, 4) + G(4, 4) * G(1, 3) ** 2 + G(3, 3) * G(1, 4) ** 2)
          - G(1, 1) * f2)
    M = np.zeros_like(g)
    M[:, 0, 0] = np.sqrt(f2 / f3)
    M[:, 1, 0] = (G(1, 2) * G(3, 4) ** 2 + G(1, 3) * G(2, 3) * G(4, 4) - G(1, 3) * G(2, 4) * G(3, 4) - G(1, 4) * G(2, 3) * G(3, 4) + G(1, 4) * G(2, 4) * G(3, 3) - G(1, 2) * G(3, 3) * G(4, 4)) / np.sqrt(f2 * f3)
    M[:, 2, 0] = (G(1, 3) * G(2, 4) ** 2 - G(1, 4) * G(2, 3) * G(2, 4) + G(1, 2) * G(2, 3) * G(4, 4) - G(1, 2) * G(2, 4) * G(3, 4) - G(1, 3) * G(2, 2) * G(4, 4) + G(1, 4) * G(2, 2) * G(3, 4)) / np.sqrt(f2 * f3)
    M[:, 3, 0] = (G(1, 4) * G(2, 3) ** 2 - G(1, 3) * G(2, 3) * G(2, 4) - G(1, 2) * G(2, 3) * G(3, 4) + G(1, 2) * G(2, 4) * G(3, 3) + G(1, 3) * G(2, 2) * G(3, 4) - G(1, 4) * G(2, 2) * G(3, 3)) / np.sqrt(f2 * f3)
    M[:, 1, 1] = np.sqrt(f1 / f2)
    M[:, 2, 1] = (G(2, 4) * G(3, 4) - G(2, 3) * G(4, 4)) / np.sqrt(f1 * f2)
    M[:, 3, 1] = (G(2, 3) * G(3, 4) - G(2, 4) * G(3, 3)) / np.sqrt(f1 * f2)
    M[:, 2, 2] = np.sqrt(f0 / f1)
    M[:, 3, 2] = -G(3, 4) / np.sqrt(f0 * f1)
    M[:, 3, 3] = np.sqrt(1 / f0)
    return M


def wf_observers(n_ang=100, n_time=10):
    """WarpFactory's observer sets: the golden-ratio spiral of getEvenPointsOnSphere, normalised as
    generateUniformField does (Euclidean unit 4-vectors). Null: k = (1, n)/sqrt 2. Timelike: (1, r n)
    with r = 1 - b, b in linspace(0, 1, n_time), which runs from null (b = 0) to the Eulerian observer."""
    i = np.arange(n_ang)
    gr = (1 + 5 ** 0.5) / 2
    theta = 2 * np.pi * i / gr
    phi = np.arccos(1 - 2 * (i + 0.5) / n_ang)
    nvec = np.stack([np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)], axis=1)
    null = np.concatenate([np.ones((n_ang, 1)), nvec], axis=1) / np.sqrt(2)
    rows = []
    for b in np.linspace(0, 1, n_time):
        v = np.concatenate([np.ones((n_ang, 1)), (1 - b) * nvec], axis=1)
        rows.append(v / np.sqrt(1 + (1 - b) ** 2))
    return null, np.concatenate(rows, axis=0)


def sampled_min(T_up, metric, vecs, chunk=4000):
    """WarpFactory's Null/Weak evaluation: lower both indices with `metric`, contract with each vector, take the minimum."""
    out = np.empty(T_up.shape[0])
    for s in range(0, T_up.shape[0], chunk):
        t = T_up[s:s + chunk]
        m = metric[s:s + chunk]
        Td = np.einsum("nac,ncd,nbd->nab", m, t, m)
        out[s:s + chunk] = np.einsum("nab,ka,kb->nk", Td, vecs, vecs).min(axis=1)
    return out


# ---------------------------------------------------------------- warpax
def warpax_functions():
    import jax
    jax.config.update("jax_enable_x64", True)
    import jax.numpy as jnp
    from warpax.energy_conditions import certify_point_lmi, check_all, classify_hawking_ellis, noise_floor
    eta = jnp.asarray(ETA)
    cert_eta = jax.jit(jax.vmap(lambda t: certify_point_lmi(t, eta)))
    cert_g = jax.jit(jax.vmap(certify_point_lmi))
    floor_eta = jax.jit(jax.vmap(lambda t: noise_floor(t, eta)))
    classify = jax.jit(jax.vmap(lambda t_up: classify_hawking_ellis(t_up @ eta, eta)))
    algebraic = jax.jit(jax.vmap(check_all))
    return jax, jnp, cert_eta, cert_g, floor_eta, classify, algebraic


def in_chunks(fn, jnp, *arrays):
    """Apply a vmapped, jitted function in fixed-size padded chunks; returns a dict of NumPy arrays."""
    n = arrays[0].shape[0]
    out = {}
    for s in range(0, n, CHUNK):
        parts = []
        for a in arrays:
            p = a[s:s + CHUNK]
            if p.shape[0] < CHUNK:
                pad = np.repeat(p[-1:], CHUNK - p.shape[0], axis=0)
                p = np.concatenate([p, pad], axis=0)
            parts.append(jnp.asarray(p))
        res = fn(*parts)
        if not isinstance(res, dict):
            res = res._asdict() if hasattr(res, "_asdict") else dict(enumerate(res))
        m = min(CHUNK, n - s)
        for k, v in res.items():
            out.setdefault(k, []).append(np.asarray(v)[:m])
    return {k: np.concatenate(v, axis=0) for k, v in out.items()}


# ---------------------------------------------------------------- one case
def analyse_case(path, rho0, part1_row, fx, dirs, null_vecs, time_vecs):
    jax, jnp, cert_eta, cert_g, floor_eta, classify, algebraic = fx
    s = loadmat(path)
    beta = float(np.squeeze(s["beta"]))
    M_kg = float(np.squeeze(s["M_kg"]))
    comp = 2 * G_SI * M_kg / (R2 * C_SI ** 2)
    T = eulerian_tensor(s, EDGE)
    n = T.shape[0]
    g = coordinate_metric(s, n)
    sl = slice(EDGE, -EDGE)
    X, Y = np.meshgrid(np.asarray(s["x"]).ravel()[sl], np.asarray(s["y"]).ravel()[sl], indexing="ij")
    r = np.sqrt(X ** 2 + Y ** 2).ravel()
    act = np.abs(T).reshape(n, -1).max(axis=1) > ACTIVE * rho0
    Ta, ga, ra = T[act], g[act], r[act]
    That = np.einsum("ij,njk,kl->nil", ETA, Ta, ETA)
    eta_b = np.broadcast_to(ETA, Ta.shape)

    # route A: exact margins on the frame tensor
    t0 = time.time()
    ex = in_chunks(cert_eta, jnp, That)
    floor = in_chunks(lambda t: {"f": floor_eta(t)}, jnp, That)["f"]
    t_exact = time.time() - t0
    nulldef = 2.0 * ex["nec"]

    # route B: coordinate components through WarpFactory's own tetrad, warpax builds its own
    M = wf_eulerian_matrix(ga)
    tetrad_dev = np.abs(np.einsum("nia,nij,njb->nab", M, ga, M) - ETA).max()
    Minv = np.linalg.inv(M)
    Tab = np.einsum("nia,nij,njb->nab", Minv, That, Minv)
    idx = np.unique(np.concatenate([np.arange(0, Ta.shape[0], ROUTE_B_STRIDE), [int(np.argmin(ex[c])) for c in CONDS]]))
    exB = in_chunks(cert_g, jnp, Tab[idx], ga[idx])
    # NEC, WEC and SEC margins are invariant under the spatial rotation between the two tetrads; the DEC
    # margin is not, because warpax divides its flux margin by max |That_IJ| (slemma._flux_margin_linear,
    # "not an invariant severity"), so for DEC only the sign is compared.
    routeB = max(np.abs(exB[c] - ex[c][idx]).max() for c in ("nec", "wec", "sec")) / rho0
    routeB_dec = np.abs(exB["dec"] - ex["dec"][idx]).max() / rho0
    routeB_dec_sign = float(np.mean(np.sign(exB["dec"]) == np.sign(ex["dec"][idx])))

    # Hawking-Ellis type (warpax) against Part 1's NumPy reading; algebraic Type I margins
    cl = in_chunks(classify, jnp, Ta)
    he = cl["he_type"]
    typeI = he == 1
    typeI_p1 = type_and_swarm(Ta, rho0)[0]
    alg = in_chunks(lambda rho, p: dict(zip(CONDS, algebraic(rho, p))), jnp, cl["rho"], cl["pressures"])

    # WarpFactory's maps as exported, the consistent Null and Weak replicas, the dense null check
    maps = {k: np.asarray(s[k])[sl, sl].ravel()[act] for k in ("null", "weak", "strong", "dominant")}
    maps["null"] = 2.0 * maps["null"]
    null_fix = 2.0 * sampled_min(Ta, eta_b, null_vecs)
    weak_fix = sampled_min(Ta, eta_b, time_vecs)
    dense = nec_dense(Ta, dirs)

    viol = {"nec": nulldef < -TAU * rho0, "wec": ex["wec"] < -TAU * rho0, "sec": ex["sec"] < -TAU * rho0, "dec": ex["dec"] < -TAU * rho0}
    flag = {"null_raw": maps["null"] < -TAU * rho0, "weak_raw": maps["weak"] < -TAU * rho0,
            "strong": maps["strong"] < -TAU * rho0, "dom": maps["dominant"] < -TAU * rho0,
            "null_fix": null_fix < -TAU * rho0, "weak_fix": weak_fix < -TAU * rho0, "dense": dense < -TAU * rho0}
    flag["dec_full"] = flag["weak_fix"] | flag["dom"]

    def miss(v, f):
        return np.nan if v.sum() == 0 else float((v & ~f).sum() / v.sum())

    def false_alarm(v, f):
        return np.nan if f.sum() == 0 else float((f & ~v).sum() / f.sum())

    rec = dict(factor=float(np.squeeze(s["factor"])), compactness=comp, beta=beta, beta_over_C=beta / comp, rho0=rho0,
               n_active=int(act.sum()), t_exact_s=t_exact, tetrad_dev=tetrad_dev, routeB_maxdiff=routeB, routeB_dec_maxdiff=routeB_dec,
               routeB_dec_sign=routeB_dec_sign, routeB_n=len(idx),
               ex_nec=ex["nec"].min() / rho0, ex_nulldef=nulldef.min() / rho0, ex_wec=ex["wec"].min() / rho0,
               ex_sec=ex["sec"].min() / rho0, ex_dec=ex["dec"].min() / rho0,
               r_worst_dec=float(ra[np.argmin(ex["dec"])]),
               n_ex_nec=int(viol["nec"].sum()), n_ex_wec=int(viol["wec"].sum()), n_ex_sec=int(viol["sec"].sum()), n_ex_dec=int(viol["dec"].sum()),
               n_floor_nec=int((ex["nec"] < -floor).sum()), n_floor_wec=int((ex["wec"] < -floor).sum()),
               n_floor_sec=int((ex["sec"] < -floor).sum()), n_floor_dec=int((ex["dec"] < -floor).sum()),
               n_1e6_dec=int((ex["dec"] < -1e-6 * rho0).sum()),
               typeI_frac=float(typeI.mean()), n_typeIV=int((he == 4).sum()), n_type_other=int(((he == 2) | (he == 3)).sum()),
               typeI_agree=float((typeI == typeI_p1).mean()),
               alg_nec=np.nanmin(alg["nec"]) / rho0 if typeI.any() else np.nan, alg_wec=np.nanmin(alg["wec"]) / rho0 if typeI.any() else np.nan,
               alg_sec=np.nanmin(alg["sec"]) / rho0 if typeI.any() else np.nan, alg_dec=np.nanmin(alg["dec"]) / rho0 if typeI.any() else np.nan,
               n_viol_typeI=int((viol["dec"] & typeI).sum()),
               s_null_raw=maps["null"].min() / rho0, s_weak_raw=maps["weak"].min() / rho0, s_strong=maps["strong"].min() / rho0, s_dom=maps["dominant"].min() / rho0,
               s_null_fix=null_fix.min() / rho0, s_weak_fix=weak_fix.min() / rho0, dense=dense.min() / rho0,
               n_s_null_raw=int(flag["null_raw"].sum()), n_s_weak_raw=int(flag["weak_raw"].sum()), n_s_strong=int(flag["strong"].sum()),
               n_s_dom=int(flag["dom"].sum()), n_s_null_fix=int(flag["null_fix"].sum()), n_s_weak_fix=int(flag["weak_fix"].sum()), n_dense=int(flag["dense"].sum()),
               miss_nec_fix=miss(viol["nec"], flag["null_fix"]), miss_nec_dense=miss(viol["nec"], flag["dense"]),
               miss_wec_fix=miss(viol["wec"], flag["weak_fix"]), miss_sec=miss(viol["sec"], flag["strong"]),
               miss_dec_dom=miss(viol["dec"], flag["dom"]), miss_dec_full=miss(viol["dec"], flag["dec_full"]),
               miss_nec_raw=miss(viol["nec"], flag["null_raw"]), miss_wec_raw=miss(viol["wec"], flag["weak_raw"]),
               false_null_raw=false_alarm(viol["nec"], flag["null_raw"]), false_weak_raw=false_alarm(viol["wec"], flag["weak_raw"]),
               p1_s_dom=part1_row["minDominant"] / rho0 if part1_row else np.nan)
    return rec


def write_csv(path, rows):
    keys = list(rows[0].keys())
    np.savetxt(path, np.array([[float(x[k]) for k in keys] for x in rows]), delimiter=",", header=",".join(keys), comments="", fmt="%.10g")


# ---------------------------------------------------------------- summary
def summarise(run, png):
    rows = []
    for f in sorted(run.glob("exact_cases_f*.csv")):
        rows += load_summary(f)
    if not rows:
        sys.exit("no exact_cases_f*.csv in the run folder; compute first")
    rows.sort(key=lambda x: (-x["compactness"], x["beta"]))
    write_csv(run / "exact_cases.csv", rows)
    p1 = {round(x["compactness"], 6): x for x in load_summary(run / "analysis_brackets.csv")} if (run / "analysis_brackets.csv").exists() else {}

    brackets = []
    for comp in sorted({x["compactness"] for x in rows}, reverse=True):
        sub = sorted([x for x in rows if x["compactness"] == comp], key=lambda x: x["beta"])
        bl = [x["beta"] for x in sub]
        print(f"=== compactness {comp:.4f} ===")
        print(f"{'beta':>7s} {'beta/C':>7s} | {'exact margin / rho0 (warpax LMI)':^47s} | {'null deficit':>12s} {'dense4000':>10s} {'sampl100':>10s} | {'TypeI%':>7s} | {'miss: DEC/dom':>13s} {'NEC/100':>8s} {'routeB':>8s}")
        print(f"{'':>7s} {'':>7s} | {'nec':>11s} {'wec':>11s} {'sec':>11s} {'dec':>11s} | {'':>12s} {'':>10s} {'':>10s} | {'':>7s} | {'':>13s} {'':>8s} {'':>8s}")
        for x in sub:
            print(f"{x['beta']:7.4f} {x['beta_over_C']:7.3f} | {x['ex_nec']:+11.3e} {x['ex_wec']:+11.3e} {x['ex_sec']:+11.3e} {x['ex_dec']:+11.3e} | "
                  f"{x['ex_nulldef']:+12.3e} {x['dense']:+10.3e} {x['s_null_fix']:+10.3e} | {100 * x['typeI_frac']:7.2f} | "
                  f"{x['miss_dec_dom']:13.3f} {x['miss_nec_fix']:8.3f} {x['routeB_maxdiff']:8.1e}")
        br = {c: bracket(bl, [x[f"ex_{c}"] if c != "nec" else x["ex_nulldef"] for x in sub]) for c in CONDS}
        sens = {}
        for tau in (1e-5, 1e-3):
            sens[tau] = {c: _bracket_tau(bl, [x[f"ex_{c}"] if c != "nec" else x["ex_nulldef"] for x in sub], tau) for c in CONDS}
        p1row = p1.get(round(comp, 6))
        line = "; ".join(f"{c} pass <= {_f(br[c][0])}, fail >= {_f(br[c][1])}" for c in CONDS)
        print(f"  exact first failing shift (tau = {TAU:g}): {line}")
        print(f"  in units of C: " + "; ".join(f"{c} {_f(br[c][0], comp)} / {_f(br[c][1], comp)}" for c in CONDS))
        print(f"  sensitivity: tau = 1e-5 -> dec {_f(sens[1e-5]['dec'][0], comp)} / {_f(sens[1e-5]['dec'][1], comp)}; tau = 1e-3 -> dec {_f(sens[1e-3]['dec'][0], comp)} / {_f(sens[1e-3]['dec'][1], comp)}")
        if p1row:
            print(f"  Part 1 (sampled dominant) {_f(p1row['s_dom_pass'], comp)} / {_f(p1row['s_dom_fail'], comp)}; (null, 4000 directions) {_f(p1row['nec_dense_pass'], comp)} / {_f(p1row['nec_dense_fail'], comp)}")
        brackets.append(dict(compactness=comp,
                             **{f"ex_{c}_pass": (np.nan if br[c][0] is None else br[c][0]) for c in CONDS},
                             **{f"ex_{c}_fail": (np.nan if br[c][1] is None else br[c][1]) for c in CONDS},
                             ex_dec_pass_tau1e5=np.nan if sens[1e-5]["dec"][0] is None else sens[1e-5]["dec"][0],
                             ex_dec_fail_tau1e5=np.nan if sens[1e-5]["dec"][1] is None else sens[1e-5]["dec"][1],
                             ex_dec_pass_tau1e3=np.nan if sens[1e-3]["dec"][0] is None else sens[1e-3]["dec"][0],
                             ex_dec_fail_tau1e3=np.nan if sens[1e-3]["dec"][1] is None else sens[1e-3]["dec"][1],
                             p1_s_dom_pass=p1row["s_dom_pass"] if p1row else np.nan, p1_s_dom_fail=p1row["s_dom_fail"] if p1row else np.nan,
                             p1_nec_dense_pass=p1row["nec_dense_pass"] if p1row else np.nan, p1_nec_dense_fail=p1row["nec_dense_fail"] if p1row else np.nan))
        print()
    write_csv(run / "exact_brackets.csv", brackets)

    miss_keys = ["compactness", "beta", "beta_over_C", "n_ex_nec", "n_ex_wec", "n_ex_sec", "n_ex_dec", "n_s_null_fix", "n_s_weak_fix", "n_s_strong", "n_s_dom", "n_dense",
                 "miss_nec_fix", "miss_nec_dense", "miss_wec_fix", "miss_sec", "miss_dec_dom", "miss_dec_full", "miss_nec_raw", "miss_wec_raw", "false_null_raw", "false_weak_raw",
                 "n_floor_dec", "n_1e6_dec", "n_viol_typeI"]
    write_csv(run / "exact_miss.csv", [{k: x[k] for k in miss_keys} for x in rows])
    viol_rows = [x for x in rows if x["n_ex_dec"] > 0]
    if viol_rows:
        tot = sum(x["n_ex_dec"] for x in viol_rows)
        missed = sum(x["n_ex_dec"] * x["miss_dec_dom"] for x in viol_rows)
        tot_n = sum(x["n_ex_nec"] for x in viol_rows)
        missed_n = sum(x["n_ex_nec"] * x["miss_nec_fix"] for x in viol_rows if x["n_ex_nec"] > 0)
        print(f"pooled over the {len(viol_rows)} violating cases: exact DEC violations {int(tot)}, missed by the sampled Dominant map {int(round(missed))} ({100 * missed / tot:.2f} %);"
              f" exact NEC violations {int(tot_n)}, missed by 100 consistent null directions {int(round(missed_n))} ({100 * missed_n / tot_n:.2f} %)")
    print(f"route B agreement, worst case over all cases: nec/wec/sec {max(x['routeB_maxdiff'] for x in rows):.1e} rho0; dec sign agreement, worst {min(x['routeB_dec_sign'] for x in rows):.6f}"
          f" (dec magnitude differs by up to {max(x['routeB_dec_maxdiff'] for x in rows):.1e} rho0, tetrad-dependent normalisation); tetrad identity, worst: {max(x['tetrad_dev'] for x in rows):.1e};"
          f" Type I census agreement with Part 1, worst: {min(x['typeI_agree'] for x in rows):.6f}")
    print(f"written: {run / 'exact_cases.csv'}, {run / 'exact_brackets.csv'}, {run / 'exact_miss.csv'}")
    if png:
        plot(rows, brackets, png)


def _bracket_tau(betas, margins, tau):
    b = np.asarray(betas); m = np.asarray(margins)
    ok = m >= -tau
    return (b[ok].max() if ok.any() else None, b[~ok].min() if (~ok).any() else None)


def _f(v, scale=1.0):
    return "none" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v / scale:.4f}"


def plot(rows, brackets, png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    comps = sorted({x["compactness"] for x in rows}, reverse=True)
    fig, ax = plt.subplots(1, 3, figsize=(17, 4.8))
    for i, comp in enumerate(comps):
        sub = sorted([x for x in rows if x["compactness"] == comp and x["beta"] > 0], key=lambda x: x["beta"])
        xs = [x["beta_over_C"] for x in sub]
        ax[0].plot(xs, [x["ex_dec"] for x in sub], "o-", color=f"C{i}", label=f"exact DEC (warpax), C = {comp:.3g}")
        ax[0].plot(xs, [x["p1_s_dom"] for x in sub], "x--", color=f"C{i}", label=f"sampled Dominant (WarpFactory), C = {comp:.3g}")
    ax[0].axhline(0, color="k", lw=0.8); ax[0].set_xscale("log")
    ax[0].set_xlabel("shift / compactness"); ax[0].set_ylabel("minimum over the plane / rho0\n(LMI eigenvalue vs flux norm: compare the sign, not the depth)")
    ax[0].set_title("Exact and sampled dominant condition, same points"); ax[0].legend(fontsize=6.5); ax[0].grid(alpha=0.3, which="both")
    sub = sorted([x for x in rows if x["compactness"] == comps[0] and x["beta"] > 0], key=lambda x: x["beta"])
    xs = [x["beta_over_C"] for x in sub]
    ax[1].plot(xs, [x["ex_nulldef"] for x in sub], "o-", label="exact null deficit (warpax S-lemma)")
    ax[1].plot(xs, [x["dense"] for x in sub], "s--", label="4000 null directions (Part 1)")
    ax[1].plot(xs, [x["s_null_fix"] for x in sub], "^:", label="100 null directions, Minkowski (WarpFactory's set)")
    ax[1].plot(xs, [x["s_null_raw"] for x in sub], "v:", color="0.5", label="WarpFactory's Null map as exported (coordinate metric)")
    ax[1].axhline(0, color="k", lw=0.8); ax[1].set_xscale("log")
    ax[1].set_xlabel("shift / compactness"); ax[1].set_ylabel("min T(k,k) over null k, / rho0")
    ax[1].set_title(f"Depth of the null violation, C = {comps[0]:.3g}"); ax[1].legend(fontsize=6.5); ax[1].grid(alpha=0.3, which="both")
    for i, comp in enumerate(comps):
        sub = sorted([x for x in rows if x["compactness"] == comp and x["n_ex_dec"] > 0], key=lambda x: x["beta"])
        if sub:
            ax[2].plot([x["beta_over_C"] for x in sub], [100 * x["miss_dec_dom"] for x in sub], "o-", color=f"C{i}", label=f"DEC: missed by the sampled Dominant map, C = {comp:.3g}")
            ax[2].plot([x["beta_over_C"] for x in sub], [100 * x["miss_nec_fix"] for x in sub], "x--", color=f"C{i}", label=f"NEC: missed by 100 consistent null directions, C = {comp:.3g}")
    ax[2].set_xlabel("shift / compactness"); ax[2].set_ylabel("exact violations missed, %")
    ax[2].set_title("What the sampled check misses, per case"); ax[2].legend(fontsize=6.5); ax[2].grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(png, dpi=130)
    print(f"figure written: {png}")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--factors", default="all", help="comma-separated compactness indices to compute, e.g. 1,2")
    ap.add_argument("--summarise", action="store_true")
    ap.add_argument("--png", default=None)
    args = ap.parse_args()
    run = Path(args.run)
    if args.summarise:
        summarise(run, args.png)
        return

    rows = load_summary(run / "summary.csv")
    factors = sorted({r["factor"] for r in rows}, reverse=True)
    wanted = list(range(1, len(factors) + 1)) if args.factors == "all" else [int(x) for x in args.factors.split(",")]
    fx = warpax_functions()
    dirs = fibonacci_sphere(N_DIRS)
    null_vecs, time_vecs = wf_observers()
    for a in wanted:
        f = factors[a - 1]
        sub = sorted([r for r in rows if r["factor"] == f], key=lambda r: r["beta"])
        rho0 = [r for r in sub if r["beta"] == 0.0][0]["rho0_J_m3"]
        out = []
        for b, r in enumerate(sub, start=1):
            t0 = time.time()
            rec = analyse_case(run / f"slice_f{a}_b{b}.mat", rho0, r, fx, dirs, null_vecs, time_vecs)
            out.append(rec)
            print(f"f{a}_b{b}: C {rec['compactness']:.4f} beta {rec['beta']:.4f} (beta/C {rec['beta_over_C']:.3f}): exact min/rho0 nec {rec['ex_nec']:+.3e} wec {rec['ex_wec']:+.3e} "
                  f"sec {rec['ex_sec']:+.3e} dec {rec['ex_dec']:+.3e}; null deficit {rec['ex_nulldef']:+.3e} vs dense {rec['dense']:+.3e} vs 100 dirs {rec['s_null_fix']:+.3e}; "
                  f"viol dec {rec['n_ex_dec']} (missed by dom {rec['miss_dec_dom']:.3f}); TypeI {100 * rec['typeI_frac']:.2f} %; routeB {rec['routeB_maxdiff']:.1e}; {time.time() - t0:.0f} s", flush=True)
            write_csv(run / f"exact_cases_f{a}.csv", out)


if __name__ == "__main__":
    main()
