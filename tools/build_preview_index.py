"""Write modules/index.json, the browser lab's module list.

python3 tools/build_preview_index.py

Lists, in course.json `modules` order, every module that has a modules/<id>/lab.json, with the
labels the lab shows. A module that also has modules/<id>/preview.js is marked "panels": true so
the lab loads it. Rerun after adding or removing a lab.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def entry(module_id):
    meta = json.loads((ROOT / "modules" / module_id / "module.json").read_text(encoding="utf-8"))
    number = int(module_id[:2])
    title = meta["title"]
    # Lectures are numbered; checkpoints and the capstone (26-29) go by their title.
    label = title if number > 25 else f"{number} · {title}"
    item = {
        "id": module_id,
        "label": label,
        "eyebrow": (title if number > 25 else f"MODULE {number:02d} · {title}").upper(),
        "heading": meta.get("subtitle") or title,
        "subtitle": meta.get("description", ""),
    }
    if (ROOT / "modules" / module_id / "preview.js").exists():
        item["panels"] = True
    return item


def main():
    course = json.loads((ROOT / "course.json").read_text(encoding="utf-8"))
    items = [entry(mid) for mid in course["modules"] if (ROOT / "modules" / mid / "lesson.md").exists()]
    out = ROOT / "modules" / "index.json"
    out.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{out.relative_to(ROOT)}: {len(items)} module(s)")


if __name__ == "__main__":
    main()
