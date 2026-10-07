# Google Flow & Visual Video Specification Guidelines (`@IDEguide`)

This document defines the prompt, timing, and visual specification rules for generating high-quality AI video content (using Google Flow and similar generative AI video tools) for YouTube videos and YouTube Shorts.

## 1. Content Formats

Each featured IDE / Code Editor receives specifications tailored for:
1. **YouTube Shorts (Vertical 9:16 - 60s max)**: Quick overview, killer feature, pros/cons fast breakdown, pricing verdict.
2. **YouTube Video (Horizontal 16:9 - Detailed)**: Comprehensive deep dive, workflow demo, extension ecosystem, pros/cons, performance evaluation, pricing breakdown.

## 2. Prompting Standards for Google Flow AI Video

Every scene specification must include structured prompt attributes:
- **Visual Description**: Clear description of the IDE UI, code syntax highlighting, cursor movements, dark/light theme, active developer actions.
- **Camera Movement & Framing**: e.g., "Slow zoom into code autocomplete popup", "Pan left across split terminal window", "Macro shot of keybindings HUD".
- **Lighting & Aesthetics**: "Modern developer setup, ambient dark room with subtle blue neon backlighting, high-contrast crisp code display".
- **Voiceover Script & Audio Timing**: Precise narration matching the duration of each visual scene (in seconds).

## 3. Mandatory Non-Sponsorship Audio/Visual Disclaimer

Every video script must contain an explicit verbal and visual disclaimer:
- **Visual Callout**: "Independent Review • Not Sponsored" overlay badge.
- **Audio Script**: "Disclaimer: IDE Guide is independent and not sponsored or endorsed by any software vendor mentioned in this video."

## 4. Google Flow Spec Template (JSON / Markdown Structure)

```json
{
  "title": "IDE Name - Features & Honest Review",
  "aspect_ratio": "16:9 or 9:16",
  "pricing": "Free / Paid / Freemium",
  "disclaimer": "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above.",
  "scenes": [
    {
      "scene_number": 1,
      "duration_seconds": 5,
      "visual_prompt": "Cinematic close-up of [IDE Name] interface with dark mode theme...",
      "camera_motion": "Smooth push-in towards the active editor tab",
      "lighting": "Soft studio ambient lighting with subtle key highlight on screen",
      "voiceover_script": "Welcome back to IDE Guide. Today we are looking at [IDE Name]..."
    }
  ]
}
```
