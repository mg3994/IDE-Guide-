# Google Flow Video & Shorts Prompt Specifications Guidelines

This document outlines the standard prompt specifications, video parameters, and narration script formats for generating high-engagement YouTube Shorts and Videos for [YouTube @IDEguide](https://www.youtube.com/@IDEguide) using Google Flow and AI video tools.

## 1. Daily Cadence & Target Audience

- **Target Cadence**: 3 Videos / Shorts per day.
- **Goal**: High visual retention, snappy pacing, objective review of IDEs/Code Editors.
- **Audience**: Software engineers, web developers, computer science students, open-source contributors.

## 2. Video Specification Structure

Each video spec file outputted by IDE Guide generators must follow this YAML / JSON structured format:

```yaml
meta:
  ide_name: "VS Code"
  pricing: "Free / Open Source"
  target_audience: "Full-stack Developers"
  video_type: "Short" # Short (9:16) or Longform (16:9)
  aspect_ratio: "9:16"
  duration_seconds: 60

google_flow_prompts:
  - scene_id: 1
    timestamp: "00:00 - 00:05"
    prompt: "Cinematic close-up ultra-HD shot of VS Code interface with dark mode theme neon glow, floating code snippets, sleek camera zoom-in, 4K resolution, studio lighting, highly detailed."
    camera_movement: "Slow push-in zoom"
    lighting: "Dark mode neon blue and violet ambient backlight"
    caption: "Is VS Code Still the King of Editors in 2026?"

  - scene_id: 2
    timestamp: "00:05 - 00:20"
    prompt: "Macro view of developer hands typing rapidly on mechanical keyboard with RGB lighting, code displaying real-time autocomplete suggestions, high frame rate."
    camera_movement: "Tracking pan left to right"
    lighting: "Warm key light with dark background contrast"
    caption: "Top Pros: Massive Extension Ecosystem & AI Integration"

  - scene_id: 3
    timestamp: "00:20 - 00:40"
    prompt: "Split screen high tech UI comparing memory consumption graphs, high speed counter animation, clean modern tech aesthetic."
    camera_movement: "Static center focus with dynamic overlay"
    lighting: "Clean daylight studio lighting"
    caption: "The Cons: Heavy RAM usage on large monorepos"

  - scene_id: 4
    timestamp: "00:40 - 00:60"
    prompt: "Overhead shot of sleek modern desk setup with dual monitors showing code editor, smooth fade to IDE Guide logo branding."
    camera_movement: "Tilt down overhead"
    lighting: "Soft diffuse studio ambient"
    caption: "Verdict: Must-have for 90% of Web Developers"

script:
  voiceover_text: |
    Looking for the best code editor? Let's talk about VS Code.
    It is 100% free and open-source, packed with extensions and integrated AI capabilities.
    Pros: Unmatched community support and flexible debugging.
    Cons: High memory usage when opening massive monorepos.
    Verdict: Essential for web developers!
    Disclaimer: IDE Guide is independent and not sponsored by any editor vendor.

  disclaimer: "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
```

## 3. Visual Prompt Quality Rules for Google Flow

1. **Resolution & Style**: Always specify `4K resolution`, `cinematic lighting`, `ultra-HD`, `sleek tech aesthetic`.
2. **Camera Specs**: Standardize camera motion descriptors (`slow push-in zoom`, `tracking pan`, `tilt overhead`, `macro close-up`).
3. **Lighting Setup**: Specify lighting explicitly (`neon blue ambient backlight`, `warm key light`, `diffuse studio ambient`).
4. **Pacing**: Pacing for Shorts should shift visual prompts every 5-15 seconds to maximize viewer retention.

## 4. Required Disclaimer Inclusion

Every video script must conclude with the vocalized and visually displayed disclaimer:
> "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
