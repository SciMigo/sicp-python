# SICP module authoring

These owner requirements apply to rebuilt lesson + visual-lab modules. Use the merged, reviewed main branch, not an older conversion branch. Modules 1, 2, 3 and 6 establish the pattern.

- Keep SICP's own examples and exercises, rewritten in Python, with accurate section and exercise attribution. Write the teaching prose for this course; keep the book text as a separate reference link. Credit Abelson and Gerald Jay Sussman with Julie Sussman and identify translations/changes and the applicable share-alike licence.
- Build and Implement starters are stubs that execute, draw one frame and fail. Do not provide a completed function with a pre-broken line and a marker comment.
- The lesson must not print a lab answer or completed exercise solution. Use different worked instances; its transfer teaser must differ from the mastery problem.
- Write hints individually for each exercise. Every assert carries an explanatory message. Every checklist check fails on the untouched starter, except deliberate mastery correctness checks when a correct starter exceeds an operation budget.
- Count actual operations rather than wall-clock time; test varied inputs and stored frame data. Check lazy/wrong approaches explicitly. Do not treat educational tests as an anti-cheating boundary.
- Estimate the lesson at 200 prose words/minute plus code/figure study, then estimate each exercise. Mark estimates unmeasured. Keep the course free.
- Run lesson/lab/packing checks and Chrome smoke for every exercise. Review every generated figure and screenshot, including phone and dark-theme rendering.
- Work one module at a time and commit it separately. Do not restore slides or narration.

## Publication

1. Add the module id to PREVIEW_MODULES in scimigo-platform's publish-sicp-python.sh and run the publisher from the reviewed content revision.
2. Replace the module's SICP_SERIES entry in scimigo-learn with sicpModule(...), matching its metadata and prerequisites.
3. Merge the viewer change to deploy after the assets exist. Preserve the course's unlisted status until its relisting conditions are satisfied.

The old publication/ manifest workflow is unused by the registry-based course. The book-text CC notices, reference-link hosting and course-wide tutor concepts are separate outstanding work; a module conversion does not claim to complete them.
