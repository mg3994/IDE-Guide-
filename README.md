# IDE Guide: Daily Content Generator & Agentic Tools

Automated content generation engine and agentic CLI skills for [IDE Guide on YouTube (@IDEguide)](https://www.youtube.com/@IDEguide) and [Blogger (ideguide.blogspot.com)](https://ideguide.blogspot.com/).

## Features

- **Daily Content Generator**: Generates 3 full daily content packages (3 AMP HTML blog posts for Blogger and 3 Google Flow video specifications for YouTube) covering various IDEs and code editors.
- **AMP HTML Compliance**: Validates blog post output against AMP (Accelerated Mobile Pages) standards for fast mobile rendering on Blogger.
- **Google Flow Specs**: Provides detailed visual prompts, framing, lighting, camera motion, on-screen overlays, and narration scripts optimized for AI video tools like Google Flow.
- **Agentic CLI Tool**: On-demand CLI skill (`scripts/ide_guide_agent_skill.py`) to generate custom AMP blog posts and Google Flow video specs for any specified IDE or GitHub repository URL.
- **History Tracking**: Tracks generated content in `content/history.json` to prevent repetitive coverage across automated daily runs.
- **Non-Sponsorship Disclaimer**: Ensures all generated content carries the mandatory objective non-sponsorship disclaimer.

## Repository Structure

```
.
├── docs/
│   ├── amp_blogger_guidelines.md      # AMP HTML formatting guidelines for Blogger
│   └── google_flow_spec_guidelines.md # Video prompt, framing, and script standards
├── scripts/
│   ├── amp_validator.py              # AMP HTML compliance validator
│   ├── generate_daily_content.py     # Main daily 3x package generator
│   └── ide_guide_agent_skill.py      # Agentic CLI skill for custom IDE generation
├── content/
│   ├── history.json                  # History log of generated tools and dates
│   └── YYYY-MM-DD/                   # Daily output folders
├── tests/                             # Unit test suite
└── .github/workflows/
    └── daily_content_generation.yml  # Daily GitHub Actions workflow (21:30 UTC / 03:00 AM IST)
```

## Quick Start

### Running Daily Generator
```bash
python3 scripts/generate_daily_content.py
```

### Using Agentic CLI Tool
```bash
python3 scripts/ide_guide_agent_skill.py --ide "Visual Studio Code"
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/neovim/neovim"
```

### Validating AMP Content
```bash
python3 scripts/amp_validator.py --file content/2026-03-31/vscode_blogpost.html
```

### Running Tests
```bash
PYTHONPATH=. pytest tests/
```
