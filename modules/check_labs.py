#!/usr/bin/env python3
"""Check every lab in this directory: does each reference solution pass the
exercise's own tests?

Stdlib only, no dependencies:

    python3 modules/check_labs.py

Exits non-zero if any solution fails.

Solutions come in three shapes:

- Python, for implement/extend exercises. It must run and pass.
- prose, for predict/trace exercises ("it prints 2, because the instance
  attribute shadows the class attribute"). Correct content; skipped.
- broken code, which is the one to catch: an answer that opens a block or
  returns a value, so it was written to run, and does not parse. The usual
  cause is an explanatory sentence appended without a `#`, or a markdown
  code fence left around the answer — the fenced code trips the same
  markers. A learner who pastes it gets a SyntaxError.

  A fence is not itself a marker: a predict answer legitimately quotes
  expected OUTPUT in one, and flagging that would recreate the false
  positives this exists to remove.

Classifying by "does it compile" alone puts broken code in the prose bucket
and reports it as fine. That hid a defect in the published labs.
"""

from __future__ import annotations

import io
import json
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path


#: Markers that say an answer meant to run: it opens a block or returns a
#: value. A prose answer quotes code inline (`double(2)`) but does not do this.
CODE_MARKERS = re.compile(
    r"^\s*(def |class |import |from |return |for |while |if |elif |else:"
    r"|try:|except|with |@)",
    re.M,
)


def classify(source):
    """"python", "prose" or "broken_code"."""
    try:
        compile(source, "<solution>", "exec")
    except SyntaxError:
        return "broken_code" if CODE_MARKERS.search(source) else "prose"
    return "python"


def run_solution(solution, tests):
    """Exec the solution, then each test, in one shared namespace.

    A lab prints as it runs; that output is swallowed so it does not bury
    the report.
    """
    namespace = {"__name__": "__main__"}
    results = []
    with redirect_stdout(io.StringIO()):
        try:
            exec(compile(solution, "<solution>", "exec"), namespace)
        except BaseException as exc:
            return [("<solution did not load>", f"{type(exc).__name__}: {exc}")]
        for test in tests:
            name = test.get("name") or "<unnamed>"
            try:
                exec(compile(test.get("code") or "", f"<{name}>", "exec"), namespace)
                results.append((name, None))
            except BaseException as exc:
                results.append((name, f"{type(exc).__name__}: {exc}"))
    return results


def main():
    modules_dir = Path(__file__).resolve().parent
    failed = prose = passed = 0

    for path in sorted(modules_dir.glob("*/lab*.json")):
        spec = json.loads(path.read_text(encoding="utf-8"))
        label = (path.parent.name if path.name == "lab.json"
                 else f"{path.parent.name}/{path.name}")
        for exercise in spec.get("exercises", []):
            ex_id = exercise.get("exercise_id", "?")
            solution = exercise.get("solution") or ""
            tests = exercise.get("tests") or []
            if not solution:
                print(f"NO SOLUTION  {label}/{ex_id}")
                failed += 1
                continue
            kind = classify(solution)
            if kind == "prose":
                prose += 1
                continue
            if kind == "broken_code":
                failed += 1
                print(f"BROKEN  {label}/{ex_id}")
                print("          solution reads as Python but does not parse "
                      "— a learner who pastes it gets a SyntaxError")
                continue
            results = run_solution(solution, tests)
            bad = [(n, e) for n, e in results if e]
            if bad:
                failed += 1
                print(f"FAIL  {label}/{ex_id}")
                for name, error in bad:
                    print(f"          {name}: {error}")
            else:
                passed += 1
                print(f"ok    {label}/{ex_id}  {len(results)}/{len(results)} tests")

    print(f"\n{passed} solutions pass, {failed} fail, "
          f"{prose} answered in prose (skipped)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
