# IDE Guide: Automated Multi-Platform Content Engine

> **Blogger Website:** [ideguide.blogspot.com](https://ideguide.blogspot.com/)
> **YouTube Channel:** [@IDEguide](https://www.youtube.com/@IDEguide)

IDE Guide is an independent technical publication and media brand dedicated to objective, deep-dive reviews, comparisons, and workflow benchmarks of software engineering tools, integrated development environments (IDEs), and code editors.

---

## 🚀 Purpose & Content Cadence

Every single day, this automated agentic engine produces:
1. **3 AMP-Compliant Blog Posts** (for Blogger HTML editor or API).
2. **3 Google Flow Video Packages** (16:9 full feature & 9:16 YouTube Shorts specifications, prompts, voiceover scripts, and metadata).

Each post and video covers:
- **The Good (Standout Strengths)**: Developer ergonomics, speed, key extensions, and AI features.
- **The Bad (Critical Drawbacks)**: Memory bloat, telemetry, indexing lag, or configuration hurdles.
- **Pricing Breakdown**: Explicitly clarifying whether the tool is Free, Open-Source (FOSS), Freemium, or Paid Commercial.
- **Target Audience Guidance**: Exact developer persona the editor is best suited for.
- **Mandatory Non-Sponsorship Disclaimer**: Every review strictly includes an independent editorial disclaimer:
  > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

---

## 📁 Repository Structure

```text
├── .github/
│   └── workflows/
│       └── daily_content_generation.yml # Daily cron workflow (21:30 UTC / 03:00 AM IST)
├── content/
│   ├── history.json                     # History tracker preventing redundant coverage
│   └── YYYY-MM-DD/
│       ├── blog_posts/                  # Daily AMP HTML posts for Blogger
│       └── google_flow_videos/          # 16:9 and 9:16 Google Flow prompt & script specs
├── data/
│   ├── __init__.py
│   └── ide_database.py                  # Catalog of modern IDEs with rich metadata
├── docs/
│   ├── amp_blogger_guidelines.md        # Blogger AMP standards and validation rules
│   └── google_flow_spec_guidelines.md   # Google Flow video prompt formulas & visual cues
├── scripts/
│   ├── amp_validator.py                 # AMP post body validation utility
│   ├── generate_daily_content.py        # 3x daily generation orchestrator
│   └── ide_guide_agent_skill.py         # On-demand CLI agent skill for any IDE/repo
└── tests/
    ├── test_amp_validator.py            # AMP compliance tests
    ├── test_content_generation.py       # Daily pipeline & history tests
    └── test_agent_skill.py              # CLI skill tests
```

---

## 🛠️ Usage Instructions

### 1. Generating 3 Daily Content Packages Automatically

Run the daily generator script:
```bash
python3 scripts/generate_daily_content.py
```
This inspects `content/history.json`, selects the next 3 un-covered IDEs, and outputs the packages to `content/YYYY-MM-DD/`.

### 2. Using the Agentic Skill CLI (On-Demand Generation)

Generate a complete AMP blog post and Google Flow video specifications for any specific IDE:

```bash
# View all pre-configured IDEs in the catalog
python3 scripts/ide_guide_agent_skill.py --list-catalog

# Generate content for a cataloged IDE
python3 scripts/ide_guide_agent_skill.py --ide "Cursor" --output-dir custom_output/

# Generate content for an arbitrary new editor / repository URL
python3 scripts/ide_guide_agent_skill.py --ide "Lapce" --repo-url "https://github.com/lapce/lapce"
```

### 3. Uploading Blog Posts to Blogger (AMP)

1. Navigate to [Blogger Dashboard](https://www.blogger.com/) for `ideguide.blogspot.com`.
2. Click **New Post**.
3. In the post composer, toggle the left dropdown from **Compose view** to **HTML view**.
4. Copy the entire HTML content from the generated file (e.g. `content/YYYY-MM-DD/blog_posts/01_cursor_amp_post.html`) and paste it into the editor.
5. All styling, layout, structured comparison sections, and the non-sponsorship disclaimer are embedded and verified for AMP Blogger compatibility.

### 4. Creating Videos in Google Flow & AI Video Generators

1. Open the generated video specification JSON (e.g. `content/YYYY-MM-DD/google_flow_videos/01_cursor_flow_spec_16x9.json` or `_shorts_9x16.json`).
2. Input the `master_aesthetic_prompt` into Google Flow or your AI video generator tool.
3. For each scene (Hook, The Good, The Bad, Pricing & Verdict), utilize the exact `flow_visual_prompt` and `voiceover` text.
4. Export the resulting 60fps video and upload to `@IDEguide` using the provided title, description, tags, and disclaimer.

---

## 🧪 Testing

Execute the test suite to verify AMP compliance, generator history, and CLI agent skills:
```bash
PYTHONPATH=. pytest tests/
```
