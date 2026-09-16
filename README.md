# IDE Guide Engine & Agentic Skills 🚀

Automated content generation suite for **IDE Guide**
- **YouTube Channel**: [@IDEguide](https://www.youtube.com/@IDEguide)
- **Blogger Website**: [ideguide.blogspot.com](https://ideguide.blogspot.com/)

---

## Features

1. **3 Daily AMP Blog Posts & 3 Video Specifications**:
   - Generates 3 Blogger-compatible AMP HTML blog posts per day with clean responsive layouts, pricing tables, pros/cons, and channel links.
   - Generates 3 scene-by-scene AI video specifications (JSON & Markdown) optimized for **Google Flow** and video generators for both 16:9 YouTube video formats and 9:16 Shorts formats.
   - Rotates through a comprehensive catalog of code editors & IDEs (VS Code, Cursor, JetBrains IntelliJ, Neovim, Zed, Windsurf, PyCharm, Xcode, Android Studio, etc.) tracking history in `content/history.json`.

2. **Agentic CLI Skill Tool (`scripts/ide_guide_agent_skill.py`)**:
   - Enables on-demand generation of AMP blog posts and Google Flow video specs for any specific editor, tool, or repository name.

3. **Non-Sponsorship & Neutrality Standard**:
   - All generated articles, scripts, and video specs automatically include the required non-sponsorship disclosure:
   > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

4. **GitHub Actions Automation**:
   - Automatically scheduled daily at 21:30 UTC (03:00 AM IST) via `.github/workflows/daily_content_generation.yml`.

---

## Usage

### 1. Run Daily Content Generation
To generate the 3 blog posts and 3 Google Flow specs for today:
```bash
python3 scripts/generate_daily_content.py
```
To generate for a specific date:
```bash
python3 scripts/generate_daily_content.py 2026-09-18
```
Generated content is stored in `content/YYYY-MM-DD/`.

### 2. Use the Agentic CLI Skill
To generate AMP HTML and Google Flow video specs for a specific IDE or editor on demand:
```bash
python3 scripts/ide_guide_agent_skill.py --name "Helix Editor" --pricing "100% Free Open Source"
```

---

## Running Tests

Execute the full suite of unit tests with `pytest`:
```bash
PYTHONPATH=. pytest tests/
```

---

## Documentation
- **Google Flow Video Guidelines**: See [`docs/google_flow_spec_guidelines.md`](docs/google_flow_spec_guidelines.md) for prompt engineering standards, aspect ratio rules, and camera directives.
