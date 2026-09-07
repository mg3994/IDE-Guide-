# Instructions for AI Agents & Assistant Tools

## Purpose
This repository contains the content generation system and CLI skills for **IDE Guide** ([Blogger Website](https://ideguide.blogspot.com/) & [YouTube Channel @IDEguide](https://www.youtube.com/@IDEguide)).

## Core Rules for Content Generation

### 1. Blogger AMP HTML Compliance
- Every blog post file MUST be valid AMP (Accelerated Mobile Pages) HTML.
- HTML tag MUST include the `⚡` or `amp` attribute (e.g. `<html ⚡ lang="en">`).
- Must include standard AMP boilerplate: `<script async src="https://cdn.ampproject.org/v0.js"></script>` and `<style amp-boilerplate>`.
- Images MUST use `<amp-img>` tags with specified `width`, `height`, and `layout="responsive"`. Never use standard `<img>` tags in AMP blog posts.
- All custom styling must reside inside `<style amp-custom>`.

### 2. Google Flow Video Specifications
- Video scripts and specs generated for YouTube Shorts or Videos MUST conform to `docs/google_flow_spec_guidelines.md`.
- Include scene-by-scene timing, narration text, visual camera motion prompts (pan, zoom, macro close-up), and on-screen overlays.
- Color palette: Dark mode developer UI, neon cyan/purple accents, high contrast text.

### 3. Non-Sponsorship Disclaimer Requirement
- Every generated AMP blog post and Google Flow video script MUST include the exact non-sponsorship disclaimer:
  > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

### 4. Daily Schedule & Diversity
- Quota: 3 distinct IDE/code editor reviews daily (3 AMP blog posts + 3 Google Flow video specs).
- Covered IDEs must be logged in `content/history.json` to prevent repeating tools across consecutive days.

## Development & Verification Guidelines
- Before submitting code changes, run `pytest tests/` to verify that all content generators, AMP validators, and CLI tools function as expected.
- Ensure all created files pass linting and formatting standards.
