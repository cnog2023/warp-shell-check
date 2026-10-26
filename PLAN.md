# Plan: source consistency of the Fuchs et al. warp shell

Status: approved 18 October 2026 (Carlos: go; repository `warp-shell-check`, public; contact Le
early). Progress at the end of 18 October: Steps 0, 1 and 2 done (`work/notes/01`, `02`); Step 3
half done (the shell is built in CI at the authors' exact configuration and exported; the
side-by-side figures against the paper are pending); Step 4's core done for the static shell
(`work/shell/RESULTS.md`: 1D identity, 3D confirmation, smoothing sweep). Open: all-observer energy
conditions of the warp shell in both toolkits (C4, C5), the warpax-native comparison, Step 6, Step 7.
E-mails drafted in `work/notes/03`, to be sent by Carlos after reading.
Update 26 October: Part 1 of §7a done (`work/matrix/RESULTS.md`, notes 06 and 07): the allowed
shift is 0.09 to 0.10 times the compactness; the paper's 0.02 passes with a ceiling of 0.030 to
0.033; two WarpFactory defects found (GPU hard-coded in the sampling; Null and Weak maps lowered
with the coordinate metric). Wiki published. Next: Part 2 (warpax), on Carlos's word. E-mails
still on hold until Part 4.

## 0. The question

> The metric of the "constant velocity physical warp drive" (Fuchs et al. 2024) is built from a
> trial fluid: a constant-density shell with isotropic pressure, smoothed. Einstein's equations then
> dictate the matter that metric actually requires. How far apart are the two, where, and what
> does the gap imply about the claim that the shell is made of ordinary, stable matter?

Why it is open, with the evidence in `INDEX.md`:

- Fuchs et al. acknowledge the gap in words, "Einstein's equations then provide the true rho and
  P_i", and never quantify it (paper, §3.1).
- Barzegar, Buchert and Vigneron argue the construction "is not a solution to Einstein's equations"
  (Error 18, Appendix B) but compute nothing numerically, and their derivation imposes a condition,
  a(R1) = 0, that WarpFactory's own code does not impose (`alphaNumericSolver.m` matches the lapse
  to Schwarzschild at the outside and lets the cavity's lapse fall where it falls).
- Le built the exact diagnostic (`source_consistency.py`) and a reimplementation of the shell, and
  writes that his published tests "do not resolve that source-consistency question".

Nobody has published the number. It runs on a laptop.

## 1. What we already know, so the plan does not redo it

- WarpFactory's pressure step is a one-line closed form: the interior-Schwarzschild pressure of a
  uniform solid sphere, masked to the shell. The paper's text describes a numerical TOV integration
  of the hollow shell. The two differ and the difference is one thing to document.
- The smoothing is four passes of a moving average, applied separately to density and pressure
  with different widths. After smoothing the pair no longer satisfies any equilibrium equation, so
  the metric built from it must carry extra stresses. That is the expected form of the gap:
  anisotropy, tangential against radial, concentrated in the two smoothed walls.
- The hollow-shell impossibility is elementary and already stated in warpax's documentation: a free
  inner face needs zero pressure there, while TOV makes nonnegative pressure fall outward, so a
  perfect-fluid shell with a vacuum cavity cannot be static without surface or tangential stress.
- Le's Table 9 finds the regularised shell Type I everywhere with positive minimum (rho + p), so
  the pointwise energy conditions are probably not where the construction fails. The failure, if
  there is one, is in what the matter would have to be.
- Our precision probe fixed the numerical error budget of WarpFactory's solver: percent-level at
  1 m spacing, falling as the fourth power of the spacing, with a double-precision floor near 1e-8.
  Any residual we report must be shown to sit above that budget.

## 2. The deliverable

A public repository under Carlos's GitHub account, MIT licence, with a Zenodo DOI, containing:

1. A short report, about ten pages: question, method, the number, its convergence, what it means,
   and the responses of the parties consulted.
2. The scripts and notebooks that regenerate every figure and table from scratch, in both toolkits.
3. A claim register (`CLAIMS.md`) showing, for each disputed claim, the quote, the test, the result.

Audience: the three groups involved and anyone who reads the 2024 paper and wants to know whether
it holds. Tone: an independent reproduction, neutral, with every statement tied to a quote and a
computation. The word "debunk" does not appear.

Optional afterwards: an arXiv posting, which needs an endorser in gr-qc; one of the consulted
authors may offer if the work is sound. Not a goal, a possibility.

## 3. Steps

Each step has a goal, an output, who does what, and a gate: a decision Carlos takes before the next
step starts. Session counts are guesses.

### Step 0. Workbench (mostly done today)

- Goal: everything needed to compute is in place.
- Done: folder, index, both repositories, papers, Python environment with NumPy and Matplotlib,
  the precision probe restored.
- Left: install warpax into the environment and run its first two examples; create the public
  GitHub repository with MATLAB on its continuous-integration runners, which MathWorks licenses
  free for public repositories. That replaces MATLAB Online and needs no MathWorks account.
- Carlos: approve the repository name and that it is public from day one.
- Gate: warpax example 02 (Schwarzschild) runs here; a trivial MATLAB job passes on the public repo.
- Sessions: 1.

### Step 1. Close reading and the claim register

- Goal: every claim we test is quoted, located, and paired with a pass or fail rule. No test is
  designed from a summary.
- Read: Fuchs §3-4 in full; Helmerich 2024 §4 and §6; Barzegar Errors 12, 13, 18, 20, 31, 33, 37
  and Appendix B; Le §3.4, §3.6, Appendix D; the two shell modules of each toolkit.
- Specific questions to settle on paper: Does Fuchs's text anywhere impose a(R1) = 0, or an interior
  with unit lapse? What exactly does the paper claim about the final matter: fluid, "matter shell",
  or just "satisfies the energy conditions"? What does "stable" mean in the paper, and is any
  stability analysis performed?
- Output: `CLAIMS.md` with every row at status `quoted`, and `work/notes/01-reading.md`.
- Carlos: read the register; strike any claim he does not want pursued.
- Gate: Carlos signs off the list of tests.
- Sessions: 2.

### Step 2. Pen and paper: the hollow shell

- Goal: a clean, checkable derivation of what a static hollow shell of isotropic fluid requires,
  and a verdict on Appendix B of the critique.
- Content: (a) the free-inner-face argument, with the pressure at R1 that TOV forces for the
  paper's numbers; (b) whether imposing both (B.2) and (B.3) is legitimate, given that the lapse can
  only be normalised once, at infinity; (c) what the code actually does, with line references;
  (d) a thirty-line script integrating TOV inward for the paper's shell and printing P(R1)/rho c^2
  and the cavity lapse.
- Output: `work/notes/02-hollow-shell.md` and `work/hollow-shell/tov_hollow.py`.
- Carlos: read it; decide whether to write to Barzegar, Buchert and Vigneron now about (B.3), which
  starts the adversarial review early and cheaply.
- Gate: the note stands up to Carlos's reading and, if sent, to the authors' first reply.
- Sessions: 1 to 2.

### Step 3. Reproduce the shell in WarpFactory

- Goal: the paper's own figures, from the paper's own code, at the paper's parameters.
- Build the static shell (no shift) and the warp shell (shift 0.02) with R1 = 10 m, R2 = 20 m,
  M = 4.49e27 kg; the paper's smoothing; grid spacings 1 m, 0.5 m and 0.25 m. Reproduce Figs 4, 6,
  7, 8, 9, 10. Export metric, stress-energy, energy-condition fields and the trial profiles as
  `.mat` (v7.3) for warpax to read.
- Runs in the public repository's MATLAB job, or in MATLAB Online if Carlos prefers to watch.
- Output: `work/wf-reproduction/` with figures side by side with the paper's, and the exports.
- Carlos: "same picture" or "not the same" for each pair.
- Gate: all six pairs judged the same, or every difference explained.
- Sessions: 2.

### Step 4. The measurement: source consistency

- Goal: the number. Revised 18 October after the close reading (`work/notes/01-reading.md` §6):
  the construction fixes the energy density and the radial pressure to the smoothed inputs by
  design, so the only new matter it demands is the tangential pressure, set by the equilibrium
  identity P_t = P_r + (r/2)[dP_r/dr + (rho + P_r) da/dr]. First compute that exactly from
  WarpFactory's own 1D profiles (`Metric.params`), at the paper's smoothing and across a sweep of
  smoothing widths. Then confirm in 3D: Delta T = T_trial - G/(8 pi) over the whole grid in both
  toolkits, which measures the same anisotropy plus the solvers' numerical error.
- Report, for the static shell and the warp shell: energy-density residual; radial against
  tangential pressure, the anisotropy; residual momentum density; residual in the cavity and
  outside; all as fractions of rho c^2 and all as functions of radius. Show convergence with grid
  spacing against the probe's error budget, and dependence on the smoothing width, which is a free
  parameter of the construction.
- Do it twice: in WarpFactory's finite differences on its own grid, and in warpax, both on the
  imported `.mat` and on Le's native `FuchsMetric` with his `source_consistency` and anisotropic
  TOV residual. Two implementations, one answer, or an explanation.
- Output: `work/source-consistency/` with tables, figures, and one headline figure: the stress the
  shell needs that the trial fluid does not provide, as a fraction of its own energy density,
  against radius.
- Carlos: verdict on agreement between the two toolkits, by the twelve-digit rule where inputs are
  identical and by overlapping error bars where they are not.
- Gate: the residual is shown to be either above the numerical budget and convergent, or within it.
- Sessions: 3.

### Step 5. Energy conditions, cross-checked

- Goal: settle the two numerical claims that are easy once Step 4 exists.
- Run WarpFactory's sampled check and warpax's matrix-inequality check on the same exported metric;
  report the miss fraction, and whether 0.02 passes in both. Scan the shift upward to the first
  violation in each tool.
- Output: one table in `work/energy-conditions/`.
- Gate: none; this feeds the report.
- Sessions: 1.

### Step 6. Interpretation

- Goal: say what the measured stress state means physically, briefly and without overreach.
- Compare the required anisotropic stress, as a fraction of rho c^2, with the strength-to-energy
  ratio of known materials, and with what Le's elastic-shell paper finds a self-gravitating shell
  with two free faces can sustain. State plainly that no stability analysis exists in the 2024 paper
  and that we do not perform one either.
- Output: a section of the report.
- Sessions: 1.

### Step 7. Write-up, adversarial review, publication

- Goal: a report the three parties have seen before the public does.
- Draft; send to Applied Physics (Fuchs, Helmerich; create@appliedphysics.org as their contributing
  guide asks), to Barzegar, Buchert and Vigneron, and to Le, with a two-week comment window. Record
  every reply verbatim in an appendix, with permission, or summarise if not. Incorporate what is
  right; say where we disagree and why.
- Publish: repository public, Zenodo DOI minted, notebook linked; a comment on WarpFactory's issue
  tracker and on warpax's; a short post where the field reads, with the DOI.
- Carlos: all outward messages go in his name and with his sign-off; he decides the final wording of
  anything contested.
- Sessions: 2, plus waiting.

## 4. Who does what

| | Carlos | Claude |
|---|---|---|
| Decisions | Go or no-go at each gate; repository name; which claims to pursue; final wording | Recommends, never decides |
| Accounts and sending | GitHub repository creation or approval; every e-mail and comment in his name; Zenodo | Drafts all of it |
| Reading | The claim register, the notes, the report; "same picture" verdicts | All close reading, quoting, locating |
| Computation | None required | All of it, in both toolkits, with convergence evidence |
| Physics judgement | Asks the questions a careful outsider asks | Tied to quotes and computations; where a judgement is mine alone, it is labelled as such |

## 5. Gates and kill criteria

- After Step 2: if the elementary argument already settles everything the critique claims and the
  code is found to do exactly what the critique assumes, the project shrinks to a two-page
  confirmation note and stops there. Still worth publishing; nobody has written it.
- After Step 4: if the residual is within the numerical budget everywhere, the 2024 construction is
  self-consistent to the precision available, the critique's Error 18 is wrong as stated, and that
  is the headline. Equally publishable.
- At any point: if a party consulted shows us a mistake we cannot repair, we publish the correction
  with the result, not instead of it.

## 6. Risks

- **My reliability on general-relativity subtleties.** Mitigation: nothing rests on my reading
  alone; every physics statement is a quote plus a computation, and three expert parties see the
  draft before anyone else.
- **Tone.** Carlos's name is on it. Mitigation: neutral language throughout; the critique's authors
  are quoted exactly as the 2024 paper's authors are.
- **Scope creep.** Mitigation: the question in §0 is the whole scope. Dynamics, superluminal cases,
  new solutions and stability analysis are out.
- **MATLAB access.** Mitigation: free continuous-integration licence for public repositories;
  MATLAB Online as fallback; the Python port of the solver core as a last resort for the static
  shell.
- **Le or Applied Physics publishes the same number first.** Mitigation: contact Le in Step 2, not
  Step 7. A shared result credited properly is a better outcome than a race.

## 7. Effort

| | Sessions | Wall time |
|---|---|---|
| Steps 0-2 | 4 to 5 | Two weeks of evenings |
| Steps 3-6 | 7 | Three to four weeks |
| Step 7 | 2 plus the comment window | Three weeks |

Compute: this laptop. The largest grid in Step 4 is below a million points.

## 7a. Parts plan, 26 October 2026 (token-aware)

Carlos's direction: see how far the computations go before contacting anyone, in parts, each
approved separately. Compute on the GitHub runner is free; the cost is reading and writing, so each
part is one focused session that ends with a result and stops. The e-mails of `work/notes/03` wait
for Part 4.

| Part | Content | Output | Needs |
|---|---|---|---|
| **1. How far the construction goes** | (A) the allowed shift against compactness: CI matrix over compactness {1/3, 1/10, 1/30, 1/100} and shift {0.01, 0.02, 0.04, 0.08, 0.16}, Eulerian lines, energy-condition proxies along them, then one full sampled energy-condition run at the authors' point to time it and confirm 0.02 passes. (B) the swarm model finished: Type and trace checks of the warp shell's exported stress-energy, and two literature fetches on Einstein-cluster stability | beta_max(C) table and figure; `06` extended; C5 closed from WarpFactory's side | one session; CI time |
| **2. Second toolkit** | warpax matrix-inequality energy conditions on the exported slices (`pip install "warpax[interop]"` for the .mat reader) or its native FuchsMetric at matching parameters, against WarpFactory's sampled check; the shift threshold from both | C4 and C5 closed; miss fraction | one session |
| **3. Reproduction figures** | Figs 6, 8, 9 of the paper side by side with ours from the slices; 7 and 10 if Part 1's full run exists | Step 3 closed | half a session |
| **4. Write-up and contact** | the report from the notes; e-mails sent with the draft | Step 7 | one to two sessions, plus the comment window |

Stopping after any part leaves a defensible note; the present state already is one.

## 8. What this project is not

Not new physics. Not a port of WarpFactory, which warpax has made unnecessary. Not a stability
analysis. Not a verdict on warp drives. It is one measurement, done carefully twice, that three
groups have talked past, written up so that anyone can rerun it.
