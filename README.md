# IDE Guide Automation & Agentic Tooling

Welcome to the **IDE Guide** repository! This repository powers automated daily content generation and agentic skill tools for our technical publishing channels:
- **Blogger Site**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- **YouTube Channel**: [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)

---

## 🌟 Channel Purpose & Scope
IDE Guide evaluates and benchmarks modern Integrated Development Environments (IDEs) and code editors (such as VS Code, Cursor, Zed, PyCharm, Neovim, IntelliJ IDEA, and open source GitHub editors).

We produce:
1. **3 Daily Blog Posts**: AMP HTML compliant posts designed for fast mobile loading on Blogger.
2. **3 Daily Video Content Packages**: Complete video prompt specifications, framing directives, lighting guidelines, and voiceover transcripts designed for AI video creation tools (such as Google Flow / Google Veo) and text-to-speech tools.

---

## 🔒 Mandatory Non-Sponsorship Disclaimer
Every generated blog post, video prompt specification, and voiceover script includes our mandatory non-sponsorship disclaimer:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

---

## 🛠️ Components & Tools

### 1. Agentic Skill CLI Tool (`scripts/ide_guide_agent_skill.py`)
Generates on-demand AMP HTML blog posts and Google Flow video specifications for any given IDE name or GitHub repository URL.

**Usage Examples:**
```bash
# Generate content by IDE name and price
python3 scripts/ide_guide_agent_skill.py --ide "Cursor" --price "Freemium" --category "AI-Native Code Editor"

# Generate content directly from a GitHub repository URL
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed"
```

### 2. AMP HTML Validator (`scripts/amp_validator.py`)
Validates generated HTML files against Google AMP specifications (checking `<html ⚡>`, `<style amp-custom>`, presence of `v0.js`, absence of forbidden `<img>` or inline JS tags, and presence of mandatory disclaimer).

**Usage Example:**
```bash
python3 scripts/amp_validator.py content/2026-09-27/post_1_visual_studio_code_amp.html
```

### 3. Daily Content Generator (`scripts/generate_daily_content.py`)
Generates 3 packages every day and tracks previously covered editors in `content/history.json` to avoid duplicate coverage.

**Usage Example:**
```bash
PYTHONPATH=. python3 scripts/generate_daily_content.py
```

### 4. Automated Daily Workflow (`.github/workflows/daily_content_generation.yml`)
Runs automatically every day at `21:30 UTC` (`03:00 AM IST`) via GitHub Actions, committing new daily content into `content/YYYY-MM-DD/`.

---

## 📁 Repository Directory Structure

```
.
├── .github/workflows/
│   └── daily_content_generation.yml
├── content/
│   ├── history.json
│   └── YYYY-MM-DD/
│       ├── post_1_<ide>_amp.html
│       ├── video_1_<ide>_spec.json
│       ├── ...
├── docs/
│   ├── amp_blogger_guidelines.md
│   └── google_flow_spec_guidelines.md
├── scripts/
│   ├── amp_validator.py
│   ├── generate_daily_content.py
│   └── ide_guide_agent_skill.py
├── tests/
│   └── test_ide_guide.py
└── README.md
```

---

## 🧪 Testing

To run the complete unit test suite:
```bash
PYTHONPATH=. pytest tests/
```
