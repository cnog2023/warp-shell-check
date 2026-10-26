"""
einstein_cluster.py -- can orbiting matter, not material strength, hold the Fuchs shell up?

Idea (Carlos, after Sagan's counter-rotating rings): support a shell by rotation while keeping zero
net angular momentum and spherical symmetry by using many rings with different axes and opposite
senses. The continuum limit is Einstein's 1939 cluster: a static, spherically symmetric swarm of
particles on circular geodesics with randomly oriented orbital planes. Each particle is in free
fall, so no material strength is needed; the swarm's stress-energy has zero radial pressure and a
tangential pressure P_t = rho v^2 / 2, where v is the local orbital speed, with v^2 = m(r)/(r - 2m(r))
in geometric units. Being made of dust streams, it satisfies every pointwise energy condition.

Two things are computed on the authors' shell (validated NumPy replica, smoothFactor 4000):
  1. Kinetic realisability of the Fuchs stress state itself. A collisionless swarm with radial and
     tangential velocity dispersions gives P_r = rho <v_r^2> and 2 P_t = rho <v_t^2>, so the Fuchs
     (rho, P_r, P_t) is realisable by a swarm iff (P_r + 2 P_t) / rho < 1, which is the trace energy
     condition, stronger than the dominant one. Report its margin and the implied rms speed.
  2. The pure Einstein-cluster shell with the same smoothed density profile: orbital speed profile,
     tangential pressure, and the r > 3 m(r) requirement (circular photon orbit).
  3. The smoothing sweep for the trace condition, as sweep_smoothing.py did for the dominant one.

Usage: python einstein_cluster.py
"""
import numpy as np
import replicate_profiles as rp
import hoop_stress as hs

G, c = rp.G, rp.c


def analyse(sf, verbose=False):
    d = rp.build(smoothFactor=sf)
    prof = {k: d[k] for k in ("r_m", "rhosmooth_kg_m3", "Psmooth_Pa", "A_g00")}
    r, rho, Pr, Pt, a = hs.identity_tangential(prof)
    rho0 = rho.max()
    shell = (r > 2) & (r < 28)
    ok = shell & (rho > 0.01 * rho0)
    # 1. kinetic realisability of the Fuchs state
    v2_rms = (Pr[ok] + 2 * Pt[ok]) / rho[ok]
    i = int(np.argmax(v2_rms))
    # 2. Einstein-cluster shell on the same density
    m = G * d["M_kg"] / c**2
    with np.errstate(divide="ignore", invalid="ignore"):
        v2 = np.where(r > 0, m / (r - 2 * m), 0.0)
    Pt_ec = 0.5 * rho * v2
    photon = np.min((r - 3 * m)[ok])          # inside the shell material, where it matters
    j = int(np.argmax(v2[ok]))
    k = int(np.argmax(Pt_ec[shell]))
    out = dict(sf=sf, trace_margin=1 - v2_rms[i], v_rms_max=np.sqrt(v2_rms[i]), r_vrms=r[ok][i],
               ec_v_max=np.sqrt(v2[ok][j]), r_ec_v=r[ok][j], ec_Pt_peak=Pt_ec[shell][k] / rho0, r_ec_Pt=r[shell][k],
               ec_max_Pt_over_rho=0.5 * v2[ok].max(), photon_margin_m=photon,
               fuchs_Pt_peak=Pt[shell].max() / rho0)
    if verbose:
        print(f"authors' configuration (smoothFactor {sf}):")
        print(f"  Fuchs stress state as a swarm: max (P_r + 2P_t)/rho = {v2_rms[i]:.3f} at r = {r[ok][i]:.2f} m,")
        print(f"     i.e. rms particle speed {np.sqrt(v2_rms[i]):.3f} c there; trace-condition margin {1 - v2_rms[i]:.3f}")
        print(f"  Einstein-cluster shell on the same density: orbital speed rises from ~0 at the inner wall to")
        print(f"     {np.sqrt(v2[ok][j]):.3f} c at r = {r[ok][j]:.2f} m; P_t peaks at {Pt_ec[shell][k] / rho0:.4f} rho0 c^2 at r = {r[shell][k]:.2f} m")
        print(f"     (Fuchs's own P_t peak: {Pt[shell].max() / rho0:.4f}); max P_t/rho = v^2/2 = {0.5 * v2[ok].max():.3f}; P_r = 0 everywhere")
        print(f"     photon-orbit margin min(r - 3m(r)) = {photon:.2f} m (must stay positive)")
        print(f"  mass unchanged: {d['M_kg'][-1]:.3e} kg")
    return out


if __name__ == "__main__":
    analyse(4000, verbose=True)
    print("\nsmoothing sweep: is the Fuchs stress state realisable by a swarm (trace condition), and the cluster's top speed")
    print(f"{'smooth':>7s} {'traceMargin':>12s} {'v_rms_max/c':>12s} {'at r':>6s} {'EC v_max/c':>11s} {'EC Pt_peak':>11s} {'Fuchs Pt_peak':>13s}")
    for sf in (500, 1000, 1500, 2000, 3000, 4000, 6000, 8000):
        o = analyse(sf)
        print(f"{sf:7d} {o['trace_margin']:12.3f} {o['v_rms_max']:12.3f} {o['r_vrms']:6.2f} {o['ec_v_max']:11.3f} {o['ec_Pt_peak']:11.4f} {o['fuchs_Pt_peak']:13.4f}")
