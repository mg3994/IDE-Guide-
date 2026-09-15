# 🚀 IDE Guide - Automated Daily Content & Agentic Skill Platform

Welcome to **IDE Guide** — the automated content engine powering our technical developer publications:
- 🌐 **Blogger Website**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- 📹 **YouTube Channel**: [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)

IDE Guide publishes **3 AMP-compliant blog posts** and **3 visual video generation packages (Google Flow scripts & prompts)** every single day, covering IDEs, code editors, AI coding assistants, and developer tools.

---

## 📌 Key Features

1. **AMP (Accelerated Mobile Pages) Blogger Output**:
   - Generates 100% AMP HTML valid blog posts optimized for mobile performance and Blogger publishing.
   - Includes structured metadata, responsive layout tags (`<amp-img>`), clean syntax highlighting, pros/cons breakdown, and pricing analysis (Free vs. Paid vs. Freemium).

2. **Google Flow AI Video Generation Specifications**:
   - Daily production of 3 visual video specs tailored for AI video tools (Google Flow, Veo, Runway, Sora).
   - Detailed visual scene prompts: camera framing, motion, studio lighting, duration timing, text overlays, and synchronized voiceover scripts.

3. **Agentic CLI Skill (`scripts/ide_guide_agent_skill.py`)**:
   - On-demand AI skill to generate custom AMP blog posts and Google Flow video specs for any IDE name or GitHub repository URL.

4. **Automated Daily Pipeline**:
   - Powered by GitHub Actions (`.github/workflows/daily_content_generation.yml`) running daily at 21:30 UTC.
   - Automatically checks history in `content/history.json` to prevent duplicate editor coverage across consecutive days.

5. **Strict Independence & Non-Sponsorship**:
   - All content automatically enforces our independent stance with a standardized non-sponsorship disclaimer.

---

## 🛠️ Quick Start

### 1. Installation & Environment

Ensure Python 3.10+ and pytest are installed:

```bash
python3 --version
pytest --version
```

### 2. Using the Agentic CLI Skill

Generate an AMP blog post and Google Flow video spec for any IDE or GitHub repo:

```bash
# Generate content for Cursor IDE
python3 scripts/ide_guide_agent_skill.py --ide "Cursor IDE" --output-dir ./output

# Generate content from a GitHub repository URL
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed" --output-dir ./output
```

### 3. Generating Daily Content Manually

Run the daily content generation script to create today's batch (3 blog posts + 3 video specifications):

```bash
python3 scripts/generate_daily_content.py
```

Output files will be saved in `content/YYYY-MM-DD/blogs/` and `content/YYYY-MM-DD/videos/`.

---

## 🧪 Testing

Run the test suite to verify content generation, AMP compliance, and CLI functionality:

```bash
pytest tests/
```

---

## ⚖️ Disclaimer

IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
