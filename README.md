# IDE Guide Automation & Agentic Skills

Welcome to **IDE Guide** — an automated content platform providing independent, unsponsored reviews and guides for code editors, IDEs, and software development tools.

- **Blogger Website:** [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- **YouTube Channel:** [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)

---

## ⚡ Key Features

1. **AMP HTML Blog Posts (For Blogger)**:
   - 100% compliant with Accelerated Mobile Pages (AMP) standards for ultra-fast mobile reading.
   - Built-in `<amp-img>` tags, AMP boilerplate, responsive CSS styling inside `<style amp-custom>`, and canonical links.
   - Includes mandatory non-sponsorship disclaimer on every article.

2. **Google Flow Video & Shorts Specifications (For YouTube)**:
   - High-retention video prompt specifications designed for AI video generation tools like **Google Flow**, Runway, and Sora.
   - Detailed scene-by-scene breakdown (timestamps, visual prompts, framing/lighting, screen actions, voiceover narration scripts, and on-screen text overlays).
   - Tailored for YouTube Shorts (9:16 vertical format) and widescreen reviews (16:9).

3. **Daily Content Pipeline (3 Videos + 3 Blog Posts Daily)**:
   - Automated via GitHub Actions running daily at 21:30 UTC (03:00 AM IST).
   - Generates 3 complete content packages per day under `content/YYYY-MM-DD/`.
   - Built-in history tracker (`content/history.json`) prevents duplicate editor coverage until the pool rotates.

4. **Agentic CLI Skill Tool**:
   - Allows on-demand generation of AMP blog posts and Google Flow video specs for any custom IDE or code editor.

---

## 🚀 Quick Start & CLI Usage

### 1. Run Daily Content Generator
To generate today's 3 daily packages locally:
```bash
python3 scripts/generate_daily_content.py
```

Outputs will be generated in `content/YYYY-MM-DD/`:
- `post1_<ide>.html`, `post2_<ide>.html`, `post3_<ide>.html`
- `video1_<ide>_google_flow.json`, `video2_<ide>_google_flow.json`, `video3_<ide>_google_flow.json`
- `summary.md`

### 2. Validate AMP HTML Files
Validate any generated HTML file against AMP rules:
```bash
python3 scripts/amp_validator.py content/2026-10-10/post1_cursor.html
```

### 3. Use Agentic CLI Skill Tool
Generate custom blog post and Google Flow video spec for any specified IDE or repository:
```bash
python3 scripts/ide_guide_agent_skill.py --name "Lapce Editor" --category "Native Rust Editor" --pricing "Free / Open Source" --is-free --outdir "content/custom_lapce"
```

---

## 🧪 Testing

Run unit tests across the entire test suite:
```bash
PYTHONPATH=. pytest tests/
```

---

## 📜 Mandatory Non-Sponsorship Disclaimer

All generated blog posts and video specifications strictly include the following disclaimer:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
