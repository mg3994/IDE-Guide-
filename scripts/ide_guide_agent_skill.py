#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide
Generates on-demand AMP HTML blog posts and Google Flow video specs
for custom IDE names or GitHub repository URLs.
"""

import os
import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.amp_validator import REQUIRED_DISCLAIMER, validate_amp_html


def slugify(text: str) -> str:
    """Converts a string to a filesystem-friendly slug."""
    clean = "".join(c.lower() if c.isalnum() else "-" for c in text)
    return "-".join(filter(None, clean.split("-")))


def generate_custom_content(ide_name: str, repo_url: str = None, outdir: str = None) -> dict:
    slug = slugify(ide_name)
    if not outdir:
        outdir = f"content/custom/{slug}"

    out_path = Path(outdir)
    out_path.mkdir(parents=True, exist_ok=True)

    repo_info = f"<p>Source repository: <a href='{repo_url}'>{repo_url}</a></p>" if repo_url else ""

    # AMP HTML Blog Post
    amp_html = f"""<!DOCTYPE html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide_name} - In-Depth Review & Developer Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/p/{slug}-guide.html">
  <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #202124;
      background-color: #f8f9fa;
      margin: 0;
      padding: 16px;
    }}
    .container {{
      max-width: 800px;
      margin: 0 auto;
      background: #ffffff;
      padding: 24px;
      border-radius: 8px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }}
    h1 {{
      color: #1a73e8;
      font-size: 26px;
    }}
    .section-header {{
      font-size: 18px;
      color: #3c4043;
      border-bottom: 2px solid #e8eaed;
      padding-bottom: 4px;
      margin-top: 20px;
    }}
    .good-box {{ color: #137333; }}
    .bad-box {{ color: #c5221f; }}
    .disclaimer-box {{
      background: #fce8e6;
      border: 1px solid #fad2cf;
      padding: 14px;
      border-radius: 6px;
      margin-top: 28px;
      font-size: 13px;
      color: #5f6368;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>{ide_name} Developer Evaluation</h1>
    {repo_info}
    <p>An objective, technical analysis of <strong>{ide_name}</strong> for software engineers, highlighting features, pros, cons, pricing structure, and recommended developer use cases.</p>

    <amp-img src="https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800&auto=format&fit=crop" width="800" height="450" layout="responsive" alt="{ide_name} Editor Environment"></amp-img>

    <h2 class="section-header">The Good (Pros)</h2>
    <ul class="good-box">
      <li><strong>Modern architecture</strong> tailored for developer velocity and efficiency.</li>
      <li><strong>Intuitive user interface</strong> with customizable workspaces and keybinding profiles.</li>
      <li><strong>Extensible design</strong> supporting language server protocol (LSP) standards.</li>
    </ul>

    <h2 class="section-header">The Bad (Cons)</h2>
    <ul class="bad-box">
      <li><strong>Plugin ecosystem</strong> may be growing or require configuration tuning.</li>
      <li><strong>Resource consumption</strong> depends on project scale and background indexing tasks.</li>
    </ul>

    <h2 class="section-header">Pricing & Licensing</h2>
    <p>Evaluate licensing models, free tiers, and commercial subscriptions prior to enterprise adoption.</p>

    <h2 class="section-header">Verdict & Recommendation</h2>
    <p>Ideal for software engineers looking for tailored code editing capabilities and modern developer ergonomics.</p>

    <div class="disclaimer-box">
      <p>{REQUIRED_DISCLAIMER}</p>
    </div>
  </div>
</body>
</html>"""

    # Validate AMP
    val_res = validate_amp_html(amp_html)
    if not val_res["valid"]:
        raise ValueError(f"Generated custom AMP HTML failed validation: {val_res['errors']}")

    blog_file = out_path / "blog_post.amp.html"
    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # Google Flow Video Spec
    flow_spec = {
        "channel": "@IDEguide",
        "tool_name": ide_name,
        "repository_url": repo_url,
        "target_formats": [
            {"type": "YouTube Standard", "aspect_ratio": "16:9", "resolution": "1920x1080"},
            {"type": "YouTube Shorts", "aspect_ratio": "9:16", "resolution": "1080x1920"}
        ],
        "visual_prompts": {
            "style": "Dark mode code editor with neon cyan and magenta highlighting",
            "lighting": "Clean studio lighting with soft ambient rim light on desk workspace",
            "camera": "Dynamic close-ups, macro code focus, smooth tracking pans"
        },
        "narration_script": [
            f"Looking for an inside view on {ide_name}? Let's break down its top features, performance, and best developer use cases in 60 seconds!",
            f"The Good: Built with modern architecture, fast code parsing, and clean workspace ergonomics.",
            f"The Bad: Plugin ecosystem and keybinding setup may require initial configuration.",
            f"Verdict: Great option for modern software developers. Full AMP review live on ideguide.blogspot.com!"
        ],
        "disclaimer": REQUIRED_DISCLAIMER
    }

    spec_json_file = out_path / "video_flow_spec.json"
    with open(spec_json_file, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    spec_md_file = out_path / "video_flow_spec.md"
    with open(spec_md_file, "w", encoding="utf-8") as f:
        f.write(f"# Google Flow Video Spec: {ide_name}\n\n"
                f"- **Channel**: @IDEguide\n"
                f"- **Repo**: {repo_url or 'N/A'}\n\n"
                f"## Script\n" + "\n".join([f"- {s}" for s in flow_spec['narration_script']]) +
                f"\n\n## Disclaimer\n> {REQUIRED_DISCLAIMER}\n")

    return {
        "output_directory": str(out_path),
        "blog_file": str(blog_file),
        "spec_json_file": str(spec_json_file),
        "spec_md_file": str(spec_md_file)
    }


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic CLI Skill Tool")
    parser.add_argument("--ide", type=str, help="Name of the IDE or Code Editor")
    parser.add_argument("--repo", type=str, help="GitHub Repository URL of the IDE/Editor")
    parser.add_argument("--outdir", type=str, help="Custom output directory")

    args = parser.parse_args()

    if not args.ide and not args.repo:
        parser.error("At least one of --ide or --repo must be provided.")

    ide_name = args.ide
    if not ide_name and args.repo:
        # Extract repo name from URL
        ide_name = args.repo.rstrip("/").split("/")[-1].capitalize()

    result = generate_custom_content(ide_name=ide_name, repo_url=args.repo, outdir=args.outdir)
    print(f"Agentic skill successfully generated content for '{ide_name}':")
    print(f" - Output Directory: {result['output_directory']}")
    print(f" - AMP Blog Post: {result['blog_file']}")
    print(f" - Google Flow Specs: {result['spec_json_file']}")


if __name__ == "__main__":
    main()
