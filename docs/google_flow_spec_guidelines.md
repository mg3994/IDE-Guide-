# Google Flow Video Generation Specification Guidelines

This document outlines the standard guidelines for generating prompt specifications tailored for **Google Flow** and secondary AI video generation tools (e.g., Runway, Pika, Sora, Luma) for the **@IDEguide** YouTube channel.

## 1. Video Formats & Specifications

Every IDE guide feature video requires two aspect ratio targets:
1. **Standard YouTube Video (16:9 Widescreen):**
   - Aspect Ratio: `16:9`
   - Resolution: `1080p` / `4K`
   - Pace: Structured narrative, 60-120 seconds.
2. **YouTube Shorts (9:16 Vertical):**
   - Aspect Ratio: `9:16`
   - Resolution: `1080x1920`
   - Pace: High-energy visual cuts, 30-60 seconds.

## 2. Visual Prompting Principles

To achieve high visual engagement and professional quality in Google Flow video renders:

- **Lighting & Atmosphere:** Dark modern IDE theme (`#1E1E1E` or `#0D1117`), futuristic studio accent lighting (neon cyan `#00F0FF` and purple `#8A2BE2` backlighting), subtle glassmorphism overlay reflections.
- **Camera Angles:** Macro closeups on code cursor typing, slow smooth push-in zooms on key UI panels (e.g. extension manager, AI sidebar, memory benchmark graphs), wide dynamic tilt shot showing multi-monitor setup.
- **Rendering Quality Terms:** `cinematic tech review lighting`, `photorealistic 8k render`, `ultra crisp UI elements`, `smooth 60fps terminal motion`, `unbiased tech documentary style`.

## 3. Structural Video Blueprint

Each Google Flow spec file is structured into scenes with exact timing:

| Scene # | Duration | Visual Description & Camera | Audio / Voiceover Track |
|---|---|---|---|
| Scene 1 | 00:00 - 00:05 | Dynamic high-speed zoom into IDE logo with glowing border | Hook statement highlighting top unique feature or performance claim |
| Scene 2 | 00:05 - 00:30 | Macro pan across key editor features, code completion, UI response | Core feature walkthrough and memory/speed benchmarks |
| Scene 3 | 00:30 - 00:50 | Split screen showing pros (green highlights) vs cons (red highlights) | Honest "Good & Bad" assessment (startup time, extension ecosystem, memory usage) |
| Scene 4 | 00:50 - 01:10 | Pricing badge overlay (Free / Open-Source / Paid) with feature comparison | Pricing transparency breakdown and licensing rules |
| Scene 5 | 01:10 - 01:30 | Sleek developer desk shot with clear best-use recommendation card | Final verdict: Who should use this IDE and link to Blogger post |

## 4. Required Non-Sponsorship Statement
Every video script ends with the voiceover and visible caption overlay:
> *"IDE Guide is independent and unsponsored. Subscribe for honest developer editor guides daily!"*

## 5. Output Format Requirement
Google Flow prompt files are exported as both JSON (`.flow.json`) and Markdown (`.flow.md`) containing camera instructions, prompt strings, timing, and voiceover text so creators can copy-paste directly into Google Flow or automated video pipelines.
