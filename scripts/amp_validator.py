#!/usr/bin/env python3
"""
AMP HTML Validator for IDE Guide Blogger Posts.
Validates generated HTML against Blogger AMP rules:
1. No standard <img> tags (must use <amp-img>).
2. <amp-img> must have width, height, and layout attributes.
3. No forbidden inline style attributes on <img> tags.
4. Must contain the non-sponsorship disclaimer.
"""

import re
import sys
from typing import List, Tuple

MANDATORY_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)


def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    """
    Validates HTML content against Blogger AMP standards.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    # 1. Check for forbidden standard <img> tags
    raw_img_matches = re.findall(r'<img\b[^>]*>', html_content, re.IGNORECASE)
    if raw_img_matches:
        errors.append(f"Forbidden standard <img> tags found: {len(raw_img_matches)} instance(s). Use <amp-img> instead.")

    # 2. Check <amp-img> tag attributes
    amp_img_matches = re.findall(r'<amp-img\b([^>]*)>', html_content, re.IGNORECASE)
    for idx, attrs in enumerate(amp_img_matches, 1):
        if 'width=' not in attrs.lower():
            errors.append(f"<amp-img> #{idx} missing 'width' attribute.")
        if 'height=' not in attrs.lower():
            errors.append(f"<amp-img> #{idx} missing 'height' attribute.")
        if 'layout=' not in attrs.lower():
            errors.append(f"<amp-img> #{idx} missing 'layout' attribute (e.g. layout=\"responsive\").")

    # 3. Check for inline style on amp-img or illegal tags
    if re.search(r'<amp-img\b[^>]*\bstyle=', html_content, re.IGNORECASE):
        errors.append("<amp-img> contains forbidden inline 'style' attribute.")

    # 4. Check for mandatory non-sponsorship disclaimer
    # Normalize whitespaces for comparison
    normalized_content = " ".join(html_content.split())
    normalized_disclaimer = " ".join(MANDATORY_DISCLAIMER.split())
    if normalized_disclaimer not in normalized_content:
        errors.append("Mandatory non-sponsorship disclaimer is missing or modified.")

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
        print(f"Error reading file '{filepath}': {e}")
        sys.exit(1)

    is_valid, errors = validate_amp_html(content)
    if is_valid:
        print(f"✅ AMP Validation Passed for: {filepath}")
        sys.exit(0)
    else:
        print(f"❌ AMP Validation Failed for: {filepath}")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
