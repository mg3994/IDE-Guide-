# IDE Guide Content Generator & Agentic Skills

Welcome to **IDE Guide**, an automated content generation platform and agentic skill suite powering our official channels:
- 🌐 **Blogger Post Hub**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- 🎥 **YouTube Channel**: [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)

---

## 📌 Project Overview

This repository automates the daily generation of high-quality technical reviews for software development environments, code editors, and IDEs. Everyday, the system produces **3 AMP HTML blog posts** for Blogger and **3 Google Flow visual video specifications** for YouTube videos and Shorts.

Key features include:
1. **AMP (Accelerated Mobile Pages) Compliance**: Content strictly adheres to AMP standards for fast mobile loading on Blogger.
2. **Google Flow & AI Video Spec Generator**: Detailed visual prompting specs, camera angles, lighting configs, narration scripts, and timings for AI video platforms (Google Flow, Google Veo, Runway, Sora).
3. **Agentic CLI Skill**: An on-demand tool (`scripts/ide_guide_agent_skill.py`) that allows AI agents or human developers to instantly generate customized AMP posts and video specs for any IDE or GitHub repository URL.
4. **History & Deduplication**: Tracks evaluated IDEs in `content/history.json` to ensure fresh daily content across the catalog.
5. **Mandatory Independent Disclaimer**: Every blog post and video script includes our strict non-sponsorship disclosure:
   > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

---

## 🛠 Directory Structure

```text
├── docs/
│   └── google_flow_spec_guidelines.md   # Google Flow video prompt and script guidelines
├── scripts/
│   ├── generate_daily_content.py        # Core daily content batch generator
│   └── ide_guide_agent_skill.py         # On-demand Agentic CLI Skill tool
├── tests/
│   ├── test_amp_html.py                 # AMP compliance and structure tests
│   ├── test_content_generator.py        # Daily generator & history tests
│   ├── test_cli_skill.py                # Agentic CLI skill tests
│   └── test_history.py                  # History loading & saving tests
├── content/                             # Output directory for daily packages & history.json
└── .github/workflows/
    └── daily_content_generation.yml     # GitHub Actions workflow (21:30 UTC daily)
```

---

## 🚀 Quick Start & Agentic Skill Usage

### 1. Run Daily Content Generator
To generate 3 daily content packages for today's date:
```bash
python3 scripts/generate_daily_content.py
```
Output files will be generated under `content/YYYY-MM-DD/`.

### 2. Run Agentic CLI Skill (On-Demand Content Generation)

Generate customized AMP HTML and Google Flow video specs for a specific IDE:
```bash
python3 scripts/ide_guide_agent_skill.py --ide "Visual Studio Code"
```

Generate specs directly from a GitHub repository URL:
```bash
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed"
```

Format specification for YouTube Shorts (9:16 vertical ratio):
```bash
python3 scripts/ide_guide_agent_skill.py --ide "Cursor" --shorts
```

Specify custom output directory:
```bash
python3 scripts/ide_guide_agent_skill.py --ide "Fleet" --out-dir "./my_custom_output"
```

---

## 🧪 Testing

Run all unit tests using pytest:
```bash
pytest tests/
```

---

## 📅 Automated Scheduling

The repository includes a GitHub Actions workflow (`.github/workflows/daily_content_generation.yml`) scheduled to execute every day at **21:30 UTC** (03:00 AM IST), automatically generating and committing new content packages to the `content/` folder.
