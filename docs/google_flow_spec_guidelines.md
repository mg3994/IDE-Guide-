# Google Flow Video Generation Specification Guidelines

This document outlines the visual, auditory, and structural specifications for generating videos and YouTube Shorts using **Google Flow** and AI video tools for [@IDEguide](https://www.youtube.com/@IDEguide).

## Overview

IDE Guide produces 3 daily short-form and long-form video packages covering code editors, IDEs, and developer tools. To ensure visually striking, high-retention videos that attract developer audiences, every video specification file must include detailed prompts for AI video generation engines like Google Flow, Runway, or Sora.

## Video Specification Structure

Each video spec file (JSON or YAML/Markdown format) must provide:

### 1. Metadata
- **Title**: Attention-grabbing, high CTR title.
- **Target Audience**: Developers, software engineers, devops, students.
- **IDE / Editor Name**: Exact tool covered.
- **Pricing Status**: Free / Freemium / Open Source / Paid.
- **Duration**: Target length (e.g., 60 seconds for Shorts, 5-8 minutes for detailed guides).

### 2. Scene-by-Scene Prompt Breakdown
Each scene must explicitly define:
- **Scene Number & Duration**: Timestamp window.
- **Google Flow Visual Prompt**: High-detail prompt describing subject, environment, camera movement, lighting, and art style.
- **Framing & Aspect Ratio**: 9:16 vertical for Shorts / 16:9 widescreen for main videos.
- **Lighting & Aesthetics**: e.g., "Cinematic dark studio, neon blue & purple ambient rim lighting, 4K resolution, ultra-crisp interface elements".
- **Screen Action**: Code editor UI interactions (e.g., AI autocomplete in action, split view debugging, extension installation).
- **Voiceover / Narration Script**: Conversational, fast-paced, insightful dev commentary.
- **On-Screen Text Overlay**: Bold key phrases for muted viewing retention.

### 3. Visual Prompting Standards for Google Flow
- **Environment**: Clean modern developer desk setup, glowing OLED monitor displaying code, dark mode IDE.
- **Camera Work**: Smooth pan, slow zoom into key UI features, fast dynamic transitions between pros and cons.
- **Tone & Mood**: High-tech, unbiased, sleek, professional yet accessible.

### 4. Required Content Breakdown
Every video must cover:
1. **Hook**: Immediate visual callout (e.g., "Is VS Code still king in 2026 or is Cursor taking over?").
2. **Core Features Showcase**: Top 2-3 standout features with visual prompt cues.
3. **The Good (Pros)**: Why developers love it.
4. **The Bad (Cons)**: Objective weaknesses or resource hogs.
5. **Pricing & Verdict**: Paid vs Free breakdown and recommendation.
6. **Mandatory Audio/Visual Disclaimer**:
   > "IDE Guide is independent and unsponsored. All reviews are 100% objective developer evaluations."

## Example Google Flow Visual Prompt
```text
Cinematic close-up of a developer's workstation at night. A futuristic dark-mode code editor interface glows on an ultra-wide screen with syntax-highlighted Python code. Cyberpunk-inspired subtle blue rim lighting, smooth camera dolly push-in towards the editor window, 8k resolution, highly detailed interface elements, realistic dynamic lighting.
```
