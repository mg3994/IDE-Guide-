#!/usr/bin/env python3
"""
AMP HTML & Compliance Validator for IDE Guide Blog Posts.
Validates HTML content against AMP HTML constraints and required disclaimer clauses.
"""

import re
import sys
from typing import List, Tuple

REQUIRED_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based "
    "strictly on objective developer evaluation."
)


def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    """
    Validates AMP HTML string for mandatory tags and prohibited rules.
    Returns (is_valid: bool, errors: List[str])
    """
    errors = []

    # 1. Root tag check
    if not re.search(r"<html\s+[^>]*\b(amp|⚡)\b[^>]*>", html_content, re.IGNORECASE):
        errors.append("Missing `<html amp>` or `<html ⚡>` tag.")

    # 2. Meta charset
    if not re.search(r'<meta\s+charset=["\']utf-8["\']\s*/?>', html_content, re.IGNORECASE):
        errors.append("Missing `<meta charset=\"utf-8\">` declaration.")

    # 3. AMP JS Library
    if "https://cdn.ampproject.org/v0.js" not in html_content:
        errors.append("Missing AMP core JS script `<script async src=\"https://cdn.ampproject.org/v0.js\"></script>`.")

    # 4. Canonical link
    if not re.search(r'<link\s+rel=["\']canonical["\']', html_content, re.IGNORECASE):
        errors.append("Missing `<link rel=\"canonical\" href=\"...\">` tag.")

    # 5. Viewport meta
    if not re.search(r'<meta\s+name=["\']viewport["\']', html_content, re.IGNORECASE):
        errors.append("Missing `<meta name=\"viewport\" ...>` tag.")

    # 6. AMP Boilerplate CSS
    if "<style amp-boilerplate>" not in html_content:
        errors.append("Missing `<style amp-boilerplate>` block.")

    # 7. Prohibited regular img tags
    if re.search(r"<img\b[^>]*>", html_content, re.IGNORECASE):
        errors.append("Prohibited `<img` tag found. AMP requires `<amp-img>`.")

    # 8. Inline style attributes
    if re.search(r'\bstyle=["\'][^"\']*["\']', html_content, re.IGNORECASE):
        errors.append("Prohibited inline `style=\"...\"` attribute found.")

    # 9. Non-sponsorship disclaimer check
    # Normalize spaces for comparison
    normalized_content = " ".join(html_content.split())
    normalized_disclaimer = " ".join(REQUIRED_DISCLAIMER.split())
    if normalized_disclaimer not in normalized_content:
        errors.append("Missing required non-sponsorship disclaimer in HTML content.")

    return (len(errors) == 0, errors)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <filepath_or_html>")
        sys.exit(1)

    arg = sys.argv[1]

    if arg in ("--help", "-h"):
        print("AMP Validator CLI - Validates HTML files for Blogger AMP compliance.")
        sys.exit(0)

    try:
        with open(arg, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        content = arg

    is_valid, errors = validate_amp_html(content)
    if is_valid:
        print("✅ AMP HTML Validation Passed successfully.")
        sys.exit(0)
    else:
        print("❌ AMP HTML Validation Failed with the following errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
