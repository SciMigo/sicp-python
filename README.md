# SICP Python

Content repository for the **Structure and Interpretation of Computer Programs (Python)** course.

## Overview

This repo contains course content for generating interactive video lectures:
- Reading materials (HTML)
- Module definitions (topic, outline, labs)
- Reference materials for LLM context
- Branding assets

**This is a content-only repo.** Generation and viewing happen in separate repos:
- [mini_lecture](https://github.com/scimigo/mini_lecture) — Generation pipeline
- [scimigo-learn](https://github.com/scimigo/scimigo-learn) — Viewer application

## Course Structure

| Module | Title | Duration |
|--------|-------|----------|
| 01 | Higher-Order Functions | 45 min |
| 02 | Environment Diagrams | 30 min |
| 03 | Recursive Functions | 40 min |
| 04 | Data Abstraction | 50 min |
| 05 | Sequences | 45 min |
| 06 | Trees | 40 min |
| 07 | Mutable Data | 35 min |
| 08 | Object-Oriented Programming | 60 min |
| 09 | Interpreters | 90 min |

## Directory Structure

```
sicp-python/
├── course.json          # Course metadata
├── branding/            # Cover images, promo copy
├── reading/             # User-facing reading materials (HTML)
├── modules/             # Per-module generation config
│   └── <module-id>/
│       ├── module.json  # Module metadata
│       ├── topic.md     # Topic description for LLM
│       └── outline.md   # Slide outline
└── reference/           # LLM context (not user-facing)
```

## Generating Lectures

```bash
cd ~/src/mini_lecture
source .venv/bin/activate

python cli/run_curriculum_agent.py \
  --content-repo ~/src/sicp-python \
  --output-dir output/sicp-python
```

## Attribution

Based on *Structure and Interpretation of Computer Programs* by Harold Abelson and Gerald Jay Sussman (MIT Press, 1996), adapted to Python following UC Berkeley CS 61A.

## License

Content is provided for educational purposes. See course.json for attribution requirements.
