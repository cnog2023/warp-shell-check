# warp-research

A local research archive and workbench for one question:

> Does the "constant velocity physical warp drive" shell of Fuchs et al. (2024), as built by
> WarpFactory, consist of the ordinary matter the paper says it does, and does that hold up under
> the February 2026 critique by Barzegar, Buchert and Vigneron and under warpax's observer-robust
> energy-condition tests?

Started 18 October 2026 by Carlos Nogueira with Claude. Nothing here is affiliated with Applied
Physics, with the critique's authors, or with the warpax project.

## Layout

| Path | What it holds |
|---|---|
| `INDEX.md` | The annotated index of every source: what it is, where it is, why it matters. Start here |
| `PLAN.md` | The step-by-step plan for the reproduction and consistency check, with gates |
| `CLAIMS.md` | The claim register: each claim under test, its source, the test, the pass/fail rule |
| `sources/papers/` | The papers as PDF, named `YEAR_firstauthor_topic_ARXIVID.pdf`; `MANIFEST.tsv` lists them with the title arXiv states |
| `sources/papers-text/` | Tag-stripped text of the same papers, for grep. Derived copies, not for redistribution |
| `sources/web/` | Saved web pages (toolkit docs, repositories, licensing notes), each with its URL and retrieval date |
| `repos/WarpFactory/` | Shallow clone of the MATLAB toolkit (MIT) |
| `repos/warpax/` | Shallow clone of the JAX toolkit (MIT) |
| `work/` | Our own computations. Each sub-folder has its own README or RESULTS file |

`sources/` and `repos/` are local-only and excluded from git: they are other people's work, and the
index links to the canonical copies. Everything under `work/` and the three top-level documents are
ours and are versioned.

## Conventions

- Every number quoted in a document carries the file and location it came from.
- A claim is quoted, never paraphrased, before it is tested.
- Every computation is reproducible from this folder with the commands in its README.
