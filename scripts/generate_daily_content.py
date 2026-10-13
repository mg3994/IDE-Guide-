#!/usr/bin/env python3
"""
Daily Content Generator Engine for IDE Guide.
Generates 3 AMP HTML blog posts & 3 Google Flow video specs per day.
Updates history in content/history.json.
"""

import os
import json
import datetime
from typing import Dict, Any, List

REQUIRED_DISCLAIMER = "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "ide_database.json")
HISTORY_PATH = os.path.join(PROJECT_ROOT, "content", "history.json")

def load_ide_database() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"IDE database not found at {DATA_PATH}")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_history() -> Dict[str, Any]:
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_ides": [], "daily_runs": []}

def save_history(history: Dict[str, Any]):
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def generate_amp_blog_post(ide: Dict[str, Any]) -> str:
    """Generates valid AMP HTML for Blogger."""
    pros_html = "".join([f"<li>{p}</li>" for p in ide.get("pros", [])])
    cons_html = "".join([f"<li>{c}</li>" for c in ide.get("cons", [])])
    features_html = "".join([f"<li><strong>{f}</strong></li>" for f in ide.get("key_features", [])])

    canonical_url = f"https://ideguide.blogspot.com/p/{ide['id']}-review.html"

    html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Deep Dive Review - Best Code Editors | IDE Guide</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1a202c; background-color: #f7fafc; margin: 0; padding: 20px; }}
    .container {{ max-width: 800px; margin: 0 auto; background: #ffffff; border-radius: 8px; padding: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
    .badge {{ display: inline-block; background-color: #3182ce; color: #ffffff; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 14px; margin-bottom: 12px; }}
    h1 {{ color: #2d3748; font-size: 28px; margin-top: 0; margin-bottom: 10px; }}
    .subtitle {{ font-size: 16px; color: #718096; margin-bottom: 20px; }}
    .meta-card {{ background-color: #edf2f7; border-left: 4px solid #3182ce; padding: 15px; border-radius: 4px; margin-bottom: 25px; }}
    .grid-section {{ display: flex; gap: 20px; margin-bottom: 25px; flex-wrap: wrap; }}
    .card-pro {{ flex: 1; min-width: 280px; background-color: #f0fff4; border: 1px solid #c6f6d5; padding: 15px; border-radius: 6px; }}
    .card-con {{ flex: 1; min-width: 280px; background-color: #fff5f5; border: 1px solid #fed7d7; padding: 15px; border-radius: 6px; }}
    .card-pro h3 {{ color: #22543d; margin-top: 0; }}
    .card-con h3 {{ color: #742a2a; margin-top: 0; }}
    ul {{ padding-left: 20px; }}
    .verdict-box {{ background-color: #ebf8ff; border: 1px solid #bee3f8; padding: 20px; border-radius: 6px; margin-top: 25px; }}
    .disclaimer-box {{ background-color: #fffaf0; border: 1px solid #feebc8; padding: 15px; border-radius: 6px; margin-top: 30px; font-size: 13px; color: #744210; }}
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">{ide['category']}</span>
    <h1>{ide['name']} Review & Developer Assessment</h1>
    <p class="subtitle">Vendor: <strong>{ide['vendor']}</strong> | Pricing: <strong>{ide['pricing_type']} ({ide['pricing_details']})</strong></p>

    <div class="meta-card">
      <p><strong>Target Audience:</strong> {ide['target_audience']}</p>
      <p><strong>Pricing breakdown:</strong> {ide['pricing_details']}</p>
    </div>

    <h2>Key Highlights & Features</h2>
    <ul>
      {features_html}
    </ul>

    <div class="grid-section">
      <div class="card-pro">
        <h3>Top Advantages (Pros)</h3>
        <ul>
          {pros_html}
        </ul>
      </div>
      <div class="card-con">
        <h3>Limitations (Cons)</h3>
        <ul>
          {cons_html}
        </ul>
      </div>
    </div>

    <div class="verdict-box">
      <h2>Final Developer Verdict</h2>
      <p>{ide['verdict']}</p>
    </div>

    <div class="disclaimer-box">
      <strong>Independent Review Notice:</strong><br>
      {REQUIRED_DISCLAIMER}
    </div>
  </div>
</body>
</html>"""
    return html

def generate_google_flow_spec(ide: Dict[str, Any]) -> Dict[str, Any]:
    """Generates video specifications for Google Flow AI video generator."""
    return {
        "ide_id": ide["id"],
        "ide_name": ide["name"],
        "channel": "@IDEguide",
        "youtube_url": "https://www.youtube.com/@IDEguide",
        "blogger_url": "https://ideguide.blogspot.com/",
        "disclaimer": REQUIRED_DISCLAIMER,
        "shorts_spec": {
            "title": f"{ide['name']} - Is it worth it? (1-Min Review)",
            "aspect_ratio": "9:16",
            "resolution": "1080x1920",
            "duration_seconds": 45,
            "scenes": [
                {
                    "scene_number": 1,
                    "google_flow_prompt": f"Ultra clean cinematic studio shot of a workstation glowing in dark mode with {ide['name']} interface open, high contrast macro lens on screen.",
                    "framing": "Vertical 9:16 Close-Up",
                    "camera_angle": "Slow forward dolly push",
                    "audio_narration": f"Looking for the best code editor? Let's break down {ide['name']} in 45 seconds!",
                    "overlay_text": f"{ide['name']}\n{ide['category']}"
                },
                {
                    "scene_number": 2,
                    "google_flow_prompt": f"Detailed interface view of {ide['name']} showing code auto-complete and key features in action, mechanical keyboard blurred in foreground.",
                    "framing": "Vertical 9:16 Medium Shot",
                    "camera_angle": "Pan right across editor tabs",
                    "audio_narration": f"Here are the top pros: {', '.join(ide['pros'][:2])}.",
                    "overlay_text": "TOP ADVANTAGES"
                },
                {
                    "scene_number": 3,
                    "google_flow_prompt": f"Split comparison visual displaying pricing details for {ide['name']}: {ide['pricing_type']}.",
                    "framing": "Vertical 9:16 Center Focus",
                    "camera_angle": "Static macro view",
                    "audio_narration": f"Pricing model: {ide['pricing_details']}. Overall verdict: {ide['verdict']}",
                    "overlay_text": f"PRICING: {ide['pricing_type']}"
                }
            ]
        },
        "full_video_spec": {
            "title": f"{ide['name']} Comprehensive Breakdown - Features, Pros, Cons & Pricing",
            "aspect_ratio": "16:9",
            "resolution": "1920x1080",
            "duration_seconds": 300,
            "scenes": [
                {
                    "scene_number": 1,
                    "google_flow_prompt": f"Sleek developer setup with ambient RGB lighting, widescreen display rendering {ide['name']} IDE in high resolution.",
                    "framing": "Horizontal 16:9 Wide Shot",
                    "camera_angle": "Over-the-shoulder developer view",
                    "audio_narration": f"Welcome back to IDE Guide! Today we analyze {ide['name']} built by {ide['vendor']}.",
                    "overlay_text": f"IDE GUIDE EVALUATION: {ide['name']}"
                },
                {
                    "scene_number": 2,
                    "google_flow_prompt": f"Dynamic screen recording animation showing {ide['name']} code navigation, extension hub, and auto-complete speed.",
                    "framing": "Horizontal 16:9 Full Screen UI",
                    "camera_angle": "Smooth zoom into terminal",
                    "audio_narration": f"Key features include: {', '.join(ide['key_features'])}.",
                    "overlay_text": "KEY FEATURES & WORKFLOW"
                },
                {
                    "scene_number": 3,
                    "google_flow_prompt": f"High quality graphical breakdown card displaying Pros vs Cons for {ide['name']}.",
                    "framing": "Horizontal 16:9 Split Graphics",
                    "camera_angle": "Static presentation view",
                    "audio_narration": f"On the pros side: {', '.join(ide['pros'])}. On the cons side: {', '.join(ide['cons'])}.",
                    "overlay_text": "PROS & CONS ASSESSMENT"
                }
            ]
        }
    }

def generate_video_markdown_script(ide: Dict[str, Any], flow_spec: Dict[str, Any]) -> str:
    """Generates Markdown video script documentation."""
    return f"""# YouTube Video Script & Specs: {ide['name']}

**Channel:** [@IDEguide](https://www.youtube.com/@IDEguide)
**Blog:** [IDE Guide Blogspot](https://ideguide.blogspot.com/)
**Target IDE:** {ide['name']} ({ide['vendor']})
**Pricing:** {ide['pricing_type']} - {ide['pricing_details']}

---

## 📱 Shorts / Reels Script (9:16 Vertical)
**Title:** {flow_spec['shorts_spec']['title']}

### Scene 1 (0-15s)
- **Visual Prompt:** {flow_spec['shorts_spec']['scenes'][0]['google_flow_prompt']}
- **Camera:** {flow_spec['shorts_spec']['scenes'][0]['camera_angle']}
- **Audio Script:** "{flow_spec['shorts_spec']['scenes'][0]['audio_narration']}"
- **Overlay Text:** {flow_spec['shorts_spec']['scenes'][0]['overlay_text']}

### Scene 2 (15-30s)
- **Visual Prompt:** {flow_spec['shorts_spec']['scenes'][1]['google_flow_prompt']}
- **Camera:** {flow_spec['shorts_spec']['scenes'][1]['camera_angle']}
- **Audio Script:** "{flow_spec['shorts_spec']['scenes'][1]['audio_narration']}"
- **Overlay Text:** {flow_spec['shorts_spec']['scenes'][1]['overlay_text']}

### Scene 3 (30-45s)
- **Visual Prompt:** {flow_spec['shorts_spec']['scenes'][2]['google_flow_prompt']}
- **Camera:** {flow_spec['shorts_spec']['scenes'][2]['camera_angle']}
- **Audio Script:** "{flow_spec['shorts_spec']['scenes'][2]['audio_narration']}"
- **Overlay Text:** {flow_spec['shorts_spec']['scenes'][2]['overlay_text']}

---

## 🎬 Full YouTube Video Script (16:9 Horizontal)
**Title:** {flow_spec['full_video_spec']['title']}

### Intro Scene
- **Visual Prompt:** {flow_spec['full_video_spec']['scenes'][0]['google_flow_prompt']}
- **Audio Script:** "{flow_spec['full_video_spec']['scenes'][0]['audio_narration']}"

### Feature Deep Dive
- **Visual Prompt:** {flow_spec['full_video_spec']['scenes'][1]['google_flow_prompt']}
- **Audio Script:** "{flow_spec['full_video_spec']['scenes'][1]['audio_narration']}"

### Pros, Cons & Final Verdict
- **Visual Prompt:** {flow_spec['full_video_spec']['scenes'][2]['google_flow_prompt']}
- **Audio Script:** "{flow_spec['full_video_spec']['scenes'][2]['audio_narration']}"

---

## 📢 Mandatory Disclaimer
{REQUIRED_DISCLAIMER}
"""

def run_daily_generation(target_date: str = None) -> List[str]:
    if not target_date:
        target_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    output_dir = os.path.join(PROJECT_ROOT, "content", target_date)
    os.makedirs(output_dir, exist_ok=True)

    ides = load_ide_database()
    history = load_history()

    covered = set(history.get("covered_ides", []))
    available = [i for i in ides if i["id"] not in covered]

    # If all IDEs covered, reset history cycle
    if len(available) < 3:
        history["covered_ides"] = []
        covered = set()
        available = ides

    selected_ides = available[:3]
    generated_files = []

    run_entry = {"date": target_date, "ides": []}

    for ide in selected_ides:
        # 1. AMP Blog Post HTML
        blog_html = generate_amp_blog_post(ide)
        blog_path = os.path.join(output_dir, f"blog_post_{ide['id']}.html")
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(blog_html)
        generated_files.append(blog_path)

        # 2. Google Flow Spec JSON
        flow_spec = generate_google_flow_spec(ide)
        spec_path = os.path.join(output_dir, f"video_spec_{ide['id']}.json")
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)
        generated_files.append(spec_path)

        # 3. Video Markdown Script
        script_md = generate_video_markdown_script(ide, flow_spec)
        script_path = os.path.join(output_dir, f"video_script_{ide['id']}.md")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_md)
        generated_files.append(script_path)

        history.setdefault("covered_ides", []).append(ide["id"])
        run_entry["ides"].append(ide["id"])

    history.setdefault("daily_runs", []).append(run_entry)
    save_history(history)

    print(f"✅ Generated daily content package for {target_date} in {output_dir}")
    for file in generated_files:
        print(f"   - {file}")

    return generated_files

if __name__ == "__main__":
    run_daily_generation()
