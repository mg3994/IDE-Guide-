# IDE Guide - Content Generation & Agentic Automation Engine

Welcome to the **IDE Guide** official automation repository. This system automatically generates daily AMP (Accelerated Mobile Pages) HTML blog posts for our Blogger site and visual AI video specifications (for **Google Flow** and AI video creation tools) for our YouTube channel.

* **YouTube Channel:** [@IDEguide](https://www.youtube.com/@IDEguide)
* **Blogger Website:** [ideguide.blogspot.com](https://ideguide.blogspot.com/)
* **Publishing Frequency:** 3 Content Packages Daily (3 Blog Posts + 3 Videos/Shorts)

---

## 🚀 Key Capabilities

1. **AMP HTML Blog Posts (For Blogger):**
   - Strictly validated `<html ⚡>` AMP markup optimized for instant mobile loading on Blogger.
   - Microdata JSON-LD schemas (`TechArticle`) for SEO indexation.
   - In-depth technical breakdown: Pros vs Cons, Key Architecture, Pricing Model (Free vs Paid), and Target Developer Recommendations.
2. **Google Flow Video Specifications (For YouTube Shorts & Videos):**
   - Scene-by-scene prompts for AI video tools like **Google Flow**.
   - Prescribes camera movement (macro zooms, pans), studio lighting (dark mode, neon blue/teal accents), exact voiceover scripts, caption overlays, and audio cues.
3. **Agentic Skill Tool CLI:**
   - On-demand generation for custom IDE names or GitHub repo URLs (`scripts/ide_guide_agent_skill.py`).
4. **Mandatory Non-Sponsorship Disclaimer:**
   - Automatically included in all posts and specs to guarantee 100% independent evaluation.

---

## 🛠 Project Layout

```text
.
├── docs/
│   └── google_flow_spec_guidelines.md  # Detailed prompt engineering guidelines for Google Flow
├── scripts/
│   ├── generate_daily_content.py       # Core generator for 3 daily content packages
│   └── ide_guide_agent_skill.py        # Agentic CLI tool for custom on-demand queries
├── content/                            # Dated output packages (e.g. content/2026-08-28/)
│   └── history.json                    # History tracker preventing repeated IDE coverage
├── tests/
│   └── test_content_generator.py       # Comprehensive unit test suite
└── .github/
    └── workflows/
        └── daily_content_generation.yml # Scheduled GitHub Actions workflow (21:30 UTC)
```

---

## 💻 Usage & Workflows

### 1. Generating 3 Daily Content Packages

Run the daily generator script:
```bash
python3 scripts/generate_daily_content.py
```
Options:
* `--date YYYY-MM-DD`: Override date target.
* `--dry-run`: Generate files without updating `content/history.json`.
* `--force`: Allow selecting IDEs even if already covered.

Output saved to `content/YYYY-MM-DD/`:
* `post_1_<ide_slug>.amp.html` (Blogger AMP Post)
* `video_1_<ide_slug>_flow_spec.json` (Google Flow Machine Spec)
* `video_1_<ide_slug>_flow_spec.md` (Google Flow Readable Prompt Guide)
* *(Repeated for posts & videos 2 and 3)*

### 2. Agentic Skill CLI (On-Demand Content Generation)

To generate an AMP blog post and Google Flow video spec for any custom IDE or GitHub repo URL:

```bash
# By IDE Name
python3 scripts/ide_guide_agent_skill.py --ide "Cursor"

# By GitHub Repository URL
python3 scripts/ide_guide_agent_skill.py --repo-url "https://github.com/zed-industries/zed"

# By Custom Topic
python3 scripts/ide_guide_agent_skill.py --topic "Cursor vs Zed vs VS Code" --output-dir "my_output"
```

---

## 🧪 Running Unit Tests

Execute the unit test suite to verify AMP validation and script integrity:

```bash
python3 -m unittest discover -s tests
```

---

## 🤖 GitHub Actions Schedule

The repository includes an automated workflow `.github/workflows/daily_content_generation.yml` scheduled to run every day at **21:30 UTC** (**03:00 AM IST**). It runs tests, generates 3 fresh content packages, and commits the output into `content/`.

---

## ⚖️ Non-Sponsorship Disclaimer

All generated blog posts and video specifications include the exact mandatory non-sponsorship statement:

> **Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.**
