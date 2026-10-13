# IDE Guide Content Generation & Agentic Pipeline

Welcome to the **IDE Guide** content automation repository!

This system powers daily content generation and agentic skill tools for:
- **Blogger Website:** [ideguide.blogspot.com](https://ideguide.blogspot.com/)
- **YouTube Channel:** [@IDEguide](https://www.youtube.com/@IDEguide)

---

## 🚀 Key Features

1. **AMP HTML Blogger Post Generation**:
   - Generates fully compliant AMP (Accelerated Mobile Pages) HTML posts styled specifically for Blogger publishing.
   - Includes developer evaluation, paid vs free analysis, key features, pros/cons, and recommended target audience.

2. **Google Flow Video & Shorts Generation Specs**:
   - Creates video prompts and scripts tailored for AI video tools (such as Google Flow).
   - Generates both **Shorts / Reels (9:16 vertical)** and **Full YouTube Videos (16:9 horizontal)** with camera angles, visual lighting prompts, audio narration scripts, and text overlays.

3. **Daily Content Pipeline (3 Videos & 3 Blog Posts / Day)**:
   - Automated script selects 3 unreviewed IDEs/editors daily from the database and saves generated packages under `content/YYYY-MM-DD/`.
   - Prevents duplicate coverage across runs by tracking history in `content/history.json`.

4. **Agentic CLI Skill Tool**:
   - Allows on-demand content creation for any custom IDE or GitHub repository URL.

5. **Strict Non-Sponsorship Guarantee**:
   - Every post and video specification includes our mandatory non-sponsorship disclaimer:
   > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

---

## 📁 Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── daily_content_generation.yml  # GitHub Actions workflow (21:30 UTC daily)
├── data/
│   └── ide_database.json                 # Comprehensive dataset of IDEs and code editors
├── docs/
│   ├── amp_blogger_guidelines.md         # AMP HTML standards & Blogger publishing rules
│   └── google_flow_spec_guidelines.md    # Google Flow prompt structure & video specs
├── scripts/
│   ├── amp_validator.py                  # Strict AMP HTML validator tool
│   ├── generate_daily_content.py         # Daily 3x3 content generation engine
│   └── ide_guide_agent_skill.py          # Agentic CLI skill tool for custom IDEs/repos
├── content/                              # Dated generated packages (YYYY-MM-DD)
└── tests/                                # Automated unit test suite
```

---

## 🛠️ Usage Commands

### 1. Daily Content Generation (3 Posts & 3 Video Specs)
To generate today's batch of 3 AMP blog posts and 3 video specs:
```bash
PYTHONPATH=. python3 scripts/generate_daily_content.py
```

### 2. On-Demand Custom Generation (Agentic CLI Skill)
To generate an AMP post and Google Flow video spec for any custom IDE or GitHub repo URL:
```bash
PYTHONPATH=. python3 scripts/ide_guide_agent_skill.py --ide "Helix Editor" --pricing "Free / Open Source"
```

### 3. AMP Validation
To validate any generated blog post against AMP standards:
```bash
python3 scripts/amp_validator.py content/2026-10-13/blog_post_vscode.html
```

### 4. Running Tests
To run the automated test suite:
```bash
PYTHONPATH=. pytest tests/
```

---

## 🤖 Automated Schedule
Daily generation runs automatically via GitHub Actions at **21:30 UTC (03:00 AM IST)**.
