"""
compactness_scan.py -- the only remedy the paper offers for the stress, made quantitative.

Fuchs et al. 2024 §3.2: "For realistic materials that may have a limited range of pressures
possible, this requirement can always be satisfied by making the shell large and modifying the
density profile, hence, reducing the gravitational forces." Here the geometry and smoothing are
held at the authors' values and the mass is scaled down, so the compactness 2GM/(R2 c^2) falls.
The validated NumPy replica gives the profiles; the equilibrium identity gives the hoop stress.

Usage: python compactness_scan.py   (writes compactness_scan.csv)
"""
import numpy as np
import replicate_profiles as rp
import hoop_stress as hs

G, c = rp.G, rp.c
rows = []
print(f"{'2GM/R2c^2':>10s} {'M [kg]':>10s} {'rho0 [kg/m^3]':>14s} {'Pt_peak/rho0c^2':>16s} {'max Pt/rho(r)':>14s} {'Pt_peak [Pa]':>13s} {'(Pt/rho)/C':>11s}")
for f in (1 / 3, 1 / 10, 1 / 30, 1 / 100, 1 / 1000, 1 / 10000):
    d = rp.build(factor=f)
    prof = {k: d[k] for k in ("r_m", "rhosmooth_kg_m3", "Psmooth_Pa", "A_g00")}
    r, rho, Pr, Pt, a = hs.identity_tangential(prof)
    rho0 = rho.max()
    shell = (r > 2) & (r < 28)
    ok = shell & (rho > 0.01 * rho0)
    C = 2 * G * d["m"] / (20.0 * c**2)
    ratio = np.max(Pt[ok] / rho[ok])
    rows.append((C, d["m"], rho0 / c**2, Pt[shell].max() / rho0, ratio, Pt[shell].max(), ratio / C))
    print(f"{C:10.2e} {d['m']:10.2e} {rho0 / c**2:14.2e} {Pt[shell].max() / rho0:16.4f} {ratio:14.4f} {Pt[shell].max():13.2e} {ratio / C:11.3f}")
np.savetxt("compactness_scan.csv", np.array(rows), delimiter=",", comments="", fmt="%.10g",
           header="compactness,M_kg,rho0_kg_m3,Pt_peak_over_rho0c2,max_Pt_over_rho,Pt_peak_Pa,ratio_over_compactness")
print("written: compactness_scan.csv")
print("\nStrength over rho c^2 for reference materials:")
for name, s, dens in (("structural steel, yield", 0.5e9, 7850), ("carbon fibre, tensile", 7e9, 1800),
                      ("graphene, ideal tensile", 130e9, 2267), ("diamond, compressive", 110e9, 3510)):
    print(f"  {name:26s} {s / (dens * c**2):10.1e}")
