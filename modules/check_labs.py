#!/usr/bin/env python3
"""Check every lab in this directory: does each reference solution pass the
exercise's own tests?

Stdlib only, no dependencies:

    python3 modules/check_labs.py

Exits non-zero if any solution fails.

Solutions come in two shapes. Implement/extend exercises are answered in
Python and must run and pass. Predict/trace exercises are answered in prose,
which is not code; those are reported as "prose" and skipped. That is correct
content, not a gap.
"""

from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path


def is_python(source):
    try:
        compile(source, "<solution>", "exec")
    except SyntaxError:
        return False
    return True


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
            if not is_python(solution):
                prose += 1
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
