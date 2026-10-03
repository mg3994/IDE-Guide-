# IDE Guide Agentic Content System

Automated content generation engine and agentic tooling for **IDE Guide** publishing to:
- 🌐 **Blogger Website**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/) (AMP HTML compliant posts)
- 🎬 **YouTube Channel**: [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide) (Google Flow video specifications & scripts)

---

## 🌟 Key Features

1. **Daily 3x Content Automation**:
   - Generates 3 complete AMP HTML blog posts daily for Blogger.
   - Generates 3 Google Flow video specifications (JSON & Markdown scripts) daily for YouTube Shorts (9:16) and Landscape showcases (16:9).
   - Tracks rotation history in `content/history.json` to ensure fresh, diverse IDE coverage without repetitive posts.

2. **Strict AMP HTML Standards**:
   - Built-in validator (`scripts/amp_validator.py`) enforces strict Accelerated Mobile Pages rules (AMP runtime, `<amp-img>`, style size limits, required meta headers).

3. **Google Flow Video Specifications**:
   - Formatted visual prompts for Google Flow / Veo video generation engines.
   - Includes camera framing, lighting environment, timed shot breakdowns, voiceover scripts, and B-roll notes.

4. **Agentic Skill CLI Tool**:
   - Generate AMP posts and video specs on demand for any IDE or GitHub repository URL using `scripts/ide_guide_agent_skill.py`.

5. **Independent & Non-Sponsored**:
   - Every piece of generated content automatically includes the mandatory non-sponsorship disclaimer:
   > *Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.*

---

## 🚀 Quick Start & Usage

### 1. Run Daily Content Generation
To generate today's 3 daily content packages (or a specific date):
```bash
python3 scripts/generate_daily_content.py
# Or for a specific date:
python3 scripts/generate_daily_content.py 2026-10-01
```
Output files are saved in `content/YYYY-MM-DD/`.

### 2. Validate AMP HTML Blog Posts
Validate any HTML file against AMP standards:
```bash
python3 scripts/amp_validator.py content/2026-10-01/post_1_pycharm.html
```

### 3. Agentic Skill (On-Demand Custom Generation)
Generate custom AMP blog post and Google Flow video specs for any IDE or GitHub URL:
```bash
python3 scripts/ide_guide_agent_skill.py --name "Helix Editor" --repo "https://github.com/helix-editor/helix"
```

### 4. Running Tests
Run all unit tests using `pytest`:
```bash
PYTHONPATH=. pytest tests/
```

---

## 📁 Repository Structure

```
├── .github/workflows/
│   └── daily_content_generation.yml   # Scheduled GitHub Action (21:30 UTC / 03:00 AM IST)
├── docs/
│   ├── amp_blogger_guidelines.md       # AMP HTML requirements for Blogger posts
│   └── google_flow_spec_guidelines.md # Google Flow video specification rules
├── scripts/
│   ├── amp_validator.py               # AMP compliance checker utility
│   ├── generate_daily_content.py      # Daily generator & IDE database
│   └── ide_guide_agent_skill.py       # Agentic CLI skill tool
├── content/                           # Daily generated content output
│   └── history.json                   # Covered IDE tracking history
└── tests/
    └── test_content_generator.py      # Unit test suite
```
