# CLAUDE.md - sicp-python

Content repository for the "Structure and Interpretation of Computer Programs (Python)" course.

## Repository Purpose

This repo contains **course content only** — reading materials, module definitions, lab exercises, and branding assets. It does NOT contain generation code or viewer application code.

**Related repositories:**
| Repo | Purpose |
|------|---------|
| `mini_lecture` | Generation pipeline — takes this content repo as input, produces video lectures, slides, audio |
| `scimigo-learn` | Viewer application — user-facing web app that displays the generated content |

## Directory Structure

```
sicp-python/
├── course.json              # Course-level metadata (title, description, prerequisites, etc.)
├── CLAUDE.md                # This file
│
├── branding/                # Visual assets
│   ├── cover.png            # Course cover image (1280x720)
│   ├── thumbnail.png        # Thumbnail for listings (400x225)
│   └── promo.md             # Marketing copy, taglines
│
├── reading/                 # User-facing reading materials (HTML)
│   ├── 01-higher-order-functions.html
│   ├── 02-environment-diagrams.html
│   └── ...
│
├── modules/                 # Per-module generation configuration
│   ├── 01-higher-order-functions/
│   │   ├── module.json      # Module metadata (title, duration, prereqs)
│   │   ├── topic.md         # Topic description for LLM context
│   │   ├── outline.md       # Slide-by-slide outline
│   │   └── lab.json         # Full lab: prompts, starter code, tests,
│   │                        # hints, solutions (see modules/LABS.md)
│   └── ...
│
└── reference/               # LLM context materials (not user-facing)
    ├── 1.3-higher-order-procedures.md
    └── ...
```

## Generating Content

To generate lectures from this content repo:

```bash
cd ~/src/mini_lecture
source .venv/bin/activate

# Generate all modules
python cli/run_curriculum_agent.py \
  --content-repo ~/src/sicp-python \
  --output-dir output/sicp-python

# Generate single module
python cli/run_curriculum_agent.py \
  --content-repo ~/src/sicp-python \
  --filter 01-higher-order-functions \
  --output-dir output/sicp-python

# Spec-only (fast iteration)
python cli/run_curriculum_agent.py \
  --content-repo ~/src/sicp-python \
  --spec-only \
  --output-dir output/sicp-python
```

## Module Configuration

Each module in `modules/<id>/` contains:

### module.json
```json
{
  "id": "01-higher-order-functions",
  "title": "Higher-Order Functions",
  "subtitle": "Functions as first-class values, closures, and the summation abstraction",
  "chapter": "1.6",
  "estimatedMinutes": 45,
  "prerequisites": [],
  "targetSeconds": 420,
  "referenceFiles": ["1.3-higher-order-procedures.md"],
  "labExercises": ["1.29", "1.31", "1.34"],
  "diagramTemplates": ["function_graph", "environment_diagram"],
  "interactionCheckpoints": 2
}
```

### topic.md
LLM context describing the topic, key concepts, and examples to cover.

### outline.md
Slide-by-slide outline with specific content for each slide.

### lab.json
The full lab a learner works through: prompt, starter code, assert-based tests,
hints and a reference solution, in the engine's `lab_v1` schema. Schema,
provenance and known defects: [modules/LABS.md](modules/LABS.md).

Note `module.json`'s `lab.exercises` is only a *hint* to the generator, not a
description of this file — the two have drifted. `lab.json` is authoritative.

## Adding a New Module

1. Create directory: `modules/<id>/`
2. Add `module.json` with metadata
3. Add `topic.md` with topic description
4. Add `outline.md` with slide outline
5. (Optional) Add `lab.json` for exercises
6. Add reading material to `reading/<id>.html`
7. Update `modules` array in `course.json`

## Content Guidelines

- **Reading materials**: Self-contained HTML with embedded styles. Should work offline.
- **Topic descriptions**: Focus on "what to teach" not "how to present" — the LLM decides presentation.
- **Outlines**: Specific enough to guide structure, flexible enough for LLM creativity.
- **Labs**: Executable in Pyodide (browser Python). Avoid dependencies beyond stdlib.

## Deployment

Generated content is deployed to Cloudflare CDN:
- Base URL: `https://cdn.scimigo.com/courses/sicp-python/`
- Module bundles: `https://cdn.scimigo.com/courses/sicp-python/<module-id>/`

The viewer app (`scimigo-learn`) fetches content from this CDN at runtime.
