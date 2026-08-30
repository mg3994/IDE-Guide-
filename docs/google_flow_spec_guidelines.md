# Google Flow Video & Shorts Generation Specification Guidelines

This document provides standardized prompt engineering and video generation guidelines for producing high-quality YouTube videos and Shorts for the **IDE Guide** channel ([@IDEguide](https://www.youtube.com/@IDEguide)).

---

## 1. Overview & Objectives
- **Target Audience:** Software developers, engineers, students, and tech enthusiasts.
- **Content Goal:** Provide objective, visual reviews and comparisons of modern IDEs, code editors, and AI coding assistants.
- **Output Formats:**
  1. **YouTube Shorts (9:16 Vertical)**: Fast-paced, punchy, 30–60 second summaries highlighting key pros, cons, pricing, and overall recommendation.
  2. **YouTube Videos (16:9 Horizontal)**: In-depth 3 to 5-minute detailed breakdowns with full feature showcases, workflow demonstrations, pros & cons, pricing analysis, and audience-tailored recommendations.

---

## 2. Standardized Video Structure (Daily Schedule: 3 Videos / Shorts Per Day)
Every video produced using Google Flow AI video generation tools must strictly follow this structure:

1. **Hook (0-5s):** Dynamic visual of the IDE in action + high-impact query (e.g., "Is VS Code still king in 2026?").
2. **Overview & Interface (5-15s):** Key architectural highlights, supported languages, primary target audience.
3. **The Good (Pros) (15-30s):** Top standout features (AI integration, performance, extension ecosystem, memory efficiency).
4. **The Bad (Cons) (30-45s):** Limitations, heavy RAM usage, learning curve, missing extension support, or telemetry concerns.
5. **Pricing Breakdown (45-55s):** Clear indicator if it is 100% Free / Open Source, Freemium, or Paid Enterprise.
6. **Verdict & Non-Sponsorship Disclaimer (55-60s):** Final decision on who should use it + mandatory disclaimer.

---

## 3. Google Flow Prompt Specifications

### Camera & Motion Guidelines
- **Shot Types:** Close-up on sleek editor interface, medium panning shot over developer workspace, macro shot on code syntax highlighting.
- **Camera Movements:** Slow cinematic pan left/right, steady zoom-in on code completion popups, smooth vertical tilt along file trees.
- **Framing & Composition:** Rule-of-thirds alignment, sharp contrast between editor background (dark theme default) and syntax colors.

### Lighting & Aesthetic
- **Lighting:** Cyberpunk ambient LED backdrop (cyan, neon purple, deep dark blue), soft key light on mechanical keycaps/desks.
- **Aesthetic:** Modern, futuristic tech studio vibe, crisp 4K resolution render aesthetic.

### Text Overlays & Motion Graphics
- **Shorts (9:16):** Bold centered animated text overlay (Yellow/White font with subtle drop shadow), progress bar, floating rating badges.
- **Videos (16:9):** Lower thirds for IDE specs, side-by-side comparison tables, visual checkmarks (green) and crosses (red) for pros/cons.

---

## 4. Mandatory Non-Sponsorship Disclaimer

Every video script and voiceover must include the exact disclaimer statement:

> **"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."**

---

## 5. Standard Output Template Schema (JSON Specification)

```json
{
  "title": "IDE Name - Review & Guide",
  "aspect_ratio": "16:9 | 9:16",
  "disclaimer": "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.",
  "scenes": [
    {
      "scene_number": 1,
      "type": "Hook",
      "duration_seconds": 5,
      "visual_prompt": "Cinematic close-up of dark mode IDE editor window with neon syntax highlighting, smooth camera zoom-in.",
      "voiceover_script": "Is [IDE Name] the best choice for your developer setup today? Let's break it down in under 60 seconds.",
      "text_overlay": "[IDE Name] Detailed Review"
    }
  ]
}
```
