# IDE Guide Content Generator & Agentic Tools

Automated content generation pipeline and agentic skills for [IDE Guide Blogger](https://ideguide.blogspot.com/) and [YouTube Channel @IDEguide](https://www.youtube.com/@IDEguide).

## 🚀 Overview

IDE Guide produces **3 daily videos/shorts** and **3 daily blog posts** analyzing code editors and IDEs (e.g. VS Code, Cursor, PyCharm, Neovim, Zed, Sublime Text 4, IntelliJ IDEA, Windsurf, Fleet).

The content features:
- Objective pros & cons evaluation
- Pricing & license transparency (Free vs Paid tier details)
- **100% AMP HTML Compliance** for fast mobile loading on Blogger
- Structured **Google Flow video specifications** with cinematic visuals, camera movements, lighting, captions, and scripts
- **Non-Sponsorship Disclaimer** on every post and video

---

## 🛠️ Repository Structure

```
├── .github/workflows/
│   └── daily_content_generation.yml  # Daily automated workflow (21:30 UTC / 03:00 AM IST)
├── content/
│   ├── history.json                   # History tracking to avoid repeating IDE reviews
│   └── YYYY-MM-DD/                   # Daily generated AMP posts & Google Flow video specs
├── docs/
│   ├── amp_blogger_guidelines.md      # AMP HTML compliance specification for Blogger
│   └── google_flow_spec_guidelines.md # Video prompt engineering guidelines for Google Flow
├── scripts/
│   ├── amp_validator.py              # AMP HTML & disclaimer validation script
│   ├── generate_daily_content.py     # Main 3x daily content package generator
│   └── ide_guide_agent_skill.py      # Agentic CLI skill tool for on-demand generation
└── tests/                             # Unit test suite
```

---

## 🤖 Agentic CLI Skill Tool Usage

Generate customized AMP blog posts and Google Flow video specs on demand for any IDE or repository URL:

```bash
PYTHONPATH=. python3 scripts/ide_guide_agent_skill.py \
  --ide "Cursor" \
  --repo "https://github.com/getcursor/cursor" \
  --pricing "Freemium ($20/mo Pro)" \
  --category "AI-First IDE" \
  --pros "Deep AI code generation" "Multi-file prompt context" \
  --cons "Subscription needed for high AI usage" \
  --verdict "Top choice for AI-assisted coding." \
  --out-dir "content/custom"
```

---

## 📅 Daily Automated Pipeline

Run the daily generator locally to create 3 AMP posts and 3 Google Flow video specs:

```bash
PYTHONPATH=. python3 scripts/generate_daily_content.py
```

Validate any AMP HTML blog post:

```bash
python3 scripts/amp_validator.py content/2026-10-27/post_1_vs-code.html
```

---

## 🧪 Testing

Run all unit tests:

```bash
PYTHONPATH=. pytest tests/
```

---

## ⚖️ Non-Sponsorship Disclaimer

> **Disclaimer**: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
