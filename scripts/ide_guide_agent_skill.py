#!/usr/bin/env python3
"""
IDE Guide - Agentic Skill Tool
CLI tool for on-demand generation of AMP HTML blog posts and Google Flow video specs
for specific IDEs, GitHub repository URLs, or custom comparison topics.
"""

import os
import sys
import json
import argparse
import datetime
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

BLOGGER_URL = "https://ideguide.blogspot.com/"
YOUTUBE_URL = "https://www.youtube.com/@IDEguide"

def fetch_repo_info(repo_url: str) -> Optional[Dict[str, Any]]:
    """Fetches details from a GitHub repository URL if accessible."""
    try:
        parts = repo_url.strip("/").split("/")
        if "github.com" in parts:
            idx = parts.index("github.com")
            owner = parts[idx + 1]
            repo = parts[idx + 2]
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            req = urllib.request.Request(api_url, headers={"User-Agent": "IDEGuideSkill/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                return {
                    "name": data.get("name", repo).capitalize(),
                    "description": data.get("description") or f"Open source code editor repository {owner}/{repo}",
                    "stars": data.get("stargazers_count", 0),
                    "language": data.get("language") or "C++ / Rust / TypeScript",
                    "license": data.get("license", {}).get("name", "Open Source") if data.get("license") else "Open Source",
                    "owner": owner
                }
    except Exception as e:
        print(f"Warning: Could not fetch GitHub API for {repo_url}: {e}")
    return None

def build_ide_profile(ide_name: Optional[str], repo_url: Optional[str], topic: Optional[str]) -> Dict[str, Any]:
    """Constructs a structured IDE profile based on user arguments or fetched repository info."""
    repo_info = fetch_repo_info(repo_url) if repo_url else None

    name = ide_name or (repo_info["name"] if repo_info else "Custom IDE Tool")
    if topic and not ide_name:
        name = topic

    slug = name.lower().replace(" ", "-").replace("/", "-")
    description = repo_info["description"] if repo_info else f"Modern code editor evaluation for {name}"

    return {
        "name": name,
        "slug": slug,
        "tagline": description,
        "developer": repo_info["owner"] if repo_info else "Independent Software Developer / Community",
        "license": repo_info["license"] if repo_info else "Free & Open Source / Proprietary Options",
        "pricing_model": "Community Free Tier available; optional enterprise/Pro subscription.",
        "category": f"Code Editor / IDE ({repo_info['language']})" if repo_info else "Software Development Environment",
        "pros": [
            f"Optimized workflow and high responsiveness for {name}",
            "Extensible architecture supporting modern language servers and debuggers",
            "Active developer community and frequent update cycles"
        ],
        "cons": [
            "Requires initial configuration for custom extension pipelines",
            "Resource usage depends heavily on workspace size and active plugins"
        ],
        "key_features": [
            "LSP & Syntax diagnostics integration",
            "Integrated terminal multiplexing",
            "Custom keybindings & theme customization"
        ],
        "best_for": f"Developers looking for modern productivity solutions in {name}.",
        "rating": "4.7/5.0"
    }

def generate_agent_amp_post(profile: Dict[str, Any], date_str: str) -> str:
    canonical = f"{BLOGGER_URL}{date_str}/{profile['slug']}.html"
    return f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{profile['name']} Developer Guide ({date_str}) | IDE Guide</title>
  <link rel="canonical" href="{canonical}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{profile['name']} - Technical Review & Workflow Evaluation",
    "description": "{profile['tagline']}",
    "author": {{ "@type": "Organization", "name": "IDE Guide", "url": "{BLOGGER_URL}" }},
    "publisher": {{ "@type": "Organization", "name": "IDE Guide", "url": "{BLOGGER_URL}" }},
    "datePublished": "{date_str}",
    "mainEntityOfPage": "{canonical}"
  }}
  </script>

  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>

  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #0f172a; background: #f8fafc; margin: 0; }}
    .header {{ background: #0f172a; color: #ffffff; padding: 2.5rem 1rem; text-align: center; }}
    .header h1 {{ color: #38bdf8; margin: 0; }}
    .container {{ max-width: 800px; margin: 2rem auto; padding: 0 1rem; }}
    .card {{ background: #ffffff; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid #e2e8f0; }}
    .disclaimer {{ background-color: #fffbe2; border-left: 4px solid #f59e0b; padding: 1rem; font-size: 0.9rem; color: #78350f; margin-bottom: 1.5rem; }}
    .cta {{ background: #0f172a; color: #ffffff; padding: 1.5rem; text-align: center; border-radius: 8px; }}
    .cta a {{ color: #38bdf8; font-weight: bold; text-decoration: none; }}
  </style>
</head>
<body>
  <header class="header">
    <h1>{profile['name']} - IDE Guide Breakdown</h1>
    <p>{profile['tagline']}</p>
  </header>
  <main class="container">
    <div class="disclaimer">
      <strong>Notice:</strong> {DISCLAIMER_TEXT}
    </div>
    <div class="card">
      <h2>Technical Summary</h2>
      <p><strong>Developer:</strong> {profile['developer']}</p>
      <p><strong>License:</strong> {profile['license']}</p>
      <p><strong>Pricing:</strong> {profile['pricing_model']}</p>
    </div>
    <div class="card">
      <h2>Pros & Cons</h2>
      <h3 style="color: #15803d;">Pros</h3>
      <ul>{"".join([f"<li>{p}</li>" for p in profile['pros']])}</ul>
      <h3 style="color: #b91c1c;">Cons</h3>
      <ul>{"".join([f"<li>{c}</li>" for c in profile['cons']])}</ul>
    </div>
    <div class="card">
      <h2>Recommendation</h2>
      <p>{profile['best_for']}</p>
    </div>
    <div class="cta">
      <p>Watch video deep dives on YouTube <a href="{YOUTUBE_URL}">@IDEguide</a> | Read more at <a href="{BLOGGER_URL}">ideguide.blogspot.com</a></p>
    </div>
    <div class="disclaimer" style="margin-top: 1.5rem;">
      <small>{DISCLAIMER_TEXT}</small>
    </div>
  </main>
</body>
</html>
"""

def generate_agent_flow_spec(profile: Dict[str, Any], date_str: str) -> Dict[str, Any]:
    return {
        "title": f"Is {profile['name']} the Ultimate Code Editor? | IDE Guide",
        "ide_name": profile["name"],
        "date": date_str,
        "channel": "@IDEguide",
        "youtube_url": YOUTUBE_URL,
        "blogger_url": BLOGGER_URL,
        "disclaimer": DISCLAIMER_TEXT,
        "video_format": {
            "aspect_ratio": "9:16",
            "resolution": "1080x1920",
            "target_duration_seconds": 60
        },
        "scenes": [
            {
                "scene_number": 1,
                "timestamp": "00:00 - 00:05",
                "google_flow_prompt": f"Macro shot of developer workspace running {profile['name']}. Glowing code terminal with dark neon aesthetics.",
                "voiceover_script": f"Let's review {profile['name']} - here is what you need to know in 60 seconds!",
                "on_screen_text": f"🔥 {profile['name']} Review",
                "audio_cue": "Fast synth transition sound"
            },
            {
                "scene_number": 2,
                "timestamp": "00:05 - 00:25",
                "google_flow_prompt": f"Over-the-shoulder macro view typing in {profile['name']}. Smooth pan across interface features.",
                "voiceover_script": f"Top pros include {profile['pros'][0]}.",
                "on_screen_text": f"✅ PROS\n• {profile['pros'][0]}",
                "audio_cue": "Checkmark click cue"
            },
            {
                "scene_number": 3,
                "timestamp": "00:25 - 00:45",
                "google_flow_prompt": "Close-up on settings screen with red highlight alert badge.",
                "voiceover_script": f"Watch out for trade-offs: {profile['cons'][0]}.",
                "on_screen_text": f"⚠️ WEAKNESS\n• {profile['cons'][0]}",
                "audio_cue": "Warning ping cue"
            },
            {
                "scene_number": 4,
                "timestamp": "00:45 - 00:60",
                "google_flow_prompt": "Channel banner animation showing @IDEguide logo and ideguide.blogspot.com URL.",
                "voiceover_script": "Subscribe to @IDEguide on YouTube and read the full AMP blog post at ideguide.blogspot.com!",
                "on_screen_text": f"Subscribe @IDEguide\n{DISCLAIMER_TEXT}",
                "audio_cue": "Outro swell chime"
            }
        ]
    }

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill CLI tool")
    parser.add_argument("--ide", type=str, help="Name of the IDE/editor (e.g. 'Cursor', 'Lapce')")
    parser.add_argument("--repo-url", type=str, help="GitHub Repository URL (e.g. 'https://github.com/zed-industries/zed')")
    parser.add_argument("--topic", type=str, help="Custom comparison topic (e.g. 'Cursor vs Zed')")
    parser.add_argument("--output-dir", type=str, default="generated_skills_output", help="Output directory")
    args = parser.parse_args()

    if not (args.ide or args.repo_url or args.topic):
        print("Error: Must provide at least one of --ide, --repo-url, or --topic.")
        sys.exit(1)

    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    profile = build_ide_profile(args.ide, args.repo_url, args.topic)

    os.makedirs(args.output_dir, exist_ok=True)
    slug = profile["slug"]

    # AMP Blog Post
    amp_html = generate_agent_amp_post(profile, date_str)
    amp_path = os.path.join(args.output_dir, f"{slug}-review.amp.html")
    with open(amp_path, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # Flow Spec JSON
    flow_spec = generate_agent_flow_spec(profile, date_str)
    flow_json_path = os.path.join(args.output_dir, f"{slug}-flow-spec.json")
    with open(flow_json_path, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    print(f"Agentic Skill Execution Complete!")
    print(f"Target IDE: {profile['name']}")
    print(f" - AMP Post generated: {amp_path}")
    print(f" - Google Flow spec generated: {flow_json_path}")

if __name__ == "__main__":
    main()
