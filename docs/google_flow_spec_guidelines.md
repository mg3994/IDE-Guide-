# Google Flow Video Spec Guidelines for IDE Guide (@IDEguide)

This document defines the prompt engineering standards, visual framing, camera direction, lighting setup, audio specifications, and script structures used to generate high-converting YouTube videos and Shorts for IDE Guide using Google Flow and video AI generation tools.

---

## 1. Overview & Channel Mission

- **Channel:** IDE Guide ([@IDEguide](https://www.youtube.com/@IDEguide))
- **Blog:** [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- **Target Audience:** Software developers, engineers, DevOps specialists, computer science students, and technology enthusiasts seeking objective IDE/Code Editor reviews.
- **Content Frequency:** 3 videos per day (Shorts & Long-form) alongside 3 daily AMP HTML blog posts.
- **Mandatory Disclaimer:**
  > "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."

---

## 2. Video Format Specifications

### A. YouTube Shorts (Vertical 9:16)
- **Duration:** 45 to 60 seconds
- **Resolution:** 1080x1920 (9:16 vertical aspect ratio)
- **Target Pacing:** Fast, dynamic scene cuts every 2-4 seconds.
- **Structure:**
  1. **Hook (0-5s):** High-impact visual scene and problem statement (e.g., "Is VS Code still king in 2026?").
  2. **Core Breakdown (5-45s):** Key pros, cons, performance benchmark comparison, and free vs. paid tier details.
  3. **Verdict & CTA (45-60s):** Final recommendation, link to blog review, and prompt to subscribe to @IDEguide.

### B. Long-Form Video (Horizontal 16:9)
- **Duration:** 3 to 8 minutes
- **Resolution:** 3840x2160 (4K) or 1920x1080 (1080p 16:9 aspect ratio)
- **Structure:**
  1. **Intro & Hook (0-30s):** Overview of the IDE, setup, and evaluation criteria.
  2. **Feature Deep-Dive & UX (30s - 3m):** Interface tour, code autocompletion speed, extension ecosystem, memory footprint.
  3. **Pros & Cons Matrix (3m - 5m):** Objective analysis of strengths and flaws.
  4. **Pricing & Licensing (5m - 6m):** Free community tier vs. commercial licenses.
  5. **Final Verdict & Disclaimer (6m - end):** Summary rating, target audience fit, non-sponsorship disclosure.

---

## 3. Google Flow Prompt Engineering & Scene Specs

When crafting visual prompts for Google Flow video generation, use structured scene blocks with specific parameters:

### Visual Prompt Structure Template:
```text
[Subject & Action] + [Camera Shot & Angle] + [Lighting & Aesthetic] + [Color Palette & Tone] + [Render Quality & Engine Specs]
```

### Camera Angles & Shot Types:
- **Macro Close-Up:** Syntactically highlighted code on OLED monitor display, 85mm lens, f/1.4 shallow depth of field, subtle motion blur.
- **Over-the-Shoulder (OTS):** Developer seated at ergonomic desk typing on mechanical keyboard, glowing dual-monitor setup, cinematic 35mm view.
- **Dynamic Pan & Zoom:** Smooth horizontal tracking shot across IDE UI elements (terminal, debugger, file explorer).
- **Split Screen / Comparison Shot:** Side-by-side visual comparison of Editor A vs Editor B displaying resource consumption gauges.

### Lighting & Atmosphere:
- **Cyberpunk / Dark Developer Theme:** Deep obsidian backgrounds (#0f172a), neon blue (#38bdf8) and violet (#a855f7) accent rim lighting, ambient soft glow.
- **Clean Tech Studio:** Minimalist natural soft light (5500K daylight balance), neutral grey desk surfaces, frosted glass aesthetics.

### Audio & Voice Specs:
- **Voiceover Style:** Energetic, authoritative, articulate technical host (warm tone, moderate pacing ~150 WPM).
- **Background Music:** Lo-Fi synthwave or energetic modern tech electronic track ducked at -18dB during voiceover.

---

## 4. Script & Visual Flow Spec Output Format

Every generated Google Flow video spec file (`video_spec_*.json` / `video_spec_*.md`) must include:

1. **Metadata Header:** Title, target platform, resolution, estimated duration, IDE evaluated.
2. **Required Non-Sponsorship Disclaimer.**
3. **Scene-by-Scene Breakdown:**
   - Scene Number & Timestamp
   - Visual Prompt (optimized for Google Flow)
   - Voiceover Script (Word-for-word text)
   - On-Screen Graphic / Text Overlay Specs
   - Audio Cue / SFX
