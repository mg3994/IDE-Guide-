# Google Flow Video Prompt Standards & Specification Guidelines

## Overview
This document defines the prompt structure, visual parameters, camera directions, and script specifications for generating high-converting YouTube videos and Shorts for **IDE Guide** (@IDEguide) using AI video flow tools like Google Flow.

---

## Content Strategy & Daily Quota
- **Daily Target**: 3 YouTube Videos/Shorts + 3 Blogger AMP Posts published every day.
- **Channel Focus**: Objective reviews, head-to-head comparisons, feature walkthroughs, pros & cons, free vs. paid tier breakdowns, and developer suitability guides for IDEs and code editors (e.g., VS Code, Cursor, Zed, PyCharm, Neovim, IntelliJ IDEA, Windsurf, Helix, Sublime Text).
- **Mandatory Non-Sponsorship Disclaimer**:
  > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

---

## Visual & Prompt Framing Standards

### 1. Aspect Ratios & Formats
- **YouTube Shorts / Mobile Vertical**: `9:16` (1080x1920), fast pacing (30–60 seconds), dynamic transitions, high aesthetic contrast.
- **YouTube Long Form / Desktop Horizontal**: `16:9` (1920x1080), detailed breakdown (3–10 minutes), structured chapters, cinematic B-roll, clean screen capture aesthetic.

### 2. Visual Style & Aesthetics
- **Color Palette**: Dark mode developer aesthetic, cybernetic neon accents (cyan `#00f3ff`, purple `#8a2be2`, electric blue `#1e90ff`), dark slate gray background (`#0f172a`).
- **Lighting**: Soft ambient key light, low-key background glow, rim lighting on desk setup/monitors, high contrast code text readability.
- **Environment**: Modern developer studio, sleek minimalist desk, dual ultra-wide monitors displaying glowing IDE interface code, ergonomic chair, subtle background bokeh.

### 3. Camera Motions & Prompts for Google Flow
- **Pan / Tracking**: `Slow horizontal tracking shot across sleek IDE interface highlighting AI autocomplete in action, 4k ultra-detailed, cinematic lighting.`
- **Macro / Close-up**: `Extreme close-up macro lens shot of high-contrast code snippet syntax highlighting, smooth glowing cursor movement, photorealistic, 60fps.`
- **Zoom In**: `Smooth push-in zoom on IDE benchmark results chart showing memory usage comparison, crisp typography, sleek dark theme overlay.`
- **Transition**: `Glitch wipe transition from Cursor dark mode UI into Zed rust-native code editor interface, high speed visual sweep.`

---

## Standard Video Script & Prompt Template Structure

Every Google Flow video generation specification JSON/YAML generated for IDE Guide follows this structure:

```json
{
  "title": "IDE Name Review - Is It Worth It?",
  "target_platform": "YouTube Shorts (9:16)",
  "duration_seconds": 60,
  "ide_name": "IDE Name",
  "pricing_model": "Free / Freemium / Paid ($X/mo)",
  "scenes": [
    {
      "scene_number": 1,
      "duration": 5,
      "narration_script": "Opening hook presenting the main question or high-impact metric of the IDE.",
      "visual_prompt": "Cinematic visual description for Google Flow prompt input.",
      "camera_motion": "Smooth push-in zoom",
      "overlay_text": "HOOK TEXT ON SCREEN"
    },
    {
      "scene_number": 2,
      "duration": 15,
      "narration_script": "Showcasing top positive features (The Good).",
      "visual_prompt": "Prompt showing feature workflow in action.",
      "camera_motion": "Horizontal pan",
      "overlay_text": "PROS / ADVANTAGES"
    },
    {
      "scene_number": 3,
      "duration": 15,
      "narration_script": "Showcasing limitations or drawbacks (The Bad).",
      "visual_prompt": "Prompt showing resource usage or UI clutter.",
      "camera_motion": "Macro zoom",
      "overlay_text": "CONS / DRAWBACKS"
    },
    {
      "scene_number": 4,
      "duration": 15,
      "narration_script": "Pricing breakdown (Free vs Paid) and final verdict.",
      "visual_prompt": "Pricing matrix & badge prompt.",
      "camera_motion": "Static punch-in",
      "overlay_text": "FREE vs PAID & VERDICT"
    },
    {
      "scene_number": 5,
      "duration": 10,
      "narration_script": "Non-sponsorship disclaimer and call to action to read full AMP blog post on ideguide.blogspot.com.",
      "visual_prompt": "Closing screen with YouTube and Blogger logos, dark ambient studio background.",
      "camera_motion": "Slow pull-out zoom",
      "overlay_text": "Independent & Unsponsored | Link in Bio"
    }
  ],
  "disclaimer": "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
}
```

---

## Quality Checklist for Generated Videos
1. **Clarity**: Code snippets and text overlays must be legible on mobile devices.
2. **Objectivity**: Must present both pros and cons fairly without bias.
3. **Pacing**: Short video scene transitions must occur every 3-5 seconds to maintain high retention.
4. **Compliance**: Disclaimer must be clearly audible or visually displayed in every video.
