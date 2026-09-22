# IDE Guide: Agentic Content & Video Spec Engine

[![Daily Content Generation](https://github.com/mg3994/IDE-Guide-/actions/workflows/daily_content_generation.yml/badge.svg)](https://github.com/mg3994/IDE-Guide-/actions/workflows/daily_content_generation.yml)

**IDE Guide** is an automated platform and agentic toolkit built for managing content production across:
- **Blogger Website:** [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- **YouTube Channel:** [@IDEguide](https://www.youtube.com/@IDEguide)

---

## 🚀 Core Mandate & Cadence

Every day, the system automatically produces:
1. **3 AMP HTML Blog Posts** formatted strictly per Accelerated Mobile Pages (AMP) standards for Blogger publishing.
2. **3 Google Flow Video Specifications** tailored for YouTube Shorts (9:16 vertical) and long-form reviews (16:9 landscape) using Google Flow / Veo AI tools.

---

## 🛡️ Non-Sponsorship Mandate

All content generated across blog posts and video specifications includes the required non-sponsorship disclosure:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

---

## 🛠️ Repository Architecture

```text
├── docs/
│   └── google_flow_spec_guidelines.md  # Video prompt specs, framing, lighting, & timing
├── scripts/
│   ├── ide_guide_agent_skill.py        # CLI agent skill for on-demand IDE content generation
│   └── generate_daily_content.py       # Daily generator script & catalog manager
├── content/
│   ├── history.json                    # Tracking history to avoid repeating recent IDEs
│   └── YYYY-MM-DD/                     # Dated output folders containing posts & video specs
├── .github/workflows/
│   └── daily_content_generation.yml    # Daily cron workflow at 21:30 UTC (03:00 AM IST)
├── tests/                              # Pytest suite verifying AMP HTML & generator logic
└── README.md
```

---

## ⚡ Agentic CLI Skill Usage

You can generate custom AMP HTML blog posts and Google Flow video specs on demand using the CLI tool:

### 1. Generate by IDE Name
```bash
python3 scripts/ide_guide_agent_skill.py --ide "Cursor" --output-dir "./custom_output"
```

### 2. Generate by Repository URL
```bash
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed" --output-dir "./custom_output"
```

### 3. Generate Specific Format Only
```bash
# Output AMP HTML blog post only
python3 scripts/ide_guide_agent_skill.py --ide "Neovim" --format amp-blog

# Output Google Flow video specification only
python3 scripts/ide_guide_agent_skill.py --ide "Neovim" --format video-spec
```

---

## 📅 Daily Automation Engine

To manually run the daily generator (which selects 3 fresh IDEs, generates posts/specs, and updates `content/history.json`):

```bash
python3 scripts/generate_daily_content.py
```

The GitHub Actions workflow (`.github/workflows/daily_content_generation.yml`) runs this daily at **21:30 UTC** (**03:00 AM IST**).

---

## 🎥 Google Flow Video Prompt Standards

For video generation guidelines, framing (9:16 vs 16:9), lighting specs, camera motions, and scene timing matrices, refer to [`docs/google_flow_spec_guidelines.md`](docs/google_flow_spec_guidelines.md).

---

## 🧪 Testing & Verification

Run the unit test suite to verify AMP HTML validity, history tracking, and agent CLI execution:

```bash
PYTHONPATH=. pytest tests/
```
