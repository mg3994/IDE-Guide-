# IDE Guide 🚀

**IDE Guide** is an automated content creation engine and agentic CLI toolkit for generating technical reviews, feature comparisons, and developer setup guides for modern Integrated Development Environments (IDEs) and code editors.

Published daily across two primary channels:
- **Blogger (AMP HTML):** [ideguide.blogspot.com](https://ideguide.blogspot.com/)
- **YouTube (@IDEguide):** [youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)

---

## ⚡ Key Features

- **3 Posts & 3 Videos Daily:** Automatically selects 3 unique code editors / IDEs every day and builds complete content packages (AMP-compliant HTML blog posts + Google Flow video generation specs).
- **AMP (Accelerated Mobile Pages) Compliant:** Generates clean, fast-loading, valid AMP HTML tailored specifically for Blogger publishing with responsive styling, inline AMP CSS (`<style amp-custom>`), layout constraints, and AMP runtime script tags (`https://cdn.ampproject.org/v0.js`).
- **Google Flow Video Generation Specs:** Detailed visual prompts, camera controls, lighting setups, timecodes, voiceover scripts, and scene-by-scene specifications for YouTube Shorts (9:16) and YouTube Long-form Videos (16:9).
- **History Tracking (`content/history.json`):** Remembers previously covered IDEs to avoid duplicate coverage and ensure diverse daily output across open-source, freemium, commercial, and emerging tools.
- **Agentic Skill Tool (`scripts/ide_guide_agent_skill.py`):** On-demand CLI command for AI agents and human developers to generate custom AMP blog posts and video specs for any IDE name or GitHub repository URL.
- **Non-Sponsorship Disclaimer:** Guarantees objective, unbiased evaluations by automatically including standard mandatory non-sponsorship disclaimers on every post and video spec.

---

## 📂 Content Directory Structure

Daily content packages are generated under `content/YYYY-MM-DD/`:

```
content/
├── history.json
└── 2026-03-30/
    ├── post_1_cursor.html         (AMP HTML for Blogger)
    ├── video_spec_1_cursor.json   (Google Flow spec for YouTube)
    ├── post_2_zed.html
    ├── video_spec_2_zed.json
    ├── post_3_neovim.html
    └── video_spec_3_neovim.json
```

---

## 🛠️ Usage

### 1. Daily Content Generation (Automated or Manual)

To run the daily generator manually:
```bash
python3 scripts/generate_daily_content.py
```

To run a dry-run without writing files:
```bash
python3 scripts/generate_daily_content.py --dry-run
```

### 2. Agentic CLI Skill Tool

Generate AMP blog posts and Google Flow video specs on demand for any IDE or GitHub repository:

```bash
# Generate content for a specific IDE
python3 scripts/ide_guide_agent_skill.py --ide "Windsurf Editor"

# Generate content from a GitHub repository URL
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/lapce/lapce"

# Output custom directory
python3 scripts/ide_guide_agent_skill.py --ide "Zed" --output-dir "custom_output"
```

---

## 🧪 Testing

Run the full test suite using `pytest`:

```bash
pytest tests/
```

The test suite validates:
1. AMP HTML compliance (valid tags, boilerplate, style restrictions, runtime scripts).
2. Dynamic content generation logic and history updating.
3. Agentic CLI skill functionality.
4. Non-sponsorship disclaimer inclusion in all outputs.

---

## ⚖️ Non-Sponsorship Disclaimer

All generated content includes the following standard disclaimer:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
