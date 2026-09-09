"""
Google Flow Video Specification Generator for YouTube (@IDEguide)
Generates AI video generation prompts, framing, lighting, and scene scripts.
"""

from typing import Dict, Any

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

def generate_google_flow_video_spec(ide_data: Dict[str, Any], format_type: str = "shorts") -> str:
    """
    Generate a Google Flow video spec document in Markdown.
    format_type: 'shorts' (9:16 vertical) or 'longform' (16:9 horizontal)
    """
    name = ide_data.get("name", "IDE Review")
    developer = ide_data.get("developer", "Developer")
    license_type = ide_data.get("license_type", "Free / Open Source")
    pricing = ide_data.get("pricing", "Free")
    description = ide_data.get("description", "")
    pros = ide_data.get("pros", ["Great features", "Smooth workflow"])
    cons = ide_data.get("cons", ["Learning curve", "Resource usage"])
    target_audience = ide_data.get("target_audience", "Developers")
    verdict_rating = ide_data.get("verdict_rating", "9.0/10")
    verdict_summary = ide_data.get("verdict_summary", "Recommended code editor.")

    aspect_ratio = "9:16 (Vertical 1080x1920)" if format_type == "shorts" else "16:9 (Horizontal 1920x1080)"
    target_duration = "60 Seconds" if format_type == "shorts" else "180 Seconds"

    pro1 = pros[0] if len(pros) > 0 else "High performance and flexibility"
    pro2 = pros[1] if len(pros) > 1 else "Rich plugin and tooling support"
    con1 = cons[0] if len(cons) > 0 else "Requires slight setup time"

    markdown_spec = f"""# Google Flow Video Specification: {name}

**Channel**: YouTube ([@IDEguide](https://www.youtube.com/@IDEguide))
**Target Format**: {format_type.upper()}
**Aspect Ratio**: {aspect_ratio}
**Target Duration**: {target_duration}
**Subject**: {name} (by {developer})
**License & Pricing**: {license_type} ({pricing})

---

## 🎬 Production & Prompt Engineering Directives

- **Visual Aesthetic**: Sleek futuristic programmer desk setup, ultra-high resolution dark mode coding interface, dynamic cyber-ambient studio backlight (blue/violet accent lighting), sharp focus, 8K hyper-realistic render.
- **Color Palette**: Dark Slate (`#0f172a`), Electric Cyan (`#38bdf8`), Neon Purple (`#a855f7`), Emerald Green (`#22c55e`).
- **Audio Profile**: Crisp, clear male/female tech presenter voiceover, ambient low-fi electronic background music with gentle bass drop on scene transitions.

---

## 📽️ Scene-by-Scene Script & Google Flow Prompts

### Scene 1: Visual Hook (0:00 - 0:08)
- **Google Flow Visual Prompt**: `A high-tech ultra-wide curved OLED monitor glowing with sleek dark-mode code editor UI in a dark minimalist programmer studio. Neon blue ambient backlight reflecting on polished desk surface. 8K resolution, photorealistic.`
- **Camera Movement**: Dramatic fast dolly forward zoom towards the editor screen with subtle motion blur.
- **Lighting & Framing**: High-contrast dark room with vibrant code syntax highlighting glowing on monitor. Center framed.
- **On-Screen Text**: "Is {name} Worth Your Time in 2025? 🤔"
- **Voiceover Script**: "Is {name} the ultimate code editor you should be using right now, or is it just another hyped tool? Let's break down the good, the bad, and who it's actually built for!"

---

### Scene 2: Feature Showcase & Overview (0:08 - 0:22)
- **Google Flow Visual Prompt**: `Close-up macro detail shot of code auto-typing inside {name} UI on a glossy high-refresh-rate monitor. Smooth cursor movements, glowing syntax highlighting, floating code suggestions.`
- **Camera Movement**: Slow steady horizontal tracking pan across the code lines with shallow depth of field.
- **Lighting & Framing**: Soft studio key light with subtle purple fill light. Macro close-up shot.
- **On-Screen Text**: "{name} Overview | Developer: {developer}"
- **Voiceover Script**: "{name}, developed by {developer}, is engineered for modern developers. {description}"

---

### Scene 3: The Good (Pros) (0:22 - 0:36)
- **Google Flow Visual Prompt**: `Brightly illuminated developer workspace with a dual monitor setup displaying fast multi-file indexing and instant terminal output in {name}. Emerald green glow indicators.`
- **Camera Movement**: Over-the-shoulder medium shot smoothly orbiting around the programmer typing at a ergonomic mechanical keyboard.
- **Lighting & Framing**: Crisp white key light with green rim lighting highlighting high performance.
- **On-Screen Text**: "✅ THE GOOD: Fast & Powerful"
- **Voiceover Script**: "Here's what makes {name} shine: First, {pro1}. Second, {pro2}. It delivers an exceptional velocity boost for daily coding."

---

### Scene 4: The Bad (Cons) (0:36 - 0:48)
- **Google Flow Visual Prompt**: `Warm amber backlit studio workspace with a close-up screen view showing configuration settings and system resource meters in {name}.`
- **Camera Movement**: High-angle slow tilt down towards the keyboard and screen.
- **Lighting & Framing**: Warm amber accent lighting providing a balanced, cautious mood.
- **On-Screen Text**: "⚠️ THE BAD: Things to Consider"
- **Voiceover Script**: "However, it's not without drawbacks. Keep in mind that {con1}. Make sure your workflow aligns with these trade-offs."

---

### Scene 5: Pricing, License & Verdict (0:48 - 0:55)
- **Google Flow Visual Prompt**: `Sleek futuristic 3D badge graphic showing 'RATING: {verdict_rating}' floating in front of a glowing glass panel with cyber background.`
- **Camera Movement**: Static center lock with smooth rotational camera sweep.
- **Lighting & Framing**: Studio spotlight on rating badge card.
- **On-Screen Text**: "Rating: {verdict_rating} | {pricing}"
- **Voiceover Script**: "{name} comes as {pricing} under {license_type}. Overall rating: {verdict_rating}! {verdict_summary}"

---

### Scene 6: Disclaimer & Outro (0:55 - 1:00)
- **Google Flow Visual Prompt**: `Clean IDE Guide branded end card showing YouTube subscribe button, bell icon, and website URL ideguide.blogspot.com on dark glassmorphism background.`
- **Camera Movement**: Smooth zoom out with ambient particle glow fading to black.
- **Lighting & Framing**: Balanced cyan ambient glow.
- **On-Screen Text**: "Subscribe to @IDEguide | ideguide.blogspot.com"
- **Voiceover Script**: "Subscribe to IDE Guide for daily objective editor comparisons! Check out our full in-depth blog post at ideguide.blogspot.com."

---

## 📜 Non-Sponsorship Disclaimer

{DISCLAIMER_TEXT}
"""
    return markdown_spec
