# Note 10: two issues for WarpFactory's tracker (drafts for Carlos to post)

27 October 2026. To be posted at github.com/NerdsWithAttitudes/WarpFactory/issues by Carlos, after
the Applied Physics authors have had the chance to say whether they want them there (e-mail 3,
question 3). Both against WarpFactory at commit 03b10cb (the clone of 18 October 2026); line
references are to that commit. Tone: a bug report, nothing else.

---

## Issue 1: getEnergyConditions fails without a GPU because generateUniformField hard-codes the GPU flag

**Summary.** `Analyzer/utils/generateUniformField.m` calls `getEvenPointsOnSphere(R, numberOfPoints, 1)`
with the third argument, `useGPU`, fixed at 1, in both the "timelike" and the "nulllike" branches.
`getEvenPointsOnSphere` then allocates with `gpuArray`, so on a machine without a CUDA device
`getEnergyConditions` fails with "Error using gpuArray" whatever the caller passed as `tryGPU`. The
function's own `tryGPU` argument is only applied afterwards, to the finished field.

**To reproduce.** On any machine without a GPU (for example a GitHub-hosted runner), build any
metric, compute its stress-energy and call
`getEnergyConditions(energy, metric, "Null", 100, 10, 0, 0)`.

**Fix.** Pass the caller's flag through: `getEvenPointsOnSphere(1 - bb(jj), numAngularVec, tryGPU)` in
the timelike branch and `getEvenPointsOnSphere(1, numAngularVec, tryGPU)` in the null-like one (and
drop the stray first call in the null-like branch, whose result is unused). A copy with that change
is `matlab/shadow/generateUniformField.m` in github.com/cnog2023/warp-shell-check; with it the four
sampled conditions on three 300 x 300 planes take about 9 s per case on a runner's CPU.

---

## Issue 2: the Null and Weak branches of getEnergyConditions lower the Eulerian frame tensor's indices with the coordinate metric

**Summary.** `Analyzer/getEnergyConditions.m` first transforms the stress-energy into the orthonormal
Eulerian frame (`doFrameTransfer`, which returns it flagged contravariant). The Dominant and Strong
branches then change its index position with a Minkowski metric (`metricGet_Minkowski`), which is
the consistent choice for components in an orthonormal frame. The Null and Weak branches instead
call `changeTensorIndex(energyTensor, "covariant", metric)` with the coordinate metric. For a frame
tensor that mixes components wherever the coordinate metric is not Minkowski: inside a shell where
g_rr differs from 1, and wherever a shift makes g_01 nonzero.

**Effect.** For the constant-velocity warp shell of Fuchs et al. 2024 at the paper's configuration,
the Null and Weak maps report violations from a shift of about 0.023 (0.07 times the compactness)
that the Dominant and Strong maps, a 4000-direction null check and warpax's exact S-lemma test all
place at 0.030 to 0.033. At the paper's own shift of 0.02 no map shows a violation, so the published
conclusion is unaffected; the Null and Weak panels of the paper's Figures 7 and 10 do read low by
about the square of g00 (a plateau of 2.8e39 J/m^3 where the Strong panel reaches 7.1e39).

**Evidence.** `work/matrix/verify_null_bug.py` in github.com/cnog2023/warp-shell-check replicates the
Null branch in NumPy on an exported slice: with the coordinate metric it reproduces WarpFactory's
map to 1.3e-16 of the peak energy density; with Minkowski the spurious minima vanish (at a shift of
0.08 times the compactness, -0.049 of the peak energy density becomes -3e-7). Table in
`work/matrix/RESULTS.md` section 4.

**Fix.** In the Null and Weak branches use the same Minkowski metric the Dominant and Strong
branches build: `energyTensor = changeTensorIndex(energyTensor, "covariant", metricMinkowski)`.
