# IDE Guide - Automated Content Engine & Agentic Tools

Welcome to the **IDE Guide** platform codebase. This repository powers the daily content generation engine for our technical blog on Blogger ([ideguide.blogspot.com](https://ideguide.blogspot.com/)) and video production pipeline for our YouTube channel ([@IDEguide](https://www.youtube.com/@IDEguide)).

---

## 🎯 Purpose & Channels

* **Blogger Website:** [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
  * All generated blog content is published in strict **AMP (Accelerated Mobile Pages)** HTML format for lightning-fast mobile loading and SEO optimization.
* **YouTube Channel:** [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)
  * Video generation scripts and visual specifications targeting **Google Flow** and AI video creation tools for both 16:9 videos and 9:16 vertical Shorts.
* **Daily Goal:** 3 AMP blog posts and 3 Google Flow video specifications published daily.
* **Mandatory Disclaimer:** Every published post and video spec includes our exact non-sponsorship disclosure:
  > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

---

## 🚀 Key Features & Components

### 1. Daily Content Generation Engine (`scripts/generate_daily_content.py`)
* Automatically discovers IDEs/code editors via GitHub Search API or curated IDE dataset.
* Tracks covered tools in `content/history.json` to prevent repeated coverage.
* Outputs daily packages under `content/YYYY-MM-DD/` containing:
  * `post_1_<slug>.html`, `post_2_<slug>.html`, `post_3_<slug>.html` (Valid AMP HTML)
  * `video_1_<slug>.md`, `video_2_<slug>.md`, `video_3_<slug>.md` (Google Flow Specs)

```bash
python3 scripts/generate_daily_content.py
```

### 2. Agentic CLI Skill Tool (`scripts/ide_guide_agent_skill.py`)
Allows users or AI agents to generate custom AMP blog posts and Google Flow video specs on demand for any specified IDE or GitHub repository URL.

```bash
# Generate by IDE Name
python3 scripts/ide_guide_agent_skill.py --ide "Cursor" --output-dir "my_output"

# Generate by GitHub Repository URL
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed" --output-dir "my_output"
```

### 3. Google Flow Video Specifications (`docs/google_flow_spec_guidelines.md`)
Detailed guidelines on framing, camera motion, lighting, voiceover timing, and visual prompt templates for Google Flow and Veo AI video generation.

### 4. GitHub Actions Automation (`.github/workflows/daily_content_generation.yml`)
Runs daily at `21:30 UTC` (03:00 AM IST) to generate and commit the daily content package automatically.

---

## 🧪 Testing & Verification

Run the full unit test suite using `pytest`:

```bash
pytest tests/
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
