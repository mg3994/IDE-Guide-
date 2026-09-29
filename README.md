# IDE Guide Content Generator & Agentic Skills

Automated AMP HTML blog post generation for **Blogger** (`https://ideguide.blogspot.com/`) and Google Flow AI video prompt specification generator for **YouTube** (`https://www.youtube.com/@IDEguide`).

## Overview

**IDE Guide** publishes 3 daily reviews of IDEs and code editors across YouTube and Blogger:
1. **AMP HTML Blog Posts:** Compliant with Google AMP standards, optimized for Blogger embedding, mobile loading speed, and modern styling.
2. **Google Flow Video Specifications:** Detailed multi-scene prompts, timing breakdowns, visual camera instructions, voiceover transcripts, audio cues, and free vs paid breakdowns designed for Google Flow and AI video tools.
3. **Agentic Skills CLI:** On-demand content generator for single IDEs, custom editors, or repository URLs.
4. **Independent & Unbiased:** Every post and video spec automatically embeds the mandatory non-sponsorship disclosure statement.

---

## Channels & Links

- **Blogger Website:** [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- **YouTube Channel:** [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)

---

## Directory Structure

```text
├── .github/workflows/
│   └── daily_content_generation.yml  # Daily GitHub Actions schedule (21:30 UTC / 03:00 AM IST)
├── docs/
│   ├── amp_blogger_guidelines.md      # AMP HTML compliance guidelines for Blogger
│   └── google_flow_spec_guidelines.md # Video prompt structure & camera guidelines for Google Flow
├── scripts/
│   ├── amp_validator.py              # Custom AMP HTML validation engine
│   ├── generate_daily_content.py     # Main daily generation script (3 posts & 3 video specs)
│   └── ide_guide_agent_skill.py      # Agentic CLI skill for on-demand IDE content generation
├── content/
│   ├── history.json                  # History log of reviewed IDEs to prevent duplication
│   └── YYYY-MM-DD/                   # Daily generated packages (3 AMP posts + 3 Flow JSONs)
└── tests/
    └── test_content_and_amp.py       # Comprehensive pytest suite
```

---

## Daily Content Workflow

Run the daily generator script locally or via GitHub Actions:

```bash
python3 scripts/generate_daily_content.py
```

This outputs 3 AMP blog posts and 3 Google Flow video spec files inside `content/YYYY-MM-DD/` and updates `content/history.json`.

---

## Agentic Skill CLI Usage

To generate content on-demand for a specific IDE or code editor:

```bash
# Generate for a custom paid editor
PYTHONPATH=. python3 scripts/ide_guide_agent_skill.py --ide "Sublime Text" --paid --pricing-details "$99 individual license"

# Generate for a free open source editor
PYTHONPATH=. python3 scripts/ide_guide_agent_skill.py --ide "Zed Editor"
```

Generated outputs will be saved in `content/custom/`.

---

## AMP HTML Validation

To validate any generated HTML file against AMP rules:

```bash
python3 scripts/amp_validator.py content/2026-09-29/blog_1_vscode.html
```

---

## Testing

Run the full pytest suite:

```bash
PYTHONPATH=. pytest tests/
```

---

## Non-Sponsorship Disclaimer

All generated blog posts and video specifications include the exact required statement:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
