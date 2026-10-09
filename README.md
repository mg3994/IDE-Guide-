# IDE Guide 🚀

Automated Content Generation Engine, Agentic Skills, and Google Flow Video Specifications for **IDE Guide**.

- **Blogger Website**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- **YouTube Channel**: [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)

---

## 📖 Overview

**IDE Guide** provides objective, independent, and developer-focused evaluations, comparisons, pros & cons (the good & the bad), and pricing analysis across modern IDEs, code editors, and developer tools.

Every day, this repository generates **3 content packages** consisting of:
1. **AMP HTML Blog Posts**: Content formatted specifically for Blogger Accelerated Mobile Pages (AMP) compliance.
2. **Google Flow Video Specifications**: Visual prompts, framing, lighting guidelines, timestamps, and voiceover narration scripts for YouTube long-form videos (16:9) and YouTube Shorts (9:16).

---

## 🛠️ Features & Agentic Skill Tools

### 1. Agentic CLI Skill Tool (`scripts/ide_guide_agent_skill.py`)
Generate custom AMP blog posts and Google Flow video specs on demand for any IDE name or GitHub repository URL.

```bash
# Generate content package for an IDE
python3 scripts/ide_guide_agent_skill.py --ide "Cursor" --out-dir output/

# Generate content package from a GitHub repository URL
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed" --out-dir output/
```

### 2. AMP HTML Validator (`scripts/amp_validator.py`)
Ensures generated blog posts comply strictly with Blogger AMP standards (e.g., `<amp-img>` usage, prohibited inline styles, no disallowed scripts/iframes) and verifies the mandatory non-sponsorship disclaimer.

```bash
python3 scripts/amp_validator.py content/2025-02-15/visual_studio_code_post.html
```

### 3. Daily Content Generator (`scripts/generate_daily_content.py`)
Generates 3 daily blog posts and 3 Google Flow video specs in `content/YYYY-MM-DD/`, while updating `content/history.json` to prevent repeating covered tools across consecutive days.

```bash
# Generate today's 3 daily packages
python3 scripts/generate_daily_content.py

# Generate for a specific date
python3 scripts/generate_daily_content.py 2025-02-15
```

---

## 🤖 Automated Workflow

Daily generation is scheduled via GitHub Actions (`.github/workflows/daily_content_generation.yml`) at **21:30 UTC** (03:00 AM IST) every day.

The workflow:
1. Runs `scripts/generate_daily_content.py` to produce 3 new AMP posts and 3 video specs.
2. Executes test suite and AMP validation checks.
3. Automatically commits updated files and history log back to the repository.

---

## 🧪 Testing

Run the full pytest suite to verify AMP validation, content generation logic, history tracking, and agentic CLI skills:

```bash
PYTHONPATH=. pytest tests/
```

---

## 📌 Guidelines & Documentation

- **[AMP Blogger Guidelines](docs/amp_blogger_guidelines.md)**: Formatting rules, prohibited tags, CSS restrictions, and structural requirements.
- **[Google Flow Video Specs Guidelines](docs/google_flow_spec_guidelines.md)**: Prompt engineering guidelines, camera framing, lighting setup, timestamps, and narration.

---

## ⚖️ Non-Sponsorship Disclaimer

All generated articles, videos, descriptions, and specifications include the following mandatory disclaimer:

> **Disclaimer**: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
