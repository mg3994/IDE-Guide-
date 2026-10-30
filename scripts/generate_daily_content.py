"""Daily Content Package Generator for IDE Guide.

Produces 3 AMP-compliant Blogger blog posts and 3 Google Flow video/shorts specifications
every day. Maintains history to cycle through IDEs without repeating until all are covered.
"""

import os
import sys
import json
import datetime
from typing import Dict, Any, List, Tuple

# Ensure project root is in sys.path when invoked directly
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from data.ide_database import IDE_CATALOG, get_all_ide_names
from scripts.amp_validator import validate_amp_blogger_content, MANDATORY_DISCLAIMER_KEYWORD

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

HISTORY_FILE_PATH = "content/history.json"


def load_history(history_path: str = HISTORY_FILE_PATH) -> List[str]:
    """Load previously covered IDE names."""
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("covered_ides", [])
        except Exception:
            return []
    return []


def save_history(covered_ides: List[str], history_path: str = HISTORY_FILE_PATH) -> None:
    """Save covered IDE names to history file."""
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "total_covered": len(covered_ides),
                "covered_ides": covered_ides,
            },
            f,
            indent=2,
        )


def select_daily_ides(count: int = 3, history_path: str = HISTORY_FILE_PATH) -> List[str]:
    """Select 'count' IDEs that have not been covered recently."""
    all_ides = get_all_ide_names()
    covered = load_history(history_path)

    available = [ide for ide in all_ides if ide not in covered]
    if len(available) < count:
        # If all or most IDEs have been covered, reset cycle while keeping sequence
        covered = []
        available = all_ides

    selected = available[:count]
    covered.extend(selected)
    save_history(covered, history_path)
    return selected


def generate_amp_blog_post(ide_data: Dict[str, Any]) -> str:
    """Generate AMP-compliant HTML blog post content specifically for Blogger."""
    name = ide_data["name"]
    tagline = ide_data["tagline"]
    category = ide_data["category"]
    pricing_model = ide_data["pricing_model"]
    pricing_details = ide_data["pricing_details"]
    pros = ide_data["pros"]
    cons = ide_data["cons"]
    best_for = ide_data["best_for"]
    official_url = ide_data["official_url"]

    pros_html = "\n".join([f"    <li><strong>{p}</strong></li>" for p in pros])
    cons_html = "\n".join([f"    <li><strong>{c}</strong></li>" for c in cons])

    price_badge_color = "#10b981" if not ide_data["is_paid"] else "#f59e0b"
    price_badge_text = "FREE / OPEN SOURCE" if not ide_data["is_paid"] else "COMMERCIAL / FREEMIUM"

    html = f"""<article class="ide-guide-post" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.68; color: #1e293b; max-width: 840px; margin: 0 auto; padding: 18px;">
  <header style="border-bottom: 2px solid #e2e8f0; padding-bottom: 20px; margin-bottom: 24px;">
    <span style="background: {price_badge_color}; color: #ffffff; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">{price_badge_text}</span>
    <span style="background: #0284c7; color: #ffffff; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 700; margin-left: 8px;">{category}</span>
    <h1 style="font-size: 28px; line-height: 1.3; color: #0f172a; margin-top: 14px; margin-bottom: 8px;">{name} Deep Dive: The Good, The Bad & The Verdict</h1>
    <p style="font-size: 16px; color: #475569; font-style: italic; margin-top: 0;">{tagline}</p>
  </header>

  <section class="overview-section" style="margin-bottom: 28px;">
    <h2 style="font-size: 20px; color: #1e293b; border-left: 4px solid #0284c7; padding-left: 10px; margin-bottom: 12px;">Executive Summary</h2>
    <p>Choosing the right development environment directly dictates your productivity, memory overhead, and daily programming ergonomics. In this independent analysis from <strong>IDE Guide</strong>, we scrutinize <strong>{name}</strong> to discover whether it deserves a spot in your daily engineering toolkit.</p>
    <p>Official Website: <a href="{official_url}" target="_blank" rel="noopener noreferrer" style="color: #0284c7; text-decoration: underline;">{official_url}</a></p>
  </section>

  <section class="the-good" style="background: #f0fdf4; border-left: 4px solid #16a34a; padding: 18px 22px; border-radius: 6px; margin-bottom: 24px;">
    <h2 style="font-size: 20px; color: #166534; margin-top: 0; margin-bottom: 12px;">👍 The Good (Standout Strengths)</h2>
    <ul style="margin: 0; padding-left: 20px; color: #14532d;">
{pros_html}
    </ul>
  </section>

  <section class="the-bad" style="background: #fef2f2; border-left: 4px solid #dc2626; padding: 18px 22px; border-radius: 6px; margin-bottom: 24px;">
    <h2 style="font-size: 20px; color: #991b1b; margin-top: 0; margin-bottom: 12px;">👎 The Bad (Critical Drawbacks)</h2>
    <ul style="margin: 0; padding-left: 20px; color: #7f1d1d;">
{cons_html}
    </ul>
  </section>

  <section class="pricing-tier" style="margin-bottom: 28px; background: #f8fafc; padding: 18px; border-radius: 6px; border: 1px solid #e2e8f0;">
    <h2 style="font-size: 20px; color: #1e293b; margin-top: 0;">💰 Pricing Model: {pricing_model}</h2>
    <p style="margin-bottom: 0;"><strong>Cost Details:</strong> {pricing_details}</p>
  </section>

  <section class="verdict-section" style="margin-bottom: 28px;">
    <h2 style="font-size: 20px; color: #1e293b; border-left: 4px solid #f59e0b; padding-left: 10px; margin-bottom: 12px;">🎯 Who Is It Best For?</h2>
    <p><strong>Ideal Developer Persona:</strong> {best_for}</p>
  </section>

  <footer class="independent-disclaimer" style="margin-top: 36px; padding: 16px; background: #f1f5f9; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 13px; color: #64748b; line-height: 1.5;">
    <p style="margin: 0;"><strong>Editorial Transparency:</strong> {DISCLAIMER_TEXT}</p>
  </footer>
</article>
"""
    # Validation step
    is_valid, errors = validate_amp_blogger_content(html)
    if not is_valid:
        raise ValueError(f"Generated post failed AMP validation: {errors}")
    return html


def generate_flow_video_spec(ide_data: Dict[str, Any], is_short: bool = False) -> Dict[str, Any]:
    """Generate structured Google Flow and generative AI video production package."""
    name = ide_data["name"]
    category = ide_data["category"]
    tagline = ide_data["tagline"]
    pricing_model = ide_data["pricing_model"]
    pricing_details = ide_data["pricing_details"]
    pros = ide_data["pros"]
    cons = ide_data["cons"]
    best_for = ide_data["best_for"]
    flow_prompt = ide_data["flow_broll_prompt"]
    visual_theme = ide_data["visual_theme"]

    aspect_ratio = "9:16 (1080x1920)" if is_short else "16:9 (1920x1080)"
    duration = "55 Seconds" if is_short else "4 Minutes 30 Seconds"
    format_type = "YouTube Shorts / Vertical Reel" if is_short else "Full YouTube Video Feature"

    scenes = [
        {
            "scene_number": 1,
            "timestamp": "00:00 - 00:06",
            "title": "The Hook",
            "voiceover": (
                f"Stop blindly choosing your code editor. Today we test {name}—{tagline}. "
                f"Is it worth your time, or a total memory hog?"
            ),
            "flow_visual_prompt": (
                f"Cinematic {aspect_ratio.split()[0]} dynamic macro shot of illuminated fingers flying across "
                f"a mechanical keyboard, camera rapidly panning into a dark 4K monitor displaying {name} code view. "
                f"Lighting: Neon cyan and amber accent rim light, 60fps high shutter speed, photorealistic."
            ),
            "on_screen_text": f"{name.upper()}: HONEST TRUTH",
            "sound_design": "High energy digital riser followed by a deep sub bass impact.",
        },
        {
            "scene_number": 2,
            "timestamp": "00:06 - 00:22",
            "title": "The Good (Strengths)",
            "voiceover": (
                f"Here is why engineers love {name}: First, {pros[0]}. "
                f"Second, {pros[1]}."
            ),
            "flow_visual_prompt": flow_prompt,
            "on_screen_text": f"PROS: {pros[0][:38]}...",
            "sound_design": "Rhythmic modern lo-fi tech beat with crisp keystroke clicks.",
        },
        {
            "scene_number": 3,
            "timestamp": "00:22 - 00:38",
            "title": "The Bad (Downsides)",
            "voiceover": (
                f"Now for the painful truth: {cons[0]}. "
                f"Additionally, {cons[1]}."
            ),
            "flow_visual_prompt": (
                f"Cinematic {aspect_ratio.split()[0]} close-up of a split screen showing system resource graphs "
                f"surging in red with warning diagnostics, moody industrial lighting, shallow depth of field, 8k render."
            ),
            "on_screen_text": f"CONS: {cons[0][:38]}...",
            "sound_design": "Sudden low pass filter on music with subtle alert chime.",
        },
        {
            "scene_number": 4,
            "timestamp": "00:38 - 00:55",
            "title": "Pricing & Independent Verdict",
            "voiceover": (
                f"Pricing model: {pricing_model}. {pricing_details}. "
                f"Verdict: Best for {best_for}. "
                f"We are 100% independent and unsponsored—subscribe to IDE Guide for honest dev reviews."
            ),
            "flow_visual_prompt": (
                f"Clean minimalist studio shot {aspect_ratio.split()[0]} displaying high-contrast typography badges "
                f"for '{pricing_model}' and {name} logo banner, soft cinematic bokeh, smooth dolly back."
            ),
            "on_screen_text": f"PRICE: {pricing_model.upper()} | SUBSCRIBE @IDEguide",
            "sound_design": "Upbeat synthesizer swell ending with an authoritative kick drum.",
        },
    ]

    return {
        "channel": "@IDEguide",
        "target_platform": "YouTube & Shorts",
        "ide_name": name,
        "format": format_type,
        "aspect_ratio": aspect_ratio,
        "estimated_duration": duration,
        "visual_style_theme": visual_theme,
        "google_flow_prompts": {
            "master_aesthetic_prompt": (
                f"Ultra-detailed developer workstation aesthetic, {visual_theme}, cinematic lighting, "
                f"volumetric dust motes, 35mm lens, depth of field, photorealistic 8k render, {aspect_ratio.split()[0]}."
            ),
            "scenes": scenes,
        },
        "youtube_metadata": {
            "title": f"{name} Review (2026): Is It Good or Bad? | Free vs Paid Explained",
            "description": (
                f"Our independent breakdown of {name} ({tagline}).\n\n"
                f"In this video we explore:\n"
                f"- Standout strengths and workflow boosts\n"
                f"- Critical drawbacks and performance hurdles\n"
                f"- Pricing tiers ({pricing_model})\n"
                f"- Who should actually use it\n\n"
                f"{DISCLAIMER_TEXT}\n\n"
                f"Subscribe to @IDEguide for daily code editor benchmarks and developer guides!"
            ),
            "tags": [
                name,
                "IDE Guide",
                "Code Editor Review",
                "Programming",
                pricing_model,
                category,
                "Developer Productivity",
            ],
        },
        "independent_disclaimer": DISCLAIMER_TEXT,
    }


def run_daily_generation(output_base_dir: str = "content", target_date: str = None) -> Dict[str, Any]:
    """Execute complete daily generation of 3 blog posts and 3 video packages."""
    if not target_date:
        target_date = datetime.date.today().isoformat()

    daily_dir = os.path.join(output_base_dir, target_date)
    posts_dir = os.path.join(daily_dir, "blog_posts")
    videos_dir = os.path.join(daily_dir, "google_flow_videos")

    os.makedirs(posts_dir, exist_ok=True)
    os.makedirs(videos_dir, exist_ok=True)

    history_path = os.path.join(output_base_dir, "history.json")
    selected_ides = select_daily_ides(count=3, history_path=history_path)

    results = {
        "date": target_date,
        "selected_ides": selected_ides,
        "generated_files": [],
    }

    for idx, ide_key in enumerate(selected_ides, start=1):
        ide_data = IDE_CATALOG[ide_key]
        safe_name = ide_key.lower().replace(" ", "_").replace("(", "").replace(")", "")

        # 1. Generate AMP Blog Post
        amp_html = generate_amp_blog_post(ide_data)
        blog_file = os.path.join(posts_dir, f"{idx:02d}_{safe_name}_amp_post.html")
        with open(blog_file, "w", encoding="utf-8") as f:
            f.write(amp_html)
        results["generated_files"].append(blog_file)

        # 2. Generate Google Flow Video Spec (Full 16:9)
        video_spec_16_9 = generate_flow_video_spec(ide_data, is_short=False)
        video_file_16_9 = os.path.join(videos_dir, f"{idx:02d}_{safe_name}_flow_spec_16x9.json")
        with open(video_file_16_9, "w", encoding="utf-8") as f:
            json.dump(video_spec_16_9, f, indent=2)
        results["generated_files"].append(video_file_16_9)

        # 3. Generate Google Flow Shorts Spec (Vertical 9:16)
        video_spec_9_16 = generate_flow_video_spec(ide_data, is_short=True)
        video_file_9_16 = os.path.join(videos_dir, f"{idx:02d}_{safe_name}_flow_spec_shorts_9x16.json")
        with open(video_file_9_16, "w", encoding="utf-8") as f:
            json.dump(video_spec_9_16, f, indent=2)
        results["generated_files"].append(video_file_9_16)

    return results


if __name__ == "__main__":
    out = run_daily_generation()
    print(f"Generated daily package for {out['date']}:")
    for f in out["generated_files"]:
        print(f" - {f}")
