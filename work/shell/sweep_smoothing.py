"""
sweep_smoothing.py -- how the required hoop stress depends on the construction's free parameter.

The smoothing width is the one knob in the Fuchs construction (paper §3.1 step 5: iterated "until
we find a metric that satisfies the energy conditions at the boundaries"). Using the NumPy replica
of the 1D construction, validated against WarpFactory's own export to 1e-13 (compare_profiles.py),
rebuild the shell for a range of smoothFactor values and report the tangential pressure the shell
then requires. Everything else (R1, R2, M) is held at the authors' values.

Columns: smoothFactor; 10-90% width of the smoothed density at the inner wall [m]; peak P_r/rho0 c^2;
peak P_t/rho0 c^2 and its radius; min P_t/rho0 c^2; max P_t/rho(r) where rho > 1% of peak
(the dominant-energy-condition ratio); total smoothed mass / M.

Usage: python sweep_smoothing.py   (writes sweep_smoothing.csv)
"""
import numpy as np
import replicate_profiles as rp
import hoop_stress as hs

rows = []
print(f"{'smooth':>7s} {'wall10-90[m]':>12s} {'Pr_max':>8s} {'Pt_max':>8s} {'r(Pt_max)':>9s} {'Pt_min':>8s} {'max Pt/rho':>10s} {'Msmooth/M':>10s}")
for sf in (250, 500, 1000, 2000, 3000, 4000, 6000, 8000, 12000, 16000):
    d = rp.build(smoothFactor=sf)
    prof = {k: d[k] for k in ("r_m", "rhosmooth_kg_m3", "Psmooth_Pa", "A_g00")}
    r, rho, Pr, Pt, a = hs.identity_tangential(prof)
    rho0 = rho.max()
    shell = (r > 2.0) & (r < 28.0)
    # 10-90% width of the smoothed density on the inner wall
    inner = (r > 2.0) & (r < 15.0)
    ri, rhoi = r[inner], rho[inner] / rho0
    r10 = ri[np.argmax(rhoi >= 0.10)]
    r90 = ri[np.argmax(rhoi >= 0.90)]
    ok = shell & (rho > 0.01 * rho0)
    i_max = np.argmax(Pt[shell])
    row = dict(smoothFactor=sf, wall_10_90_m=r90 - r10, Pr_max=Pr[shell].max() / rho0,
               Pt_max=Pt[shell][i_max] / rho0, r_Pt_max=r[shell][i_max], Pt_min=Pt[shell].min() / rho0,
               max_Pt_over_rho=np.max(Pt[ok] / rho[ok]), Msmooth_over_M=d["M_kg"][-1] / d["m"])
    rows.append(row)
    print(f"{sf:7d} {row['wall_10_90_m']:12.3f} {row['Pr_max']:8.4f} {row['Pt_max']:8.4f} {row['r_Pt_max']:9.2f} {row['Pt_min']:+8.4f} {row['max_Pt_over_rho']:10.3f} {row['Msmooth_over_M']:10.5f}")

keys = list(rows[0].keys())
np.savetxt("sweep_smoothing.csv", np.array([[row[k] for k in keys] for row in rows]), delimiter=",",
           header=",".join(keys), comments="", fmt="%.10g")
print("written: sweep_smoothing.csv")
