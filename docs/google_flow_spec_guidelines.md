# Google Flow & Visual Video Specification Guidelines (IDE Guide)

This document specifies the format and structure for video generation specifications targeting YouTube (@IDEguide).

## 1. Video Types & Specifications
- **Shorts (Vertical - 9:16)**: Duration ~45 to 60 seconds. High pacing, quick hooks, visual overlays, clear call to action.
- **Full Video / Showcase (Landscape - 16:9)**: Duration 3 to 8 minutes. Comprehensive review, split screen demonstrations, detailed breakdown of pros/cons and workflow integration.

## 2. Google Flow Video Prompt & Spec Structure
Every video specification file (`.json` and `.md`) must contain structured fields for Google Flow video tools:

### JSON Structure (`video_spec_*.json`)
- `metadata`:
  - `title`: Catchy video title.
  - `channel`: `@IDEguide`
  - `format`: `Shorts (9:16)` or `Landscape (16:9)`
  - `target_ide`: IDE name (e.g. VS Code, Cursor, Neovim)
  - `duration_seconds`: Target length (e.g. 60)
- `google_flow_prompts`:
  - `style_preset`: High-tech Developer Aesthetic, Cyberpunk Code Ambient, Clean Minimal Studio, etc.
  - `camera_style`: Cinematic Macro, Smooth Pan, Split Screen Code View.
  - `lighting_environment`: Neon accent LED, Soft Studio Key Light, Dark Mode OLED Glow.
- `shots`: List of scene objects:
  - `timestamp_range`: e.g., "00:00 - 00:05"
  - `visual_description`: Detailed visual prompt for AI video generators (e.g., Google Flow / Veo).
  - `voiceover_script`: Exact narration script.
  - `b_roll_notes`: Screen recording prompts, UI highlights, macro keyboard keypresses.
- `pricing_and_verdict`: Quick summary of pricing model and recommendation.
- `disclaimer`: Standard non-sponsorship disclosure.

## 3. Mandatory Non-Sponsorship Disclaimer
Every video script description and spoken voiceover outro must include:
```
Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
```
