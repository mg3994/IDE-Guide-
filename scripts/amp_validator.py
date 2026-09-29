#!/usr/bin/env python3
"""
AMP HTML Validator for IDE Guide Blogger Posts.
Validates HTML content against Google AMP specifications and IDE Guide guidelines.
"""

import re
import sys
from typing import List, Tuple

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based "
    "strictly on objective developer evaluation."
)


def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    errors = []

    # 1. Check root html tag
    if not re.search(r"<html\s+(⚡|amp)[\s>]", html_content, re.IGNORECASE):
        errors.append("Missing `<html ⚡>` or `<html amp>` tag.")

    # 2. Check meta charset
    if not re.search(r'<meta\s+charset=["\']utf-8["\']\s*/?>', html_content, re.IGNORECASE):
        errors.append("Missing `<meta charset=\"utf-8\">` declaration.")

    # 3. Check AMP JS runtime
    if 'src="https://cdn.ampproject.org/v0.js"' not in html_content and "src='https://cdn.ampproject.org/v0.js'" not in html_content:
        errors.append("Missing AMP runtime script `<script async src=\"https://cdn.ampproject.org/v0.js\"></script>`.")

    # 4. Check canonical link
    if not re.search(r'<link\s+rel=["\']canonical["\']\s+href=', html_content, re.IGNORECASE):
        errors.append("Missing `<link rel=\"canonical\" href=\"...\">` tag.")

    # 5. Check viewport meta tag
    if "width=device-width" not in html_content:
        errors.append("Missing viewport meta tag with `width=device-width`.")

    # 6. Check amp-boilerplate
    if "<style amp-boilerplate>" not in html_content:
        errors.append("Missing `<style amp-boilerplate>` block.")

    # 7. Check for forbidden standard <img> tags
    if re.search(r'<img\s+[^>]*>', html_content, re.IGNORECASE):
        errors.append("Forbidden standard `<img>` tag found. Use `<amp-img>` instead.")

    # 8. Check for forbidden inline style attributes
    if re.search(r'\sstyle=["\'][^"\']*["\']', html_content, re.IGNORECASE):
        errors.append("Forbidden inline `style=\"...\"` attribute found in AMP HTML.")

    # 9. Check amp-img tags have required attributes
    amp_img_matches = re.findall(r'<amp-img\s+([^>]+)>', html_content, re.IGNORECASE)
    for idx, attrs in enumerate(amp_img_matches, start=1):
        for req_attr in ["src=", "width=", "height=", "alt="]:
            if req_attr not in attrs.lower():
                errors.append(f"<amp-img> #{idx} is missing required attribute '{req_attr.rstrip('=')}'")

    # 10. Check non-sponsorship disclaimer
    if DISCLAIMER_TEXT not in html_content:
        errors.append("Missing required non-sponsorship disclaimer text.")

    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        sys.exit(1)

    is_valid, errors = validate_amp_html(content)
    if is_valid:
        print(f"✅ AMP HTML validation PASSED for {filepath}")
        sys.exit(0)
    else:
        print(f"❌ AMP HTML validation FAILED for {filepath}:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
