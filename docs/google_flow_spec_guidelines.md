# Google Flow & AI Video Specification Guidelines

This document outlines the standard specification format for generating short and long-form video content for YouTube ([@IDEguide](https://www.youtube.com/@IDEguide)) using Google Flow and video generation tools.

## 1. Video Formats Supported

- **YouTube Short (9:16 vertical)**: ~60 seconds fast-paced overview.
- **YouTube Long-Form Video (16:9 widescreen)**: 3-5 minute comprehensive IDE walkthrough and comparison.

## 2. Google Flow Video Spec Structure

Each generated video specification JSON/Markdown document must include:

1. **Title & Meta Information**:
   - Catchy YouTube title.
   - Video format / aspect ratio (`16:9` or `9:16`).
   - Estimated duration.
   - Target IDE / Code Editor.

2. **Narrative & Script Breakdown**:
   - **Hook (0-5s)**: High-energy opening phrase framing the IDE comparison.
   - **Overview & Pricing (5-20s)**: Whether the IDE is Free, Open Source, or Paid.
   - **Pros & Standout Features (20-40s)**: Visual cues demonstrating feature highlights (AI completion, speed, extensions, debugging).
   - **Cons & Drawbacks (40-50s)**: Objective trade-offs (memory usage, ecosystem maturity, setup complexity).
   - **Verdict & Call to Action (50-60s)**: Target audience recommendation and disclaimer.

3. **Google Flow Scene Specifications**:
   For each scene, provide:
   - `scene_id`: Sequential scene number.
   - `timecode`: e.g. `00:00 - 00:05`.
   - `visual_prompt`: Detailed prompt optimized for Google Flow text-to-video / image-to-video tools (specifying lighting, camera angle, interface style, motion speed).
   - `camera_movement`: e.g. `Slow zoom in on code editor cursor`, `Pan right across dark theme UI`.
   - `narration_script`: Voiceover transcript.
   - `on_screen_text`: Text overlays for readability.
   - `audio_cues`: Background music tempo and sound effects (SFX).

4. **Mandatory Non-Sponsorship Disclaimer**:
   Must be displayed on screen during the closing CTA and included in the script audio/text:
   `Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.`
