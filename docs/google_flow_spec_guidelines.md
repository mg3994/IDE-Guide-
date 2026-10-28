# Google Flow & Visual Video Specification Guidelines for IDE Guide

This document defines the specification guidelines for generating video visual prompts, scene breakdowns, camera/lighting framing, and audio scripts tailored for Google Flow and video tools for YouTube (@IDEguide).

## Channel Profile & Objective
- **Channel**: IDE Guide (`https://www.youtube.com/@IDEguide`)
- **Cadence**: 3 videos per day (Shorts / Long-form video specs).
- **Core Focus**: IDEs, Code Editors, Developer Tooling comparisons, Pros vs. Cons, Free vs. Paid analysis.
- **Independence Statement**: All video specifications must embed an explicit disclaimer confirming unbiased evaluation without vendor sponsorship.

## Google Flow Prompt & Visual Specifications

### 1. Scene Structure & Visual Prompts
Each video spec generation must break down into structured scenes:

- **Intro / Hook Scene (0:00 - 0:05)**:
  - *Visual*: Dynamic 3D render or cinematic screen view of the IDE interface glowing on a modern developer workstation.
  - *Camera*: Slow push-in or wide-to-close tracking shot.
  - *Lighting*: Neon ambient accent lighting (cyan/purple code editor vibe) with dark background studio aesthetic.

- **Feature & Strengths Scene (The Good) (0:05 - 0:15)**:
  - *Visual*: Close-up Macro view of fast syntax highlighting, instant auto-completion / AI code generation in action.
  - *Camera*: Pan left-to-right across code viewport.
  - *Lighting*: High-contrast studio lighting highlighting screen detail.

- **Drawbacks & Performance Scene (The Bad) (0:15 - 0:25)**:
  - *Visual*: Visual indicator or UI overlay showing resource usage (RAM/CPU) or complex menu setup.
  - *Camera*: Dynamic overhead angle or tilted close-up.
  - *Lighting*: Warm warning tint overlay or subtle contrast shift.

- **Pricing & Tier Scene (Free vs. Paid) (0:25 - 0:35)**:
  - *Visual*: Clean dual-pane side-by-side graphical card displaying "Free Tier" vs "Pro/Paid Features".
  - *Camera*: Static centered composition with animated text cues.

- **Verdict & Outro Scene (0:35 - 0:45)**:
  - *Visual*: Final verdict badge, recommendation score card, YouTube subscribe prompt overlay.
  - *Lighting*: Clean neutral daylight studio setup.

### 2. Audio & Voiceover Script Rules
- **Tone**: Professional, clear, engaging, developer-to-developer.
- **Pacing**: Fast-paced (~140-160 words per minute for Shorts / concise specs).
- **Mandatory Audio Disclaimer**:
  > "IDE Guide is independent and not sponsored by any editor vendor. All reviews are 100% developer-focused."

### 3. Google Flow Prompt Formatting Schema
```json
{
  "title": "IDE / Editor Video Title",
  "ide_name": "Editor Name",
  "pricing": "Free / Paid / Freemium",
  "scenes": [
    {
      "scene_id": 1,
      "duration_seconds": 5,
      "google_flow_prompt": "Cinematic shot of [IDE] workspace, dark studio, glowing code syntax, 4k ultra realistic, highly detailed UI, cyber aesthetic",
      "camera_angle": "4K macro lens, smooth zoom in",
      "lighting": "Volumetric neon rim lighting",
      "voiceover_script": "Is [IDE] worth your time in 2026? Let's break down the good, the bad, and the pricing."
    }
  ],
  "disclaimer": "IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
}
```
