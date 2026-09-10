#!/usr/bin/env python3
"""
IDE Guide Agentic Skill CLI Tool
Agentic tool enabling users to generate custom AMP HTML blog posts and Google Flow video specs
for any specified IDE name or GitHub repository URL.
"""

import argparse
import json
import os
import sys
import datetime
import urllib.request
import urllib.parse
from generate_daily_content import generate_amp_html, generate_google_flow_spec, MANDATORY_DISCLAIMER

def fetch_github_repo_info(repo_url):
    """Fetch details from GitHub API if a repository URL is provided."""
    # Parse repo owner and name from URL e.g. https://github.com/vscodium/vscodium
    parts = repo_url.strip("/").split("/")
    if len(parts) >= 2:
        owner, repo = parts[-2], parts[-1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        req = urllib.request.Request(api_url, headers={"User-Agent": "IDEGuide-Skill"})
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    name = data.get("name", repo).replace("-", " ").capitalize()
                    desc = data.get("description") or f"{name} code editor repository."
                    license_name = data.get("license", {}).get("name", "Open Source") if data.get("license") else "Open Source"
                    return {
                        "name": name,
                        "category": "Open Source Code Editor / IDE",
                        "tagline": desc[:100] + "..." if len(desc) > 100 else desc,
                        "description": desc,
                        "pricing_model": "100% Free & Open Source",
                        "pricing_details": f"Licensed under {license_name}. Free community software.",
                        "pros": [
                            f"Over {data.get('stargazers_count', 0)} stars on GitHub",
                            "Transparent open source codebase and issue tracker",
                            f"Primary language: {data.get('language', 'Polyglot')}"
                        ],
                        "cons": [
                            "Community-driven plugin ecosystem and manual build configuration"
                        ],
                        "best_for": "Developers seeking an open-source, flexible, and custom coding environment.",
                        "url": data.get("html_url", repo_url)
                    }
        except Exception:
            pass

    # Fallback if GitHub API fails or non-standard URL
    repo_name = parts[-1].replace("-", " ").capitalize()
    return {
        "name": repo_name,
        "category": "Code Editor",
        "tagline": f"Custom development environment for {repo_name}",
        "description": f"{repo_name} is a feature-rich development environment and code editor.",
        "pricing_model": "Free / Open Source",
        "pricing_details": "Free community edition or open-source availability.",
        "pros": [
            "Extensible editor framework",
            "Customizable keybindings and theme options",
            "High efficiency workspace"
        ],
        "cons": [
            "Requires initial setup configuration"
        ],
        "best_for": "Developers seeking a custom and adaptable coding experience.",
        "url": repo_url
    }

def main():
    parser = argparse.ArgumentParser(
        description="IDE Guide Agentic Skill - Generate custom AMP HTML blog post and Google Flow video spec on demand."
    )
    parser.add_argument("--ide", type=str, help="Name of the IDE or Code Editor (e.g., 'Cursor', 'Sublime Text', 'Helix')")
    parser.add_argument("--repo", type=str, help="GitHub repository URL for the code editor (e.g., 'https://github.com/helix-editor/helix')")
    parser.add_argument("--output-dir", type=str, default="generated_skills", help="Directory where generated assets will be stored.")

    args = parser.parse_args()

    if not args.ide and not args.repo:
        print("Error: Please specify either --ide <name> or --repo <github_url>")
        sys.exit(1)

    if args.repo:
        print(f"Fetching repository details for: {args.repo}...")
        ide_data = fetch_github_repo_info(args.repo)
        if args.ide:
            ide_data["name"] = args.ide
    else:
        ide_name = args.ide
        ide_data = {
            "name": ide_name,
            "category": "Modern Code Editor / IDE",
            "tagline": f"Comprehensive developer breakdown and review of {ide_name}",
            "description": f"{ide_name} is a modern code editor engineered to increase developer velocity, streamline syntax management, and provide robust coding workflows.",
            "pricing_model": "Freemium / Open Source options available",
            "pricing_details": f"Check official {ide_name} website for tiered licensing and developer plans.",
            "pros": [
                f"Tailored productivity features designed for {ide_name}",
                "Fast syntax highlighting and language server integration",
                "Customizable keymaps and UI themes"
            ],
            "cons": [
                "Ecosystem plugin availability varies by language stack"
            ],
            "best_for": f"Developers looking for an efficient {ide_name} workflow.",
            "url": f"https://www.google.com/search?q={urllib.parse.quote(ide_name)}+code+editor"
        }

    os.makedirs(args.output_dir, exist_ok=True)
    clean_name = ide_data["name"].lower().replace(" ", "_").replace("/", "_")

    # Generate AMP HTML
    amp_html = generate_amp_html(ide_data)
    amp_path = os.path.join(args.output_dir, f"{clean_name}_blog_post.amp.html")
    with open(amp_path, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # Generate Google Flow spec
    flow_spec = generate_google_flow_spec(ide_data)
    spec_path = os.path.join(args.output_dir, f"{clean_name}_google_flow_spec.json")
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    print(f"Successfully generated agentic skill assets for '{ide_data['name']}':")
    print(f"  [+] AMP HTML Blog Post: {amp_path}")
    print(f"  [+] Google Flow Video Spec: {spec_path}")

if __name__ == "__main__":
    main()
