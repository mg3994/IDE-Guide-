# Google Flow Video Prompt & Content Generation Guidelines

## Overview

This document defines the specification guidelines for generating video visual prompts, scripts, and AMP HTML blog posts for the **IDE Guide** platform across YouTube ([@IDEguide](https://www.youtube.com/@IDEguide)) and Blogger ([ideguide.blogspot.com](https://ideguide.blogspot.com/)).

---

## Content Schedule

- **Frequency:** 3 publications daily (3 blog posts and 3 videos/shorts per day).
- **Format Focus:**
  - **Blogger:** Valid AMP HTML (Accelerated Mobile Pages) blog posts designed for fast mobile loading on ideguide.blogspot.com.
  - **YouTube:** Video generation specs compatible with Google Flow / AI video creation tools, optimized for both YouTube Shorts (vertical 9:16) and YouTube Long-form/Landscape (16:9).

---

## Non-Sponsorship Disclaimer Policy

Every generated blog post, video description, and video script **must** include the following exact disclaimer text:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

---

## Google Flow Video Specification Standards

To generate visually engaging and high-converting video content using AI video engines like Google Flow, each video specification must adhere to the following visual prompt guidelines:

### 1. Visual Framing & Composition
- **Aspect Ratio:** 9:16 (Shorts) or 16:9 (Landscape).
- **Shot Types:** Close-up on IDE code editor UI, medium wide shot of modern dark-mode developer setup with neon ambient glow, macro detail on keyboard/code typing.
- **Camera Movement:** Smooth slow pan across UI elements, subtle zoom-in on key feature highlights, dynamic cinematic fly-through of code blocks.

### 2. Lighting & Aesthetics
- **Lighting:** Cyberpunk-inspired ambient lighting, high contrast dark theme UI with glowing syntax highlighting (cyan, purple, orange accent colors), subtle volumetric fog/glow.
- **Color Palette:** Deep obsidian gray (`#0f172a`), neon blue (`#0284c7`), vibrant purple (`#9333ea`), emerald green (`#10b981`).

### 3. Scene Breakdown Structure
Each video spec is divided into timed scenes (e.g. Scene 1: Hook, Scene 2: Feature Overview, Scene 3: Pros & Cons / Paid vs Free breakdown, Scene 4: Final Recommendation & Call to Action).

---

## AMP HTML Guidelines for Blogger

All blog posts generated for Blogger must strictly conform to the AMP HTML standard:

1. **Doctype & Tag:** Starts with `<!doctype html><html ⚡ lang="en">` or `<html amp lang="en">`.
2. **AMP Boilerplate:** Must include `<script async src="https://cdn.ampproject.org/v0.js"></script>` and the standard AMP CSS boilerplate block in `<head>`.
3. **Styling:** Custom CSS must reside inside a single `<style amp-custom>` tag inside `<head>`, with a maximum size limit of 75KB.
4. **Disallowed Tags:** No inline `style="..."` attributes, no custom external `<script>` tags, no `<img>` without `<amp-img>`.
5. **Content Structure:**
   - Title & Summary
   - Key Features Breakdown
   - Pricing Model (Free / Paid / Freemium)
   - Pros & Cons Table/Comparison
   - Best For (Target Developer Use Cases)
   - Non-Sponsorship Disclaimer
