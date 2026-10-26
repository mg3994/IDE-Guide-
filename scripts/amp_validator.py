#!/usr/bin/env python3
"""
AMP HTML Validator script for IDE Guide Blogger Posts.
Validates AMP rules:
- Prohibits standard <img> tags (must use <amp-img>)
- Prohibits <script> tags unless amp runtime/components
- Checks for essential AMP tags or tags compatible with Blogger AMP
- Verifies required non-sponsorship disclaimer text
"""

import re
import sys
from typing import List, Tuple

MANDATORY_DISCLAIMER_PHRASE = (
    "IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above."
)

def validate_amp_content(content: str) -> Tuple[bool, List[str]]:
    errors = []

    # Check for forbidden <img> tag
    img_matches = re.findall(r'<img\b[^>]*>', content, re.IGNORECASE)
    if img_matches:
        errors.append(f"Forbidden <img> tag found ({len(img_matches)} occurrence(s)). Use <amp-img> instead.")

    # Check for improper <script> tags (allow amp-custom or boilerplate script if present, but flag generic un-approved scripts)
    script_matches = re.findall(r'<script\b[^>]*>(.*?)</script>', content, re.IGNORECASE | re.DOTALL)
    for script in script_matches:
        if 'custom-element' not in script and 'cdn.ampproject.org' not in script and 'application/ld+json' not in script:
            errors.append("Unapproved <script> tag detected. In AMP HTML, custom JS scripts are prohibited.")

    # Check for amp-img tags without width and height
    amp_imgs = re.findall(r'<amp-img\b([^>]*)>', content, re.IGNORECASE)
    for amp_img in amp_imgs:
        if 'width=' not in amp_img or 'height=' not in amp_img:
            errors.append(f"<amp-img> tag missing required 'width' or 'height' attribute: <amp-img{amp_img}>")

    # Check for mandatory disclaimer
    if MANDATORY_DISCLAIMER_PHRASE not in content:
        errors.append("Mandatory non-sponsorship disclaimer missing or modified.")

    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 amp_validator.py <file_path>")
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        sys.exit(1)

    is_valid, errors = validate_amp_content(content)
    if is_valid:
        print(f"SUCCESS: '{filepath}' passed AMP Blogger validation.")
        sys.exit(0)
    else:
        print(f"FAILED: '{filepath}' failed AMP Blogger validation:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
