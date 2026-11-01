# IDE Guide — Automated Content & Agentic Publishing Platform

[![Daily IDE Guide Content Generation](https://github.com/mg3994/IDE-Guide-/actions/workflows/daily_content_generation.yml/badge.svg)](https://github.com/mg3994/IDE-Guide-/actions/workflows/daily_content_generation.yml)

Official automated content publishing repository for:
- 🌐 **Blogger Publication**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- 🎥 **YouTube Channel**: [@IDEguide](https://www.youtube.com/@IDEguide)

---

## 🚀 Mission & Scope

**IDE Guide** publishes **3 daily in-depth reviews and comparisons** covering modern integrated development environments (IDEs), code editors, and AI coding assistants:
1. **3 Blogger Posts Every Day**: Strictly compliant with **AMP (Accelerated Mobile Pages)** standards, optimized for mobile readers with responsive styling, `<amp-img>` elements, and no disallowed scripts.
2. **3 Video / Shorts Specs Every Day**: Structured for generative video tools like **Google Flow**, including scene-by-scene visual framing, lighting, camera motions, narration audio scripts, and YouTube metadata.
3. **Objective & Independent**: Clear breakdowns of pros, cons, target audience, and free vs. paid pricing tiers.
4. **Mandatory Non-Sponsorship Disclosure**: Every post and script contains our strict independence declaration:
   > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

---

## 📂 Repository Structure

```text
├── .github/
│   └── workflows/
│       └── daily_content_generation.yml # Daily scheduled automation (21:30 UTC / 03:00 AM IST)
├── content/
│   ├── history.json                     # Rotation history preventing repeated coverage
│   └── YYYY-MM-DD/                      # Daily generated assets
│       ├── post_1_<editor>_amp.html      # AMP HTML post ready for Blogger
│       ├── video_1_<editor>_flow_spec.json # Google Flow video prompt & script
│       ├── post_2_...
│       └── ...
├── data/
│   └── ide_database.json                # Structured catalog of IDEs, pricing, pros/cons
├── docs/
│   ├── amp_blogger_guidelines.md        # Blogger AMP HTML rules and standards
│   └── google_flow_spec_guidelines.md   # Google Flow video prompt & script standards
├── scripts/
│   ├── amp_validator.py                 # AMP validator utility
│   ├── generate_daily_content.py        # Daily batch generator for 3 posts & 3 videos
│   └── ide_guide_agent_skill.py         # Agentic CLI skill for on-demand synthesis
└── tests/                               # Test suite for validation, generator & database
```

---

## 🛠️ Usage & Agentic Skills

### 1. Run Daily Content Generator (Batch of 3)
Generates 3 AMP blog posts and 3 video specs under `content/YYYY-MM-DD/`:
```bash
python3 scripts/generate_daily_content.py
# Or for a specific date:
python3 scripts/generate_daily_content.py 2026-11-01
```

### 2. On-Demand Agentic CLI Skill
Use the agentic skill to synthesize custom content for any IDE:
```bash
# List all cataloged editors
python3 scripts/ide_guide_agent_skill.py --list

# Synthesize Blogger AMP post and Google Flow video spec for an editor
python3 scripts/ide_guide_agent_skill.py --name "Cursor" --out-dir ./output

# Synthesize for Zed or Neovim
python3 scripts/ide_guide_agent_skill.py --name "Zed"
```

### 3. Validate AMP HTML
Ensure any generated or custom Blogger HTML adheres to AMP standards:
```bash
python3 scripts/amp_validator.py content/2026-11-01/post_1_cursor_amp.html
```

### 4. Run Test Suite
Run the automated test suite:
```bash
PYTHONPATH=. pytest tests/
```

---

## 🎨 Google Flow Video Prompt Structure

Each generated video specification contains 5 coordinated scenes designed for Google Flow:
1. **Scene 1 (Hook)**: Dynamic macro push-in on code syntax with rim lighting.
2. **Scene 2 (Superpower)**: Demonstration of the editor's primary strength with smooth camera tracking.
3. **Scene 3 (Red Flags)**: Realistic critique of resource usage or limitations with high-contrast warning cues.
4. **Scene 4 (Pricing & Verdict)**: Glassmorphic rating breakdown (Free vs. Paid details).
5. **Scene 5 (CTA & Disclosure)**: Call to subscribe to `@IDEguide`, visit `ideguide.blogspot.com`, and the mandatory non-sponsorship disclosure.

---

## 📄 License & Attribution

All content, scripts, and workflows are provided under the MIT License. Published reviews remain independent and unaffiliated with referenced software vendors.
