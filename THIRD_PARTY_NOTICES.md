# Third-party notices

This repository's own content is under the MIT licence in `LICENSE`. It builds on, quotes, or calls
the following works, which keep their own licences.

## WarpFactory (MIT)

https://github.com/NerdsWithAttitudes/WarpFactory

Copyright (c) 2023 Christopher Helmerich & Jared Fuchs. MIT License.

- `work/precision-probe/precision_probe.py` is a line-for-line port of `Solver/utils/*.m` to
  NumPy and is therefore a derivative work; the notice above applies to it.
- The scripts under `matlab/` call WarpFactory at run time (the CI job clones it); nothing from it
  is vendored here.
- Its authors ask that use of the code be cited: Helmerich et al., "Analyzing Warp Drive Spacetimes
  with Warp Factory", Class. Quantum Grav. 41, 095009 (2024), arXiv:2404.03095.

## warpax (MIT)

https://github.com/anindex/warpax

Copyright (c) 2026 An T. Le. MIT License.

- Used as a Python dependency (`pip install warpax`); nothing from it is vendored here.
- Cite: Le, "Observer-robust energy condition verification for warp drive spacetimes",
  arXiv:2602.18023; software archived at doi:10.5281/zenodo.18715933.

## Papers

Quoted in short extracts with citation, under ordinary quotation rights. The paper under test,
Fuchs et al. 2024 (arXiv:2405.02709), is published under CC BY 4.0, which permits reuse of its
figures with attribution; where we reproduce one of its figures for side-by-side comparison, the
caption says so. No paper text or PDF is redistributed from this repository; `INDEX.md` links the
canonical copies and `tools/fetch_sources.py` re-downloads them.
