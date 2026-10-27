# Note 08: Part 2 (27 October 2026)

Log entry; the write-up is `work/matrix/RESULTS.md` section 7.

- warpax 1.5.1's S-lemma margins (`certify_point_lmi`, all four conditions, every observer, no
  sampling, no rapidity cap) were run on every active cell of all 68 exported slices, by two routes:
  the frame tensor with Minkowski, and the coordinate tensor rebuilt through WarpFactory's own
  tetrad, which was ported and checked (M^T g M = eta to 7e-16). Null, weak and strong margins agree
  between the routes to 4e-15 rho0 (7e-14 on the coarse run, margins to 80 rho0); the dominant
  margin agrees in sign everywhere and not in magnitude, because warpax normalises its flux margin
  by a tetrad-dependent scale. Found on the first pass, which reported the combined difference and
  had to be rerun with the conditions separated.
- Result: the exact threshold is 0.09 to 0.10 times the compactness at every compactness, for each
  condition, the bracket Part 1 found by sampling; the paper's 0.02 passes for every observer with
  every margin at the finite-difference noise floor (1e-7 rho0). C4 and C5 closed. The failing cells
  are Type IV in warpax's census, in the inner wall at right angles to the shift, where the momentum
  density reaches half the energy density.
- Miss fraction of the sampled check: 5 % to 66 % of the violating cells at the first failing shift
  (worse at low compactness, where the violation is shallow), 1 to 5 % one step up, 0.1 % in deep
  violations. Adequate for the verdict on a case, not for counts or depths near the threshold.
- Correction to Part 1: the "factor two" by which 100 directions seemed to underestimate the depth
  was WarpFactory's k/sqrt 2 normalisation of its Null map against the dense check's k = (1, n). The
  real shortfall is 7 % at C = 1/3. Fixed in RESULTS section 4, CLAIMS C4 and the wiki (Findings 8
  and 10); note 07 stands as the log of what was believed on 26 October.
- Cost: 37 to 75 s per case alone on the laptop's 16 threads; six processes in parallel took about
  2.5 min per case each. One figure of the central plane (`exact_maps.png`) for the wiki, at Carlos's
  request for illustrations, and the margins figure (`exact_fine.png`).

Open after Part 2: the side-by-side figures (Part 3), the write-up, e-mails and the two upstream
issues (Part 4). warpax's native `FuchsMetric` remains an optional, separate comparison.
