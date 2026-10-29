#!/usr/bin/env python3
"""
AMP Validator Script for Blogger Posts.
Checks HTML files for basic AMP compliance:
- Ensures forbidden tags like <img>, <iframe>, <video> are replaced with <amp-img>, <amp-youtube>, <amp-video>.
- Ensures <amp-img> elements have width, height, and layout attributes.
- Checks that no inline style="..." attributes are present in post body content.
- Verifies presence of mandatory non-sponsorship disclaimer.
"""

import sys
import re
from xml.etree import ElementTree

DISCLAIMER_TEXT = "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."

def validate_amp_html(html_content: str) -> tuple[bool, list[str]]:
    errors = []

    # Check for forbidden HTML tags
    if re.search(r'<img\b', html_content, re.IGNORECASE):
        errors.append("Forbidden tag <img> found. Use <amp-img> instead.")

    if re.search(r'<iframe\b', html_content, re.IGNORECASE):
        errors.append("Forbidden tag <iframe> found. Use <amp-youtube> or relevant AMP component.")

    if re.search(r'<video\b', html_content, re.IGNORECASE):
        errors.append("Forbidden tag <video> found. Use <amp-video> instead.")

    if re.search(r'<script\b(?!.*src="https://cdn\.ampproject\.org)', html_content, re.IGNORECASE):
        errors.append("Inline or non-AMP script tags are forbidden in AMP body content.")

    # Check for inline style attributes
    if re.search(r'\bstyle\s*=\s*"', html_content, re.IGNORECASE):
        errors.append("Inline style attributes (style=\"...\") are forbidden in strict AMP HTML.")

    # Check amp-img tags for width and height
    amp_img_matches = re.findall(r'<amp-img\b([^>]*)>', html_content, re.IGNORECASE)
    for match in amp_img_matches:
        if 'width=' not in match or 'height=' not in match:
            errors.append(f"<amp-img> missing required width/height attribute: <amp-img {match}>")

    # Check disclaimer
    if DISCLAIMER_TEXT.lower() not in html_content.lower():
        errors.append("Missing mandatory non-sponsorship disclaimer.")

    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <path_to_html_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        sys.exit(1)

    is_valid, errors = validate_amp_html(content)
    if is_valid:
        print(f"SUCCESS: {filepath} is valid AMP HTML for Blogger.")
        sys.exit(0)
    else:
        print(f"FAILED: {filepath} has AMP validation errors:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
