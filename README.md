# IDE Guide 🚀

Official content generation engine and agentic CLI tools for **IDE Guide**:
- 🌐 **Blogger Website:** [ideguide.blogspot.com](https://ideguide.blogspot.com/)
- 📺 **YouTube Channel:** [@IDEguide](https://www.youtube.com/@IDEguide)

---

## 📌 Features

- **Daily Automated Generation (3 Posts & 3 Videos / Day):**
  - Generates **3 AMP HTML blog posts** optimized for Accelerated Mobile Pages (Blogger compatible).
  - Generates **3 Google Flow Video Generation Specs** formatted for AI video engines (Google Flow, Veo, Sora) targeting YouTube Shorts (9:16) and YouTube Longform (16:9).
- **Agentic Skill CLI Tool (`scripts/ide_guide_agent_skill.py`):**
  - On-demand custom AMP blog post and Google Flow video spec generation for any specified IDE or GitHub repository URL.
- **Objective Editor Evaluation:**
  - Standardized breakdowns covering pros (good points), cons (bad points), target developer recommendations, and clear pricing structure (Free, Paid, Freemium, Open Source).
- **Non-Sponsorship Transparency:**
  - All generated content strictly enforces our mandatory non-sponsorship disclaimer across posts and scripts.
- **Automated Workflow:**
  - Scheduled GitHub Actions workflow (`.github/workflows/daily_content_generation.yml`) runs daily at **21:30 UTC (03:00 AM IST)**.

---

## 📂 Output Folder Structure

Daily runs output organized packages under `content/YYYY-MM-DD/`:

```text
content/
├── history.json
└── 2026-09-19/
    ├── item-1-vscode/
    │   ├── amp_post.html
    │   ├── google_flow_spec.json
    │   └── google_flow_spec.md
    ├── item-2-cursor/
    │   ├── amp_post.html
    │   ├── google_flow_spec.json
    │   └── google_flow_spec.md
    └── item-3-intellij-idea/
        ├── amp_post.html
        ├── google_flow_spec.json
        └── google_flow_spec.md
```

---

## 🛠️ Usage & Commands

### 1. Run Daily Content Generator

Discovers unvisited IDEs, builds 3 daily content packages, and updates `content/history.json`:

```bash
python3 scripts/generate_daily_content.py
```

### 2. Run Agentic Skill CLI Tool

Generate custom AMP blog posts and Google Flow video specs on-demand:

```bash
# By IDE Name:
python3 scripts/ide_guide_agent_skill.py --ide "Cursor"

# By GitHub Repository URL:
python3 scripts/ide_guide_agent_skill.py --url "https://github.com/zed-industries/zed"

# Custom Output Path & Save to History:
python3 scripts/ide_guide_agent_skill.py --ide "Zed Editor" --out "./output/zed" --save-history
```

---

## ⚡ AMP HTML Standards

Blog posts generated for Blogger follow AMP HTML specifications:
- `<!doctype html>` with `<html ⚡ lang="en">`
- Async AMP runtime script `https://cdn.ampproject.org/v0.js`
- `<link rel="canonical" href="...">` & viewport tags
- Mandatory `<style amp-boilerplate>` and `<noscript>` blocks
- Responsive styling isolated inside `<style amp-custom>`
- Dedicated non-sponsorship disclosure box

---

## 🎥 Google Flow Video Spec Guidelines

Video specifications follow guidelines in [`docs/google_flow_spec_guidelines.md`](docs/google_flow_spec_guidelines.md):
- Cinematic lighting setups (neon rim light, dark mode studio aesthetic)
- Scene-by-scene camera framing (close-ups, macro lens, split comparisons)
- 60-second high-energy voiceover scripts for YouTube Shorts
- JSON & Markdown structured visual prompts for Google Flow / Veo generators

---

## 🧪 Testing

Run unit tests using `pytest`:

```bash
pytest tests/
```

---

## ⚖️ Non-Sponsorship Disclaimer

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
