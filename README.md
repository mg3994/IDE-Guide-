# IDE Guide Automation & Agentic Skills Engine

[![IDE Guide YouTube](https://img.shields.io/badge/YouTube-@IDEguide-red)](https://www.youtube.com/@IDEguide)
[![IDE Guide Blog](https://img.shields.io/badge/Blogger-ideguide.blogspot.com-orange)](https://ideguide.blogspot.com/)

Automated content generation engine and agentic skills suite for **IDE Guide**, delivering 3 daily AMP HTML blog posts for Blogger and 3 Google Flow visual video creation specifications for YouTube daily.

---

## Features

- ⚡ **AMP HTML Blog Generator (`scripts/lib/amp_generator.py`):** Generates lightweight, fully compliant AMP HTML blog posts optimized for fast mobile rendering on [ideguide.blogspot.com](https://ideguide.blogspot.com/).
- 🎬 **Google Flow Video Spec Generator (`scripts/lib/google_flow_generator.py`):** Produces detailed AI video prompt specs (framing, camera angles, lighting, scene breakdown, timing, voiceover) optimized for [YouTube @IDEguide](https://www.youtube.com/@IDEguide) Shorts & long-form videos.
- 📅 **Daily Automation Engine (`scripts/generate_daily_content.py`):** Automatically selects 3 new or trending IDEs/editors daily (via GitHub Search API & curated fallback list), tracks history in `content/history.json` to prevent duplicates, and saves content packages in `content/YYYY-MM-DD/`.
- 🤖 **Agentic CLI Skill (`scripts/ide_guide_agent_skill.py`):** Allows instant on-demand content creation for any specified IDE name or repository URL.
- ⏰ **Scheduled Workflow (`.github/workflows/daily_content_generation.yml`):** Runs daily at 21:30 UTC (03:00 AM IST) to publish daily content packages.
- 🛡️ **Mandatory Disclaimer Enforcement:** Ensures all generated content carries the standard non-sponsorship disclaimer.

---

## Quick Start

### 1. Daily Content Generation
To generate the daily 3 content packages:
```bash
python3 scripts/generate_daily_content.py
```

### 2. On-Demand Agentic CLI Skill
To generate content for a specific IDE or repository URL:
```bash
python3 scripts/ide_guide_agent_skill.py --ide "Cursor"
# or via repo URL
python3 scripts/ide_guide_agent_skill.py --url "https://github.com/zed-industries/zed"
```

### 3. Running Unit Tests
```bash
pytest tests/
```

---

## Content Policy & Disclaimer

All content produced by this project carries the following non-sponsorship disclaimer:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
