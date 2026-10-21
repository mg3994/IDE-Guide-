# IDE Guide - Automated Content Engine & Agentic Skills

Welcome to the **IDE Guide** repository! This platform powers automated, daily content generation for:
- 🌐 **Blogger Web Publication**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/) (100% Accelerated Mobile Pages - AMP HTML compliant)
- 🎬 **YouTube Channel**: [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide) (Google Flow & Veo Video Specifications & Prompts)

---

## 🎯 Channel & Publication Mission
IDE Guide delivers objective, transparent, and high-impact technical analysis of IDEs, code editors, extensions, and AI coding tools. Every piece of content features:
- In-depth feature breakdown & comparison
- Honest Pros & Cons
- Clear Pricing Tier information (Free vs Paid vs Freemium)
- Objective Developer Persona Recommendations
- Mandatory non-sponsorship disclaimer to guarantee 100% editorial neutrality

> **Disclaimer**: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

---

## ⚙️ Architecture & Features

1. **AMP Blogger Compliance**:
   All blog posts generated strictly adhere to Google's AMP HTML specifications (AMP Boilerplate, inline CSS, prohibited standard `<img/>` and custom scripts) to guarantee instant loading on mobile search.
2. **Google Flow Video Prompt Generator**:
   Generates production-ready JSON specifications for **Google Flow** and AI video creation tools, complete with visual prompts, camera framing, lighting cues, voiceover scripts, and aspect ratio formatting (9:16 Shorts / 16:9 Videos).
3. **Daily Content Engine (3 Posts + 3 Videos/Day)**:
   Automated engine runs daily at 21:30 UTC (03:00 AM IST) to generate 3 blog posts and 3 video specs under `content/YYYY-MM-DD/` while recording history in `content/history.json` to prevent repeated tool coverage.
4. **Agentic CLI Skill Tool**:
   CLI utility (`scripts/ide_guide_agent_skill.py`) that enables on-demand generation of AMP blog posts and Google Flow video specs for any IDE or GitHub repository URL.

---

## 🛠️ Installation & Setup

```bash
# Clone the repository
git clone https://github.com/mg3994/IDE-Guide-.git
cd IDE-Guide-

# Run tests
PYTHONPATH=. pytest tests/
```

---

## 🚀 Usage

### 1. Daily Content Generator
To generate 3 fresh content packages for today:
```bash
python3 scripts/generate_daily_content.py
```
Outputs are written to `content/YYYY-MM-DD/`.

### 2. Validate AMP HTML
To check if an HTML post is AMP compliant:
```bash
python3 scripts/amp_validator.py content/2026-10-21/post_1_cursor.amp.html
```

### 3. Agentic Skill Tool (On-Demand Content)
Generate custom AMP blog post and Google Flow video spec for any editor or GitHub repository:
```bash
# By IDE Name
python3 scripts/ide_guide_agent_skill.py "Cursor" --output-dir ./custom_output

# By Repository URL
python3 scripts/ide_guide_agent_skill.py "https://github.com/neovim/neovim" --output-dir ./custom_output
```

---

## 📚 Guidelines & Specifications
- [Blogger AMP HTML Guidelines](docs/amp_blogger_guidelines.md)
- [Google Flow Video Prompt Guidelines](docs/google_flow_spec_guidelines.md)
