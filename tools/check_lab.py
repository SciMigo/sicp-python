"""Check every browser lab (modules/*/lab.json) against the lab's own Python bridge.

.venv/bin/python tools/check_lab.py [module-id-prefix ...]

Runs in CPython with preview/scimigo_bridge.py, the file the browser worker runs, so figure(),
frame() and the check hooks behave as they do for the learner (straightedge must be importable,
as it is in .venv). For each lab:
  - lab_v1 shape: lab_spec_id, recap, exercise fields, checklist and questions well formed;
  - every exercise's solution (in lab.json, or in lab_solutions.json beside it) passes every test,
    each within runtime.timeout_ms / 3;
  - the starter code runs without error and fails at least one test;
  - no published text mentions a rubric or says "tutor only".
"""

import json
import pathlib
import re
import signal
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "preview"))
import scimigo_bridge as bridge  # noqa: E402

LEAK = re.compile(r"rubric|tutor[ -]only", re.I)
EXERCISE_FIELDS = {"exercise_id": str, "title": str, "prompt_md": str, "starter_code": str,
                   "tests": list, "hints": list}


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout


def run_tests_bounded(source, tests, fixtures, seconds):
    """bridge.run_tests with a hard stop, so a looping program cannot hang the check."""
    signal.signal(signal.SIGALRM, _alarm)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        return bridge.run_tests(source, tests, fixtures)
    except Timeout:
        return [{"name": test["name"], "passed": False, "error": f"stopped after {seconds:.0f}s", "ms": seconds * 1000}
                for test in tests]
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def check_shape(lab, module_id, problems):
    def need(condition, message):
        if not condition:
            problems.append(message)
        return condition

    need(lab.get("schema_version") == "lab_v1", "schema_version is not lab_v1")
    need(lab.get("lab_spec_id") == f"sicp-python-{module_id}",
         f"lab_spec_id is {lab.get('lab_spec_id')!r}, expected 'sicp-python-{module_id}'")
    need(isinstance(lab.get("runtime", {}).get("timeout_ms"), int), "runtime.timeout_ms missing")
    recap = lab.get("recap")
    if need(isinstance(recap, dict), "no recap"):
        for part in ("learned", "in_real_programs"):
            items = recap.get(part)
            need(isinstance(items, list) and items and all(isinstance(i, str) and i for i in items),
                 f"recap.{part} must be a non-empty list of sentences")
        for part in ("invariant", "complexity", "common_mistake"):
            need(isinstance(recap.get(part), str) and recap[part], f"recap.{part} missing")
        retrieval = recap.get("retrieval")
        need(isinstance(retrieval, dict) and retrieval.get("question") and retrieval.get("answer"),
             "recap.retrieval needs question and answer")
    exercises = lab.get("exercises")
    if not need(isinstance(exercises, list) and exercises, "no exercises"):
        return
    ids = [exercise.get("exercise_id") for exercise in exercises]
    need(len(ids) == len(set(ids)), "duplicate exercise ids")
    for exercise in exercises:
        eid = exercise.get("exercise_id", "?")
        for field, kind in EXERCISE_FIELDS.items():
            need(isinstance(exercise.get(field), kind), f"{eid}: {field} missing or not a {kind.__name__}")
        tests = exercise.get("tests") or []
        need(tests and all(isinstance(t.get("name"), str) and isinstance(t.get("code"), str) for t in tests),
             f"{eid}: tests need name and code")
        names = [t.get("name") for t in tests]
        need(len(names) == len(set(names)), f"{eid}: duplicate test names")
        need(exercise.get("hints"), f"{eid}: no hints")
        if "checklist" in exercise:
            steps = exercise["checklist"]
            named = [name for step in steps for name in step.get("checks", [])]
            need(all(step.get("step") and step.get("checks") for step in steps), f"{eid}: empty checklist step")
            need(len(named) == len(set(named)), f"{eid}: a check is named by more than one step")
            need(set(named) == set(names), f"{eid}: checklist and tests differ: {sorted(set(named) ^ set(names))}")
        for index, question in enumerate(exercise.get("questions", [])):
            choices = question.get("choices", [])
            need(question.get("step") and question.get("prompt"), f"{eid}: question {index + 1} needs step and prompt")
            need(len(choices) >= 2 and all(c.get("text") and c.get("why") for c in choices),
                 f"{eid}: question {index + 1} needs two or more choices, each with text and why")
            need(question.get("answer") in range(len(choices)), f"{eid}: question {index + 1} answer index out of range")


def check_lab(lab_path):
    module_id = lab_path.parent.name
    raw = lab_path.read_text(encoding="utf-8")
    lab = json.loads(raw)
    problems = []
    check_shape(lab, module_id, problems)
    if LEAK.search(raw):
        problems.append("published lab text mentions a rubric or 'tutor only'")
    solutions_path = lab_path.parent / "lab_solutions.json"
    solutions = json.loads(solutions_path.read_text(encoding="utf-8")) if solutions_path.exists() else {}
    timeout = lab.get("runtime", {}).get("timeout_ms", 5000) / 1000
    fixtures = lab.get("fixtures", [])
    tests_run = 0
    for exercise in lab.get("exercises", []):
        eid = exercise.get("exercise_id", "?")
        tests = exercise.get("tests") or []
        solution = exercise.get("solution", solutions.get(eid))
        if not isinstance(solution, str):
            problems.append(f"{eid}: no solution (in lab.json or lab_solutions.json)")
            continue
        for result in run_tests_bounded(solution, tests, fixtures, 2 * timeout):
            tests_run += 1
            if not result["passed"]:
                problems.append(f"{eid}: solution fails {result['name']}: {result['error'] or 'AssertionError'}")
            elif result["ms"] > timeout * 1000 / 3:
                problems.append(f"{eid}: {result['name']} takes {result['ms']:.0f} ms (> timeout_ms/3)")
        starter = exercise.get("starter_code", "")
        outcome = bridge.run_program(starter, fixtures)
        if outcome["error"]:
            problems.append(f"{eid}: starter raises: {outcome['error'].strip().splitlines()[-1]}")
        if tests and all(r["passed"] for r in run_tests_bounded(starter, tests, fixtures, 2 * timeout)):
            problems.append(f"{eid}: starter already passes every test")
    return module_id, len(lab.get("exercises", [])), tests_run, problems


def main(prefixes):
    paths = sorted(p for p in (ROOT / "modules").glob("*/lab.json") if (p.parent / "lesson.md").exists())
    if prefixes:
        paths = [p for p in paths if p.parent.name.startswith(tuple(prefixes))]
    if not paths:
        print("No labs found")
        return 1
    failed = 0
    for path in paths:
        module_id, exercises, tests, problems = check_lab(path)
        print(f"{'FAIL' if problems else 'ok  '} {module_id}: {exercises} exercises, {tests} solution checks")
        for problem in problems:
            print(f"     - {problem}")
        failed += bool(problems)
    print(f"{len(paths) - failed} of {len(paths)} lab(s) pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
