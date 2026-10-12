# Google Flow Video & Shorts Specification Guidelines

This document specifies the format and parameters for AI video generation tools (including Google Flow, Runway, Pika, Sora, and ElevenLabs) for [YouTube @IDEguide](https://www.youtube.com/@IDEguide).

## 1. Video Production Specifications
- **Frequency:** 3 videos per day (Shorts / Vertical 9:16 aspect ratio or Standard 16:9 widescreen).
- **Target Audience:** Software developers, engineers, students, and tech enthusiasts.
- **Tone:** Energetic, objective, highly informative, and visually engaging.

## 2. Google Flow Video Prompt Standard Format
Each video specification JSON / Markdown document must include structured prompts for Google Flow:

### Scene Prompt Structure
- **Visual Prompt:** Detailed description of the IDE UI, cinematic camera angle, lighting, background motion, and focus.
- **Camera Movement:** E.g., `Slow zoom-in on code editor syntax highlighting`, `Pan left across terminal output`.
- **Lighting & Atmosphere:** E.g., `Dark mode UI, vibrant neon code highlights, soft ambient studio lighting`.
- **Voiceover Script:** Natural-sounding spoken script timed per scene (approx. 130-150 words per minute).
- **On-Screen Text Overlay:** Key bullet points, pricing tags (e.g., `FREE / $20/mo`), pros & cons badges.

## 3. Required Video Sections
1. **Hook (0-5s):** Dynamic visual and compelling question/statement comparing the IDE.
2. **Overview (5-15s):** Fast breakdown of what the code editor is best at.
3. **The Good (15-35s):** Top 3 features, speed benchmarks, AI features.
4. **The Bad (35-50s):** Honest limitations, RAM consumption, pricing model.
5. **Final Verdict & Recommendation (50-60s):** Who should download or buy it.
6. **Mandatory Non-Sponsorship Disclaimer (On-Screen & Script):**
   > *Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.*

## 4. Visual Prompt Template Example
```json
{
  "scene_id": 1,
  "visual_prompt": "Ultra-realistic 4K close-up shot of a dark-themed code editor with glowing green and cyan syntax highlighting on a crisp 4K monitor, camera slowly zooming in with subtle shallow depth of field.",
  "camera_motion": "Slow push-in zoom",
  "lighting": "Cinematic dark room with blue backlight reflection on desk",
  "voiceover": "Looking for the ultimate AI code editor in 2026? Let's break down Cursor IDE.",
  "text_overlay": "Cursor IDE Review | IDE Guide"
}
```
