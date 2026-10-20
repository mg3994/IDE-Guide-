# IDE Guide Content Generator & Agentic Skills

Automation toolkit and agentic skills for generating daily AMP HTML blog posts (for [ideguide.blogspot.com](https://ideguide.blogspot.com/)) and Google Flow video specifications (for [YouTube @IDEguide](https://www.youtube.com/@IDEguide)).

## Features

- **Daily Automated Content (3x Videos & 3x Blog Posts)**: Generates 3 complete AMP HTML blog posts and 3 Google Flow video/shorts specifications daily.
- **AMP HTML Compliance**: All blog posts strictly adhere to AMP HTML rules for Blogger, verified by `scripts/amp_validator.py`.
- **Google Flow Specs**: Comprehensive video prompts including visual cues, framing, lighting, camera angles, voiceover scripts, and audio directions.
- **Agentic CLI Skill**: CLI tool (`scripts/ide_guide_agent_skill.py`) to generate custom AMP blog posts and Google Flow video specs on demand for any IDE or repository.
- **Independent & Objective**: Enforces non-sponsorship disclaimers across all generated content.

## Repository Structure

```
.
├── docs/
│   ├── amp_blogger_guidelines.md
│   └── google_flow_spec_guidelines.md
├── scripts/
│   ├── amp_validator.py
│   ├── generate_daily_content.py
│   └── ide_guide_agent_skill.py
├── content/
│   ├── history.json
│   └── YYYY-MM-DD/
├── tests/
│   ├── test_amp_validator.py
│   ├── test_daily_content.py
│   └── test_agent_skill.py
└── .github/workflows/
    └── daily_content_generation.yml
```

## CLI Usage

### 1. Validate AMP HTML Content
```bash
python3 scripts/amp_validator.py content/2026-10-20/post_1_vscode.html
```

### 2. Run Daily Content Generator
```bash
python3 scripts/generate_daily_content.py
```

### 3. Agentic CLI Skill (Custom IDE / Repo)
```bash
python3 scripts/ide_guide_agent_skill.py --ide "Cursor" --output-dir "content/custom"
```

## Running Tests
```bash
PYTHONPATH=. pytest tests/
```
