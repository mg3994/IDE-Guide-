# Google Flow & AI Video Spec Guidelines for IDE Guide

This document defines the prompt, script, and visual layout specifications for AI video generators (e.g., Google Flow, Runway, Sora, Pika, HeyGen) used by **IDE Guide** for YouTube Shorts and YouTube Long-form videos (`https://www.youtube.com/@IDEguide`).

## 1. Daily Video Strategy & Specifications

IDE Guide publishes 3 videos daily accompanying the 3 daily blog posts.

- **Video Format:**
  - **YouTube Shorts / Reels (9:16 vertical, 1080x1920):** Fast-paced 60-second IDE summary highlight.
  - **YouTube Video / Walkthrough (16:9 widescreen, 1920x1080):** Comprehensive 3-5 minute IDE deep dive.
- **Visual Style:** Modern dark-mode UI aesthetics, crisp developer workspaces, macro mechanical keyboard shots, glowing neon syntax highlighting, smooth pan and zoom transitions.

## 2. Google Flow Prompt & Scene Structure

Each video spec JSON/YAML or Markdown output generated for Google Flow must contain the following components:

### A. Scene Breakdown Table
Every video is structured into distinct timed scenes (e.g., 0-5s, 5-15s, 15-35s, 35-50s, 50-60s).

Each scene includes:
- **Timestamp / Duration:** Exact timing.
- **Visual Prompt (Google Flow format):** Cinematic, detailed AI generation prompt specifying subject, camera motion, lighting, and resolution.
- **Camera Movement:** E.g., Slow track forward, macro pan across code, rack focus on error highlight.
- **Voiceover Script:** Word-for-word spoken transcript.
- **On-Screen Text Overlay:** Key highlights (e.g., "FREE vs PAID", "PROS & CONS", "BEST FOR PYTHON").
- **Audio & Sound Effects (SFX):** Keystroke SFX, swoosh transitions, ambient chill synth background music.

### B. Free vs. Paid & Ideal Developer Profile
Clear callout in both narration and visual overlay specifying:
- Pricing category (100% Open Source Free, Freemium, Paid / Commercial).
- Recommended developer persona (e.g., "Best for Flutter Developers", "Ideal for Low-Memory Machines").

### C. Standard Google Flow Prompt Syntax
Prompts generated for Google Flow should adhere to the format:
`[Subject/Scene] + [Camera Motion] + [Lighting & Color Palette] + [Resolution & Style]`

*Example:*
> "Macro cinematic shot of a developer's dark mode editor displaying high-tech Python code with vibrant neon syntax highlighting, camera slowly dolly zooms forward into the cursor, soft ambient blue and purple LED backlight, 4k resolution, hyper-realistic."

## 3. Mandatory Non-Sponsorship Audio & Visual Disclaimer

Every video script must include an on-screen visual overlay and spoken disclaimer at the closing scene:

- **On-Screen Text:** "Independent Review • Not Sponsored"
- **Spoken Narration / End Card:** "IDE Guide is independent and not sponsored by any editor vendor. Subscribe for unbiased developer tools guides!"
