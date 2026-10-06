# Module 04 review — 2026-10-06

Checked local draft; publication pending. Based on reviewed merged main 5f8554a.

## Scope

1814 prose words, seven executable Python blocks, two semantic figures. Follows SICP §§2.1.1–2.1.4: rational arithmetic, reduction, representation boundaries, laws, points and segments, procedural pairs, normalization placement, intervals and repeated-variable dependence. Lab covers exercises 2.1, 2.3 and 2.4, measured gcd calls and a distinct shipping task. The public lesson does not solve signed normalization or the function-choice pair, does not print lab demo answers and uses a map-units teaser separate from shipping mastery. New lesson carries credit, a changes statement and CC BY-SA 4.0 notice. Original book text remains optional reference.

## Verification

- Seven lesson blocks and two figures pass; lab packing is current.
- Ten solution checks pass. All five starters run and draw; every check fails on untouched code except deliberately correct-but-over-budget mastery behavior (nine red of ten). Every Python assert has a message.
- Mutation probes reject missing reduction, direct rectangle indexing, reversed pair parts, inferred rather than counted gcd calls, and replacing the first maximum with a later tie.
- Cases include both denominator signs, zero numerator, zero-denominator rejection, seeded fractions, alternate rectangle packages, identity-preserving pair selection, independent captured pairs, actual helper-call counts and restoration after exceptions, empty manifests, zero weights, ties, alternate layouts, input preservation and 500 opaque records.
- Chrome/Pyodide smoke passes all five exercises, playback, questions, mastery unlock, embedded sizing and host/example integration; no page errors. Real Pyodide 0.27.4 was cached locally for this draft; no external-CDN claim for Module 4.
- Inspected all sixteen smoke images and both lesson figures. Phone labels are readable; diagrams explicitly distinguish dependencies from recursive calls and coordinate lists from scaled geometry.
- Layout checked at 1366/390 pixels in light and dark, with no horizontal overflow. Body contrast 16.74/15.26; phone starter runs and shows the editable function first.

## Estimate and limits

20–25-minute lesson (200 words/minute plus code/figures), five labs at 10, 10, 10, 15 and 15 minutes; 80–85 total, unmeasured. Arithmetic and gcd calls are not claimed to have fixed bit cost. Replacing a selector package does not migrate old stored values. The interval example does not track dependence. Educational checks are not secure anti-cheating. Course-wide concepts/tutor tags, all old-reading licence notices, raw reference-link hosting and publication cleanup remain separate work. Module 4 has not been published; publisher and viewer registration must follow content review.

Evidence: output/review/04-data-abstraction/.
