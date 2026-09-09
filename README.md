# IDE Guide - Automated Content Engine & Agentic Skills

Welcome to the **IDE Guide** repository! This repository powers automated daily content creation and agentic skill tools for the **IDE Guide** publication channels:
- 🌐 **Blogger Website**: [ideguide.blogspot.com](https://ideguide.blogspot.com/)
- 🎥 **YouTube Channel**: [@IDEguide](https://www.youtube.com/@IDEguide)

---

## 📌 Overview

**IDE Guide** provides objective, independent evaluations of integrated development environments (IDEs), code editors, and developer tools (e.g. VS Code, Cursor, Windsurf, IntelliJ IDEA, Neovim, Zed, PyCharm, Sublime Text, Eclipse, Xcode, Fleet, and emerging tools).

The system generates:
1. **AMP HTML Blog Posts**: Fully valid Accelerated Mobile Pages (AMP) HTML formatted posts tailored for seamless publishing on Blogger (`ideguide.blogspot.com`).
2. **Google Flow Video Specifications**: Structured video generation prompts, scene-by-scene timing, voiceover scripts, camera motion, and visual specs for YouTube videos and Shorts (`@IDEguide`).

---

## 🚀 Key Features

- **Daily Automated Content Generation**: Generates **3 complete blog posts** and **3 Google Flow video specifications** daily.
- **AMP HTML Compliance**: All blog posts strictly adhere to AMP HTML standards (`amp-img`, custom CSS, boilerplate JS, valid tags) for maximum mobile SEO and performance on Blogger.
- **Google Flow Video Prompts**: Built-in prompt generator creating scene-by-scene camera movements, visual lighting, voiceovers, and duration timing for AI video generators (Google Flow / Veo / Sora).
- **Agentic CLI Skill (`scripts/ide_guide_agent_skill.py`)**: An on-demand CLI tool for agents or developers to generate custom AMP HTML reviews and video specs for any specified IDE or GitHub repository URL.
- **History Tracking (`content/history.json`)**: Dynamic tracking of covered editors to prevent duplicate coverage and continuously discover trending open-source IDEs via GitHub Search API.
- **Strict Independence Disclaimer**: Every piece of content automatically incorporates our standardized non-sponsorship disclaimer.

---

## ⚙️ Repository Structure

```
├── .github/
│   └── workflows/
│       └── daily_content_generation.yml   # Scheduled daily workflow (21:30 UTC / 03:00 AM IST)
├── docs/
│   └── google_flow_spec_guidelines.md      # Guidelines for Google Flow prompt engineering & video specs
├── scripts/
│   ├── generate_daily_content.py          # Batch generator for 3 daily content packages
│   └── ide_guide_agent_skill.py           # On-demand CLI skill for custom IDE review generation
├── src/
│   └── ide_guide/
│       ├── __init__.py
│       ├── amp_generator.py               # AMP HTML generator engine for Blogger
│       ├── catalog.py                     # IDE catalog & dynamic GitHub search discovery
│       ├── google_flow_generator.py       # Google Flow video specification & script engine
│       └── history_tracker.py             # History tracking in content/history.json
├── content/
│   ├── history.json                       # Record of evaluated IDEs
│   └── YYYY-MM-DD/                        # Daily output folders containing HTML posts and video specs
└── tests/
    ├── test_amp_generator.py
    ├── test_catalog.py
    ├── test_google_flow_generator.py
    ├── test_history_tracker.py
    ├── test_agent_skill.py
    └── test_daily_generation.py
```

---

## 🛠️ Usage

### 1. Agentic CLI Skill Tool

Generate a custom AMP HTML post and Google Flow video spec for any IDE or repository URL:

```bash
# Generate by IDE name
python3 scripts/ide_guide_agent_skill.py --ide "Cursor"

# Generate by GitHub Repository URL
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed"

# Specify custom output directory
python3 scripts/ide_guide_agent_skill.py --ide "Helix" --output-dir "content/custom"
```

### 2. Manual Daily Batch Generation

Run the daily generator to produce 3 new IDE content packages:

```bash
python3 scripts/generate_daily_content.py
```

### 3. Running Unit Tests

Run the complete test suite:

```bash
pytest tests/
```

---

## 📜 Non-Sponsorship Disclaimer

All generated blog posts and video specifications include the exact required non-sponsorship statement:

> **Disclaimer**: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
