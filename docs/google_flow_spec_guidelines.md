# Google Flow & Video Generation Specifications Guidelines

This document outlines the guidelines, prompt formats, visual framing, and script structures for generating video prompts and specs (for Google Flow, AI video tools, and YouTube Shorts / Long-form videos) for [@IDEguide on YouTube](https://www.youtube.com/@IDEguide).

## 1. Visual & Audio Specifications for Google Flow / AI Video Generators

To produce high-quality, engaging visuals for YouTube Shorts (9:16 vertical) and YouTube Videos (16:9 widescreen), every video prompt specification must define:

1. **Aspect Ratio & Resolution**:
   - Shorts: `9:16` vertical video prompt specs.
   - Standard YouTube Video: `16:9` widescreen prompt specs.

2. **Framing & Camera Angles**:
   - *Cinematic Macro*: Close-up of glowing code editor dark themes, syntax highlighting, animated cursors, IDE UI elements.
   - *Over-the-shoulder*: Developer typing at a sleek minimalist workstation with ambient rgb lighting.
   - *Split-screen / Comparison*: Side-by-side IDE comparison shots.

3. **Lighting & Aesthetic Style**:
   - Cyberpunk dark-mode / sleek tech studio lighting.
   - Neon accent lighting (blue, purple, cyan, emerald) reflecting developer theme aesthetics.

4. **Tone & Narration Voice**:
   - Dynamic, authoritative, objective, and clear developer voiceover.
   - Fast-paced for YouTube Shorts (under 60 seconds), articulate and structured for long-form tutorials.

## 2. Daily Video Content Structure (3 Daily Shorts / Videos)

Each daily video specification generated must include:

1. **Title & Target Tool**: Name of the IDE/Code Editor reviewed.
2. **Hook (0-5s)**: High-energy question or statement catching developer interest.
3. **Core Review (5-45s)**:
   - Standout Features & Workflow highlights.
   - Pros & Cons breakdown.
   - Free vs. Paid status clearly declared.
4. **Recommendation / Call to Action (45-55s)**: Who should choose this IDE.
5. **Mandatory Audio/Visual Disclaimer (55-60s)**:
   - Spoken / Visual On-Screen Text: "Disclaimer: IDE Guide is an independent publication. Not sponsored or affiliated with any IDE vendor."

## 3. Google Flow Prompt Output Specification

For each video, a structured prompt JSON or Markdown file is generated containing:
- `prompt_visual_scenes`: Detailed text descriptions for text-to-video AI tools (Google Flow, Runway, Pika, Sora).
- `narration_script`: Word-for-word voiceover script with timing.
- `on_screen_text`: Text overlays for key highlights, pricing badges, and disclaimers.
- `audio_cues`: Sound effects (key clicks, swooshes, ambient tech synth).
