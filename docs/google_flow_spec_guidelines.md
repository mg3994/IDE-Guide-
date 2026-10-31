# Google Flow Video Generation & Script Specifications

This document defines the agentic prompting, visual composition, pacing, and script standards for generating YouTube videos and Shorts for **IDE Guide** (`https://www.youtube.com/@IDEguide`).

## 1. Goal & Format
Every IDE review must produce:
1. **Vertical YouTube Shorts (9:16 aspect ratio)**: Fast-paced, engaging 45–60 second video designed to maximize viewer retention and click-through.
2. **Horizontal In-Depth Video (16:9 aspect ratio)**: Comprehensive 3–5 minute video breaking down features, live coding workflow, benchmarks, pros & cons, pricing, and final verdict.

## 2. Google Flow Visual & Scene Prompting Standard
When generating prompts for Google Flow, Runway Gen-3, Luma Dream Machine, or Sora:
- **Cinematic Camera Directives**: Specify camera angles (macro close-up on code syntax, slow dolly zoom, sleek 45-degree angle of laptop display with floating holographic UI, isometric desktop render).
- **Lighting & Atmosphere**: Cyberpunk/developer neon accents, volumetric soft rim lighting, OLED dark mode studio vibe.
- **Pacing**: Rapid cut intervals (every 2.5 to 3.5 seconds) in Shorts; sustained explanatory visual B-roll (5-7 seconds) in long-form.
- **Visual Cues**: Screen captures of real code refactoring, split-screen comparison with VS Code / competitors, benchmarks bar charts rendering smoothly.

## 3. Required Sections for Every Video Spec

Each video package JSON / Markdown must contain:

1. **Metadata**:
   - `video_title`: Attention-grabbing title under 65 chars (e.g., "Is Cursor Really Better Than VS Code in 2025?").
   - `hook_statement`: The first 3 seconds that stop the scroll (e.g., "Stop paying for Copilot until you see what this free editor can do!").
   - `target_ide`: Tool name and version.
   - `pricing_tier`: "Free & Open Source", "Freemium", or "Commercial / Paid".
   - `tags`: YouTube SEO keywords (`#coding`, `#webdev`, `#aiide`, `#programming`).

2. **Scene-by-Scene Storyboard**:
   For each scene (Hook, Overview, The Good, The Bad, Pricing & Best For, Final Verdict):
   - `scene_number`: Integer.
   - `duration_seconds`: Target timestamp duration.
   - `google_flow_prompt`: Precise generative video prompt describing foreground, background, camera motion, lighting, and action.
   - `on_screen_text`: Bold lower-third text overlay for sound-off viewers.
   - `voiceover_script`: Conversational, authoritative developer narration.
   - `b_roll_suggestion`: Screencast footage description (e.g., "Terminal benchmark running Neovim vs VS Code startup time").

3. **Audio & Sound Effects (SFX)**:
   - Upbeat, modern electronic/lo-fi background music track suggestion.
   - Sound FX triggers: Whoosh on transitions, subtle keyboard typing clatter, error buzzer on cons, cash register on pricing mention.

4. **Mandatory Non-Sponsorship Disclaimer**:
   Every script must verbalize or display:
   > "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
