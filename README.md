# IDE Guide Content Engine & Agentic Skills

This repository serves as the content generator and agentic skill suite for [IDE Guide on Blogger](https://ideguide.blogspot.com/) and [@IDEguide on YouTube](https://www.youtube.com/@IDEguide).

## Channel & Publication Links
- **Blogger Website (AMP HTML Posts)**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- **YouTube Channel (Videos & Shorts)**: [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)

---

## Features

1. **AMP (Accelerated Mobile Pages) Blogger Validation**:
   - Every generated blog post strictly complies with AMP HTML specifications (`<!doctype html>`, `<html ⚡>`, `<meta charset="utf-8">`, inlined amp-custom CSS ≤ 75KB, and `<amp-img>` / `<amp-youtube>` tags).
   - Validation script (`scripts/amp_validator.py`) ensures compliance before publication.

2. **Google Flow Video Specifications**:
   - Generates visual video creation specs tailored for Google Flow / Veo / AI video generation tools.
   - Includes scene-by-scene visual prompts, camera framing, lighting, on-screen text overlays, voiceover scripts, and background audio prompts.

3. **Daily Content Pipeline (3 Videos & 3 Posts Daily)**:
   - Evaluates code editors and IDEs (e.g. VS Code, Cursor, Neovim, Zed, IntelliJ IDEA, PyCharm, Sublime Text, Fleet, Windsurf).
   - Details pros, cons, paid vs. free breakdown, and target developer recommendations.
   - Saves daily packages into dated folders (`content/YYYY-MM-DD/`).
   - Tracks covered IDEs in `content/history.json` to avoid duplicate coverage across runs.

4. **Agentic CLI Skill Tool**:
   - On-demand custom generator (`scripts/ide_guide_agent_skill.py`) for custom IDEs or newly released developer tools.

5. **Mandatory Non-Sponsorship Disclaimer**:
   - Every post and video specification includes the required non-sponsorship disclosure:
   > "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."

---

## Usage Instructions

### 1. Daily Content Generation
Generate 3 daily AMP blog posts and 3 Google Flow video specifications:
```bash
python3 scripts/generate_daily_content.py
```

### 2. Custom Agentic Skill
Generate AMP post and video specs on-demand for any custom editor:
```bash
python3 scripts/ide_guide_agent_skill.py --ide "Eclipse" --pricing "Free & Open Source" --pros "Rich plugin ecosystem; Java focus" --cons "Outdated UI; Heavy memory footprint"
```

### 3. Validate AMP HTML
Check any HTML file against AMP rules:
```bash
python3 scripts/amp_validator.py content/2026-10-04/post_1_vs_code.html
```

### 4. Run Test Suite
Run unit tests for content generation and AMP validation:
```bash
PYTHONPATH=. pytest tests/
```

---

## Documentation
- [AMP Blogger Guidelines](docs/amp_blogger_guidelines.md)
- [Google Flow Video Prompt Guidelines](docs/google_flow_spec_guidelines.md)
