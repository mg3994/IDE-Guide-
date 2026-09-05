# Google Flow Video Generation Specification & Guidelines

This document outlines the visual, prompt, framing, lighting, and script specifications for generating AI videos and YouTube Shorts for **IDE Guide** (`https://www.youtube.com/@IDEguide`).

---

## 1. Overview & Objectives

**IDE Guide** produces daily video specs and content packages covering code editors, IDEs, and developer extensions. Each daily release covers 3 tools per day across 3 video scripts and 3 AMP HTML blog posts.

### Primary Channels
- **YouTube Channel**: [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide)
- **Blogger Site**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)

---

## 2. Google Flow Video Prompt Standards

When generating prompts for Google Flow (and related AI video generation tools), prompts must adhere to standard visual and cinematographic constraints to ensure high audience engagement, crisp UI visualization, and strong visual appeal.

### Visual Style & Aesthetic
- **Environment**: Modern tech workstation, clean dark-mode setup, subtle RGB backlight, minimalist mechanical keyboard, high-resolution monitor displaying code editor interface.
- **Lighting**: Soft cinematic key light (5600K cool daylight) balanced with ambient teal/magenta accent neon backlight.
- **Color Grading**: High contrast, crisp dark mode theme, vibrant syntax highlighting accent colors (cyan, gold, purple).
- **Framing & Aspect Ratios**:
  - **Shorts / Reels (Vertical)**: `9:16` aspect ratio, centered close-up on UI features, clear readable typography overlays.
  - **Longform Video (Horizontal)**: `16:9` widescreen, dynamic camera pans over code editor windows and feature demos.
- **Camera Movement**: Slow cinematic tracking shot, slow zoom into AI code completions, macro close-up on status bars and extensions.

---

## 3. Video Script & Structure Requirements

Each video specification generated for an IDE must contain the following timed elements:

1. **Hook (0-5s)**: High-energy problem statement or feature spotlight (e.g., "Is this AI editor better than VS Code?").
2. **Overview & Interface (5-15s)**: Visual showcase of the IDE interface, speed, theme, and architecture.
3. **Key Features & Strengths (15-35s)**: Top pros, unique AI features, extensions, language support, or performance benchmarks.
4. **Drawbacks & Cons (35-45s)**: Honest evaluation of memory usage, ecosystem gaps, or learning curves.
5. **Paid vs Free Breakdown (45-55s)**: Pricing tier analysis (Open Source, Free Tier, Pro Subscription pricing).
6. **Final Verdict & Recommendation (55-60s)**: Clear target audience guidance (e.g., "Best for Rust developers", "Ideal for quick web editing").
7. **Non-Sponsorship Disclaimer**: Explicitly rendered in script and visual overlay.

---

## 4. Mandatory Non-Sponsorship Disclaimer

All video specifications and narration scripts **must** include the following exact disclaimer text:

> `Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.`

---

## 5. Sample Google Flow Spec JSON Output Format

When generated via `scripts/generate_daily_content.py` or `scripts/ide_guide_agent_skill.py`, Google Flow specifications follow this schema:

```json
{
  "title": "IDE Guide: Is Cursor the Ultimate AI Code Editor?",
  "target_platform": "YouTube Shorts / Longform (@IDEguide)",
  "aspect_ratio": "9:16",
  "ide_name": "Cursor",
  "pricing_model": "Freemium (Free tier available, Pro $20/mo)",
  "pros": ["Native Claude 3.5 Sonnet integration", "Fork of VS Code - supports all extensions"],
  "cons": ["Requires subscription for unlimited AI requests", "Closed source core"],
  "recommendation": "Best for developers wanting deeply integrated AI pair programming.",
  "visual_prompts": {
    "lighting": "Cinematic dark mode desk setup, 5600K key light, subtle cyan neon background ambient glow.",
    "camera_motion": "Slow zoom into code autocomplete popup, panning shot across dark UI.",
    "framing": "Vertical 9:16 aspect ratio, macro close-up of code editor window."
  },
  "narration_script": [
    {"timestamp": "00:00-00:05", "visual": "Close-up of AI inline code generation", "audio": "Can Cursor really replace VS Code?"},
    ...
  ],
  "disclaimer": "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
}
```
