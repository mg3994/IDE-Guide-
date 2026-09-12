# IDE Guide Content Generator & Agentic Tools

Automated content generation pipeline and agentic CLI skills for **IDE Guide**:
- **Blogger Site**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- **YouTube Channel**: [@IDEguide](https://www.youtube.com/@IDEguide)

---

## 🚀 Features

1. **Agentic CLI Skill (`scripts/ide_guide_agent_skill.py`)**:
   - Generates AMP (Accelerated Mobile Pages) HTML blog posts specifically designed for Blogger publishing.
   - Generates Google Flow video creation specifications (prompts, scene breakdowns, voiceover scripts, framing, lighting) for YouTube & YouTube Shorts.
   - Evaluates IDE key features, pros (good), cons (bad), pricing model (free/paid/freemium), recommendation, and includes mandatory non-sponsorship disclaimers.

2. **Daily Content Automated Generator (`scripts/generate_daily_content.py`)**:
   - Generates 3 unique blog posts and 3 video specs every single day.
   - Saves daily packages into dated directories (`content/YYYY-MM-DD/`).
   - Maintains `content/history.json` to prevent repeating previously covered IDEs and discover new/trending text editors via GitHub APIs.

3. **Scheduled Automation (`.github/workflows/daily_content_generation.yml`)**:
   - Runs automatically every day at 21:30 UTC (03:00 AM IST) via GitHub Actions.
   - Executes unit tests and commits the daily content package to the repo.

4. **Google Flow Video Specifications (`docs/google_flow_spec_guidelines.md`)**:
   - Detailed visual style standards, lighting parameters, prompt engineering structures, and script templates for video creation tools.

---

## 🛠️ Usage

### Running the Agentic CLI Skill
Generate content for any specific IDE or repository on demand:

```bash
# By IDE Name
python3 scripts/ide_guide_agent_skill.py --ide "Cursor IDE" --pricing "Freemium ($20/mo)" --output-dir "output/"

# By GitHub Repository URL
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed" --output-dir "output/"
```

### Running Daily Content Generation Manually
To trigger generation of today's 3 blog posts and 3 video specs:

```bash
python3 scripts/generate_daily_content.py
```

---

## 🧪 Running Unit Tests

Run the test suite using `pytest`:

```bash
pytest tests/
```

Tests verify:
- AMP HTML compliance (valid boilerplate, tags, inline CSS constraints).
- Mandatory non-sponsorship disclaimer inclusion.
- Google Flow video prompt and script structures.
- History tracking and non-repetitive IDE selection.

---

## ⚖️ Non-Sponsorship Disclaimer

> **Disclaimer**: *IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.*
