"""Google Flow Video Specification Generator for YouTube (@IDEguide).

Generates AI video prompts, scene breakdowns, visual lighting/camera specifications,
and voiceover scripts compatible with Google Flow and video production tools.
"""

from typing import Dict, Any, List
import json
from scripts.lib.amp_generator import DISCLAIMER_TEXT


def generate_google_flow_spec(ide_info: Dict[str, Any]) -> Dict[str, Any]:
    """Generates structured video specification for Google Flow / AI Video Tools."""
    name = ide_info.get("name", "Unknown IDE")
    tagline = ide_info.get("tagline", "A powerful code editor for modern developers.")
    description = ide_info.get("description", "Comprehensive editor review.")
    pricing_type = ide_info.get("pricing_type", "Freemium")
    pricing_details = ide_info.get("pricing_details", "Free tier available.")
    features: List[str] = ide_info.get("features", ["AI assistance", "Lightning fast performance"])
    pros: List[str] = ide_info.get("pros", ["Extensible", "Fast"])
    cons: List[str] = ide_info.get("cons", ["Learning curve"])

    top_feature_1 = features[0] if len(features) > 0 else "Smart Code Completion"
    top_feature_2 = features[1] if len(features) > 1 else "Integrated Developer Tools"

    spec = {
        "title": f"{name} - Is It Worth Using? (Pros, Cons, Paid vs Free)",
        "channel": "@IDEguide",
        "youtube_url": "https://www.youtube.com/@IDEguide",
        "aspect_ratios": {
            "shorts": "9:16",
            "landscape": "16:9"
        },
        "target_duration_seconds": 60,
        "visual_style": {
            "theme": "Dark cyberpunk developer aesthetic with high contrast glowing syntax highlighting",
            "lighting": "Ambient blue (#0284c7) and purple (#9333ea) backlight with volumetric soft fog",
            "camera_angles": [
                "Macro extreme close-up on code typing on mechanical keyboard",
                "Cinematic slow zoom onto IDE editor workspace",
                "Wide shot of sleek dual-monitor developer desk setup"
            ],
            "color_palette": ["#0f172a", "#0284c7", "#9333ea", "#10b981", "#ef4444"]
        },
        "scenes": [
            {
                "scene_id": 1,
                "name": "Hook",
                "duration_seconds": 10,
                "google_flow_visual_prompt": f"Close-up cinematic shot of {name} IDE screen showing dark mode code editor with vibrant glowing syntax. Camera slow zoom-in as cursor types code rapidly.",
                "voiceover_script": f"Is {name} the ultimate code editor for developers? Let's break down its key features, pricing, and pros vs cons in 60 seconds!"
            },
            {
                "scene_id": 2,
                "name": "Core Features & Overview",
                "duration_seconds": 20,
                "google_flow_visual_prompt": f"Smooth pan across {name} UI showcasing sidebar, terminal, and intelligent suggestions. High contrast lighting highlighting key interface features.",
                "voiceover_script": f"{name} offers {top_feature_1} alongside {top_feature_2}. Built specifically to boost developer productivity with clean interface design."
            },
            {
                "scene_id": 3,
                "name": "Pricing & Pros vs Cons",
                "duration_seconds": 20,
                "google_flow_visual_prompt": f"Split screen visual: Left side highlighting green checkmarks for pros ({', '.join(pros[:2])}), right side highlighting red cross for cons ({', '.join(cons[:2])}). Overlay text showing pricing model: {pricing_type}.",
                "voiceover_script": f"Regarding pricing: it's {pricing_type.lower()} — {pricing_details}. On the plus side, {pros[0] if pros else 'great user experience'}. However, keep in mind {cons[0] if cons else 'minor setup required'}."
            },
            {
                "scene_id": 4,
                "name": "Verdict & Call to Action",
                "duration_seconds": 10,
                "google_flow_visual_prompt": f"Sleek animation of IDE Guide logo with YouTube subscribe icon and Blogger link ideguide.blogspot.com. Dark elegant background with blue glow.",
                "voiceover_script": f"Subscribe to @IDEguide for unbiased daily code editor reviews and visit ideguide.blogspot.com for full technical guides!"
            }
        ],
        "disclaimer": DISCLAIMER_TEXT
    }

    return spec


def format_google_flow_spec_md(spec: Dict[str, Any]) -> str:
    """Formats a video specification dictionary as a Markdown document."""
    title = spec.get("title", "IDE Review Video Spec")
    disclaimer = spec.get("disclaimer", DISCLAIMER_TEXT)
    scenes = spec.get("scenes", [])
    style = spec.get("visual_style", {})

    scenes_md = ""
    for s in scenes:
        scenes_md += f"""### Scene {s.get('scene_id')}: {s.get('name')} ({s.get('duration_seconds')}s)
- **Visual Prompt for Google Flow:** `{s.get('google_flow_visual_prompt')}`
- **Voiceover / Audio Script:** "{s.get('voiceover_script')}"

"""

    md = f"""# Google Flow Video Generation Spec: {title}

**Channel:** [YouTube @IDEguide]({spec.get('youtube_url')})
**Target Duration:** {spec.get('target_duration_seconds')} seconds (Shorts 9:16 / Video 16:9)

---

## Visual & Lighting Guidelines
- **Theme:** {style.get('theme')}
- **Lighting:** {style.get('lighting')}
- **Color Palette:** {', '.join(style.get('color_palette', []))}

---

## Scene Breakdown

{scenes_md}
---

## Mandatory Non-Sponsorship Disclaimer
> {disclaimer}
"""
    return md.strip()
