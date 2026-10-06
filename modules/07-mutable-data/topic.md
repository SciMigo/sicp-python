# Mutable Data: authoring and review notes

Branch from reviewed main; one module per PR. The public lesson uses the book's withdrawal, decrementer and z1/z2 sharing examples. Labs use different histories and pair values. Scope: 3.1.1–3.1.3 and mutable pairs in 3.3.1; leave queue/table/circuit/constraint machinery out.

Five labs: accumulator plus monitor (3.1/3.2), destructive append (3.12), protected account (3.3), actual counted field function passed to traversal (3.16/3.17), connected service access (3.7). Measure receives fields explicitly; no globals replacement. Every solution replays state changes. All starters are runnable stubs, not pre-broken solutions. Mastery adds an explicit non-mutating check request; reserved monitor commands cannot be worker arguments. Sequential integer teaching models, no security/concurrency claim.

Primary sources: repo reference/3.1-assignment-local-state.md and reference/3.3-mutable-data.md, separate original reading. Python docs checked 2026-10-06: https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement and https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects . Language behavior used is supported by Pyodide's older Python too.

Oral anchors: constructor calls create independent bindings; aliases retain same closure. Copy outer then mutate inner exposes retained identity. Mark before expanding avoids cyclic recursion; equal contents can belong to distinct objects. No lesson code implements accumulator, monitor, password dispatch or joint access. Measurement table is computed recurrence, not experimental evidence.
