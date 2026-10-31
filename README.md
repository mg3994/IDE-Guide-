# IDE Guide Content Generation Suite

[![Daily IDE Guide Content Generation](https://github.com/mg3994/IDE-Guide-/actions/workflows/daily_content_generation.yml/badge.svg)](https://github.com/mg3994/IDE-Guide-/actions/workflows/daily_content_generation.yml)

Automated Agentic Content Engine producing daily Accelerated Mobile Pages (AMP) HTML blog posts and Google Flow video generation specs for:
- **Blogger Publication:** [ideguide.blogspot.com](https://ideguide.blogspot.com/)
- **YouTube Channel:** [@IDEguide](https://www.youtube.com/@IDEguide)

---

## 🌟 Channel & Brand Mission

**IDE Guide** is an independent technical publication and video channel providing candid, objective reviews of developer environments, AI-first code editors, modal text tools, and enterprise IDEs.

Every single review covers:
1. **The Good**: Unique superpowers, speed, language servers, AI composer integration.
2. **The Bad**: System memory consumption, telemetry, configuration friction, proprietary vendor lock-in.
3. **Pricing Tier**: Explicit classification of **100% Free / Open-Source**, **Freemium**, or **Commercial / Paid**.
4. **Who It's Best For**: Precise developer persona recommendations.
5. **Editorial Independence Guarantee**:
   > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

---

## 📁 Repository Structure

```
├── .github/workflows/
│   └── daily_content_generation.yml   # Scheduled daily at 21:30 UTC (03:00 AM IST)
├── content/                           # Generated daily packages (history.json & dated folders)
│   └── YYYY-MM-DD/
│       ├── post_1_{ide}_amp_blogger.html
│       ├── video_1_{ide}_google_flow_spec.json
│       └── script_1_{ide}_voiceover.md
├── data/
│   └── ide_database.json              # Knowledgebase of IDEs (pros, cons, pricing, links)
├── docs/
│   ├── amp_blogger_guidelines.md      # Strict AMP HTML rules for Blogger post bodies
│   └── google_flow_spec_guidelines.md # Video prompts, pacing, framing & Shorts guidelines
├── scripts/
│   ├── amp_validator.py               # AMP compliance and disclaimer validator
│   ├── ide_guide_agent_skill.py       # Agentic CLI skill for custom on-demand reviews
│   └── generate_daily_content.py      # Daily pipeline generating 3 posts + 3 videos
└── tests/                             # Comprehensive automated test suite
```

---

## 🚀 Quickstart & Usage

### 1. Run the Daily Pipeline (3 Posts + 3 Videos)
Generates 3 full packages (3 AMP blog posts, 3 Google Flow JSON specs, 3 Voiceover markdown scripts) in `content/YYYY-MM-DD/` and updates `content/history.json` so no editor is unnecessarily repeated:

```bash
python3 scripts/generate_daily_content.py
```

To backfill or test for a specific date:
```bash
python3 scripts/generate_daily_content.py 2025-02-15
```

### 2. On-Demand Review via Agentic Skill CLI
Generate custom AMP HTML and Google Flow specs for any editor in the database or an ad-hoc new tool:

```bash
python3 scripts/ide_guide_agent_skill.py --ide "Cursor" --outdir my_reviews/
python3 scripts/ide_guide_agent_skill.py --ide "Windsurf" --outdir my_reviews/
python3 scripts/ide_guide_agent_skill.py --ide "Zed" --outdir my_reviews/
```

### 3. Validate AMP HTML Compliance
Ensure that any blog post HTML meets Blogger AMP standards and includes the mandatory disclaimer:

```bash
python3 scripts/amp_validator.py content/2025-02-15/post_1_cursor_amp_blogger.html
```

### 4. Run Automated Tests
```bash
PYTHONPATH=. pytest tests/
```

---

## ⚡ Accelerated Mobile Pages (AMP) for Blogger
All generated blog posts are formatted as clean, content-only HTML snippets:
- Zero raw `<script>` tags or disallowed attributes (no inline `style=""` or `onclick`).
- Fully responsive CSS scoped under `<style amp-custom>`.
- Responsive AMP image/video tag specifications.
- Copy and paste directly into Blogger's HTML post editor without broken layout shifts.

---

## 🎥 Google Flow & Generative Video Engine
The video specs (`*_google_flow_spec.json`) and scripts (`*_voiceover.md`) provide:
- **Cinematic Google Flow Prompts**: Lighting, camera motion, macro keycaps, code rendering.
- **Shorts Pacing**: Rapid cuts every 2.5–3.5s designed for 9:16 vertical retention.
- **Full Video Coverage**: 16:9 widescreen B-roll suggestions and UI comparisons.
- **Auditory SFX Cues**: Whooshes, cash registers on pricing, chord hits on cons.
