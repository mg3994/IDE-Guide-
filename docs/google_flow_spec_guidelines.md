# Google Flow Video Generation Specification Guidelines - IDE Guide

## Overview
This document outlines the standard specifications for generating video prompts, scripts, and scene-by-scene visual instructions for **Google Flow** (and other AI video synthesis tools like Veo / Sora) for [IDE Guide YouTube Channel (@IDEguide)](https://www.youtube.com/@IDEguide).

We produce 3 videos per day (a mix of YouTube Shorts / Vertical 9:16 and Long-form horizontal 16:9 videos).

## Google Flow Visual Prompt Structure
To ensure high-quality, engaging visual output in Google Flow, each scene visual prompt must specify:
1. **Subject & Environment**: High-tech developer desk, glowing monitors, code editors with syntax highlighting, sleek futuristic dark mode interfaces.
2. **Camera Motion**: Smooth pan, macro zoom on code cursor, dynamic orbit, slow dolly forward.
3. **Lighting & Atmosphere**: Cyberpunk cyan/purple ambient LEDs, soft cinematic key lighting, shallow depth of field (f/1.8).
4. **Style Keywords**: "4K cinematic, ultra-detailed developer workstation, sleek modern UI, hyper-realistic lighting, 60fps smooth render".

## Video Script Components
Every generated video spec JSON/Markdown document must contain:
1. **Metadata**:
   - `title`: Catchy title optimizing YouTube search CTR
   - `format`: `YouTube Shorts (9:16)` or `Horizontal Video (16:9)`
   - `target_ide`: The IDE / Editor being reviewed
   - `pricing`: Free / Paid / Freemium tag
   - `description`: Full YouTube description with timestamps and blog link (`https://ideguide.blogspot.com/`)
   - `tags`: High ranking YouTube tags
2. **Scene-by-Scene Breakdown**:
   - `scene_number`: Integer
   - `timecode`: e.g. `0:00 - 0:05`
   - `visual_prompt`: Specific prompt fed directly to Google Flow tool
   - `camera_movement`: e.g. "Slow dolly-in towards terminal screen"
   - `onscreen_text`: Key bold callouts overlaid on screen
   - `voiceover_script`: Conversational, clear, engaging audio narration script
   - `audio_cues`: Background track vibe, sound effects (whoosh, keypress clicks)
3. **Mandatory Non-Sponsorship Disclaimer**:
   - Spoken in voiceover and included in description:
     *"IDE Guide is strictly independent and not sponsored by any software vendor."*

## Scene Flow Pattern (3 Videos / Day)
- **Video 1 (Short/Reel)**: Rapid 30-Second Comparison (e.g. "VS Code vs Cursor AI: Which should you choose in 2025?")
- **Video 2 (In-Depth Review)**: 3 to 5 Minute Deep Dive on a specific IDE (Pros, Cons, Free vs Paid features, Live workflow demo prompts)
- **Video 3 (Short/Reel)**: "Top 3 Hidden Features of [IDE Name]" or "Is [IDE Name] Worth Paying For?"
