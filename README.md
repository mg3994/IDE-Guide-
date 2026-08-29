# IDE Guide - Automated Content & Video Generation Engine

Welcome to **IDE Guide**! This repository powers the daily content pipeline for our Blogger platform ([ideguide.blogspot.com](https://ideguide.blogspot.com/)) and YouTube Channel ([@IDEguide](https://www.youtube.@IDEguide)).

---

## 🌟 Channel & Platform Mission

- **Blogger Website:** [ideguide.blogspot.com](https://ideguide.blogspot.com/)
- **YouTube Channel:** [@IDEguide](https://www.youtube.@IDEguide)
- **Daily Content Output:** 3 AMP HTML Blog Posts + 3 Google Flow Video & Shorts Specs generated every day.
- **Scope:** Coverage of IDEs, code editors, and developer tools (VS Code, Cursor, Neovim, JetBrains suite, Zed, Helix, PyCharm, etc.).
- **Objective Evaluation:** Highlighting pros & cons, paid vs. free tiers, key features, performance benchmarks, and recommendations.
- **Non-Sponsorship Commitment:** Every blog post and video spec contains our mandatory non-sponsorship disclosure.

---

## 🚀 Repository & Pipeline Architecture

```text
├── .github/workflows/
│   └── daily_content_generation.yml  # Daily GitHub Actions schedule (21:30 UTC / 03:00 AM IST)
├── content/
│   ├── history.json                   # Tracks covered IDEs to avoid duplicates
│   └── YYYY-MM-DD/                    # Dated packages containing 3 AMP posts & 3 Video Specs
├── docs/
│   └── google_flow_spec_guidelines.md # Video prompt engineering standards for Google Flow & AI tools
├── scripts/
│   ├── generate_daily_content.py      # Core automated daily content generator
│   └── ide_guide_agent_skill.py       # Agentic CLI skill tool for on-demand generation
└── tests/
    └── test_content_generation.py     # Comprehensive unit tests
```

---

## ⚡ Usage & Agentic Skills

### 1. Daily Automated Content Generation
To manually trigger or test the daily pipeline locally:
```bash
python3 scripts/generate_daily_content.py
```
This generates dated content in `content/YYYY-MM-DD/` and updates `content/history.json`.

### 2. On-Demand Agentic CLI Skill (`ide_guide_agent_skill.py`)
Use this tool to generate AMP HTML blog posts and Google Flow specs for any IDE or GitHub repository on demand:

**By IDE Name:**
```bash
python3 scripts/ide_guide_agent_skill.py --ide "Sublime Text" --pricing "$99 License" --developer "Sublime HQ"
```

**By GitHub Repository URL:**
```bash
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed"
```

---

## 📱 AMP HTML Blogger Integration

All blog posts produced by the engine strictly adhere to **AMP (Accelerated Mobile Pages)** standards for maximum mobile performance on Blogger:
- Standard AMP HTML boilerplate (`<html ⚡ lang="en">`, `<script async src="https://cdn.ampproject.org/v0.js"></script>`).
- Embedded responsive CSS inside `<style amp-custom>`.
- Mobile-optimized layout for mobile and desktop readers.

---

## 🎬 Google Flow & Video Generation Specs

Video specifications produced in `video_spec_*.json` provide rich prompt engineering parameters for AI video tools (such as Google Flow):
- **Presets & Lighting:** Cyberpunk dark tech, neon syntax glow.
- **Aspect Ratios:** 16:9 4K UHD for main YouTube videos and 9:16 for YouTube Shorts.
- **Camera Directions:** Macro close-ups on UI elements, push-in zooms, split-screen benchmark comparisons.
- **Audio & Script Sequence:** Structured 6-part scene breakdown including hook, pricing, pros/cons, verdict, and disclaimer.

---

## 🛡️ Non-Sponsorship Disclaimer

Every piece of content includes the mandatory exact disclaimer:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
