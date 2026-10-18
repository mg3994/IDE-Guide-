# IDE Guide Content Generation Automation & Agentic Skills

Automation system and agentic CLI skills for **IDE Guide** ([ideguide.blogspot.com](https://ideguide.blogspot.com/) & [YouTube @IDEguide](https://www.youtube.com/@IDEguide)).

This repository generates daily content packages (3 AMP HTML blog posts & 3 Google Flow video specifications) comparing code editors and IDEs (e.g. VS Code, Cursor, JetBrains IntelliJ, Neovim, Zed, Windsurf, PyCharm, Xcode, Replit, Fleet).

---

## 🌟 Key Features

1. **AMP (Accelerated Mobile Pages) HTML Blog Posts**:
   - Strictly formatted for Blogger compliance (valid `<html amp>`, boilerplate, `<amp-img>` elements, canonical links).
   - Validated automatically via built-in `scripts/amp_validator.py`.

2. **Google Flow Video Specifications**:
   - Structured JSON scene-by-scene specifications for Google Flow and video AI tools.
   - Includes prompt camera angles, lighting, background styles, timing, on-screen GFX, and voiceover scripts.
   - Highlights free vs paid pricing tiers clearly for high audience engagement.

3. **Agentic CLI Skill Tool**:
   - Generate custom AMP blog posts and Google Flow video specs on demand for any specified IDE or repository URL using `scripts/ide_guide_agent_skill.py`.

4. **Non-Sponsorship Compliance**:
   - Includes exact required non-sponsorship disclaimer across all generated blog posts and video specifications:
     > **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

5. **Automated GitHub Actions Schedule**:
   - Scheduled daily workflow at **21:30 UTC** (**03:00 AM IST**) to produce 3 daily content packages in `content/YYYY-MM-DD/`.

---

## 🚀 Quick Start & Usage

### 1. Execute Agentic CLI Skill
To generate an AMP blog post and Google Flow video spec for a custom editor on demand:

```bash
PYTHONPATH=. python3 scripts/ide_guide_agent_skill.py --ide "Cursor IDE" --pricing "Freemium"
```

To run for a custom editor with a website URL:
```bash
PYTHONPATH=. python3 scripts/ide_guide_agent_skill.py --ide "Zed Editor" --category "High-Performance Editor" --pricing "Free" --url "https://zed.dev"
```

### 2. Generate Daily Content Packages (3 Blog Posts + 3 Video Specs)
```bash
PYTHONPATH=. python3 scripts/generate_daily_content.py
```
Output files are stored under `content/YYYY-MM-DD/`.

### 3. Validate AMP HTML Compliance
```bash
python3 scripts/amp_validator.py content/2026-10-18/post_1_neovim_amp.html
```

---

## 🧪 Running Tests

To run the complete test suite:

```bash
PYTHONPATH=. pytest tests/
```

---

## 📁 Repository Structure

```
├── .github/workflows/
│   └── daily_content_generation.yml  # Daily GitHub Actions schedule
├── content/
│   ├── history.json                  # Tracks covered IDEs to avoid repetitions
│   └── YYYY-MM-DD/                   # Daily output packages
├── docs/
│   ├── amp_blogger_guidelines.md     # AMP HTML compliance specifications
│   └── google_flow_spec_guidelines.md# Google Flow prompt & video guidelines
├── scripts/
│   ├── amp_validator.py              # AMP HTML validator CLI utility
│   ├── generate_daily_content.py     # Batch content generator script
│   └── ide_guide_agent_skill.py      # Agentic CLI skill tool
└── tests/
    ├── test_agent_skill.py           # Unit tests for CLI agent skill
    ├── test_amp_validator.py         # Unit tests for AMP HTML validator
    └── test_daily_content.py        # Unit tests for content generator
```
