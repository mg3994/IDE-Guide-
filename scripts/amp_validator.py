#!/usr/bin/env python3
"""
AMP HTML Validator for IDE Guide Blog Posts.
Validates AMP HTML rules and verifies non-sponsorship disclaimer compliance.
"""

import re
import sys
from typing import List, Tuple

REQUIRED_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any "
    "software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)


def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    """
    Validates HTML content against AMP Blogger standards.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    # 1. Check for illegal <img> tags in AMP (must use <amp-img>)
    img_matches = re.findall(r'<img\s+[^>]*>', html_content, re.IGNORECASE)
    if img_matches:
        errors.append(f"Found forbidden <img> tag(s): {len(img_matches)}. AMP requires <amp-img>.")

    # 2. Check for illegal inline event handlers or custom scripts (unless amp scripts)
    inline_script_matches = re.findall(r'<script(?!\s+type=["\']application/ld\+json["\']|\s+async|\s+custom-element)[^>]*>', html_content, re.IGNORECASE)
    if inline_script_matches:
        errors.append("Found forbidden custom <script> tags without proper AMP async/custom attributes.")

    # 3. Check for illegal inline style attributes
    style_attr_matches = re.findall(r'\sstyle=["\'][^"\'\'>]+["\']', html_content, re.IGNORECASE)
    if style_attr_matches:
        errors.append(f"Found forbidden inline style attributes: {len(style_attr_matches)}. AMP prohibits style=\"...\".")

    # 4. Check for mandatory amp-img attributes if <amp-img> is present
    amp_img_tags = re.findall(r'<amp-img\s+[^>]*>', html_content, re.IGNORECASE)
    for tag in amp_img_tags:
        if 'layout=' not in tag.lower():
            errors.append(f"<amp-img> missing layout attribute: {tag}")
        if 'width=' not in tag.lower() or 'height=' not in tag.lower():
            errors.append(f"<amp-img> missing width/height attributes: {tag}")

    # 5. Check for non-sponsorship disclaimer
    # Normalize whitespaces for robust matching
    normalized_content = " ".join(html_content.split())
    normalized_disclaimer = " ".join(REQUIRED_DISCLAIMER.split())
    if normalized_disclaimer not in normalized_content:
        errors.append("Missing required exact non-sponsorship disclaimer text.")

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

    is_valid, errors = validate_amp_html(content)
    if is_valid:
        print(f"SUCCESS: {filepath} passed AMP HTML validation!")
        sys.exit(0)
    else:
        print(f"FAILED: {filepath} has AMP HTML validation errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
