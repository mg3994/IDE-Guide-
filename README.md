# IDE Guide Content Generator & Agentic Skill Pipeline

[![IDE Guide Blog](https://img.shields.io/badge/Blogger-ideguide.blogspot.com-FF5722?style=flat&logo=blogger)](https://ideguide.blogspot.com/)
[![YouTube Channel](https://img.shields.io/badge/YouTube-@IDEguide-FF0000?style=flat&logo=youtube)](https://www.youtube.com/@IDEguide)

Automated content generation system and agentic skills for **IDE Guide** — covering IDEs, code editors, AI programming assistants, pros & cons, pricing models (Free vs Paid), developer suitability, and objective reviews.

---

## Content Engine Specifications

### 1. Daily Quota
- **3 AMP HTML Blog Posts / Day** published for [ideguide.blogspot.com](https://ideguide.blogspot.com/)
- **3 Video & Shorts Specs / Day** formatted for AI video generation tools like Google Flow for [@IDEguide YouTube](https://www.youtube.com/@IDEguide)

### 2. Blogger AMP (Accelerated Mobile Pages) Compliance
All generated blog posts adhere strictly to the AMP HTML standard required for Blogger optimization:
- Uses `<html ⚡>` or `<html amp>` markup tag.
- AMP boilerplate JS (`https://cdn.ampproject.org/v0.js`) and `<style amp-boilerplate>`.
- Responsive layout with `<amp-img>` instead of standard `<img>` tags.
- Custom inline styling contained in `<style amp-custom>`.
- Structured metadata (JSON-LD `TechArticle` / `Review`).
- Validated via built-in AMP validator tool.

### 3. Google Flow Video Specifications
Videos and YouTube Shorts scripts are generated with detailed scene-by-scene prompts for AI video tools:
- Specific visual prompts (cybernetic dark mode, high-contrast code UI, glowing cursor accents).
- Camera motion instructions (pan, macro close-up, push-in zoom).
- Scene durations and spoken narration script.
- On-screen typography and overlay text.
- Formatted as structured JSON and Markdown specs under `docs/google_flow_spec_guidelines.md`.

### 4. Non-Sponsorship Disclaimer
Every post and video script includes the explicit independent evaluation disclaimer:
> **Disclaimer**: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

---

## Directory Structure

```
.
├── .github/
│   └── workflows/
│       └── daily_content_generation.yml    # GitHub Actions workflow (21:30 UTC daily)
├── content/
│   ├── history.json                       # Record of covered IDEs to prevent duplicate posts
│   └── YYYY-MM-DD/                        # Daily generated blog posts and video specs
│       ├── ide_1_blog_post.amp.html
│       ├── ide_1_google_flow_video.json
│       ├── ide_2_blog_post.amp.html
│       ├── ide_2_google_flow_video.json
│       ├── ide_3_blog_post.amp.html
│       └── ide_3_google_flow_video.json
├── docs/
│   └── google_flow_spec_guidelines.md    # Video prompt engineering standards
├── scripts/
│   ├── generate_daily_content.py          # Daily 3x3 content generator script
│   └── ide_guide_agent_skill.py           # CLI tool for on-demand generation & AMP validation
└── tests/                                 # Pytest test suite
```

---

## Usage Instructions

### Using the Agentic CLI Skill (`scripts/ide_guide_agent_skill.py`)

Generate a single AMP blog post and Google Flow video spec on demand for any IDE or GitHub repository:

```bash
# Generate content for a specific IDE
python3 scripts/ide_guide_agent_skill.py generate --ide "Cursor" --output-dir ./output

# Generate content from a GitHub repository URL
python3 scripts/ide_guide_agent_skill.py generate --repo "https://github.com/zed-industries/zed" --output-dir ./output

# Validate an existing HTML file for AMP compliance
python3 scripts/ide_guide_agent_skill.py validate-amp --file ./output/cursor_blog_post.amp.html
```

### Running Daily Content Generation (`scripts/generate_daily_content.py`)

Generate 3 blog posts and 3 video specs for today:

```bash
python3 scripts/generate_daily_content.py
```

Options:
- `--date YYYY-MM-DD`: Specify target date for content generation directory.
- `--force`: Re-generate content even if today's directory already exists.

---

## Running Tests

Run the test suite using `pytest`:

```bash
pytest tests/
```
