# warp-shell-check

An independent reproduction and consistency check of the "constant velocity physical warp drive"
shell of Fuchs et al. (2024), using the authors' own toolkit (WarpFactory, MATLAB) and an
independent one (warpax, JAX), written up so that anyone can rerun it.

> Does the matter that the shell's metric actually requires match what the paper says the shell is
> made of, and does the construction hold up under the February 2026 critique by Barzegar, Buchert
> and Vigneron and under observer-robust energy-condition tests?

Started 18 October 2026 by Carlos Nogueira with Claude. Not affiliated with Applied Physics, with
the critique's authors, or with the warpax project. GitHub: `cnog2023/warp-shell-check`. The local
working folder is called `warp-research`; the two names refer to the same repository.

## Layout

| Path | What it holds |
|---|---|
| `INDEX.md` | The annotated index of every source: what it is, where it is, why it matters. Start here |
| `PLAN.md` | The step-by-step plan for the reproduction and consistency check, with gates |
| `CLAIMS.md` | The claim register: each claim under test, its source, the test, the pass or fail rule |
| `CLAUDE.md` | Standing instructions for the AI sessions that do the computing and drafting |
| `sources/papers/` | The papers as PDF, named `YEAR_firstauthor_topic_ARXIVID.pdf`; `MANIFEST.tsv` lists them with the title arXiv states. Not committed; `tools/fetch_sources.py` rebuilds the folder |
| `sources/papers-text/` | Tag-stripped text of the same papers, for grep. Not committed |
| `sources/web/` | Saved web pages (toolkit docs, repositories, licensing notes), each with its URL and retrieval date. Not committed |
| `repos/WarpFactory/`, `repos/warpax/` | Shallow clones of the two toolkits (both MIT). Not committed |
| `matlab/` | MATLAB scripts run against WarpFactory by the CI job in `.github/workflows/matlab.yml`. MathWorks licenses MATLAB free on GitHub-hosted runners for public repositories |
| `tools/` | Helper scripts, starting with `fetch_sources.py` |
| `work/` | Our own computations. Each sub-folder has its own README or RESULTS file |

## Reproduce

```
git clone https://github.com/cnog2023/warp-shell-check
cd warp-shell-check
python -m venv .venv
.venv\Scripts\python -m pip install numpy matplotlib warpax
.venv\Scripts\python tools\fetch_sources.py
.venv\Scripts\python work\precision-probe\precision_probe.py work\precision-probe\precision_probe.png
```

The MATLAB half runs in GitHub Actions on every push that touches `matlab/`; the job's log and its
`results/smoke` artifact hold the numbers.

## Conventions

- Every number quoted in a document carries the file and location it came from.
- A claim is quoted, never paraphrased, before it is tested.
- Every computation is reproducible from this folder with the commands in its README.
- Licences: ours is MIT (`LICENSE`); for everything we build on see `THIRD_PARTY_NOTICES.md`.
