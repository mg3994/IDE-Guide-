# IDE Guide Content Engine & Agentic Skills

Automated Content Generation Engine & Agentic Skills for the **IDE Guide** platform:
- 🌐 **Blogger Website:** [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- 📺 **YouTube Channel:** [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)

---

## 🎯 Purpose & Production Target
IDE Guide produces **3 daily blog posts** and **3 daily videos/shorts** evaluating developer code editors, IDEs, and AI coding tools.

Every evaluation includes:
- **Good Points (Pros):** Speed, static analysis, AI capabilities, extensions.
- **Bad Points (Cons):** Memory overhead, telemetry, licensing limits, learning curve.
- **Pricing Matrix:** Free vs Paid vs Freemium breakdown.
- **Target Audience Guidance:** Which developer role should use which IDE.
- **Visual Video Specs for AI Tools (Google Flow):** Precise scene framing, lighting, camera motion, and voiceover transcripts.
- **Non-Sponsorship Disclaimer:** Independent evaluation disclaimer included in every post and video.

---

## 🛠️ Project Architecture
```text
.
├── docs/
│   └── google_flow_spec_guidelines.md   # Specifications for Google Flow visual prompts
├── scripts/
│   ├── amp_validator.py                 # Blogger AMP HTML validator script
│   ├── ide_guide_agent_skill.py         # On-demand agentic skill tool
│   └── generate_daily_content.py        # Daily batch content generator (3 posts + 3 video specs)
├── content/                             # Dated output content packages (YYYY-MM-DD)
│   └── history.json                     # History tracker preventing repeated IDE coverage
├── tests/                               # Comprehensive unit tests
└── .github/
    └── workflows/
        └── daily_content_generation.yml # Scheduled GitHub Action workflow
```

---

## 🚀 How to Use

### 1. Generating Custom Content on Demand (Agentic Skill)
Run `scripts/ide_guide_agent_skill.py` to generate AMP HTML blog posts and Google Flow video specs for any IDE:
```bash
# Generate for Cursor IDE
python3 scripts/ide_guide_agent_skill.py --ide cursor --outdir ./output

# Generate for Zed Editor
python3 scripts/ide_guide_agent_skill.py --ide zed --outdir ./output
```

### 2. Running Daily Batch Content Generation
Generate 3 blog posts and 3 video specs for today:
```bash
python3 scripts/generate_daily_content.py
```
Or specify a custom date:
```bash
python3 scripts/generate_daily_content.py 2026-03-30
```

### 3. Validating Blogger AMP Compliance
Validate any generated HTML against Blogger AMP standards:
```bash
python3 scripts/amp_validator.py content/2026-03-30/post_1_cursor_ide_amp.html
```

---

## 🧪 Running Unit Tests
Run pytest to verify AMP compliance, Google Flow video prompt generation, and daily batch generation:
```bash
PYTHONPATH=. pytest tests/
```

---

## 📜 Non-Sponsorship Disclaimer
> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
