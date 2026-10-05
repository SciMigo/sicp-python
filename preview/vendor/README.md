# Vendored: straightedge

`straightedge-0.8.0-py3-none-any.whl` is the SVG diagram library behind the lab's `figure()` call.

- Version: 0.8.0 (`straightedge.__version__`)
- Source: SciMigo/straightedge, commit `8cf9d5c17e6aaf15475c504213b689c829d1873f` (2026-09-08),
  built from a clean `git archive` of that commit (the local checkout had uncommitted changes,
  which are not in this wheel)
- SHA-256: `02800c90317fcd8dbb15aa68b84e29664cd031d25ebb088e66b98595cd5bddb2`
- Licence: MIT (text in `../THIRD_PARTY_NOTICES.txt`)

**Why it is vendored.** The lab runs learner code in Pyodide in the browser. `straightedge.diagrams`
is pure standard-library Python, so the worker installs it offline: it fetches this wheel from
the lab's own origin, unzips it onto `sys.path`, and imports it. That keeps the lab to one
third-party download (Pyodide itself), needs no `micropip` or package index, and pins the exact
templates the labs were checked against. `tools/check_lab.py` runs the same checks in CPython
against the straightedge installed in `.venv`; keep the two at the same version.

**Updating.** Build the wheel from the new commit and update the file name in
`preview/worker.js` (`STRAIGHTEDGE_WHEEL`) and this file:

```bash
git -C /path/to/straightedge archive HEAD | tar -x -C /tmp/straightedge-src
.venv/bin/pip wheel --no-deps -w preview/vendor /tmp/straightedge-src
```

Then run `tools/check_lab.py` and `tools/preview_smoke.mjs`.
