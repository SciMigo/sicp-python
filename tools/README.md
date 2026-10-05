# Converted-module tools

Module 06 is the first lesson + visual-lab conversion. Other modules retain their legacy format. The course remains free.

The browser runtime and check/build tools were copied from the sibling algorithm-design course on 2026-10-04 and adapted to SICP. Vendored runtime notices are in preview/THIRD_PARTY_NOTICES.txt. Author lab files in lab_src; pack with ~/.codex/skills/scimigo-course-module/scripts/lab_src.py.

Python dependencies: straightedge 0.8.0, markdown, pymdown-extensions, latex2mathml (currently available in ../algorithm-design/.venv). Browser smoke: Playwright from ../scimigo-learn/node_modules.

```
../algorithm-design/.venv/bin/python tools/lessons.py check 06
../algorithm-design/.venv/bin/python tools/check_lab.py 06
../algorithm-design/.venv/bin/python tools/lessons.py build output/reading 06
python3 tools/build_preview_index.py
CHROMIUM_EXECUTABLE_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' node tools/preview_smoke.mjs 06-trees --all --out output/review/06-trees
python3 -m http.server 8768
```

Local lesson: /output/reading/06-trees.html; lab: /preview/?module=06-trees; optional background: /reading/06-trees.html. No publishing is performed by these commands. Site routing and public asset export are separate integration work.
