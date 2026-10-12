# IDE Guide Content Engine & Agentic Skills 🚀

[![Daily IDE Guide Content Generation](https://github.com/mg3994/IDE-Guide-/actions/workflows/daily_content_generation.yml/badge.svg)](https://github.com/mg3994/IDE-Guide-/actions/workflows/daily_content_generation.yml)

Automated content generation engine and agentic skills for **IDE Guide**:
- 🌐 **Blogger Website:** [ideguide.blogspot.com](https://ideguide.blogspot.com/)
- 📺 **YouTube Channel:** [@IDEguide](https://www.youtube.com/@IDEguide)

---

## 📌 Features

1. **Daily Automated Content (3 Videos + 3 Blog Posts Every Day):**
   - Scheduled via GitHub Actions daily at **21:30 UTC / 03:00 AM IST**.
   - Rotates through popular, emerging, and niche IDEs & code editors without duplicate repeats (`content/history.json`).
   - Output structured into dated directories: `content/YYYY-MM-DD/`.

2. **AMP (Accelerated Mobile Pages) HTML Blog Posts for Blogger:**
   - Strict AMP HTML compliance validator (`scripts/amp_validator.py`).
   - Clean, mobile-friendly styles and responsive design.
   - Comprehensive sections: *Overview*, *The Good (Pros)*, *The Bad (Cons)*, *Pricing breakdown*, and *Final Verdict*.

3. **Google Flow Video & Shorts Specifications:**
   - Standardized scene-by-scene visual prompts for **Google Flow**, Runway, Sora, and ElevenLabs AI tools.
   - Includes cinematic lighting, camera motion, precise voiceover timing, and text overlay banners.

4. **Agentic CLI Skill Tool:**
   - On-demand generation of AMP blog posts and Google Flow video specs for any IDE, editor, or repository URL.

5. **Mandatory Non-Sponsorship Disclaimer:**
   Every generated video spec and blog post includes the exact non-sponsorship disclosure:
   > *Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.*

---

## 🛠️ Installation & Setup

```bash
# Clone repository
git clone https://github.com/mg3994/IDE-Guide-.git
cd IDE-Guide-

# Run tests
PYTHONPATH=. pytest tests/
```

---

## 🤖 Usage Guide

### 1. Daily Automated Generator
Generate 3 daily AMP blog posts and 3 video specs:
```bash
PYTHONPATH=. python3 scripts/generate_daily_content.py
```
Or for a specific date:
```bash
PYTHONPATH=. python3 scripts/generate_daily_content.py 2026-08-26
```

### 2. Agentic CLI Skill Tool (On-Demand Content Generation)
Generate custom content for any IDE (e.g., Cursor, Windsurf, Neovim, Zed):
```bash
# Print output to console
PYTHONPATH=. python3 scripts/ide_guide_agent_skill.py --ide "Cursor"

# Save outputs directly to files
PYTHONPATH=. python3 scripts/ide_guide_agent_skill.py \
  --ide "Windsurf" \
  --out-blog content/windsurf_blog.html \
  --out-video content/windsurf_video.json
```

### 3. Validate AMP HTML Compliance
```bash
python3 scripts/amp_validator.py content/2026-08-26/blog_1_cursor.html
```

---

## 📂 Project Structure

```
.
├── .github/workflows/
│   └── daily_content_generation.yml  # GitHub Actions Daily Automation
├── content/
│   ├── history.json                   # Tracked history pool to avoid duplicate selections
│   └── YYYY-MM-DD/                    # Output directory for 3 daily videos & 3 daily blogs
├── docs/
│   ├── amp_blogger_guidelines.md      # AMP HTML requirements for Blogger
│   └── google_flow_spec_guidelines.md # Video spec & prompt guidelines for Google Flow
├── scripts/
│   ├── amp_validator.py               # AMP compliance & disclaimer validator
│   ├── generate_daily_content.py      # Daily content runner
│   └── ide_guide_agent_skill.py       # Agentic CLI skill tool
└── tests/
    └── test_content_generation.py     # Unit test suite
```

---

## ⚖️ Disclaimer
IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
