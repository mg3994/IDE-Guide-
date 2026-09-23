# Google Flow Video Specifications & AMP HTML Guidelines for IDE Guide

## Overview
This document outlines the visual, prompt, and technical specifications for generating daily content for:
- **Blogger Website**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/) (AMP HTML Blog Posts)
- **YouTube Channel**: [https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide) (Google Flow Video Generation Specs & Scripts)

---

## Non-Sponsorship Disclaimer Requirement
Every published blog post and video script **MUST** explicitly state the following non-sponsorship disclaimer:

> **Disclaimer**: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

---

## 1. Google Flow Video Generation Prompt Standards

### Video Formats
- **YouTube Shorts / Reels (9:16 vertical, 1080x1920, 60s max)**: Dynamic, fast-paced, high impact.
- **YouTube Standard Video (16:9 widescreen, 1920x1080, 3-5 mins)**: Comprehensive deep dive, side-by-side comparison, code execution walk-through.

### Scene Prompt Structure & Framing
Each scene prompt in Google Flow must strictly adhere to the following composition:
1. **Camera Angle & Framing**: Close-up on editor window, medium shot of developer workstation, over-the-shoulder coding view, or cinematic split-screen comparison.
2. **Lighting & Mood**: Soft studio key lighting, neon code highlight accents, dark mode IDE aesthetics (monokai, dracula, github dark high contrast).
3. **Action & Motion**: Smooth panning across syntax trees, fast cursor movement, keypress overlay animations, active AI completion popups.
4. **Visual Cues**: Clear badges for **FREE**, **PAID**, or **FREEMIUM**, side-by-side Pros & Cons overlays, feature scorecards.

### Example Google Flow Prompt
```
Cinematic medium shot of a developer's clean setup with a 4K monitor displaying VS Code vs Cursor side-by-side in dark mode. Cyberpunk aesthetic key lighting in cyan and magenta. Dynamic smooth zoom into the AI completion window while code auto-completes. High resolution, ultra-detailed text, professional tech channel style.
```

---

## 2. Daily Output Volume & Structure
Daily automated pipelines generate **3 Content Packages per day** in `content/YYYY-MM-DD/`:
1. `01_<ide_slug>/` -> AMP HTML post + Google Flow Video Spec
2. `02_<ide_slug>/` -> AMP HTML post + Google Flow Video Spec
3. `03_<ide_slug>/` -> AMP HTML post + Google Flow Video Spec

---

## 3. AMP HTML Standards (Blogger Compatible)
All blog post content generated for Blogger MUST comply with Google AMP (Accelerated Mobile Pages) standards:
- Root tag: `<html ⚡>` or `<html amp>`.
- Mandatory `<script async src="https://cdn.ampproject.org/v0.js"></script>`.
- Boilerplate CSS in `<style amp-boilerplate>` and custom inline styles in `<style amp-custom>`.
- Images using `<amp-img>` with explicit `width`, `height`, and `layout="responsive"`.
- Valid structured metadata (`ld+json`).
