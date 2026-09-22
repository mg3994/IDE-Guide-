# Google Flow Video Prompt Standards & Guidelines for IDE Guide

This document establishes the official visual, audio, and prompt engineering specifications for producing YouTube videos and Shorts for **IDE Guide** ([@IDEguide](https://www.youtube.com/@IDEguide)) using **Google Flow** and related AI video generation tools.

---

## 1. Overview & Content Philosophy

IDE Guide provides high-value, unbiased, and objective reviews, feature comparisons, and workflows for developer tools, IDEs, and code editors.

Every video produced must strictly adhere to the non-sponsorship mandate:
> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

---

## 2. Video Formats & Technical Specifications

| Parameter | YouTube Shorts | Long-Form Videos |
| :--- | :--- | :--- |
| **Aspect Ratio** | 9:16 Vertical (1080x1920) | 16:9 Landscape (1920x1080 / 3840x2160) |
| **Duration** | 45–60 seconds | 3–5 minutes |
| **Pacing** | Fast, high-energy cuts (1.5s - 3s per scene) | Measured, analytical (4s - 8s per scene) |
| **Target Audience** | Mobile developers scrolling Shorts | Desktop developers researching tools |

---

## 3. Visual Prompting & Styling Standards

When generating visual prompts for Google Flow / Veo AI, use the following standardized visual descriptors:

### Framing & Camera Movement
- **Extreme Close-Up (ECU):** Mechanical keyboard switches being pressed, cursor clicking on AI code completion options, terminal command execution.
- **Medium Shot (MS):** Clean minimalist developer desk setup with dual ultra-wide monitors displaying glowing code editor UI.
- **Camera Motions:**
  - `Slow cinematic dolly-in towards the glowing IDE syntax highlighting.`
  - `Smooth right-to-left pan across sleek editor sidebar with file tree and AI chat.`
  - `Top-down aesthetic desk view with laptop running the IDE.`

### Lighting & Color Grading
- **Environment Lighting:** Soft moody studio rim lighting, 5000K neutral white ambient desk light, subtle blue/cyan neon reflection on dark-mode code editors.
- **Color Grade:** High dynamic range (HDR), crisp contrast, rich dark tones (`#0f172a` slate editor background), vibrant syntax highlighting (emerald green keywords, vibrant orange strings, crisp purple functions).

---

## 4. Scene Structure & Timing Matrix (Shorts Workflow)

1. **Scene 1: The Hook (0:00 - 0:05)**
   - *Visual Prompt:* Macro shot of hands typing at high speed on a mechanical keyboard, switching smoothly to a bold glow text overlay of the IDE logo.
   - *Voiceover Script:* "Is [IDE Name] actually worth switching to in [Year]? Here is what nobody is telling you!"

2. **Scene 2: Core Feature Showcase (0:05 - 0:25)**
   - *Visual Prompt:* Ultra-smooth cinematic screen capture pan showing AI autocompletion, multi-cursor editing, and fast file indexing in [IDE Name].
   - *Voiceover Script:* "[IDE Name] brings [Key Feature 1] and ultra-fast [Key Feature 2], making code navigation feel instantaneous."

3. **Scene 3: Pros vs. Cons Breakdown (0:25 - 0:42)**
   - *Visual Prompt:* Split visual composition. Left side displaying green checkmarks (Pros: Speed, AI integration), right side displaying subtle orange warning tags (Cons: High RAM usage or paid subscription).
   - *Voiceover Script:* "The good: incredible responsiveness and built-in AI agents. The bad: heavy memory consumption and subscription tiers."

4. **Scene 4: Pricing Model & Verdict (0:42 - 0:52)**
   - *Visual Prompt:* Clean graphical overlay contrasting Free vs Paid plans with clear pricing tags ($0 vs $20/mo).
   - *Voiceover Script:* "[IDE Name] offers a [Free / Freemium / Paid] model. Best suited for [Target Developer Persona]."

5. **Scene 5: Call to Action & Non-Sponsorship Disclaimer (0:52 - 1:00)**
   - *Visual Prompt:* Minimalist IDE Guide badge overlay with subscribe animation and non-sponsorship disclaimer text banner at the bottom.
   - *Voiceover Script:* "Subscribe to IDE Guide for daily unbiased dev tool reviews! Independent and 100% unsponsored."

---

## 5. Google Flow AI Prompt Template

When generating individual scene video clips using Google Flow AI prompts, format the text prompt as follows:

```text
Cinematic 4K shot, [Camera Angle & Motion], [Subject/IDE UI Detail], soft studio rim lighting, neon cyan glow, dark mode IDE interface, hyper-realistic, 60fps smoothness --ar [16:9 or 9:16]
```
