"""
fit_smoothing.py -- which smoothing produced the paper's Figure 6? (Part 3)

The paper's smoothed inputs rho~ and P~ (Figure 6, digitised by digitise_paper.py) have the same
radii and mass as the W1 live script's but narrower walls. The construction's only free parameters
at fixed geometry and mass are the two moving-average spans (density and pressure; four passes each,
paper section 3.1 and footnote 7: "a ratio between the span of density and pressure s_rho / s_P ~ 1.72";
the live script uses 1.79 x smoothFactor and smoothFactor, smoothFactor = 4000). This script fits each
span to the digitised curve with the validated NumPy replica of the construction
(`work/shell/replicate_profiles.py`, MATLAB's smooth() edge rule included), then rebuilds the metric
at the fitted spans and predicts the tangential pressure from the equilibrium identity
(`work/shell/hoop_stress.py`), to be compared with the paper's digitised P_1 = P_3 spike.

Spans are in radial samples of the replica's grid (dr = 5.07e-4 m, the same as WarpFactory's
rsample); the misfit is the RMS difference over the digitised points, as a fraction of the curve's
peak.

Usage: python fit_smoothing.py
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "work" / "shell"))
import hoop_stress as hs  # noqa: E402
import replicate_profiles as rp  # noqa: E402

G, c = rp.G, rp.c


def digitised(fig, name):
    rows = [x for x in csv.DictReader(open(HERE / "paper_curves.csv", encoding="utf-8")) if x["figure"] == fig and x["curve"] == name]
    r = np.array([float(x["r_m"]) for x in rows]); v = np.array([float(x["value"]) for x in rows])
    o = np.argsort(r)
    return r[o], v[o]


def smooth4(y, span):
    for _ in range(4):
        y = rp.matlab_smooth(y, span)
    return y


def construct(base, span_rho, span_P):
    """The replica's construction after the smoothing step, with independent spans."""
    r = base["r_m"]
    rhos = smooth4(base["rho_kg_m3"], span_rho)
    Ps = smooth4(base["P_Pa"], span_P)
    Ms = rp.cumtrapz(r, 4 * np.pi * rhos * r ** 2)
    Ms[Ms < 0] = Ms.max()
    with np.errstate(invalid="ignore", divide="ignore"):
        dalpha = (G * Ms / c ** 2 + 4 * np.pi * G * r ** 3 * Ps / c ** 4) / (r ** 2 - 2 * G * Ms * r / c ** 2)
    dalpha[0] = 0.0
    aT = rp.cumtrapz(r, dalpha)
    a = aT + (0.5 * np.log(1 - 2 * G * Ms[-1] / r[-1] / c ** 2) - aT[-1])
    return dict(r_m=r, rhosmooth_kg_m3=rhos, Psmooth_Pa=Ps, A_g00=-np.exp(2 * a), M_kg=Ms)


def misfit(r_d, v_d, r, v):
    return np.sqrt(np.mean((np.interp(r_d, r, v) - v_d) ** 2)) / v_d.max()


def width_10_90(r, v, inner=True):
    m = v.max(); sel = (r > 2) & (r < 15) if inner else (r > 15) & (r < 28)
    rr, vv = r[sel], v[sel] / m
    if not inner:
        rr, vv = rr[::-1], vv[::-1]
    return abs(rr[np.argmax(vv >= 0.9)] - rr[np.argmax(vv >= 0.1)])


def main():
    base = rp.build(smoothFactor=4000)
    r = base["r_m"]
    rd, rho_d = digitised("6", "rho_smoothed_c2")
    pd_, P_d = digitised("6", "P_smoothed")
    sel_r = (rd > 3) & (rd < 27); sel_p = (pd_ > 3) & (pd_ < 27)
    rd, rho_d, pd_, P_d = rd[sel_r], rho_d[sel_r], pd_[sel_p], P_d[sel_p]

    print("W1 live script (smoothFactor 4000: density span 7160, pressure span 4000):")
    print(f"  rho~ misfit {misfit(rd, rho_d, r, smooth4(base['rho_kg_m3'], 7160) * c ** 2):.4f}, P~ misfit {misfit(pd_, P_d, r, smooth4(base['P_Pa'], 4000)):.4f}")

    spans = np.arange(3000, 9001, 20)
    mr = np.array([misfit(rd, rho_d, r, smooth4(base["rho_kg_m3"], s) * c ** 2) for s in spans])
    mp = np.array([misfit(pd_, P_d, r, smooth4(base["P_Pa"], s)) for s in spans])
    s_rho, s_P = spans[np.argmin(mr)], spans[np.argmin(mp)]
    print(f"independent fits: density span {s_rho} samples ({s_rho * (r[1] - r[0]):.3f} m per pass), misfit {mr.min():.4f}; "
          f"pressure span {s_P} ({s_P * (r[1] - r[0]):.3f} m), misfit {mp.min():.4f}; ratio {s_rho / s_P:.3f} (paper: ~1.72; live script: 1.79)")
    rd4, rho4 = digitised("4", "rho_smoothed_c2"); pd4, P4 = digitised("4", "P_smoothed")
    s4r = (rd4 > 3) & (rd4 < 27); s4p = (pd4 > 3) & (pd4 < 27)
    mr4 = np.array([misfit(rd4[s4r], rho4[s4r], r, smooth4(base["rho_kg_m3"], s) * c ** 2) for s in spans])
    mp4 = np.array([misfit(pd4[s4p], P4[s4p], r, smooth4(base["P_Pa"], s)) for s in spans])
    print(f"the same fits to Figure 4's smoothed curves: density span {spans[np.argmin(mr4)]}, misfit {mr4.min():.4f}; pressure span {spans[np.argmin(mp4)]}, misfit {mp4.min():.4f}")
    _, Pu4 = digitised("4", "P_unsmoothed")
    print(f"Figure 4's unsmoothed pressure peaks at {Pu4.max():.4e} J/m^3 = {Pu4.max() / (base['rho_kg_m3'].max() * c ** 2):.4f} rho0 c^2 (closed form masked to the shell: {base['P_Pa'].max() / (base['rho_kg_m3'].max() * c ** 2):.4f}; inward TOV integration, work/notes/02: 0.073)")
    for ratio in (1.72, 1.79):
        joint = np.array([misfit(rd, rho_d, r, smooth4(base["rho_kg_m3"], ratio * s) * c ** 2) + misfit(pd_, P_d, r, smooth4(base["P_Pa"], s)) for s in spans])
        sb = spans[np.argmin(joint)]
        print(f"  with the ratio fixed at {ratio}: best pressure span {sb} (density {ratio * sb:.0f}), joint misfit {joint.min():.4f}")

    # the construction at the fitted spans, and what it predicts
    rows = []
    for label, a_, b_ in (("W1 live script", 7160, 4000), ("fitted to Figure 6", s_rho, s_P)):
        prof = construct(base, a_, b_)
        rr, rho, Pr, Pt, _ = hs.identity_tangential(prof)
        shell = (rr > 2.0) & (rr < 28.0)
        i = np.argmax(Pt[shell])
        rows.append((label, a_, b_, rho.max(), width_10_90(rr, rho), Pr[shell].max(), Pt[shell][i], rr[shell][i], prof["M_kg"][-1] / base["m"]))
    r6, p6 = digitised("6", "P_1 = P_3 (tangential)")
    r6b, rho6 = digitised("6", "rho")
    rows.append(("paper, Figure 6", 0, 0, rho6.max(), width_10_90(rd, rho_d), digitised("6", "P_2 (radial)")[1].max(), p6.max(), r6[np.argmax(p6)], np.nan))
    print(f"\n{'construction':<20s} {'span_rho':>8s} {'span_P':>7s} | {'rho~ peak':>10s} {'wall 10-90':>10s} {'P_r peak':>10s} {'P_t peak':>10s} {'at r':>5s} {'M_s/M':>7s}")
    for row in rows:   # identity_tangential returns rho in J/m^3 already
        print(f"{row[0]:<20s} {row[1]:8d} {row[2]:7d} | {row[3]:10.3e} {row[4]:10.3f} {row[5]:10.3e} {row[6]:10.3e} {row[7]:5.2f} {row[8]:7.4f}")
    # what the two constructions predict for Figure 5: the cavity g00 and the peak of g22 = 1/(1 - 2Gm(r)/(r c^2))
    r5, g00_5 = digitised("5", "g00"); _, g22_5 = digitised("5", "g22")
    for label, a_, b_ in (("W1 live script", 7160, 4000), ("fitted to Figure 6", s_rho, s_P)):
        prof = construct(base, a_, b_)
        with np.errstate(divide="ignore", invalid="ignore"):
            B = 1.0 / (1.0 - 2 * G * prof["M_kg"] / (r * c ** 2))
        ok = (r > 1) & (r < 30)
        print(f"Figure 5 prediction, {label}: cavity g00 {prof['A_g00'][np.argmin(abs(r - 5))]:+.4f}, g22 peak {B[ok].max():.4f} at {r[ok][np.argmax(B[ok])]:.2f} m")
    print(f"Figure 5 digitised: cavity g00 {g00_5[np.argmin(abs(r5 - 5))]:+.4f}, g22 peak {g22_5.max():.4f} at {r5[np.argmax(g22_5)]:.2f} m")
    with open(HERE / "fit_smoothing.csv", "w", encoding="utf-8") as f:
        f.write("construction,span_rho_samples,span_P_samples,rho_smoothed_peak_J_m3,wall_10_90_m,P_r_peak_J_m3,P_t_peak_J_m3,r_of_P_t_peak_m,M_smoothed_over_M\n")
        for row in rows:
            f.write(",".join(str(x) if not isinstance(x, float) else f"{x:.6g}" for x in row) + "\n")
        f.write(f"# independent fits: density span {s_rho} (misfit {mr.min():.4f}), pressure span {s_P} (misfit {mp.min():.4f}), ratio {s_rho / s_P:.3f}; "
                f"W1 misfits {misfit(rd, rho_d, r, smooth4(base['rho_kg_m3'], 7160) * c ** 2):.4f} and {misfit(pd_, P_d, r, smooth4(base['P_Pa'], 4000)):.4f}\n")
    print("written:", HERE / "fit_smoothing.csv")


if __name__ == "__main__":
    main()
