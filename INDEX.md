# Index of sources

Retrieved 18 October 2026 unless stated. Paths are relative to this folder. When one of our documents
cites a source, it gives the path and the location inside it: section, equation, figure, error number
or source line. `sources/papers/MANIFEST.tsv` lists every PDF with the title arXiv states for it, so a
mis-named file can be caught.

## A. The two toolkits (`repos/`, local clones, excluded from git)

### WarpFactory, `repos/WarpFactory/`

MATLAB, MIT licence, Applied Physics (Christopher Helmerich, Jared Fuchs). Clone of `main` at
`03b10cb`, 23 May 2024; no commits since. No test suite. Documentation at
https://applied-physics.gitbook.io/warp-factory.

| Where | What it is and why it matters |
|---|---|
| `Solver/getEnergyTensor.m`, `Solver/utils/met2den.m`, `ricciT.m`, `takeFiniteDifference1.m`, `takeFiniteDifference2.m`, `c4Inv.m`, `cDet.m`, `einT.m`, `einE.m` | The metric-to-stress-energy pipeline: fourth-order central differences with edge fill, cofactor 4x4 inverse, Ricci loops, c^4/(8 pi G) scaling to J/m^3. Ported line for line in `work/precision-probe/` |
| `Metrics/WarpShell/metricGet_WarpShellComoving.m` | The Fuchs shell as actually built. Constant-density profile between R1 and R2; pressure from `TOVconstDensity`; four passes of moving-average smoothing on density (width 1.79 x) and pressure; mass recomputed from the smoothed density; lapse from `alphaNumericSolver`; the "warp" added to g_01 only, through `compactSigmoid` scaled by `vWarp` |
| `Metrics/utils/TOVconstDensity.m` | One line. The closed-form interior-Schwarzschild pressure of a uniform solid sphere of radius R2 and mass M, multiplied by the shell's density profile so it vanishes outside R1..R2. It is not an integration of the hollow shell's own TOV equation, which the paper's text says it is (§3.1 step 2, eq. 21) |
| `Metrics/utils/alphaNumericSolver.m` | Lapse by cumulative trapezoid of da/dr from r = 0 outward, then shifted so a matches Schwarzschild at the outer edge of the radial sample. The cavity's lapse is whatever results, below zero. Nothing imposes a(R1) = 0, which is the condition (B.3) the 2026 critique uses |
| `Analyzer/getEnergyConditions.m`, `Analyzer/utils/getEvenPointsOnSphere.m`, `generateUniformField.m` | The sampled observer check, directions times speeds, that Le 2026 measures against his matrix-inequality test |
| `Examples/4 Warp Shell/W1_Warp_Shell.mlx` | The live script that builds and analyses the shell. Binary; needs MATLAB to open |
| `LICENSE`, `CONTRIBUTING.md` | MIT; forks and derivative works welcome "so long as Warp Factory is properly cited"; contact create@appliedphysics.org |

### warpax, `repos/warpax/`

Python 3.12 or newer, JAX 0.10, Equinox; MIT licence; An T. Le (VinUniversity, TU Darmstadt). Clone
of `main` at `cb68eee`, 9 October 2026, version 1.5.1. Has tests, lint, a docs build and
`reproduce_all.sh`. Install: `pip install warpax`.

| Where | What it is and why it matters |
|---|---|
| `src/warpax/metrics/fuchs_construction.py`, `_fuchs_legacy.py`, `_tov_scan.py` | Le's reimplementation of the Fuchs construction: TOV integrated inward, kernel smoothing, a and b from the spherical Einstein equations, Schwarzschild imposed analytically outside. His own regularisation choices are documented in the module docstring. The legacy module keeps the unsmoothed intermediate |
| `src/warpax/constraints/source_consistency.py` | The diagnostic this project needs: Delta T = T_input - G/(8 pi) at a point. Its docstring calls it "the central diagnostic from Barzegar-Buchert-Vigneron (2026)" |
| `src/warpax/tov/residuals.py` | Anisotropic (Bowers-Liang) TOV equilibrium residual, derivatives by autodiff |
| `src/warpax/io/warpfactory.py` | Reads a WarpFactory `.mat` export (v7.3 through mat73, older through SciPy) into an interpolated ADM metric |
| `src/warpax/energy_conditions/slemma.py`, `certificate.py`, `interval_lmi.py`, `observer.py`, `sweep.py` | The S-lemma matrix-inequality tests, exact certificates, interval bounds, and the observer sampling he compares against |
| `scripts/run_construction_verification.py`, `src/warpax/analysis/construction_adapter.py` | Produces the paper's Table 9: Alcubierre, Rodal, Fuchs and Garattini under standardised kinematics |
| `docs/how-to/reproduce_warpshell_paper.md`, `docs/reference/metric_catalog.md` | States the hollow-shell impossibility in four sentences ("vacuum matching requires p(a) = 0, while the TOV equation makes nonnegative pressure nonincreasing outward") and the limits of his earlier S-/T-shell prescriptions |
| `examples/11_elastic_shell.py`, `results/elastic_shell/` | The Einstein-elastic shell boundary-value problem of Le's second paper, the material-support question |

## B. Papers (`sources/papers/` as PDF, `sources/papers-text/` as greppable text)

### B1. The Applied Physics line

| File | Citation | Why it matters, and where to look |
|---|---|---|
| `2021_bobrick_martire_introducing_physical_warp_drives_2102.06824` | Bobrick, Martire. CQG 38, 105009 (2021) | The framework the shell paper builds on: warp drives as shells of material; the claim that subluminal positive-energy drives are possible. Critiqued in Santiago et al. 2022 App. A and B, and in Barzegar et al. 2026 Errors 4, 10, 12, 14, 27 |
| `2023_helmerich_warpfactory_aiaa_2404.10855` | Helmerich et al. AIAA SciTech 2023 | The first WarpFactory paper |
| `2024_helmerich_warpfactory_cqg_2404.03095` | Helmerich, Fuchs, Bobrick, Sellers, Melcher, Martire. CQG 41, 095009 (2024) | The methods paper. Fourth-order differences, 1 m grid, four error sources, drop two edge cells; Figs 21-22 error analysis; §4 the "comoving frame" (Barzegar Error 12); §6 the energy-condition sampling claim (Barzegar Error 20) |
| `2024_fuchs_constant_velocity_physical_warp_drive_2405.02709` | Fuchs, Helmerich, Bobrick, Sellers, Melcher, Martire. CQG 41, 095013 (2024) | **The paper under test.** §3.1 metric creation in five steps (Fig. 3, eqs 19-21); the text admits the isotropic-pressure assumption "is not valid for the R1 boundary" and that Einstein's equations then give "the true rho and P_i"; §4 the shift beta_warp = 0.02; Fig. 4 density and pressure before and after smoothing; Figs 6-7 static shell; Figs 8-10 warp shell; Fig. 15 and Table 1 light-ray test, 7.6 ns. Parameters R1 = 10 m, R2 = 20 m, M = 4.49e27 kg |

### B2. The critiques

| File | Citation | Why it matters, and where to look |
|---|---|---|
| `2022_santiago_schuster_visser_generic_warp_drives_violate_nec_2105.03079` | Santiago, Schuster, Visser. PRD 105, 064038 (2022) | Generic null-energy violation for a broad class; Appendices A and B critique Bobrick and Martire. Barzegar et al. call it the best prior critique and note its own minor errors (their Errors 9 and 29) |
| `2023_schuster_santiago_visser_adm_mass_warp_drive_2205.15950` | Schuster, Santiago, Visser. Gen. Relativ. Gravit. (2023) | ADM mass in warp spacetimes; the "transported Schwarzschild drive" the Fuchs paper cites |
| `2025_barzegar_buchert_restrictions_of_current_warp_drives_2407.00720` | Barzegar, Buchert. Universe 11, 293 (2025) | Precursor of the 2026 critique; defines the S-Warp and T-Warp classes it refers back to |
| `2026_barzegar_buchert_vigneron_classification_demystification_2602.16495` | Barzegar, Buchert, Vigneron. arXiv, 18 Feb 2026, 33 pp. | **The critique.** Classification (S-Warp, R-Warp, Natário, Alcubierre); 37 numbered Errors; Theorems IV.31-33; **Error 18 and Appendix B**: the TOV and junction argument, eqs B.1-B.6, including the condition a(R1) = 0 (B.3) that we must assess against what the code does; Errors 12, 13, 20, 31, 33, 37 on Fuchs and Helmerich; Error 35 on Clough et al.; §IV.6 the Synge G-method; §V discussion and conclusions |

### B3. Robust verification and shells

| File | Citation | Why it matters, and where to look |
|---|---|---|
| `2026_le_observer_robust_energy_conditions_warpax_2602.18023` | Le. arXiv v6, 24 Sep 2026 | S-lemma matrix inequalities replace observer sampling. §3.4: WarpFactory's sampling found 93.4% of the points his method flags in a Rodal case; the Eulerian frame alone misses most violations for some metrics. Table 9: the Fuchs row is Type I throughout with positive minimum (rho + p). Appendix D "Fuchs constant-velocity shell", eqs 53-55, his regularisation. Related work: "Our pointwise tests of G/8 pi do not resolve that source-consistency question." Code and data: github.com/anindex/warpax, doi 10.5281/zenodo.18715933 |
| `2026_le_relativistic_elastic_shells_2605.25417` | Le. arXiv v3 (2026) | The material-support question for a shell with two free faces, solved as an Einstein-elastic boundary-value problem. What the interpretation step leans on |

### B4. Dynamics

| File | Citation | Why it matters, and where to look |
|---|---|---|
| `2024_clough_dietrich_khan_warp_drive_collapse_gw_2406.02466` | Clough, Dietrich, Khan. Open J. Astrophys. 7 (2024) | The only time-evolution of a warp bubble. GRChombo, CCZ4; ad hoc stiff-fluid closure; burst at f ~ 1/R, 300 kHz for 1 km, strain 1e-21 at 1 Mpc, about 0.01 solar masses released; a steady bubble emits nothing and has zero ADM mass. Barzegar et al. Error 35, and "the only sound numerical GR work" |

### B5. Other 2026 papers

| File | Citation | Why it matters |
|---|---|---|
| `2026_buchert_frackowiak_novel_realizations_2605.03653` | Buchert, Frackowiak. Universe 12, 132 (2026) | Natário subclass, Synge G-method constraints, "expected generic instability of the warp field" in the geodesic example |
| `2026_particle_geodesics_warp_drive_2608.08213` | (2026) | Geodesics in a warp spacetime; background only |

### B6. Foundations

| File | Citation | Why it matters |
|---|---|---|
| `1994_alcubierre_warp_drive_gr-qc_0009013` | Alcubierre. CQG 11, L73 (1994) | The metric. Its closed-form Eulerian energy density is the exact answer our precision probe tests against |
| `1997_pfenning_ford_unphysical_nature_of_warp_drive_gr-qc_9702026` | Pfenning, Ford. CQG 14, 1743 (1997) | Quantum inequalities applied to the Alcubierre bubble; the wall-thickness bound |
| `1999_van_den_broeck_warp_drive_reasonable_energy_gr-qc_9905084` | Van Den Broeck. CQG 16, 3973 (1999) | The pocket construction; in WarpFactory's metric set |
| `2002_natario_warp_drive_zero_expansion_gr-qc_0110086` | Natário. CQG 19, 1157 (2002) | Theorem 1.7: these models violate the weak or the strong energy condition; Barzegar et al. Theorem IV.31 cites it |
| `2021_lentz_breaking_the_warp_barrier_2006.07125` | Lentz. CQG 38, 075015 (2021) | Positive-energy soliton claim; refuted by Santiago et al.; Barzegar et al. Errors 3, 16, 17, 24, 30, 36; in WarpFactory's metric set |
| `2021_fell_heisenberg_positive_energy_warp_drive_2104.06488` | Fell, Heisenberg. CQG 38, 155020 (2021) | "Hidden geometric structures"; Barzegar et al. Errors 12, 19, 24, 36 |
| `2017_alcubierre_lobo_warp_drive_basics_2103.05610` | Alcubierre, Lobo. Fundam. Theor. Phys. 189 (2017) | The standard review chapter; Barzegar et al. Error 5 concerns its eq. (11.26) |

## C. Web pages (`sources/web/`, tag-stripped text with URL and date)

| File | What |
|---|---|
| `warpfactory_docs_overview.md`, `warpfactory_docs_installing.md`, `warpfactory_docs_a1_energy_conditions.md` | The GitBook: Cartesian-only limitation; Parallel Computing Toolbox listed as required. **It is required**: `takeFiniteDifference1.m` line 4 calls `isgpuarray()` unconditionally, a toolbox function, so the CPU path fails without it (first CI run, 18 Oct 2026). An earlier note here said the toolbox was only touched on the GPU path; that was wrong |
| `mathworks_file_exchange_warpfactory.md` | R2022a or later; toolbox "recommended"; v1.0.1, 17 Apr 2024. Written by hand: the page refuses scripted fetches |
| `github_warpfactory_readme.md`, `github_warpfactory_issue1_python_version.md` | README; the April 2024 request for a Python version, open, unanswered |
| `github_warpax_readme.md`, `pypi_warpax.md` (empty, page is script-rendered), `zenodo_warpax_record.md` | warpax's own description, install, citation |
| `github_matlab_actions_setup_matlab_licensing.md` | MathWorks licenses MATLAB free on GitHub-hosted runners for public repositories, Parallel Computing Toolbox included; not for private repositories without a batch token; no external language interfaces |
| `appliedphysics_warp_grants.md` | Half a million dollars in Phase I grants; PhD or publications expected; proposals must stay within classical relativity with positive energy |
| `oja_clough_collapse_published.md` | The journal page of the collapse paper |

## D. Our own work (`work/`)

| Where | What |
|---|---|
| `work/precision-probe/` | WarpFactory's solver arithmetic ported to NumPy and run against exact answers. `RESULTS.md` has the tables; `precision_probe.py` regenerates them and the figure |
| `work/hollow-shell/`, `work/shell/` | Steps 2 and 4: the TOV routes for the hollow shell; the 1D identity, 3D confirmation, smoothing sweep, compactness scan and the Einstein-cluster swarm, each with its `RESULTS.md` |
| `work/matrix/` | Parts 1 and 2: the shift-against-compactness matrix from CI (`matlab/shift_matrix.m`), its analysis, the Null/Weak replica, and warpax's exact energy conditions on the same slices (`exact_conditions.py`, `exact_maps.py`). `RESULTS.md` sections 1-6 are Part 1, section 7 is Part 2; `README.md` has the commands |
| `work/wf-reproduction/` | Part 3: the paper's Figures 4 to 10 next to ours from the slices (`pairs/`), the paper's curves digitised from the PDF (`digitise_paper.py`, `comparison.csv`), and the smoothing behind the figures fitted with the replica (`fit_smoothing.py`); `RESULTS.md` has the verdicts |
| `work/notes/` | Session notes, dated; 03 holds the letters as sent, 10 the two WarpFactory issue drafts |
| `REPORT.md` (root) | The draft report for the comment window, 27 October 2026; its appendix will hold the replies |

## E. Still to add

- Rodal's papers on curvature invariants and the irrotational profile (Le's reference [6] and [27, 28]).
- Abellán et al., Bolívar et al., Garattini and Zatrimaylov: cited on both sides, not yet fetched.
- Kuwahara and Cannon 2023 on searching detector data for exotic bursts, cited by Clough et al.
- Any reply by Applied Physics to the February 2026 critique. None found as of 18 October 2026.
