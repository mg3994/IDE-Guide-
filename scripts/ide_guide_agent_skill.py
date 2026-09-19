#!/usr/bin/env python3
"""
IDE Guide - Agentic Skill Tool
Allows on-demand generation of AMP HTML blog posts and Google Flow video specs for any IDE or GitHub Repository.

Usage:
  python3 scripts/ide_guide_agent_skill.py --ide "Zed Editor"
  python3 scripts/ide_guide_agent_skill.py --url "https://github.com/zed-industries/zed"
  python3 scripts/ide_guide_agent_skill.py --ide "Cursor" --out "./output/"
"""

import argparse
import json
import os
import re
import sys
import datetime
import urllib.request
import urllib.parse
import urllib.error

# Import helpers from generate_daily_content
try:
    from generate_daily_content import (
        CURATED_IDES,
        DISCLAIMER_TEXT,
        build_amp_html,
        build_google_flow_spec,
        build_google_flow_markdown,
        load_history,
        save_history
    )
except ImportError:
    # If running from root directory
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    from generate_daily_content import (
        CURATED_IDES,
        DISCLAIMER_TEXT,
        build_amp_html,
        build_google_flow_spec,
        build_google_flow_markdown,
        load_history,
        save_history
    )


def fetch_github_repo_info(url_or_slug):
    """
    Parses GitHub URL/slug and fetches repo metadata via GitHub REST API if possible.
    Returns synthesized IDE dictionary.
    """
    cleaned = url_or_slug.strip()
    match = re.search(r"github\.com/([^/]+)/([^/]+)", cleaned)
    if match:
        owner, repo = match.group(1), match.group(2).rstrip(".git")
    elif "/" in cleaned:
        parts = cleaned.split("/")
        owner, repo = parts[0], parts[1]
    else:
        owner, repo = "developer", cleaned

    slug = repo.lower()
    name = repo.replace("-", " ").replace("_", " ").title()

    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(api_url, headers={"User-Agent": "IDEGuideAgentSkill/1.0"})

    description = f"Modern open-source software tool: {name}."
    language = "Polyglot / Multi-language"
    stargazers = 0

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                description = data.get("description") or description
                language = data.get("language") or language
                stargazers = data.get("stargazers_count", 0)
    except Exception as e:
        # Graceful fallback on network/rate-limit error
        pass

    ide_info = {
        "id": slug,
        "name": name,
        "vendor": owner.title(),
        "category": f"{language} Development Tool / Editor" if language else "Code Editor / IDE",
        "pricing_type": "Free / Open Source",
        "pricing_details": f"Open source repository ({owner}/{repo}). {f'{stargazers:,} stars on GitHub.' if stargazers else ''}",
        "pros": [
            f"Active open source project with transparent repository development ({owner}/{repo}).",
            f"Primary language ecosystem focused on {language if language else 'modern software engineering'}.",
            f"{description}",
            "Highly extensible and community-driven architecture."
        ],
        "cons": [
            "May require active setup and configuration for specific workflow pipelines.",
            "Features subject to fast open-source development iterations.",
            "Community plugin ecosystem depending on project adoption phase."
        ],
        "best_for": f"Developers looking for modern {language} tooling and open-source customizable software environments.",
        "github_repo": f"{owner}/{repo}",
        "official_url": f"https://github.com/{owner}/{repo}"
    }

    return ide_info


def find_or_build_ide_info(ide_name=None, url=None):
    if ide_name:
        target = ide_name.strip().lower()
        for ide in CURATED_IDES:
            if target in ide["id"].lower() or target in ide["name"].lower():
                return ide

        # If not in curated list, construct custom IDE dictionary
        slug = re.sub(r"[^a-z0-9]+", "-", target).strip("-")
        return {
            "id": slug,
            "name": ide_name.strip(),
            "vendor": "Independent Software Developer",
            "category": "Code Editor / Developer Environment",
            "pricing_type": "Free / Freemium",
            "pricing_details": "Free community edition or standard pricing model available.",
            "pros": [
                f"Tailored productivity features designed for {ide_name}.",
                "Fast syntax highlighting and smart workspace navigation.",
                "Customizable layout and developer extensions.",
                "Cross-platform support for modern operating systems."
            ],
            "cons": [
                "Requires learning specific hotkeys and workspace configuration.",
                "Extension ecosystem depends on active user adoption.",
                "Memory consumption varies based on open workspace size."
            ],
            "best_for": f"Software engineers wanting a feature-rich, specialized editing experience in {ide_name}.",
            "github_repo": "",
            "official_url": f"https://ideguide.blogspot.com/search?q={urllib.parse.quote(ide_name)}"
        }

    if url:
        return fetch_github_repo_info(url)

    raise ValueError("Either --ide or --url must be provided.")


def run_agent_skill(ide_name=None, url=None, out_dir=None, record_history=False):
    ide_info = find_or_build_ide_info(ide_name=ide_name, url=url)

    if not out_dir:
        date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        out_dir = os.path.join("content", "custom", f"{date_str}-{ide_info['id']}")

    os.makedirs(out_dir, exist_ok=True)

    amp_html = build_amp_html(ide_info)
    flow_spec_json = build_google_flow_spec(ide_info)
    flow_spec_md = build_google_flow_markdown(flow_spec_json)

    amp_path = os.path.join(out_dir, "amp_post.html")
    json_path = os.path.join(out_dir, "google_flow_spec.json")
    md_path = os.path.join(out_dir, "google_flow_spec.md")

    with open(amp_path, "w", encoding="utf-8") as f:
        f.write(amp_html)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(flow_spec_json, f, indent=2, ensure_ascii=False)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(flow_spec_md)

    if record_history:
        history_file = os.path.join("content", "history.json")
        history_data = load_history(history_file)
        if ide_info["id"] not in history_data["covered_ides"]:
            history_data["covered_ides"].append(ide_info["id"])
        history_data.setdefault("history", []).append({
            "id": ide_info["id"],
            "name": ide_info["name"],
            "date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
            "path": out_dir,
            "source": "cli_agent_skill"
        })
        save_history(history_data, history_file)

    return {
        "status": "success",
        "ide_name": ide_info["name"],
        "out_dir": out_dir,
        "files": {
            "amp_html": amp_path,
            "flow_spec_json": json_path,
            "flow_spec_md": md_path
        }
    }


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agent Skill Tool")
    parser.add_argument("--ide", type=str, help="Name of the IDE or Code Editor (e.g., 'Cursor', 'Zed')")
    parser.add_argument("--url", type=str, help="GitHub repository URL (e.g., 'https://github.com/zed-industries/zed')")
    parser.add_argument("--out", type=str, help="Custom output directory path")
    parser.add_argument("--save-history", action="store_true", help="Record generation in content/history.json")

    args = parser.parse_args()

    if not args.ide and not args.url:
        parser.print_help()
        sys.exit(1)

    try:
        result = run_agent_skill(
            ide_name=args.ide,
            url=args.url,
            out_dir=args.out,
            record_history=args.save_history
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
