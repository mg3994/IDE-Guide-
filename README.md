# IDE Guide Agentic Platform

Automated daily content engine and agentic tools for [IDE Guide](https://ideguide.blogspot.com/) (Blogger) and [@IDEguide](https://www.youtube.com/@IDEguide) (YouTube).

This project generates **3 daily content packages** (3 AMP HTML blog posts and 3 Google Flow AI video generation specifications) covering code editors and IDEs across free, paid, and freemium tiers.

---

## 🌟 Key Features

1. **AMP (Accelerated Mobile Pages) Post Generator**:
   - Strictly validated HTML compliant with Blogger AMP requirements (`<style amp-boilerplate>`, `<amp-img>`, clean semantic sections).
   - Validated automatically via `scripts/amp_validator.py`.

2. **Google Flow AI Video Specification Generator**:
   - Structured JSON prompt specs tailored for text-to-video / image-to-video tools (Google Flow, Veo, Sora, etc.).
   - Includes prompt camera movements, framing, visual effects, lighting, voiceover scripts, and on-screen text overlays.
   - Supports 16:9 widescreen YouTube reviews and 9:16 vertical YouTube Shorts.

3. **Strict Non-Sponsorship Disclaimer Enforcement**:
   - Every blog post and video spec guarantees objective evaluation and includes the mandatory disclaimer:
     > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

4. **Agentic CLI Skill Tool**:
   - Generate custom AMP blog posts and Google Flow video specs on-demand for any custom IDE name or repo URL.

---

## 🚀 Quick Start

### 1. Generate Daily Content (3 Blog Posts + 3 Video Specs)
```bash
python3 scripts/generate_daily_content.py
```
Output files will be saved in `content/YYYY-MM-DD/` and recorded in `content/history.json`.

### 2. Validate AMP HTML Content
```bash
python3 scripts/amp_validator.py content/2026-03-30/vscode_blog_post.html
```

### 3. Run Agentic Skill for On-Demand Content
```bash
python3 scripts/ide_guide_agent_skill.py \
  --name "Cursor AI" \
  --pricing "Freemium ($20/mo Pro)" \
  --developer "Anysphere" \
  --category "AI Code Editor" \
  --primary-use "AI-Assisted Coding" \
  --aspect-ratio 16:9 \
  --output-dir content/custom
```

---

## 🧪 Testing

Run the full test suite with pytest:

```bash
PYTHONPATH=. pytest tests/
```

---

## 📁 Repository Structure

```
.
├── .github/workflows/
│   └── daily_content_generation.yml   # Scheduled GitHub Action (Runs at 21:30 UTC / 03:00 AM IST)
├── docs/
│   ├── amp_blogger_guidelines.md       # AMP HTML standards for Blogger
│   └── google_flow_spec_guidelines.md  # Video generation prompt specs & standards
├── scripts/
│   ├── amp_validator.py               # AMP compliance & disclaimer validator
│   ├── generate_daily_content.py      # Daily content engine (3 posts + 3 video specs)
│   └── ide_guide_agent_skill.py       # On-demand agentic CLI tool
├── tests/                             # Pytest unit test suite
├── content/                           # Generated daily and custom content output
└── README.md                          # Repository documentation
```
