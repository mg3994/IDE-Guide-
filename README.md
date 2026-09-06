# IDE Guide Content Generation Hub 🚀

Automated content generation pipeline for **IDE Guide**:
* **Blogger Website**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/) (AMP Accelerated Mobile Pages HTML)
* **YouTube Channel**: [@IDEguide](https://www.youtube.com/@IDEguide) (Google Flow Visual Video Generation Specs for Shorts & Longform)

---

## 📌 Daily Cadence
* **Frequency**: 3 Videos per day + 3 Blog Posts per day.
* **Automated Schedule**: GitHub Actions workflow runs daily at `21:30 UTC` (03:00 AM IST).
* **Non-Sponsorship Policy**: All content includes the standard non-sponsorship disclaimer:
  > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

---

## 🛠 Features

1. **AMP HTML Generator (`scripts/generate_daily_content.py`)**:
   - Generates Blogger-compliant Accelerated Mobile Pages HTML files.
   - Includes custom CSS, boilerplate tags, key features, pros/cons breakdown, and pricing details (Free, Paid, Freemium).
2. **Google Flow Video Spec Generator**:
   - Generates structured JSON visual prompts, camera motions, studio lighting setups, and narration scripts for Google Flow and AI video tools.
   - Supports both 9:16 Shorts (Vertical) and 16:9 Longform (Horizontal).
3. **Agentic CLI Skill (`scripts/ide_guide_agent_skill.py`)**:
   - On-demand CLI skill tool for agents or creators to quickly generate AMP blog posts & Google Flow video specifications for any IDE or repository name.
4. **History Tracker (`content/history.json`)**:
   - Automatically tracks covered IDEs to prevent repeated reviews.

---

## 💻 Quick Start & CLI Skill Usage

### 1. Run Daily Content Generation
To manually generate today's batch of 3 AMP blog posts and 3 Google Flow video specs:
```bash
python3 scripts/generate_daily_content.py
```
Generated content will be placed in `content/YYYY-MM-DD/`.

### 2. Run Agentic Skill for Custom IDE
Generate an AMP blog post and Google Flow video spec for a specific IDE or tool on demand:
```bash
python3 scripts/ide_guide_agent_skill.py --ide "Windsurf Editor" --pricing "Freemium" --category "AI Code Editor" --output-dir "./custom_output"
```

### 3. Run Unit Tests
To run the automated test suite verifying AMP boilerplate compliance, non-sponsorship disclaimers, and CLI skill execution:
```bash
pytest tests/
```

---

## 📂 Repository Structure

```
├── .github/workflows/
│   └── daily_content_generation.yml   # Scheduled workflow (21:30 UTC)
├── docs/
│   └── google_flow_spec_guidelines.md # Video spec guidelines for Google Flow
├── scripts/
│   ├── generate_daily_content.py      # Main daily generator script
│   └── ide_guide_agent_skill.py       # Agentic CLI skill tool
├── tests/
│   └── test_content_generation.py     # Unit test suite
└── content/
    ├── history.json                   # History tracking for covered tools
    └── YYYY-MM-DD/                    # Output directory for daily packages
```
