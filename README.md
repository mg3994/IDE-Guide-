# IDE Guide (`https://ideguide.blogspot.com/` & `@IDEguide`)

Welcome to the **IDE Guide** automation platform! This repository contains automated generators, AMP HTML compliance validators, and Agentic CLI skills for producing daily technical reviews, pros/cons breakdowns, and AI video production prompts (Google Flow) for code editors and IDEs.

---

## 🌟 Channel & Website Links

- **Blogger Site**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- **YouTube Channel**: [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)

---

## 🎯 Features

1. **AMP HTML Blog Posts (for Blogger)**:
   - Validated against strict Accelerated Mobile Pages (AMP) standards (no disallowed tags like `<img>`, `<script>`, inline `style="..."`).
   - Includes full pros, cons, target audience analysis, pricing breakdown (Paid vs Free), and killer features.
   - Embeds mandatory non-sponsorship disclaimer banner on every post.

2. **Google Flow Video Specifications (YouTube & Shorts)**:
   - Structured AI video prompts for Google Flow / generative AI video pipelines.
   - 60-second YouTube Shorts specifications (vertical 9:16).
   - Detailed 3-minute YouTube Video specifications (horizontal 16:9).
   - Visual scenes, camera motion, lighting effects, voiceover narration scripts, and timing markers.

3. **3 Daily Content Packages**:
   - Automatically selects 3 new IDEs or code editors daily.
   - Tracks covered tools in `content/history.json` to prevent duplicates.
   - Auto-scheduled via GitHub Actions at 21:30 UTC (03:00 AM IST).

4. **Agentic CLI Skill Tool (`scripts/ide_guide_agent_skill.py`)**:
   - On-demand custom generator for agents and users to generate AMP blog posts and Google Flow video specs for any IDE or repository URL.

5. **Mandatory Non-Sponsorship Disclaimer**:
   > **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

---

## 🚀 Getting Started

### 1. Requirements

- Python 3.10+
- `pytest` (for testing)

### 2. Generate 3 Daily Packages

To run the daily content generator manually:

```bash
PYTHONPATH=. python3 scripts/generate_daily_content.py
```

Outputs will be saved under `content/YYYY-MM-DD/`:
- `blogpost_1_<ide_name>.html`
- `video_flow_spec_1_<ide_name>.json`
- ...

### 3. Validate AMP HTML Files

To check any blog post against AMP HTML standards and disclaimer presence:

```bash
python3 scripts/amp_validator.py content/2026-10-07/blogpost_1_visual_studio_code.html
```

### 4. Agentic Skill Usage (Custom IDEs / GitHub Repos)

Generate custom AMP blog posts and Google Flow video specs for any IDE or tool on demand:

```bash
python3 scripts/ide_guide_agent_skill.py \
  --ide-name "Helix Editor" \
  --category "Terminal Modal Editor" \
  --pricing "Free & Open Source" \
  --repo-url "https://github.com/helix-editor/helix" \
  --pros "Built-in LSP,Selection first editing,Blazing fast Rust binary" \
  --cons "Modal keybindings learning curve" \
  --target_audience "Rust developers and terminal fans" \
  --killer-features "Selection-first modal editing,Built-in tree-sitter syntax highlighting" \
  --output-dir "content/custom_helix"
```

---

## 🧪 Testing

To run the complete test suite:

```bash
PYTHONPATH=. pytest tests/
```

---

## 📖 Documentation

- [AMP Blogger Guidelines](docs/amp_blogger_guidelines.md)
- [Google Flow Video Spec Guidelines](docs/google_flow_spec_guidelines.md)
