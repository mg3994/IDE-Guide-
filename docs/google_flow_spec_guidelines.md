# Google Flow AI Video Specification Guidelines for IDE Guide

These guidelines define the specification format for Google Flow (and similar AI video generation tools) to generate visually engaging YouTube videos and Shorts for [@IDEguide](https://www.youtube.@IDEguide).

## 1. Google Flow Spec Standard Schema

Each video generated must have a structured JSON or YAML spec file containing scene-by-scene instructions for prompt engineering, camera motion, lighting, voiceover scripts, and timing.

### Core Scene Fields
- `scene_id`: Sequential scene number (1..N).
- `duration_seconds`: Scene length in seconds (typically 3–10s per scene).
- `visual_prompt`: Detailed prompt for text-to-video / image-to-video AI generation.
- `camera_framing`: e.g., "Extreme Close-Up", "Medium Shot", "Over-The-Shoulder Pan".
- `camera_movement`: e.g., "Slow zoom into code cursor", "Horizontal tracking left to right across UI".
- `lighting_and_mood`: e.g., "Cyberpunk neon dark mode glowing code", "Clean studio bright minimal high tech".
- `voiceover_script`: Precise spoken line for AI narration or human voiceover.
- `on_screen_text`: Text overlay title/caption.

## 2. Non-Sponsorship Disclaimer Requirement

All video specs must feature the non-sponsorship disclaimer spoken in the voiceover or displayed in on-screen text during the intro or outro scene:

> "IDE Guide is an independent channel. This review is not sponsored by or affiliated with any software vendor."

## 3. Video Format Specifications

### Standard YouTube Review (16:9 - Landscape)
- Target duration: 2 to 4 minutes (120 - 240 seconds).
- Visual style: High contrast IDE dark mode interface overlays, cinematic developer desk aesthetic, smooth code panning.

### YouTube Shorts (9:16 - Vertical)
- Target duration: 30 to 60 seconds.
- Dynamic fast-paced hook in scene 1 (first 3 seconds).
- Large visible text captions in lower third.

## 4. Spec File Structure Example (JSON)

```json
{
  "title": "VS Code vs Cursor AI: Which Editor Wins in 2026?",
  "aspect_ratio": "16:9",
  "target_platform": "YouTube",
  "channel": "@IDEguide",
  "disclaimer": "IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.",
  "scenes": [
    {
      "scene_id": 1,
      "duration_seconds": 5,
      "visual_prompt": "Cinematic over-the-shoulder shot of a modern programmer typing fast in VS Code dark mode with glowing syntax highlighting.",
      "camera_framing": "Medium Shot",
      "camera_movement": "Slow forward dolly",
      "lighting_and_mood": "Subtle blue ambient studio glow with glowing OLED display reflection",
      "voiceover_script": "Welcome back to IDE Guide! Today we analyze Cursor AI versus VS Code to see which editor actually boosts your workflow.",
      "on_screen_text": "VS Code vs Cursor AI | Objective Review"
    }
  ]
}
```
