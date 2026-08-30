# IDE Guide - Daily Blogger AMP Posts & Google Flow Video Spec Generator

[![Daily Content Generation](https://github.com/mg3994/IDE-Guide-/actions/workflows/daily_content_generation.yml/badge.svg)](https://github.com/mg3994/IDE-Guide-/actions/workflows/daily_content_generation.yml)

Automated content generation engine and agentic CLI skills for **IDE Guide** platform:
- **Blogger Site:** [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- **YouTube Channel:** [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)

---

## 🚀 Overview

IDE Guide automates the generation of daily reviews and technical showcases for software development tools, IDEs, code editors, and AI coding assistants.

### Daily Outputs (Schedule: 3 Posts & 3 Videos per Day)
Every day at 21:30 UTC (03:00 AM IST), the system automatically generates:
1. **3 AMP (Accelerated Mobile Pages) HTML Blog Posts** formatted specifically for fast loading on Blogger (`ideguide.blogspot.com`).
2. **3 Google Flow AI Video Specifications & Scripts** formatted for creating high-converting YouTube Shorts (9:16 vertical) and YouTube long-form videos (16:9 horizontal) for `@IDEguide`.

---

## ⚡ AMP Compliance & Blogger Publishing Rules

All generated HTML blog posts strictly adhere to standard Google AMP guidelines:
- Starts with `<html ⚡ lang="en">` tag boilerplate.
- Contains standard `<style amp-boilerplate>` and inline custom styles inside `<style amp-custom>`.
- Includes canonical links pointing to `https://ideguide.blogspot.com/{slug}-review.html`.
- Includes custom structured badges for tool type, pricing tier, pros/cons breakdown, and final verdict.

---

## 📹 Google Flow Video & Shorts Specifications

Guidelines for prompt engineering, lighting, camera angles, text overlays, and voiceovers are documented in `docs/google_flow_spec_guidelines.md`.

- **YouTube Shorts (9:16)**: 50-second fast-paced visual summary with hook, pros/cons graphics, pricing breakdown, and channel CTA.
- **YouTube Video (16:9)**: 3-minute detailed feature walkthrough, workflow demo, side-by-side comparison tables, and audience recommendations.

---

## 🛡️ Non-Sponsorship Disclaimer

Every generated blog post, video spec, and voiceover script includes the exact non-sponsorship disclosure:

> **"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."**

---

## 🛠️ Usage & Agentic CLI Skills

### 1. Automated Daily Content Generator
To run daily content generation manually:
```bash
python3 scripts/generate_daily_content.py
```
Output will be saved in `content/YYYY-MM-DD/` and recorded in `content/history.json` to prevent repeated coverage.

### 2. Agentic CLI Skill (On-Demand Generation)
Generate custom AMP posts and Google Flow video specs for any specific IDE name or GitHub repository URL:

**By IDE Name:**
```bash
python3 scripts/ide_guide_agent_skill.py --name "Cursor" --output-dir ./content/custom/
```

**By GitHub Repository URL:**
```bash
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed"
```

---

## 🧪 Testing

Run unit tests using `pytest`:
```bash
pytest tests/
```

---

## 📂 Project Structure

```
├── .github/workflows/
│   └── daily_content_generation.yml   # Daily scheduled GitHub Action
├── content/
│   ├── history.json                   # History tracking to avoid repeated tools
│   └── YYYY-MM-DD/                    # Daily generated AMP posts & video specs
├── docs/
│   └── google_flow_spec_guidelines.md # Video prompt engineering & framing standards
├── scripts/
│   ├── generate_daily_content.py      # Core daily content generation script
│   └── ide_guide_agent_skill.py       # Agentic CLI skill tool for on-demand generation
└── tests/
    └── test_content_generation.py     # Pytest suite for AMP validation & CLI skills
```
