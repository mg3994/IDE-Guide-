#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide.
Generates AMP HTML blog posts (for Blogger) and Google Flow video generation specs (for YouTube long-form & Shorts).
Can take either an IDE key from the database OR a custom repo/IDE name.
"""

import sys
import json
import argparse
import os
from typing import Dict, Any

from scripts.amp_validator import DISCLAIMER_TEXT

def load_ide_database() -> Dict[str, Any]:
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "ide_database.json")
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def generate_amp_blog_post(ide_info: Dict[str, Any]) -> str:
    name = ide_info.get("name", "Unknown IDE")
    developer = ide_info.get("developer", "Independent / Open Source")
    category = ide_info.get("category", "Code Editor")
    pricing = ide_info.get("pricing", "Free")
    license_type = ide_info.get("license", "Open Source")
    languages = ", ".join(ide_info.get("target_languages", ["Polyglot"]))
    persona = ide_info.get("ideal_persona", "Software developers")
    pros = ide_info.get("pros", ["Feature rich", "High productivity"])
    cons = ide_info.get("cons", ["Requires learning curve"])
    verdict = ide_info.get("verdict", "Highly capable editor for software development.")

    pros_html = "\n".join([f"    <li>{p}</li>" for p in pros])
    cons_html = "\n".join([f"    <li>{c}</li>" for c in cons])

    html = f"""<article class="ide-review-post">
  <header>
    <h1>{name} Review: Features, Pros, Cons, and Pricing Analysis</h1>
    <p class="meta">Category: <strong>{category}</strong> | Developer: <strong>{developer}</strong></p>
  </header>

  <amp-img
    src="https://images.unsplash.com/photo-1555066931-4365d14bab8c"
    width="1200"
    height="675"
    layout="responsive"
    alt="{name} Interface and Editor Overview">
  </amp-img>

  <section>
    <h2>Introduction</h2>
    <p>Welcome to IDE Guide's deep dive evaluation of <strong>{name}</strong>. In modern software engineering, choosing the right tool directly influences developer speed, ergonomics, and code quality. Below is our comprehensive analysis of {name}.</p>
  </section>

  <section>
    <h2>Key Specifications & Pricing Overview</h2>
    <table>
      <tr><td><strong>Developer/Vendor</strong></td><td>{developer}</td></tr>
      <tr><td><strong>Category</strong></td><td>{category}</td></tr>
      <tr><td><strong>Pricing Tier</strong></td><td>{pricing}</td></tr>
      <tr><td><strong>License</strong></td><td>{license_type}</td></tr>
      <tr><td><strong>Primary Languages</strong></td><td>{languages}</td></tr>
    </table>
  </section>

  <section>
    <h2>Ideal Developer Persona</h2>
    <p>{persona}</p>
  </section>

  <section>
    <h2>Pros & Strengths</h2>
    <ul>
{pros_html}
    </ul>
  </section>

  <section>
    <h2>Cons & Trade-offs</h2>
    <ul>
{cons_html}
    </ul>
  </section>

  <section>
    <h2>Final Verdict</h2>
    <p>{verdict}</p>
  </section>

  <hr>

  <footer>
    <p class="disclaimer">{DISCLAIMER_TEXT}</p>
  </footer>
</article>"""
    return html

def generate_google_flow_video_spec(ide_info: Dict[str, Any]) -> str:
    name = ide_info.get("name", "Unknown IDE")
    pricing = ide_info.get("pricing", "Free")
    category = ide_info.get("category", "Code Editor")
    pros = ide_info.get("pros", ["Extensible", "Fast"])
    cons = ide_info.get("cons", ["Requires configuration"])
    verdict = ide_info.get("verdict", "Solid tool for developers.")

    spec = f"""# Google Flow Video Specs & Script Package
Target Channel: YouTube (@IDEguide)
Topic: {name} ({category})

==================================================
1. LONG-FORM VIDEO SPEC (16:9 Aspect Ratio, 1080p/4K)
==================================================

Title: Is {name} Worth It in 2026? Complete Review & Breakdown
Description: An objective breakdown of {name}. We explore features, pros, cons, and pricing ({pricing}).

[SCENE 1: Introduction]
- Duration: 0:00 - 0:30
- Google Flow Visual Prompt: High-tech developer workspace, 4k photorealistic render, dark mode background, cinematic blue/purple ambient lighting, smooth dolly zoom on glowing screen showing {name} code editor interface.
- Audio Script: "Welcome back to IDE Guide! Today, we are analyzing {name}, a popular {category}. Before we begin: IDE Guide is an independent technical publication. This review is not sponsored or affiliated with any software vendor."

[SCENE 2: Core Capabilities & Specs]
- Duration: 0:30 - 2:00
- Google Flow Visual Prompt: Macro close-up shot of mechanical keyboard typing, code auto-completion window popping up gracefully, high contrast code editor screen with smooth vertical camera pan.
- Audio Script: "{name} brings powerful capabilities to the table. Key strengths include: {pros[0]} and {pros[1] if len(pros)>1 else 'fast execution'}. Pricing tier: {pricing}."

[SCENE 3: Trade-offs & Limitations]
- Duration: 2:00 - 3:30
- Google Flow Visual Prompt: Split screen graphical overlay showing side-by-side performance benchmarks and memory consumption graphs, dark aesthetic, clean neon UI lines.
- Audio Script: "However, no editor is without limitations. What you should watch out for: {cons[0]}."

[SCENE 4: Verdict & Final Recommendation]
- Duration: 3:30 - 4:00
- Google Flow Visual Prompt: Cinematic over-the-shoulder view of software developer concluding a coding session, smooth fade to IDE Guide logo overlay with subscribe prompt.
- Audio Script: "In summary: {verdict} Make sure to subscribe to IDE Guide for more objective developer tool reviews!"


==================================================
2. YOUTUBE SHORTS SPEC (9:16 Vertical Aspect Ratio)
==================================================

Title: {name} in 60 Seconds! Should You Use It? #Shorts #Coding #IDE
Description: Quick breakdown of {name}. Free or paid? Is it worth it?

[SHORT SCENE 1: Hook]
- Duration: 0:00 - 0:15
- Google Flow Visual Prompt (Vertical 9:16): Fast vertical pan over modern setup, bold animated text overlays reading '{name} Review', dynamic cinematic camera tilt.
- Audio Script: "Thinking about using {name}? Here is what you need to know in 60 seconds! Note: IDE Guide is independent and non-sponsored."

[SHORT SCENE 2: Pros vs Cons]
- Duration: 0:15 - 0:45
- Google Flow Visual Prompt (Vertical 9:16): Rapid macro cuts of coding in {name}, green checkmark graphic for strengths, red overlay for drawbacks.
- Audio Script: "Top pros: {pros[0]}. Major cons: {cons[0]}. Pricing: {pricing}."

[SHORT SCENE 3: Verdict & Outro]
- Duration: 0:45 - 1:00
- Google Flow Visual Prompt (Vertical 9:16): Sleek vertical ending card with call to action: 'Subscribe to @IDEguide for daily dev insights!'
- Audio Script: "{verdict} Follow IDE Guide for daily dev insights!"
"""
    return spec

def main():
    parser = argparse.ArgumentParser(description="Agentic skill for generating IDE Guide content.")
    parser.add_argument("--ide", type=str, help="IDE key (e.g., vscode, cursor, zed, pycharm) or custom name")
    parser.add_argument("--output-dir", type=str, default="output", help="Directory to save generated files")
    args = parser.parse_args()

    if not args.ide:
        print("Error: --ide parameter is required.")
        sys.exit(1)

    db = load_ide_database()
    ide_key = args.ide.lower().replace(" ", "_")

    if ide_key in db:
        ide_info = db[ide_key]
    else:
        ide_info = {
            "name": args.ide.title(),
            "developer": "Independent / Developer Community",
            "category": "Code Editor",
            "pricing": "Free / Freemium",
            "is_paid": False,
            "license": "Open Source",
            "target_languages": ["General Programming"],
            "ideal_persona": "Software engineers looking for effective development tools.",
            "pros": ["Powerful customizability", "Active developer ecosystem"],
            "cons": ["Requires initial configuration"],
            "verdict": f"{args.ide.title()} is a solid editor for modern software engineering workflows."
        }

    blog_html = generate_amp_blog_post(ide_info)
    video_spec = generate_google_flow_video_spec(ide_info)

    os.makedirs(args.output_dir, exist_ok=True)
    blog_file = os.path.join(args.output_dir, f"{ide_key}_amp_blog.html")
    video_file = os.path.join(args.output_dir, f"{ide_key}_google_flow_spec.md")

    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(blog_html)

    with open(video_file, "w", encoding="utf-8") as f:
        f.write(video_spec)

    print(f"Generated AMP Blog Post: {blog_file}")
    print(f"Generated Google Flow Spec: {video_file}")

if __name__ == "__main__":
    main()
