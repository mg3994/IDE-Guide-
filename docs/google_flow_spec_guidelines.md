# Google Flow & Video Prompt Specifications for IDE Guide (@IDEguide)

This document establishes video generation specifications and prompt formatting guidelines for creating videos and Shorts for YouTube ([@IDEguide](https://www.youtube.com/@IDEguide)) using AI video tools like Google Flow.

---

## 1. Overview & Format Requirements

`IDE Guide` publishes daily technical video content comparing and reviewing IDEs and code editors.

- **YouTube Shorts (9:16 vertical)**: Fast-paced, high-impact 30-60 second vertical videos.
- **YouTube Main Video (16:9 landscape)**: Detailed 2-5 minute deep dives.
- **Daily Volume**: 3 video scripts/specs per day.

---

## 2. Video Specification Structure

Each video spec generated for Google Flow or video AI production must follow this structured JSON/Markdown schema:

1. **Metadata**: Title, Target Platform (Shorts / Main), Aspect Ratio, IDE Name, Pricing Category (Free / Paid / Freemium).
2. **Audio & Voiceover Script**:
   - Voice Profile: Energetic, professional technical narrator.
   - Word Count: ~130-160 words for 60s Shorts; ~300-600 words for main video.
3. **Scene Breakdown**:
   - **Scene Number**: Sequential marker (Scene 1, Scene 2, etc.).
   - **Duration**: Timestamp range (e.g., 00:00 - 00:05).
   - **Visual Prompt (for Google Flow)**: Detailed prompt specifying camera angle, lighting, subject matter, UI highlights, color palette, and cinematic motion.
   - **Framing & Motion Cues**: E.g., Close-up panning across code lines, macro shot of AI autocomplete prompt, high-contrast dark mode UI glow.
   - **On-Screen Text Overlay**: Punchy title overlays highlighting key takeaways.
   - **Voiceover Line**: Corresponding narration audio script line.

---

## 3. Google Flow Visual Prompt Standards

To achieve visually compelling AI-generated visual scenes, Google Flow prompts must adhere to these aesthetics:

- **Style**: Modern tech aesthetic, sleek dark-mode IDE interface, subtle neon accents, ultra-sharp 4K digital rendering, soft ambient studio lighting.
- **Lighting**: Soft cinematic blue/purple ambient rim light reflecting off clean glass surfaces or sleek developer workstations.
- **Framing**: Smooth slow panned close-ups, dynamic rack focus between code syntax highlighting and developer cursor movements, isometric 3D workstation views.
- **Color Palette**: Dark charcoal slate backdrop (#0f172a), vibrant cyan syntax highlights (#06b6d4), emerald green success indicators (#10b981), and amber warning alerts (#f59e0b).

---

## 4. Video Script Flow & Mandatory Elements

Each video script must follow this narrative arc:

1. **Hook (0-5s)**: High-curiosity question or striking visual highlight about the IDE (e.g., *"Is Cursor really replacing VS Code?"* or *"The fastest free code editor you haven't tried yet!"*).
2. **Core Feature Showcase**: Dynamic walkthrough of key features, speed, AI integration, pricing model (Paid vs Free).
3. **Pros & Cons Comparison**: Quick, balanced comparison of strengths and limitations.
4. **Final Recommendation**: Clear advice on which developers benefit most.
5. **Mandatory Non-Sponsorship Disclaimer**: Every video specification must include the spoken and visual disclaimer:
   > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*
