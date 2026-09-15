# Google Flow & Visual Video Specification Guidelines for IDE Guide

This document outlines the visual, prompt, and script specifications for creating high-performing YouTube videos (@IDEguide) and YouTube Shorts using AI video generation tools (such as Google Flow / Veo / Sora / Runway) alongside AMP HTML blog content.

---

## Channel Identity & Disclaimer Requirements

- **YouTube Channel**: [@IDEguide](https://www.youtube.com/@IDEguide)
- **Blogger Website**: [ideguide.blogspot.com](https://ideguide.blogspot.com/)
- **Daily Content Output**:
  - **3 Blog Posts per day** (AMP HTML format for Blogger)
  - **3 Video Packages per day** (YouTube Long-form / Shorts visual specs + scripts)

### Mandatory Non-Sponsorship Disclaimer
Every generated video script, visual prompt specification, and AMP blog post MUST include the following non-sponsorship disclaimer:

> **Disclaimer**: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

---

## Visual Video Generation Prompts (Google Flow Specifications)

When generating visual sequences for IDE comparisons and reviews, each video scene specification must define:

1. **Prompt Description**: Detailed cinematic prompt for text-to-video AI generation (Google Flow).
2. **Camera Framing & Motion**: Shot type (e.g., Close-up on editor screen, Macro shot of dark UI, Medium tracking shot of developer desk) and camera movements (e.g., Slow push-in, subtle pan).
3. **Lighting & Atmosphere**: Cyberpunk neon accents, soft ambient studio lighting, clean warm minimalist setup, high-contrast dark mode glow.
4. **Scene Timing**: Precise duration (e.g., 5s, 10s, 15s).
5. **Text Overlays & On-Screen UI Highlights**: Text overlays for key features, pricing badges (FREE vs PAID), and pros/cons callouts.
6. **Voiceover Script & Audio Cues**: Clear narration synchronized with screen action and ambient background synth beats.

---

## AMP HTML Standards for Blogger Content

To ensure maximum speed, Google Search mobile carousel inclusion, and Blogger compatibility:

- **Doctypes & Boilerplate**: Standard `<html ⚡>` or `<html amp>` with `<meta charset="utf-8">` and AMP boilerplate CSS.
- **Image Elements**: Use `<amp-img src="..." width="..." height="..." layout="responsive">` instead of standard `<img>` tags.
- **Custom Styling**: All custom CSS must be inline inside `<style amp-custom>...</style>` tag with total size under 75KB. No inline `style="..."` attributes allowed on HTML tags.
- **Interactive Components**: Use `<amp-accordion>` or `<amp-fit-text>` when necessary.
