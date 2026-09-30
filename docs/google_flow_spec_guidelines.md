# Google Flow & AI Video Spec Guidelines for IDE Guide

## Channel Context
- **YouTube Channel**: [@IDEguide](https://www.youtube.com/@IDEguide)
- **Daily Frequency**: 3 Videos / Shorts per day.
- **Focus**: Objective reviews, pros/cons, paid vs free guidance, and feature walkthroughs of IDEs and Code Editors.

## Standard Video Specification Structure

Each video generated for IDE Guide must follow a structured JSON / Markdown specification compatible with Google Flow / AI video creation tools.

### Key Video Prompt Elements

1. **Title & Target Length**:
   - Short Form (Shorts): 30–60 seconds.
   - Standard Video: 3–5 minutes.

2. **Visual & Style Prompting**:
   - **Style**: Modern, sleek developer tech aesthetic with high contrast dark mode IDE UI visuals.
   - **Lighting**: Soft cinematic neon accents (cyan/violet developer color palette), standard studio lighting for avatar/presenter clips.
   - **Framing & Motion**: Smooth pan and zoom transitions on high-resolution code editor UI elements. Dynamic screen recordings blended with modern motion graphics.
   - **Color Palette**: Dark theme UI `#1e1e1e`, electric cyan `#00d2ff`, modern purple `#7b2cbf`.

3. **Scene Breakdown Protocol**:
   Each scene must explicitly define:
   - `scene_number`: Sequential integer.
   - `duration_seconds`: Floating point or integer duration.
   - `visual_description`: Detailed prompt for AI image/video generation (camera angle, movement, focal subject).
   - `voiceover_narration`: Precise script spoken by narration engine.
   - `text_overlay`: On-screen captions highlighting key points (e.g., "PRICE: Free & Open Source").

4. **Required Sections in Every Video Spec**:
   - **Hook**: First 5 seconds catching developer attention.
   - **Overview & Pricing**: Free vs Paid, Licensing model.
   - **Pros (Good) & Cons (Bad)**: Balanced technical breakdown.
   - **Target Audience / Verdict**: Who should use this editor/IDE.
   - **Mandatory Disclaimer**: Standard non-sponsorship disclosure.

## Mandatory Non-Sponsorship Disclaimer

All video scripts and specs MUST include the exact text or narration equivalent of:

> "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
