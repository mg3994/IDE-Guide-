# IDE Guide Automated Content Generation System

Automation engine and agentic tools for **IDE Guide** ([https://ideguide.blogspot.com/](https://ideguide.blogspot.com/) & [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)).

## Features
- **Daily Content Generation**: Automatically discovers and generates 3 daily content packages containing:
  - Valid AMP (Accelerated Mobile Pages) HTML blog posts for Blogger.
  - Comprehensive Google Flow Video Generation specifications and scripts for YouTube videos & Shorts.
- **Agentic CLI Skill**: Generate custom AMP blog posts and Google Flow video specs on-demand by IDE name or GitHub repository URL.
- **Strict AMP Compliance**: Valid AMP HTML boilerplate, responsive layout, `<amp-img>` tags, and schema.org structured data.
- **Google Flow Video Standards**: Detailed prompt specifications, camera angles, lighting, timing, and visual cues for video synthesis models.
- **Non-Sponsorship Compliance**: Automated inclusion of non-sponsorship disclaimers across all generated content.

## Quick Start

### Run Agentic Skill CLI
Generate custom content package for any IDE or repository:
```bash
python3 scripts/ide_guide_agent_skill.py --ide "Cursor" --price-model "Freemium"
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed"
```

### Run Daily Content Generator
Generate the daily batch of 3 IDE packages:
```bash
python3 scripts/generate_daily_content.py
```

### Running Tests
Run the test suite:
```bash
PYTHONPATH=. pytest tests/
```

## Documentation
See [`docs/google_flow_spec_guidelines.md`](docs/google_flow_spec_guidelines.md) for full video prompt and AMP HTML specifications.
