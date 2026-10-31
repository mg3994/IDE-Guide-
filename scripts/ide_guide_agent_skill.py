#!/usr/bin/env python3
"""
IDE Guide Agent Skill Tool
Generates AMP-compliant HTML blog posts for Blogger (ideguide.blogspot.com)
and visual video/shorts specs (prompts, scripts, pacing) for Google Flow & YouTube (@IDEguide).
Can be invoked standalone or integrated into agentic pipelines.
"""

import argparse
import json
import os
import sys
from typing import Dict, Any, Optional

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)


def get_default_ide_data(ide_name: str) -> Dict[str, Any]:
    """Generates fallback data if a custom IDE is requested that isn't in the database."""
    safe_name = ide_name.strip()
    return {
        "id": safe_name.lower().replace(" ", "-"),
        "name": safe_name,
        "developer": f"{safe_name} Community / Team",
        "website": f"https://google.com/search?q={safe_name}+code+editor",
        "category": "Code Editor / IDE",
        "pricing_tier": "Free / Open-Source (Evaluate for Pro tiers)",
        "pricing_details": "Available as free download with optional professional extensions or subscriptions.",
        "is_open_source": True,
        "primary_languages": ["Python", "JavaScript", "TypeScript", "Rust", "Go"],
        "summary": f"An evaluation of {safe_name} examining developer ergonomics, performance, and programming workflows.",
        "pros": [
            f"Active development and responsive toolchain integration in {safe_name}",
            "Customizable workspace with support for keybindings and plugins",
            "Responsive source code syntax highlighting and navigation",
            "Accessible on major desktop operating systems"
        ],
        "cons": [
            "May require third-party language servers for full LSP autocompletion",
            "Documentation can vary depending on community-supported modules",
            "Configuration setup curve for advanced debugging pipelines",
            "Resource utilization should be benchmarked on lower-spec machines"
        ],
        "best_for": f"Developers looking to evaluate {safe_name} for streamlined coding workflows.",
        "verdict": f"A capable development tool worth test-driving if you seek an alternative to mainstream IDEs.",
        "rating": 8.7
    }


def generate_amp_blog_post(ide: Dict[str, Any]) -> str:
    """
    Generates a 100% AMP HTML valid blog post snippet for Blogger.
    Strictly follows Blogger AMP requirements: no invalid tags, inline style inside <style amp-custom>,
    and includes the mandatory non-sponsorship disclaimer.
    """
    pros_html = "".join([f"      <li class=\"pros-item\">{pro}</li>\n" for pro in ide.get("pros", [])])
    cons_html = "".join([f"      <li class=\"cons-item\">{con}</li>\n" for con in ide.get("cons", [])])
    languages = ", ".join(ide.get("primary_languages", ["Multiple Languages"]))

    html = f"""<style amp-custom>
  .ide-guide-post {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.65;
    color: #1e293b;
    background-color: #ffffff;
    max-width: 800px;
    margin: 0 auto;
    padding: 16px;
  }}
  .ide-header {{
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #f8fafc;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
  }}
  .ide-channel-tag {{
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #38bdf8;
    font-weight: 700;
    margin-bottom: 8px;
  }}
  .ide-title {{
    font-size: 28px;
    font-weight: 800;
    margin: 0 0 12px 0;
    color: #ffffff;
  }}
  .badge-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
  }}
  .badge {{
    padding: 6px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 600;
  }}
  .badge-pricing {{
    background-color: #3b82f6;
    color: #ffffff;
  }}
  .badge-category {{
    background-color: #334155;
    color: #e2e8f0;
  }}
  .badge-rating {{
    background-color: #10b981;
    color: #ffffff;
  }}
  .section-card {{
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    background-color: #f8fafc;
  }}
  .section-heading {{
    font-size: 20px;
    font-weight: 700;
    margin-top: 0;
    margin-bottom: 12px;
    color: #0f172a;
    border-left: 4px solid #3b82f6;
    padding-left: 10px;
  }}
  .pros-card {{
    border-left: 4px solid #10b981;
    background-color: #f0fdf4;
  }}
  .cons-card {{
    border-left: 4px solid #ef4444;
    background-color: #fef2f2;
  }}
  .pros-list, .cons-list {{
    margin: 0;
    padding-left: 20px;
  }}
  .pros-item {{
    margin-bottom: 8px;
    color: #166534;
  }}
  .cons-item {{
    margin-bottom: 8px;
    color: #991b1b;
  }}
  .summary-text {{
    font-size: 16px;
    color: #cbd5e1;
  }}
  .details-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
  }}
  .details-table th, .details-table td {{
    padding: 10px;
    border-bottom: 1px solid #e2e8f0;
    text-align: left;
    font-size: 14px;
  }}
  .details-table th {{
    color: #64748b;
    font-weight: 600;
    width: 30%;
  }}
  .verdict-box {{
    background: #eff6ff;
    border-radius: 8px;
    padding: 18px;
    border-left: 5px solid #2563eb;
    margin: 20px 0;
  }}
  .verdict-title {{
    margin-top: 0;
    color: #1e3a8a;
    font-size: 18px;
  }}
  .verdict-text {{
    margin-bottom: 0;
    color: #1e40af;
  }}
  .disclaimer-box {{
    margin-top: 32px;
    padding: 16px;
    border-radius: 8px;
    background-color: #f1f5f9;
    border: 1px dashed #94a3b8;
    font-size: 12px;
    color: #64748b;
    line-height: 1.5;
  }}
  .disclaimer-title {{
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 4px;
    color: #475569;
  }}
  .channel-cta {{
    text-align: center;
    margin: 24px 0;
    padding: 16px;
    background: #0f172a;
    color: #ffffff;
    border-radius: 8px;
  }}
  .channel-cta-title {{
    margin: 0 0 8px 0;
  }}
  .channel-cta-sub {{
    margin: 0;
    font-size: 14px;
  }}
  .channel-link {{
    color: #38bdf8;
    text-decoration: none;
    font-weight: bold;
  }}
  .disclaimer-text {{
    margin: 0;
  }}
  .heading-pros {{
    border-left-color: #10b981;
    color: #166534;
  }}
  .heading-cons {{
    border-left-color: #ef4444;
    color: #991b1b;
  }}
</style>

<div class="ide-guide-post">
  <div class="ide-header">
    <div class="ide-channel-tag">IDE Guide &bull; Independent Editor Review</div>
    <h2 class="ide-title">{ide.get('name')} Review: Is It Best for Your Workflow?</h2>
    <p class="summary-text">{ide.get('summary')}</p>
    <div class="badge-container">
      <span class="badge badge-pricing">Pricing: {ide.get('pricing_tier')}</span>
      <span class="badge badge-category">{ide.get('category')}</span>
      <span class="badge badge-rating">Rating: {ide.get('rating', '9.0')}/10</span>
    </div>
  </div>

  <div class="section-card">
    <h3 class="section-heading">Overview & Key Specifications</h3>
    <table class="details-table">
      <tr>
        <th>Developer / Vendor</th>
        <td>{ide.get('developer')}</td>
      </tr>
      <tr>
        <th>Pricing Model</th>
        <td><strong>{ide.get('pricing_tier')}</strong> &mdash; {ide.get('pricing_details')}</td>
      </tr>
      <tr>
        <th>License Type</th>
        <td>{"Open-Source" if ide.get('is_open_source') else "Proprietary"}</td>
      </tr>
      <tr>
        <th>Primary Languages</th>
        <td>{languages}</td>
      </tr>
      <tr>
        <th>Official Link</th>
        <td><a href="{ide.get('website')}" target="_blank" rel="noopener noreferrer">{ide.get('website')}</a></td>
      </tr>
    </table>
  </div>

  <div class="section-card pros-card">
    <h3 class="section-heading heading-pros">The Good: Key Advantages</h3>
    <ul class="pros-list">
{pros_html}    </ul>
  </div>

  <div class="section-card cons-card">
    <h3 class="section-heading heading-cons">The Bad: Limitations & Tradeoffs</h3>
    <ul class="cons-list">
{cons_html}    </ul>
  </div>

  <div class="section-card">
    <h3 class="section-heading">Who Is {ide.get('name')} Best For?</h3>
    <p>{ide.get('best_for')}</p>
  </div>

  <div class="verdict-box">
    <h3 class="verdict-title">IDE Guide Final Verdict</h3>
    <p class="verdict-text"><strong>{ide.get('verdict')}</strong></p>
  </div>

  <div class="channel-cta">
    <p class="channel-cta-title">Enjoying deep, unbiased developer breakdowns?</p>
    <p class="channel-cta-sub">Watch our video walkthroughs on YouTube: <a class="channel-link" href="https://www.youtube.com/@IDEguide" target="_blank" rel="noopener noreferrer">YouTube @IDEguide</a> &amp; bookmark our publication at <a class="channel-link" href="https://ideguide.blogspot.com/" target="_blank" rel="noopener noreferrer">ideguide.blogspot.com</a></p>
  </div>

  <div class="disclaimer-box">
    <div class="disclaimer-title">Editorial Independence Guarantee</div>
    <p class="disclaimer-text">{DISCLAIMER_TEXT}</p>
  </div>
</div>
"""
    return html.strip()


def generate_video_flow_spec(ide: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates structured prompts and storyboard specs tailored for Google Flow / generative video tools
    and YouTube video/shorts creation (@IDEguide).
    """
    name = ide.get("name")
    pricing = ide.get("pricing_tier")
    pros = ide.get("pros", ["Extensible plugin ecosystem", "Clean developer UI"])
    cons = ide.get("cons", ["Requires learning curve", "Resource overhead"])
    best_for = ide.get("best_for", "Developers looking for a reliable coding environment.")
    verdict = ide.get("verdict", "A strong contender in today's development landscape.")

    pro_1 = pros[0] if len(pros) > 0 else "High developer velocity"
    pro_2 = pros[1] if len(pros) > 1 else "Modern tooling support"
    con_1 = cons[0] if len(cons) > 0 else "Resource usage during intensive operations"

    scenes = [
        {
            "scene_number": 1,
            "scene_title": "Hook & Instant Visual Grab",
            "duration_seconds": 5,
            "aspect_ratios": ["9:16 Shorts", "16:9 Long-form"],
            "google_flow_prompt": (
                f"Cinematic close-up macro tracking shot of illuminated mechanical keyboard keys typing code in dark room, "
                f"camera pans up smoothly to reveal glowing ultrawide monitor displaying {name} editor interface with vibrant neon syntax highlighting, "
                f"anamorphic lens flare, photorealistic 8k render, hyper-modern developer aesthetic, 60fps."
            ),
            "on_screen_text": f"Is {name} REALLY Worth Your Time in 2025?",
            "voiceover_script": (
                f"Stop scrolling! Is {name} actually the best code editor for your daily development, "
                f"or is it just overhyped? Let's break down the good, the bad, and the pricing right now!"
            ),
            "b_roll_suggestion": f"High-contrast screencast of {name} launching with real code files loading rapidly.",
            "audio_cue": "Fast electronic whoosh into rhythmic synth beat."
        },
        {
            "scene_number": 2,
            "scene_title": "Editor Identity & Pricing Breakdown (Free vs Paid)",
            "duration_seconds": 10,
            "aspect_ratios": ["9:16 Shorts", "16:9 Long-form"],
            "google_flow_prompt": (
                f"Sleek 3D isometric floating render of laptop displaying {name} logo and user interface, "
                f"split holographic cards materialize showing pricing tier '{pricing}', "
                f"subtle volumetric blue and emerald lighting, high-tech studio background, smooth rotational camera pan."
            ),
            "on_screen_text": f"{name} | Tier: {pricing}",
            "voiceover_script": (
                f"First up: pricing. {name} falls under the {pricing} tier. "
                f"{ide.get('pricing_details', 'Check licensing rules before rolling out.')} "
                f"So you know exactly what is free and where you might need to open your wallet."
            ),
            "b_roll_suggestion": f"Pricing page screenshot or license tier comparison graphic.",
            "audio_cue": "Cash register chime or coin drop SFX followed by tech ambience."
        },
        {
            "scene_number": 3,
            "scene_title": "The Good: Standout Advantages",
            "duration_seconds": 15,
            "aspect_ratios": ["9:16 Shorts", "16:9 Long-form"],
            "google_flow_prompt": (
                f"Dynamic over-the-shoulder camera glide behind programmer coding furiously, "
                f"glowing green checkmark animations and floating feature cards highlighting: '{pro_1}', "
                f"smooth UI interactions, responsive code refactoring, cyberpunk dark aesthetic, crisp 4k 60fps."
            ),
            "on_screen_text": f"THE GOOD: {pro_1}",
            "voiceover_script": (
                f"Here is why developers love it. Number one: {pro_1}. "
                f"And number two: {pro_2}. The ergonomics and speed make everyday coding feel effortless."
            ),
            "b_roll_suggestion": f"Live screencast demonstrating the top feature in action (e.g. multi-file edit or indexing).",
            "audio_cue": "Subtle energetic bass drop with pleasant confirmation click sounds."
        },
        {
            "scene_number": 4,
            "scene_title": "The Bad: Honest Drawbacks & Tradeoffs",
            "duration_seconds": 12,
            "aspect_ratios": ["9:16 Shorts", "16:9 Long-form"],
            "google_flow_prompt": (
                f"Dramatic lighting shift to subtle crimson and amber accents, "
                f"camera slowly pushes in towards monitor screen showing system resource monitor or complex configuration file, "
                f"slight glitch distortion effect emphasizing bottleneck, cinematic realism."
            ),
            "on_screen_text": f"THE BAD: {con_1}",
            "voiceover_script": (
                f"Now for the ugly truth. No tool is perfect. The main drawback? {con_1}. "
                f"If this is a dealbreaker for your workflow, you must consider alternatives."
            ),
            "b_roll_suggestion": f"Activity monitor or settings complexity screencast.",
            "audio_cue": "Low warning chord / sub-bass hit."
        },
        {
            "scene_number": 5,
            "scene_title": "Who It's Best For & Final Verdict",
            "duration_seconds": 12,
            "aspect_ratios": ["9:16 Shorts", "16:9 Long-form"],
            "google_flow_prompt": (
                f"Wide cinematic studio shot with modern developer desk setup, ambient LED backlighting, "
                f"bold typography '{ide.get('rating', '9.0')}/10' renders with golden sheen, "
                f"camera pulls back smoothly with premium tech documentary aesthetic."
            ),
            "on_screen_text": f"Verdict: {ide.get('rating', '9.0')}/10 | Best for: {best_for[:40]}...",
            "voiceover_script": (
                f"Who should use it? {best_for} "
                f"Our final verdict: {verdict}"
            ),
            "b_roll_suggestion": f"Summary verdict card displaying rating and key recommendations.",
            "audio_cue": "Triumphant electronic swell."
        },
        {
            "scene_number": 6,
            "scene_title": "Outro, Call to Action & Mandatory Disclaimer",
            "duration_seconds": 6,
            "aspect_ratios": ["9:16 Shorts", "16:9 Long-form"],
            "google_flow_prompt": (
                f"End screen animation with IDE Guide logo pulsing gently on sleek graphite background, "
                f"YouTube subscribe button and Blogger link 'ideguide.blogspot.com' rendered in 3D typography, "
                f"clean minimalist composition."
            ),
            "on_screen_text": "Subscribe @IDEguide | Read on ideguide.blogspot.com | 100% Independent & Unsponsored",
            "voiceover_script": (
                f"Subscribe to @IDEguide on YouTube for daily honest reviews, and read the full AMP breakdown on ideguide.blogspot.com. "
                f"We are 100% independent and never sponsored!"
            ),
            "b_roll_suggestion": "Subscribe and notification bell animation.",
            "audio_cue": "Upbeat closing sting / bell chime."
        }
    ]

    return {
        "channel": "IDE Guide (@IDEguide)",
        "blog_url": "https://ideguide.blogspot.com/",
        "target_ide": name,
        "pricing_tier": pricing,
        "is_open_source": ide.get("is_open_source", False),
        "video_title": f"{name} Honest Review: The Good, The Bad & Pricing (2025)",
        "shorts_title": f"Is {name} Worth It? The Good vs The Bad #shorts",
        "seo_tags": [
            f"{name}", f"{name} review", "code editor", "best ide", "programming",
            "software engineering", "IDE guide", "vscode alternative", "coding tools"
        ],
        "mandatory_disclaimer": DISCLAIMER_TEXT,
        "pacing_notes": {
            "shorts_target_duration_seconds": 60,
            "longform_target_duration_seconds": 240,
            "transition_speed": "Fast cuts every 2.5-3.5 seconds for Shorts; sustained 5-7s B-roll for 16:9"
        },
        "scenes": scenes
    }


def generate_content_package(ide_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generates both AMP blog post HTML and Google Flow video spec."""
    amp_post = generate_amp_blog_post(ide_data)
    video_spec = generate_video_flow_spec(ide_data)
    return {
        "ide_id": ide_data.get("id"),
        "ide_name": ide_data.get("name"),
        "amp_blog_post_html": amp_post,
        "video_flow_spec": video_spec,
        "mandatory_disclaimer": DISCLAIMER_TEXT
    }


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Content Skill Generator")
    parser.add_argument("--ide", type=str, help="Name of the IDE/editor to review (e.g. Cursor, Neovim, Zed)")
    parser.add_argument("--database", type=str, default="data/ide_database.json", help="Path to ide_database.json")
    parser.add_argument("--outdir", type=str, default="output", help="Directory to save generated assets")
    args = parser.parse_args()

    if not args.ide:
        parser.print_help()
        sys.exit(1)

    target_name = args.ide.strip()
    selected_data = None

    if os.path.exists(args.database):
        try:
            with open(args.database, "r", encoding="utf-8") as f:
                db = json.load(f)
                for item in db:
                    if item.get("name", "").lower() == target_name.lower() or item.get("id", "").lower() == target_name.lower():
                        selected_data = item
                        break
        except Exception as e:
            print(f"Warning: could not read database {args.database}: {e}", file=sys.stderr)

    if not selected_data:
        print(f"Notice: '{target_name}' not in pre-defined database. Synthesizing data using fallback agentic template...")
        selected_data = get_default_ide_data(target_name)

    pkg = generate_content_package(selected_data)
    os.makedirs(args.outdir, exist_ok=True)

    slug = selected_data["id"]
    blog_file = os.path.join(args.outdir, f"{slug}_amp_blogpost.html")
    video_file = os.path.join(args.outdir, f"{slug}_google_flow_spec.json")

    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(pkg["amp_blog_post_html"])

    with open(video_file, "w", encoding="utf-8") as f:
        json.dump(pkg["video_flow_spec"], f, indent=2)

    print(f"Successfully generated agentic content for {selected_data['name']}:")
    print(f" - AMP Blog Post: {blog_file}")
    print(f" - Google Flow Video Spec: {video_file}")


if __name__ == "__main__":
    main()
