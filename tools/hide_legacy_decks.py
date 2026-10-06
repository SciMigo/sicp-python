"""Prepare a manifest-only retirement, preserving live labs; never uploads assets.

python3 tools/hide_legacy_decks.py LIVE_MANIFEST OUTPUT_DIRECTORY
Upload OUTPUT_DIRECTORY/sicp-python/ to that course's CDN prefix after review.
The small lab pages keep lab access working on the currently deployed viewer.
"""
import datetime
import html
import json
import pathlib
import sys

source = json.loads(pathlib.Path(sys.argv[1]).read_text())
assert source['id'] == 'sicp-python', 'Expected SICP manifest'
out = pathlib.Path(sys.argv[2]) / source['id']
(out / 'reading').mkdir(parents=True, exist_ok=True)
for module in source['modules']:
    lab_id = module.get('labId') or module.get('deckId')
    if module.get('hasLab'):
        assert lab_id, f"Missing lab bundle for {module['id']}"
        module['labId'] = lab_id
        title = html.escape(module['title'])
        page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} lab</title></head><body><h1>{title} lab</h1><p>Run the Python exercises in your browser.</p><p><a href="/labs/{html.escape(lab_id, quote=True)}">Open the interactive lab</a></p></body></html>'''
        (out / 'reading' / f"lab-{module['id']}.html").write_text(page)
    module['hasDeck'] = False
    module.pop('deckId', None)
    module.pop('videoUrl', None)
source.pop('estimatedTotalHours', None)
source['overview'] = 'Study selected ideas from SICP in Python through readings and hands-on exercises. The existing slides and voice narration are withdrawn while the modules are rebuilt as focused lessons and visual labs. The original readings remain available as background. This independent course is free.'
source['generatedAt'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
(out / 'course-manifest.json').write_text(json.dumps(source, indent=2)+'\n')
print(f"Prepared {len(source['modules'])} hidden decks; reading and lab flags preserved at {out}")
