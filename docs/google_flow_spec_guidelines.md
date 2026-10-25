# Google Flow Video Generation Guidelines (@IDEguide YouTube Channel)

This document provides prompt formatting specifications, visual direction, and audio scripting standards for creating dynamic AI-generated video content using Google Flow (and related AI video suites) for the **IDE Guide** YouTube channel (https://www.youtube.com/@IDEguide).

---

## 1. Video Types & Formats

We produce two distinct video formats daily:

1. **YouTube Shorts (9:16 Vertical, 30-60 Seconds)**
   - Fast-paced, punchy, high-hook retention.
   - Ideal for quick takeaways, feature highlights, and direct comparison verdicts (e.g., "3 Reasons to Switch from VS Code to Zed").

2. **YouTube Long-Form (16:9 Horizontal, 3-8 Minutes)**
   - Deep-dive technical breakdown.
   - Covers installation/setup, real-time code editing experience, benchmark speed tests, memory consumption, pricing models, and trade-offs.

---

## 2. Google Flow Prompt Structure

To ensure maximum visual appeal and high viewer retention, every scene prompt for Google Flow must adhere to the following schema:

### Scene Prompt Template

```json
{
  "scene_number": 1,
  "duration_seconds": 5,
  "visual_prompt": "[Camera Framing & Movement] + [Subject & IDE Interface] + [Lighting & Style] + [Atmosphere/Environment]",
  "voiceover_script": "Punctual, energetic narration matching the exact timing of the scene.",
  "on_screen_text": "Key summary bullet or highlighted feature text."
}
```

### Visual Prompt Best Practices

- **Framing**: Use macro close-ups on syntax highlighted code, wide cinematic studio shots of modern developer setups, or smooth tracking pan shots across dual ultra-wide monitors.
- **Lighting & Aesthetics**: Cyberpunk neon dark mode aesthetic, soft diffused studio key light, sleek minimal dark mode IDE themes (One Dark Pro, Dracula, Tokyo Night).
- **Motion**: Dynamic zoom into AI code generation prompts, slick UI transitions, floating 3D neon telemetry charts for speed and memory benchmarks.
- **Style Keywords**: `Ultra-realistic 4k`, `cinematic studio lighting`, `shallow depth of field`, `sleek developer workstation`, `neon accent lighting`, `clean IDE interface UI`.

---

## 3. Daily Production Strategy (3 Videos / Day)

Each day, the generator creates 3 distinct video specification packages:

1. **Video 1 (IDE Spotlight / Breakdown)**: Focuses on a newly updated or trending editor (e.g., Cursor, Neovim 0.10, Fleet).
2. **Video 2 (Head-to-Head Comparison)**: Direct comparison between two popular IDEs (e.g., PyCharm vs VS Code with Python extensions).
3. **Video 3 (Niche / Lightweight / Web Editors)**: Highlights lightweight, terminal-based, or specialized editors (e.g., Zed, Helix, Lapce, Replit).

---

## 4. Required Content Elements

Every video specification must include:

1. **Catchy Title & Description**: SEO-optimized with relevant hashtags (`#IDEGuide`, `#Coding`, `#VSCode`, `#WebDev`).
2. **Free vs Paid Tier Analysis**: Explicit guidance on pricing (e.g., Open Source, Free Tier limit, $20/mo Pro plan).
3. **Good & Bad (Pros & Cons)**: Honest, balanced review.
4. **Target Audience Recommendation**: Clear answer on who should use it.
5. **Mandatory Disclaimer**:
   > "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor mentioned in this video."

---

## 5. Sample Google Flow Spec Output

```json
{
  "video_title": "Zed Editor in 2025: Is It Really 10x Faster Than VS Code?",
  "format": "YouTube Shorts (9:16)",
  "target_ide": "Zed",
  "pricing": "Free & Open Source",
  "scenes": [
    {
      "scene": 1,
      "visual_prompt": "Cinematic close-up of a high-tech developer desk, 4K resolution, ultra-fast code scrolling on a dark theme Zed editor interface with glowing GPU-accelerated cursor motion, cyberpunk dark studio lighting.",
      "voiceover_script": "Tired of bloated code editors taking up gigabytes of RAM? Meet Zed — the GPU-accelerated editor built in Rust.",
      "on_screen_text": "Zed Editor: 10x Faster Code Editing"
    }
  ],
  "disclaimer": "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor."
}
```
