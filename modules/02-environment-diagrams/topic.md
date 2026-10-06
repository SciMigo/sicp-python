# Environment diagrams: author plan

Seven beats: surprising lexical lookup; naive caller lookup; trace definition-linked frames; nearest-owner invariant; explicit frame model and actual Python cells; counted membership tests; deferred badge callbacks.
Lesson instance: calibration offsets 8 and 60, input 5; mutable register starts 12. Lab instances: lexical offset 6 versus caller 80; box starts 20; badge prefixes 4 and 9.
Five exercises: Build nearest-binding lookup with recorded visited scopes; Trace bind arguments with definition parent; Implement shared update/read/reset behavior with independent factories; Measure actual membership probes; Mastery configure deferred badge callbacks without late binding.
Count membership tests in a deliberately explicit finite acyclic dictionary-frame model. This is not a measurement of CPython's optimized variable access. Dictionary probes are an educational unit, not elapsed time.
Mastery tell: behavior must remain distinct after setup finishes and after the caller changes its input list. No technique named in prompt. State, not speed, defeats the naive starter.

Scope: ordinary nested functions, globals, parameters, closures and nonlocal. No class, comprehension, annotation-scope or exec model. Explain UnboundLocalError rather than claiming every Python read searches dictionaries dynamically. Cells can outlive a call; no claim that closures retain whole execution frames. Model inputs have existing valid parents and no cycles; misses raise NameError. Python builtins excluded from the lab model explicitly.

Sources checked 2026-10-05: Python language reference https://docs.python.org/3/reference/executionmodel.html (binding/scope and local-before-assignment rules); https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement (nearest enclosing function binding); https://docs.python.org/3/reference/datamodel.html#user-defined-functions (closure cells). Original prose/examples are independent of the SICP source chapter. Diagrams are semantic aids, not memory layouts.
Oral anchors: identify owner of each name; why caller does not supply free variables; distinguish shared cells within a factory from fresh cells across factories; explain why membership must distinguish None from absence; predict late binding and distinguish default-argument capture.
