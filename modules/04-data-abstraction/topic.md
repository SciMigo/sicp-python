# Data abstraction — module plan, 2026-10-06

Base: merged main 5f8554a, including Claude review fixes. Owner rules: keep SICP examples/exercises in Python; book text separate; Build/Implement stubs run and draw one frame; no lesson lab answer or mastery teaser; tailored hints; every assert has a message; all untouched checklist checks fail except mastery correctness; estimates use 200 words/minute plus per-exercise work.

Seven beats: rational arithmetic problem; raw tuple representation; interface dependency and midpoint figures; ratio and pair laws; representations, numeric dispatch and interval implementation; construction versus selection gcd counts; map units teaser, distinct from the shipping mastery. Book source: local reference/2.1-data-abstraction.md §§2.1.1–2.1.4. No new real-software claims requiring external documentation. Keep the book's material, not its copied prose.

Lesson examples: book fractions 1/2 and 1/3, midpoint (1,2)..(5,8), numeric pair requests, interval [-2,3] times [4,5]. Lab examples differ: signed fractions, callable rectangle dimensions, function-choice pairs (exercise 2.4), selected counts 3/7/12, shipping records. Signed normalization and function-choice implementation are not solved in the lesson.

Five labs: make_rat (2.1), rectangle_report (2.3), cons (2.4), actual gcd-call measurement, manifest_report. Measure excludes drawing and counts actual wrapped gcd invocations, not internal gcd work or time. Mastery uses opaque records with at most one weight read each, first-tie semantics and varied packages. Small inputs all run/draw; report correctness passes on the deliberately over-budget mastery starter.

Correctness boundaries: integers/nonzero denominators; rectangle nonnegative finite dimensions; pair selectors preserve object identity; old tuple values do not become compatible with dictionary selectors merely by replacement. Simple interval arithmetic does not track repeated-variable dependence. Constructor positive-only reduction is expressly weaker than lab signed normalization.

Oral anchors: value equality versus raw-part equality; indexing is correct inside a representation implementation and wrong above its interface; closure versus selection time; representation independence does not erase migration; eager/lazy cost depends on uses.

Publication: add 04 to publisher PREVIEW_MODULES and registry sicpModule entry only when the reviewed module is ready. These are separate deployment changes; do not restore lectures or change the remaining old modules. Book reference host/CC notices across the old readings and course-wide tutor concepts remain separate work.
