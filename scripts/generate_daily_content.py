"""
IDE Guide - Daily Content Generation Engine.

Produces:
1. 3 AMP-compliant blog posts for Google Blogger (https://ideguide.blogspot.com/)
2. 3 Google Flow video generation specs and narration scripts for YouTube (https://www.youtube.com/@IDEguide)

Features:
- Selects 3 IDEs per day from data/ide_database.json avoiding recently covered ones.
- Tracks history in content/history.json.
- Strictly adheres to AMP guidelines and Google Flow specs.
- Enforces independent non-sponsorship disclaimer across all content.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "ide_database.json"
HISTORY_PATH = BASE_DIR / "content" / "history.json"
CONTENT_DIR = BASE_DIR / "content"

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, "
    "endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)


def load_database() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_history() -> Dict[str, Any]:
    if HISTORY_PATH.exists():
        try:
            with open(HISTORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"history": []}
    return {"history": []}


def save_history(history_data: Dict[str, Any]):
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2)


def select_daily_editors(editors: List[Dict[str, Any]], count: int = 3) -> List[Dict[str, Any]]:
    history = load_history()
    recent_ids = []
    for entry in reversed(history.get("history", [])):
        recent_ids.extend(entry.get("editors", []))

    # Keep unique recent IDs preserving order
    seen = set()
    ordered_recent = [x for x in recent_ids if not (x in seen or seen.add(x))]

    # Sort editors so least-recently used come first
    def sort_key(editor: Dict[str, Any]) -> int:
        ed_id = editor["id"]
        if ed_id in ordered_recent:
            return ordered_recent.index(ed_id)
        return 999999

    sorted_editors = sorted(editors, key=sort_key, reverse=True)
    selected = sorted_editors[:count]

    # If count requested is greater than database length, wrap around
    if len(selected) < count and editors:
        while len(selected) < count:
            selected.append(editors[len(selected) % len(editors)])

    return selected


def generate_amp_blog_post(editor: Dict[str, Any], date_str: str) -> str:
    """Generates an AMP-compliant Blogger HTML blog post snippet."""
    pros_html = "".join(f"      <li style=\"margin-bottom: 8px;\"><strong>+</strong> {p}</li>\n" for p in editor["pros"])
    cons_html = "".join(f"      <li style=\"margin-bottom: 8px;\"><strong>-</strong> {c}</li>\n" for c in editor["cons"])
    features_html = "".join(f"      <li style=\"margin-bottom: 8px;\">{f}</li>\n" for f in editor.get("featured_features", []))

    pricing_badge_color = "#10b981" if editor["pricing"]["is_free"] else "#f59e0b"
    pricing_status = "FREE / OPEN SOURCE" if editor["pricing"]["is_free"] else f"COMMERCIAL / {editor['pricing']['tier'].upper()}"

    html = f"""<!-- IDE Guide Review: {editor['name']} | Published: {date_str} -->
<div class="ide-guide-post" style="max-width: 820px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.7;">

  <header style="border-bottom: 2px solid #e2e8f0; padding-bottom: 1.5rem; margin-bottom: 2rem;">
    <div style="display: inline-block; background-color: {pricing_badge_color}; color: #ffffff; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em; padding: 4px 10px; border-radius: 9999px; text-transform: uppercase; margin-bottom: 10px;">
      {pricing_status}
    </div>
    <h1 style="font-size: 2.25rem; font-weight: 800; color: #0f172a; line-height: 1.25; margin: 8px 0 12px 0;">
      {editor['name']} Review: {editor['tagline']}
    </h1>
    <p style="font-size: 1.05rem; color: #64748b; margin: 0;">
      Category: <strong>{editor['category']}</strong> | Rating: <strong>{editor['rating']} / 5.0</strong> | Official Site: <a href="{editor['url']}" target="_blank" rel="noopener noreferrer" style="color: #2563eb; text-decoration: underline;">{editor['url']}</a>
    </p>
  </header>

  <!-- Hero Visual Component (AMP Responsive Image) -->
  <figure style="margin: 0 0 2rem 0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
    <amp-img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80"
             width="1200"
             height="675"
             layout="responsive"
             alt="{editor['name']} Code Editor Deep Dive and Interface Overview">
    </amp-img>
    <figcaption style="font-size: 0.85rem; color: #64748b; text-align: center; padding: 8px 0; background: #f8fafc;">
      Figure 1: {editor['name']} developer interface, workflow ergonomics, and speed benchmark analysis.
    </figcaption>
  </figure>

  <!-- Executive Summary -->
  <section style="margin-bottom: 2rem;">
    <h2 style="font-size: 1.5rem; font-weight: 700; color: #0f172a; margin-bottom: 0.75rem;">Executive Summary</h2>
    <p style="font-size: 1.1rem; color: #334155;">
      {editor['verdict']}
    </p>
  </section>

  <!-- Pricing Breakdown -->
  <section style="background: #f8fafc; border-left: 4px solid {pricing_badge_color}; padding: 1.25rem 1.5rem; border-radius: 0 8px 8px 0; margin-bottom: 2rem;">
    <h2 style="font-size: 1.35rem; font-weight: 700; color: #0f172a; margin-top: 0; margin-bottom: 0.5rem;">Pricing & Licensing Breakdown</h2>
    <p style="margin: 0; font-size: 1.02rem; color: #334155;">
      <strong>Tier:</strong> {editor['pricing']['tier']}<br>
      <strong>Details:</strong> {editor['pricing']['details']}
    </p>
  </section>

  <!-- Pros & Cons Grid -->
  <section style="margin-bottom: 2rem;">
    <h2 style="font-size: 1.5rem; font-weight: 700; color: #0f172a; margin-bottom: 1rem;">Pros vs. Cons: The Real-World Developer Verdict</h2>

    <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.25rem;">
      <h3 style="font-size: 1.15rem; font-weight: 700; color: #065f46; margin-top: 0; margin-bottom: 0.75rem;">What Works Exceptionally Well</h3>
      <ul style="margin: 0; padding-left: 1.25rem; color: #047857;">
{pros_html}      </ul>
    </div>

    <div style="background: #fff1f2; border: 1px solid #fecdd3; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.25rem;">
      <h3 style="font-size: 1.15rem; font-weight: 700; color: #9f1239; margin-top: 0; margin-bottom: 0.75rem;">Potential Drawbacks & Limitations</h3>
      <ul style="margin: 0; padding-left: 1.25rem; color: #be123c;">
{cons_html}      </ul>
    </div>
  </section>

  <!-- Featured Highlights -->
  <section style="margin-bottom: 2rem;">
    <h2 style="font-size: 1.5rem; font-weight: 700; color: #0f172a; margin-bottom: 0.75rem;">Standout Technical Highlights</h2>
    <ul style="padding-left: 1.25rem; color: #334155;">
{features_html}    </ul>
  </section>

  <!-- Target Audience -->
  <section style="background: #f1f5f9; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 2rem;">
    <h2 style="font-size: 1.35rem; font-weight: 700; color: #0f172a; margin-top: 0; margin-bottom: 0.5rem;">Who Should Use {editor['name']}?</h2>
    <p style="margin: 0; color: #334155;">
      {editor['target_audience']}
    </p>
  </section>

  <!-- Channel & Media Links -->
  <section style="border-top: 1px solid #e2e8f0; padding-top: 1.5rem; margin-bottom: 2rem; text-align: center;">
    <h3 style="font-size: 1.2rem; font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">Watch Our Video Walkthrough</h3>
    <p style="color: #64748b; margin-bottom: 1rem;">
      Subscribe to our YouTube channel for hands-on editor benchmarks, AI tool comparisons, and coding productivity breakdowns.
    </p>
    <a href="https://www.youtube.com/@IDEguide" target="_blank" rel="noopener noreferrer" style="display: inline-block; background: #dc2626; color: #ffffff; text-decoration: none; font-weight: 700; padding: 10px 22px; border-radius: 6px; font-size: 0.95rem;">
      Subscribe on YouTube @IDEguide
    </a>
  </section>

  <!-- Mandatory Non-Sponsorship Disclaimer -->
  <footer style="border-top: 2px solid #e2e8f0; padding-top: 1.25rem; margin-top: 2.5rem; font-size: 0.82rem; color: #64748b; font-style: italic; text-align: center; line-height: 1.6;">
    {DISCLAIMER_TEXT}
  </footer>

</div>
"""
    return html.strip()


def generate_google_flow_video_spec(editor: Dict[str, Any], date_str: str) -> Dict[str, Any]:
    """Generates a Google Flow video generation specification and YouTube script."""
    pricing_state = "100% Free & Open Source" if editor["pricing"]["is_free"] else f"Paid / {editor['pricing']['tier']}"

    scenes = [
        {
            "scene_number": 1,
            "title": "The Hook & Visual Shock",
            "duration_seconds": 6,
            "visual_prompt": (
                f"Cinematic ultra-macro dolly-in on a curved OLED monitor showing {editor['name']} IDE in dark mode. "
                f"Neon glowing syntax highlighting in {editor['visual_prompts']['color_palette']}. "
                f"A mechanical keyboard in foreground with slight motion blur. 4K, 60fps, shallow depth of field."
            ),
            "camera_motion": "Smooth forward push-in with 24mm f/1.4 lens bokeh",
            "lighting": "Diffused cyberpunk accent lighting reflecting off matte screen",
            "narration_script": (
                f"Is {editor['name']} truly worth your time, or is it just another overhyped coding editor? "
                f"Here is what developers actually need to know before switching."
            ),
            "on_screen_text": f"🔥 {editor['name'].upper()}: HONEST DEV REVIEW",
            "sound_design": "Subtle low bass whoosh with soft mechanical key clicks"
        },
        {
            "scene_number": 2,
            "title": "The Superpower Feature Showcase",
            "duration_seconds": 15,
            "visual_prompt": (
                f"{editor['visual_prompts']['hero_shot']} "
                f"Showcase of {editor['name']}'s main feature: {editor['featured_features'][0]}. "
                f"Code auto-formatting and multi-file diffs highlighting in real-time. High tech HUD overlay."
            ),
            "camera_motion": "Slow right-to-left panning shot tracking code execution",
            "lighting": "Vibrant studio key light with clean high contrast monitor luminescence",
            "narration_script": (
                f"Starting with what makes {editor['name']} extraordinary: {editor['pros'][0]}. "
                f"Plus, {editor['pros'][1]}."
            ),
            "on_screen_text": f"⚡ SUPERPOWER: {editor['featured_features'][0]}",
            "sound_design": "Digital data stream synth chime and satisfying IDE completion sound"
        },
        {
            "scene_number": 3,
            "title": "The Hidden Flaws & Red Flags",
            "duration_seconds": 15,
            "visual_prompt": (
                f"Transition to a moody, dim setup with red emergency indicator accents. "
                f"Monitor displaying memory usage graphs, loading spinners, or configuration panels. "
                f"Realistic frustration: {editor['cons'][0]}."
            ),
            "camera_motion": "Dutch tilt angle with subtle camera shake to emphasize friction",
            "lighting": "Split lighting: cool blue on left, amber-red warning hue on right",
            "narration_script": (
                f"But here is the catch. The biggest downsides you must watch out for: "
                f"{editor['cons'][0]}. And also, {editor['cons'][1]}."
            ),
            "on_screen_text": "⚠️ WATCH OUT: REAL DRAWBACKS",
            "sound_design": "Tense synthetic pulse with low mechanical hum"
        },
        {
            "scene_number": 4,
            "title": "Pricing Reality & The Honest Verdict",
            "duration_seconds": 14,
            "visual_prompt": (
                f"Clean minimalist glassmorphic card popping onto the screen. "
                f"Displays: {pricing_state}. Details: {editor['pricing']['details']}. "
                f"Rating badge glowing with {editor['rating']} out of 5 stars."
            ),
            "camera_motion": "Static centered composition with dynamic UI motion graphics",
            "lighting": "Bright, clean daylight studio lighting representing total clarity",
            "narration_script": (
                f"Now let's talk money: {editor['pricing']['details']}. "
                f"Our final verdict: {editor['verdict']}"
            ),
            "on_screen_text": f"💰 PRICING: {pricing_state} | ⭐ {editor['rating']}/5.0",
            "sound_design": "Clean chime sound effect on star rating reveal"
        },
        {
            "scene_number": 5,
            "title": "Call To Action & Independent Disclaimer",
            "duration_seconds": 10,
            "visual_prompt": (
                "Cinematic high-tech outro card. Floating YouTube 'Subscribe' badge for @IDEguide. "
                "Blog link card: ideguide.blogspot.com. Clean modern typography with independent review badge."
            ),
            "camera_motion": "Slow zoom out to reveal the full creator studio setup",
            "lighting": "Balanced warm studio ambient lighting",
            "narration_script": (
                f"Should you download it? If you are {editor['target_audience'].lower()} - absolutely. "
                f"Subscribe to @IDEguide for daily editor comparisons, read the full deep-dive on ideguide.blogspot.com, "
                f"and remember: we are 100% independent and never sponsored by any software vendor."
            ),
            "on_screen_text": "🔔 SUBSCRIBE @IDEguide | ideguide.blogspot.com",
            "sound_design": "Warm ascending synth outro motif with bell chime"
        }
    ]

    spec = {
        "metadata": {
            "title": f"{editor['name']} Review: Is It Best for You? (Pros, Cons & Pricing)",
            "channel": "https://www.youtube.com/@IDEguide",
            "blog_url": "https://ideguide.blogspot.com/",
            "date": date_str,
            "target_format": ["YouTube Shorts (9:16)", "YouTube Standard (16:9)"],
            "total_estimated_duration_seconds": 60,
            "flow_ai_engine": "Google Flow / Generative Video Pipeline",
            "disclaimer": DISCLAIMER_TEXT
        },
        "editor_profile": {
            "id": editor["id"],
            "name": editor["name"],
            "category": editor["category"],
            "pricing_tier": editor["pricing"]["tier"],
            "is_free": editor["pricing"]["is_free"],
            "rating": editor["rating"]
        },
        "scenes": scenes,
        "youtube_metadata": {
            "video_title": f"{editor['name']} - Honest Review & Pricing Breakdown | IDE Guide",
            "tags": list(dict.fromkeys([
                editor["id"],
                editor["name"].lower(),
                "ide review",
                "code editor",
                "programming",
                "software engineering",
                "coding tools",
                "ide guide",
                "developer productivity"
            ])),
            "description": (
                f"Honest breakdown of {editor['name']} ({editor['category']}).\n\n"
                f"Read the full AMP article on our blog: https://ideguide.blogspot.com/\n"
                f"Subscribe to @IDEguide for daily objective software reviews!\n\n"
                f"Timestamps:\n"
                f"0:00 - Introduction\n"
                f"0:06 - Key Features\n"
                f"0:21 - Drawbacks & Cons\n"
                f"0:36 - Pricing & Cost\n"
                f"0:50 - Final Verdict\n\n"
                f"{DISCLAIMER_TEXT}"
            )
        }
    }
    return spec


def run_daily_generation(date_str: str | None = None) -> List[Dict[str, Any]]:
    """Runs daily generation of 3 AMP blog posts and 3 Google Flow video specs."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    db = load_database()
    editors = db["editors"]
    selected = select_daily_editors(editors, count=3)

    daily_dir = CONTENT_DIR / date_str
    daily_dir.mkdir(parents=True, exist_ok=True)

    results = []

    for index, editor in enumerate(selected, start=1):
        ed_id = editor["id"]

        # 1. AMP Blog Post
        amp_html = generate_amp_blog_post(editor, date_str)
        blog_filename = f"post_{index}_{ed_id}_amp.html"
        blog_path = daily_dir / blog_filename
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(amp_html)

        # 2. Google Flow Video Spec
        video_spec = generate_google_flow_video_spec(editor, date_str)
        video_filename = f"video_{index}_{ed_id}_flow_spec.json"
        video_path = daily_dir / video_filename
        with open(video_path, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)

        results.append({
            "index": index,
            "editor": editor["name"],
            "id": ed_id,
            "blog_path": str(blog_path),
            "video_path": str(video_path)
        })

    # Update history
    history = load_history()
    history["history"].append({
        "date": date_str,
        "editors": [e["id"] for e in selected]
    })
    save_history(history)

    return results


if __name__ == "__main__":
    import sys
    custom_date = sys.argv[1] if len(sys.argv) > 1 else None
    res = run_daily_generation(custom_date)
    print(f"Generated {len(res)} daily packages successfully:")
    for r in res:
        print(f"[{r['index']}] {r['editor']}:")
        print(f"   Blog HTML: {r['blog_path']}")
        print(f"   Video Spec: {r['video_path']}")
