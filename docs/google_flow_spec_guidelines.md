# Google Flow Video Generation Guidelines for IDE Guide

This document defines the prompt standards, framing specifications, lighting rules, audio/script structures, and scene composition rules for generating high-converting YouTube Long-form and Shorts content using Google Flow / AI Video tools for **IDE Guide** (@IDEguide).

---

## Channel Overview & Branding
- **YouTube Channel**: [@IDEguide](https://www.youtube.com/@IDEguide)
- **Blogger Website**: [IDE Guide Blog](https://ideguide.blogspot.com/)
- **Core Mission**: Provide objective, unbiased, and visually engaging comparisons, hands-on reviews, and guides for Modern Code Editors & Integrated Development Environments (IDEs).
- **Daily Frequency**: 3 Videos / Shorts per day + 3 AMP HTML Blog Posts per day.
- **Mandatory Disclaimer**:
  > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

---

## Video Specifications

### 1. YouTube Shorts (Vertical 9:16)
- **Resolution**: 1080x1920 (9:16)
- **Duration**: 45 - 60 seconds (Target: 55s)
- **Target Pace**: Fast, engaging, high-retention cut every 2–4 seconds.
- **Visual Style**: Sleek dark-mode developer UI, cinematic studio lighting, neon accent highlights (cyan, purple, emerald), macro code closeups.
- **Structure**:
  1. **Hook (0-5s)**: High-impact question or bold statement about the IDE.
  2. **Core Pitch (5-20s)**: Primary feature / unique selling proposition (AI code completion, speed, memory usage).
  3. **Pros & Cons (20-40s)**: Direct comparison of what works and what fails.
  4. **Pricing & Verdict (40-50s)**: Is it free, freemium, or paid? Is it worth switching?
  5. **CTA & Disclaimer (50-50s / On-Screen)**: Mandatory non-sponsorship disclosure & Subscribe prompt.

### 2. YouTube Long-Form / Landscape (Horizontal 16:9)
- **Resolution**: 1920x1080 (16:9)
- **Duration**: 3 - 5 minutes
- **Target Pace**: Dynamic tech review with smooth camera pan transitions, UI screen recordings, and comparison splits.
- **Structure**:
  1. **Intro & Disclosure (0-30s)**: Overview + Non-sponsorship declaration.
  2. **Deep Dive / Features (30s-2m)**: Interface, performance, extensions, and workflow.
  3. **Good vs. Bad (2m-3.5m)**: Balanced pros/cons analysis.
  4. **Pricing Breakdown (3.5m-4.5m)**: Tiered pricing, free alternatives, value analysis.
  5. **Final Recommendation & CTA (4.5m-5m)**: Who should use this editor?

---

## Google Flow Prompt Standard Format

When populating JSON specs or prompt buffers for Google Flow, use the following scene structure:

```json
{
  "scene_id": "scene_01",
  "time_start": "00:00",
  "time_end": "00:05",
  "visual_prompt": "Cinematic close-up shot of a modern dark-mode code editor screen with syntax-highlighted TypeScript code. Glowing cyan cursor blinking rapidly. An overlay text reads 'Is Cursor Better Than VS Code?'. Studio studio lighting with subtle ambient blue and violet rim light, 4K resolution, photorealistic developer desk environment.",
  "camera_motion": "Slow zoom in towards the glowing code block",
  "lighting": "Low key dark room with neon accent backlighting",
  "voiceover": "Is this new AI code editor actually better than VS Code, or is it just hype? Let's break down the truth in 60 seconds.",
  "on_screen_text": "Cursor vs VS Code | Unbiased Review"
}
```

---

## Lighting & Visual Aesthetic Guidelines
- **Theme**: Dark Mode First (VS Code Dark+, One Dark Pro, Catppuccin Mocha, Dracula themes).
- **Lighting**: Soft cinematic key light (5600K clean white) with accent RGB backlighting (Hex color codes: `#00f0ff` Cyan, `#7000ff` Purple, `#00ff66` Emerald Green).
- **Framing**: Clean desk setups, ultra-wide monitors, mechanical keyboards, subtle bokeh background.
- **Text Styling**: High contrast sans-serif typography (Inter / Roboto) with subtle dropped shadows for legibility across mobile devices.
