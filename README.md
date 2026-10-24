# IDE Guide Content Generator & Agentic Skills

This repository powers content generation for [IDE Guide Blogger](https://ideguide.blogspot.com/) and [IDE Guide YouTube Channel (@IDEguide)](https://www.youtube.com/@IDEguide).

## Overview

The toolset automatically generates 3 AMP HTML blog posts and 3 Google Flow video specifications every day. Each review covers different code editors and IDEs (e.g., VS Code, Cursor, Zed, PyCharm, Neovim, JetBrains Fleet, WebStorm, Windsurf, Lapce), assessing pros, cons, pricing (free/paid), and ideal target developer personas.

All generated content strictly includes our mandatory non-sponsorship disclosure:
> *Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.*

---

## Directory Structure

```
.
├── docs/
│   ├── amp_blogger_guidelines.md      # AMP HTML requirements & Blogger compatibility rules
│   └── google_flow_spec_guidelines.md # Video prompt structure & Google Flow video generation specs
├── scripts/
│   ├── amp_validator.py              # AMP HTML validation engine
│   ├── generate_daily_content.py     # Main generator (3 posts & 3 video specs per day)
│   └── ide_guide_agent_skill.py      # Agentic CLI tool for custom IDE/Repo content generation
├── content/
│   ├── history.json                  # Tracks covered IDEs to prevent duplicate coverage
│   └── YYYY-MM-DD/                   # Daily generated AMP blog posts and Google Flow video specs
├── .github/workflows/
│   └── daily_content_generation.yml  # Daily automated workflow (runs at 21:30 UTC / 03:00 AM IST)
└── tests/
    └── test_content.py               # Unit test suite
```

---

## Agentic Skill Usage (CLI)

To generate custom AMP HTML blog posts and Google Flow video specifications on demand for any IDE or GitHub repository:

```bash
# Generate content for a specific IDE
PYTHONPATH=. python3 scripts/ide_guide_agent_skill.py --target "Zed Editor" --output-dir ./custom_output

# Generate content for a GitHub Repository
PYTHONPATH=. python3 scripts/ide_guide_agent_skill.py --target "https://github.com/helix-editor/helix" --output-dir ./custom_output
```

---

## Daily Automated Workflow

Run the daily generator manually at any time:

```bash
PYTHONPATH=. python3 scripts/generate_daily_content.py
```

This will:
1. Pick 3 IDEs from the database that haven't been reviewed recently.
2. Generate 3 AMP-compliant HTML blog files in `content/YYYY-MM-DD/`.
3. Generate 3 Google Flow video specification JSON files in `content/YYYY-MM-DD/`.
4. Update `content/history.json`.

---

## Validating AMP HTML

To validate any generated blog post against AMP standards:

```bash
python3 scripts/amp_validator.py content/2026-10-24/post_1_vs-code_amp.html
```

---

## Testing

Run the automated test suite with PyTest:

```bash
PYTHONPATH=. pytest tests/
```
