"""Agentic Skill Tool for IDE Guide.

Provides an on-demand CLI tool and agent skill interface to generate custom
AMP HTML blog posts and Google Flow video specs for any given IDE or repository URL.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
from typing import Dict, Any

# Ensure parent directory is in sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.lib.amp_generator import generate_amp_html
from scripts.lib.google_flow_generator import generate_google_flow_spec, format_google_flow_spec_md


def fetch_repo_details(repo_url: str) -> Dict[str, Any]:
    """Extracts repo name from GitHub URL and attempts to fetch metadata from GitHub API."""
    parsed = urllib.parse.urlparse(repo_url)
    path_parts = [p for p in parsed.path.strip("/").split("/") if p]

    if len(path_parts) >= 2:
        owner, repo = path_parts[0], path_parts[1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        headers = {"User-Agent": "IDE-Guide-Agentic-Skill"}
        req = urllib.request.Request(api_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    return {
                        "name": data.get("name", repo).capitalize(),
                        "tagline": f"GitHub Repository ({data.get('stargazers_count', 0):,} stars)",
                        "description": data.get("description") or f"Open source repository hosted on GitHub ({repo_url}).",
                        "category": "GitHub Code Repository / Editor",
                        "pricing_type": "Free",
                        "pricing_details": f"Open Source under {data.get('license', {}).get('name', 'Open Source License') if data.get('license') else 'Open Source'}.",
                        "features": [
                            "Open source code structure hosted on GitHub",
                            f"Maintained by {owner} with active community stargazers",
                            "Issue tracking and pull request collaboration",
                            "Cross-platform support and build scripts"
                        ],
                        "pros": ["Fully open-source transparent codebase", "Community support and forkability"],
                        "cons": ["May require technical knowledge to build from source"],
                        "best_for": f"Developers interested in evaluating or contributing to {data.get('name', repo)}."
                    }
        except Exception:
            pass

    repo_name = path_parts[-1].capitalize() if path_parts else "Custom IDE"
    return {
        "name": repo_name,
        "tagline": f"Custom software repository ({repo_url})",
        "description": f"Evaluation and review of {repo_name} available at {repo_url}.",
        "category": "Custom IDE / Editor",
        "pricing_type": "Free / Open Source",
        "pricing_details": "Refer to official repository for licensing and pricing tier info.",
        "features": ["Source code repository access", "Customizable configuration"],
        "pros": ["Available on GitHub", "Direct code access"],
        "cons": ["Manual setup required"],
        "best_for": "Developers evaluating customized software tools."
    }


def generate_custom_ide_content(ide_name: str = None, repo_url: str = None, output_dir: str = "content/custom") -> Dict[str, str]:
    """Agentic skill handler that generates custom AMP HTML and Google Flow video spec."""
    if repo_url:
        ide_info = fetch_repo_details(repo_url)
    elif ide_name:
        ide_info = {
            "name": ide_name,
            "tagline": f"Comprehensive developer breakdown for {ide_name}",
            "description": f"A dedicated analysis of {ide_name}, assessing user interface, developer ergonomics, features, and performance.",
            "category": "Code Editor / IDE",
            "pricing_type": "Freemium",
            "pricing_details": "Free community/trial version available with optional premium tier.",
            "features": [
                f"Advanced language support tailored for {ide_name} workflows",
                "Built-in project navigation and workspace management",
                "Extensible extensions and custom theme compatibility",
                "Integrated terminal and execution controls"
            ],
            "pros": ["Tailored feature set", "Ergonomic developer workflow", "Strong ecosystem support"],
            "cons": ["Initial setup and configuration time"],
            "best_for": f"Developers seeking an in-depth review of {ide_name}."
        }
    else:
        raise ValueError("Either --ide or --url must be provided.")

    slug = ide_info["name"].lower().replace(" ", "-").replace("/", "-")
    os.makedirs(output_dir, exist_ok=True)

    # AMP HTML Post
    amp_html = generate_amp_html(ide_info)
    amp_path = os.path.join(output_dir, f"{slug}_post.amp.html")
    with open(amp_path, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # Google Flow Video Specs
    spec = generate_google_flow_spec(ide_info)
    spec_json_path = os.path.join(output_dir, f"{slug}_video_spec.json")
    with open(spec_json_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)

    spec_md = format_google_flow_spec_md(spec)
    spec_md_path = os.path.join(output_dir, f"{slug}_video_spec.md")
    with open(spec_md_path, "w", encoding="utf-8") as f:
        f.write(spec_md)

    return {
        "amp_post": amp_path,
        "video_spec_json": spec_json_path,
        "video_spec_md": spec_md_path
    }


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill CLI - Generate custom AMP posts and Google Flow specs.")
    parser.add_argument("--ide", type=str, help="Name of the IDE or Code Editor (e.g., 'Cursor')")
    parser.add_argument("--url", type=str, help="Repository URL (e.g., 'https://github.com/zed-industries/zed')")
    parser.add_argument("--outdir", type=str, default="content/custom", help="Output directory for generated files")

    args = parser.parse_args()

    if not args.ide and not args.url:
        parser.error("Please specify either --ide or --url.")

    result = generate_custom_ide_content(ide_name=args.ide, repo_url=args.url, output_dir=args.outdir)
    print("Agentic Skill Execution Complete! Generated custom content package:")
    for key, val in result.items():
        print(f" - {key}: {val}")


if __name__ == "__main__":
    main()
