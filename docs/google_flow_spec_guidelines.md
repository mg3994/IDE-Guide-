# Google Flow Video Specification Guidelines for IDE Guide

This document defines the prompt standards, timing, visual layout, and audio specifications for generating YouTube videos and Shorts for **IDE Guide** ([@IDEguide](https://www.youtube.com/@IDEguide)) using **Google Flow** and AI video tools.

---

## 1. Overview & Content Goal

IDE Guide produces 3 daily developer video packages (Shorts & Standard YouTube videos) analyzing code editors and IDEs (e.g., VS Code, Cursor, JetBrains IntelliJ, Neovim, Zed, Windsurf, PyCharm, Xcode).

Every video specification generated MUST contain:
1. **Title & Video Meta**: Format (Shorts 60s vs Standard 3min), duration, target audience.
2. **Google Flow Scene Prompts**: Frame-by-frame AI video prompts structured with visual depth, lighting, camera motion, and camera angles.
3. **Voiceover Script & Audio Timing**: Precise timestamps matching visual scene transitions.
4. **On-Screen Graphics (GFX)**: Code overlays, UI highlights, pros/cons badges, and Free vs Paid pricing badges.
5. **Non-Sponsorship Disclaimer**: Mandated audio and visual disclaimer.

---

## 2. Google Flow Prompting Structure

For each scene in the video, a Google Flow prompt specification must follow this JSON-like or structured key-value format:

```json
{
  "scene_number": 1,
  "duration_seconds": 5,
  "flow_prompt": "Ultra-realistic 4K close-up shot of a modern dark-mode IDE interface featuring glowing syntax highlighting in neon cyan and magenta. Smooth slow cinematic zoom towards AI autocomplete prompt popup.",
  "camera": "Subtle push-in zoom, 35mm lens, f/2.8 depth of field",
  "lighting": "Volumetric ambient glow from screen onto minimalist dark desk background",
  "on_screen_text": "CURSOR vs VS CODE: WHICH IS BETTER?",
  "voiceover": "Is Cursor actually replacing VS Code in 2026? Let's break down the truth in 60 seconds."
}
```

---

## 3. Visual & Style Guidelines

- **Theme**: Dark mode developer aesthetic (`#0f172a` deep background, neon accents `#38bdf8`, `#a855f7`, `#22c55e`).
- **Typography**: Clean monospace / modern sans-serif fonts (e.g., JetBrains Mono, Inter) with drop shadow for readability.
- **Framing**:
  - **YouTube Shorts (9:16)**: Vertically cropped center focus on IDE UI, code snippets, and floating pricing badges.
  - **Standard YouTube (16:9)**: Split-screen comparisons, side-by-side performance charts, full workspace overviews.
- **Pricing Indicators**:
  - `[FREE]` badge: High-visibility green badge.
  - `[PAID]` or `[FREEMIUM]` badge: High-visibility amber/purple badge with exact pricing tier details.

---

## 4. Standard Non-Sponsorship Disclaimer

Every video script and visual overlay description must include:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
