# Google Flow Video Generation Spec Guidelines

This document outlines the standard specifications and prompt engineering structure used by IDE Guide to generate visual video generation prompts and scripts for **Google Flow** (and other AI video synthesis tools).

## Channel Context
* **YouTube Channel**: [@IDEguide](https://www.youtube.com/@IDEguide)
* **Blogger Website**: [IDE Guide](https://ideguide.blogspot.com/)
* **Daily Frequency**: 3 Videos per day (YouTube Longform/Shorts) + 3 AMP Blog Posts per day.
* **Disclaimer Requirement**: Every generated video script must explicitly include:
  > "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."

---

## 1. Video Formats

### A. YouTube Shorts (Vertical 9:16)
* **Duration**: 30 to 60 seconds
* **Aspect Ratio**: 9:16 (1080x1920)
* **Pacing**: Fast-cut, dynamic visual transitions every 3-5 seconds.
* **Target Focus**: Quick IDE comparisons, top 3 features, "Free vs Paid" verdict, or dark theme showcases.

### B. YouTube Longform Video (Horizontal 16:9)
* **Duration**: 3 to 8 minutes
* **Aspect Ratio**: 16:9 (3840x2160 or 1920x1080)
* **Pacing**: Structured breakdown (Intro, Interface Tour, Pros & Cons, Key Features, Pricing & License, Final Verdict).

---

## 2. Google Flow Prompt Specifications

When generating prompts for Google Flow, each scene must specify:

1. **Visual Prompt (`visual_prompt`)**: High-detail description of code editor UI, macro shots, developer desk setups, glowing neon accents, syntax highlighting, and smooth camera panning.
2. **Framing & Aspect Ratio (`framing`)**: e.g., `9:16 Vertical Macro Shot`, `16:9 Wide Studio Desk View`.
3. **Lighting & Style (`lighting`)**: Cinematic dark mode aesthetics, dynamic RGB rim lighting (cyan/purple/amber), soft bokeh backgrounds.
4. **Camera Motion (`camera_motion`)**: Slow pan, push-in zoom, tracking shot, macro sweep across code lines.
5. **Voiceover / Script Segment (`narration`)**: Clear, concise narration script for audio synthesis or presenter voiceover.
6. **On-Screen Graphics / Text Overlay (`text_overlay`)**: Key highlights, feature badges (e.g. `FREE`, `PAID`, `PROS / CONS`).

---

## 3. Mandatory Output Structure for Google Flow Specs

Each Google Flow spec file generated in `content/YYYY-MM-DD/video_spec_<ide_name>.json` or `.md` should follow this JSON structure:

```json
{
  "title": "IDE Guide Review: [IDE Name]",
  "format": "Shorts / Longform",
  "aspect_ratio": "9:16",
  "ide_name": "[IDE Name]",
  "pricing": "Free / Paid / Freemium",
  "disclaimer": "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.",
  "scenes": [
    {
      "scene_id": 1,
      "duration_sec": 5,
      "visual_prompt": "Ultra-detailed shot of developer laptop running [IDE Name] dark mode theme with vivid syntax highlighting.",
      "framing": "Close-up 9:16 vertical",
      "lighting": "Dark studio ambience with subtle purple rim light",
      "camera_motion": "Slow tilt upwards",
      "text_overlay": "[IDE Name] - Complete Review",
      "narration": "Looking for the ultimate editor? Here is everything you need to know about [IDE Name]."
    }
  ]
}
```
