# IDE Guide Content Engine

Automated daily content generation and agentic skill suite for **IDE Guide**:
- **Blogger:** [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/) (AMP HTML Compliant)
- **YouTube Channel:** [@IDEguide](https://www.youtube.com/@IDEguide) (Google Flow Video Generation Specs)

## Purpose

IDE Guide delivers daily unbiased evaluations, comparisons, and workflows for modern IDEs, code editors, and AI coding assistants (e.g., VS Code, Cursor, Zed, JetBrains Fleet, Neovim, Windsurf, Helix).

Every day, the system generates:
- **3 AMP HTML Blog Posts:** Valid Accelerated Mobile Pages HTML articles designed specifically for Blogger publication.
- **3 Google Flow Video Specs:** Highly detailed video generation prompts (for 16:9 videos and 9:16 Shorts) complete with scene descriptions, visual framing, camera motion, lighting rules, audio voiceovers, and timestamp cues.

## Core Evaluation Standards

All generated content follows strict technical evaluation rules:
1. **Good & Bad Analysis:** Honest assessment of strengths (performance, extensions, AI features) and drawbacks (memory usage, learning curve, vendor lock-in).
2. **Pricing Transparency:** Clear indication of Free, Open Source, Freemium, or Paid licensing model.
3. **Best Use Case Recommendation:** Explicit guidance on who should use the tool (e.g., frontend developers, backend engineers, low-resource laptops, terminal power users).
4. **Mandatory Non-Sponsorship Disclaimer:**
   > *Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.*

## Repository Layout

```
.
├── docs/
│   └── google_flow_spec_guidelines.md   # Google Flow video specification standard
├── scripts/
│   ├── generate_daily_content.py        # Daily automated generator (3 posts + 3 video specs)
│   └── ide_guide_agent_skill.py         # Agentic CLI skill for custom IDE analysis
├── content/
│   ├── history.json                     # History tracking to prevent repetitive content
│   └── YYYY-MM-DD/                      # Dated daily output folders
├── tests/
│   └── test_generator.py                # Unit test suite verifying AMP & Google Flow outputs
└── .github/workflows/
    └── daily_content_generation.yml     # Daily automated workflow execution
```

## Quick Start

### 1. Run Daily Automated Content Generation
To generate the daily batch of 3 blog posts and 3 video specs:
```bash
python3 scripts/generate_daily_content.py
```

### 2. Use Agentic Skill Tool
To generate custom AMP HTML and Google Flow video specs for a specific IDE or GitHub repository:
```bash
python3 scripts/ide_guide_agent_skill.py --ide "Cursor" --type both
```

### 3. Run Unit Tests
To verify AMP validation logic and video spec generator structure:
```bash
pytest tests/
```
