# IDE Guide Automation & Agentic Skills

Automation toolkit and agentic skills for the **IDE Guide** Blogger publication ([ideguide.blogspot.com](https://ideguide.blogspot.com/)) and YouTube channel ([@IDEguide](https://www.youtube.com/@IDEguide)).

---

## 🌟 Features

1. **Agentic CLI Tool (`scripts/ide_guide_agent_skill.py`)**:
   - On-demand content generation for any specific IDE or editor (e.g. Zed, Cursor, Neovim, VSCodium, Lapce, Fleet).
   - Generates **AMP HTML** formatted blog posts (Accelerated Mobile Pages compliant for Blogger).
   - Generates **Google Flow AI Video Specs** (including structured scene prompts, camera motion, lighting, voiceover script, and aspect ratio formatting).
   - Evaluates pros/cons, free vs. paid pricing details, and recommended developer target audience.
   - Embeds mandatory non-sponsorship disclosure.

2. **Daily Automated Content Pipeline (`scripts/generate_daily_content.py`)**:
   - Generates **3 AMP HTML blog posts** and **3 Google Flow video specifications** daily under `content/YYYY-MM-DD/`.
   - Features dynamic IDE discovery via GitHub Search API with fallback curated list.
   - Tracks previously covered editors in `content/history.json` to prevent repetitive content.

3. **Google Flow Video Specifications (`docs/google_flow_spec_guidelines.md`)**:
   - Standardized scene schemas, cinematic camera instructions, audio script formatting, and 9:16 / 16:9 aspect ratios for YouTube Shorts and Longform.

4. **Automated GitHub Actions Schedule (`.github/workflows/daily_content_generation.yml`)**:
   - Automatically runs every day at `21:30 UTC` (03:00 AM IST) to generate, commit, and update daily content packages.

---

## 🚀 Quick Start & Usage

### 1. On-Demand Content Generation (Agentic Skill CLI)
Run the agent tool for any IDE:

```bash
python3 scripts/ide_guide_agent_skill.py --ide "Zed" --output-dir ./output
```

This generates:
- `output/zed-editor_amp_blogpost.html`: AMP HTML blog post ready for Blogger.
- `output/zed-editor_google_flow_spec.json`: Machine-readable Google Flow video specification.
- `output/zed-editor_google_flow_spec.md`: Markdown summary of Google Flow prompts and narration script.

### 2. Daily Content Generation Package
To generate today's batch of 3 blog posts and 3 video specs:

```bash
PYTHONPATH=scripts python3 scripts/generate_daily_content.py
```

Generated outputs will be saved in `content/YYYY-MM-DD/` and recorded in `content/history.json`.

---

## 🧪 Testing

Run unit tests to verify AMP compliance, prompt structures, history tracking, and generation pipelines:

```bash
PYTHONPATH=scripts pytest tests/
```

---

## 🔒 Non-Sponsorship Disclaimer

All generated blog posts and video specifications include the required disclaimer:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
