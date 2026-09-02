# IDE Guide Content Generator & Agentic Tools

Automated content generation engine and agentic tools for **IDE Guide**.

- **Blogger Website**: [ideguide.blogspot.com](https://ideguide.blogspot.com/) (AMP HTML Blog Posts)
- **YouTube Channel**: [@IDEguide](https://www.youtube.com/@IDEguide) (Google Flow Video & Shorts Specs)

---

## 📌 Features

1. **Daily Automation (3 Posts + 3 Videos Daily)**:
   - Automatically generates 3 AMP HTML blog posts tailored for Blogger and 3 Google Flow video specification files for YouTube daily.
   - Outputs generated packages in `content/YYYY-MM-DD/`.
   - Tracks previously covered IDEs in `content/history.json` to prevent repetitive content.

2. **AMP HTML Compliance**:
   - Generates fully valid AMP (Accelerated Mobile Pages) HTML structures with AMP boilerplates, optimized inline styles (`amp-custom`), dark themes, and responsive design for fast mobile indexing on Blogger.

3. **Google Flow Video & Shorts Specifications**:
   - Provides cinematic prompts (camera framing, 8K dark workstation aesthetic, neon lighting accents, macro UI focus) for Google Flow and AI video tools.
   - Formatted for both 9:16 vertical YouTube Shorts and 16:9 horizontal main YouTube videos.
   - Includes timestamps, camera movement directives, and structured voiceover scripts (~140 words/min).

4. **Agentic CLI Skill Tool (`scripts/ide_guide_agent_skill.py`)**:
   - Enables on-demand generation of AMP blog posts and Google Flow video specs for custom IDE names or GitHub repository URLs.

5. **Non-Sponsorship Disclaimer**:
   - Includes the exact non-sponsorship disclaimer across all generated blog posts and video specifications to maintain editorial independence:
   > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

---

## 🛠️ Quick Start & CLI Usage

### 1. Run Daily Content Generation Engine
```bash
python3 scripts/generate_daily_content.py
```

### 2. Use the Agentic CLI Skill Tool

Generate content for a specific IDE:
```bash
python3 scripts/ide_guide_agent_skill.py --ide "Zed" --category "High-Performance Rust Editor" --pricing "100% Free & Open Source" --out-dir ./custom_output
```

Generate content from a GitHub repository URL:
```bash
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/lapce/lapce" --out-dir ./lapce_output
```

---

## 🧪 Testing & Validation

Run the test suite using `pytest`:
```bash
pytest tests/
```

---

## 📁 Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── daily_content_generation.yml # Scheduled GitHub Actions workflow (21:30 UTC / 03:00 AM IST)
├── content/
│   ├── history.json                      # Tracking state for covered IDEs
│   └── YYYY-MM-DD/                       # Daily generated AMP blog posts & video specs
├── docs/
│   └── google_flow_spec_guidelines.md    # Visual, framing & prompt rules for Google Flow
├── scripts/
│   ├── generate_daily_content.py         # Daily content generation engine
│   └── ide_guide_agent_skill.py         # Agentic CLI tool for custom IDE/repo content
├── tests/
│   └── test_content_generation.py        # Pytest test suite
└── README.md
```
