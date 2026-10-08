#!/usr/bin/env python3
"""
AMP HTML Validator for IDE Guide Blogger Posts.
Validates HTML content against Blogger AMP standards and mandatory non-sponsorship disclaimer rules.
"""

import sys
import re
from typing import List, Tuple

MANDATORY_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)


class AmpValidationError(Exception):
    """Raised when HTML content violates AMP HTML rules for Blogger."""
    pass


def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    """
    Validates HTML content against AMP Blogger standards.

    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_errors)
    """
    errors: List[str] = []

    # 1. Check for mandatory non-sponsorship disclaimer
    # Normalize whitespaces for comparison
    normalized_content = re.sub(r'\s+', ' ', html_content)
    normalized_disclaimer = re.sub(r'\s+', ' ', MANDATORY_DISCLAIMER)

    if normalized_disclaimer not in normalized_content:
        errors.append("Missing or modified mandatory non-sponsorship disclaimer.")

    # 2. Check for prohibited HTML <img> tags (must use <amp-img>)
    if re.search(r'<img\b[^>]*>', html_content, re.IGNORECASE):
        errors.append("Forbidden <img> tag found. AMP requires <amp-img>.")

    # 3. Check for inline style attributes (style="...")
    if re.search(r'\bstyle\s*=\s*["\'][^"\']*["\']', html_content, re.IGNORECASE):
        errors.append("Forbidden inline style attribute found (style=\"...\"). AMP forbids inline styles on elements.")

    # 4. Check for disallowed script or frame tags
    if re.search(r'<script\b(?![^>]*custom-element)[^>]*>', html_content, re.IGNORECASE):
        errors.append("Forbidden <script> tag found without custom-element attribute.")

    if re.search(r'<(iframe|embed|object)\b[^>]*>', html_content, re.IGNORECASE):
        errors.append("Forbidden frame/embed tag found (<iframe/embed/object>).")

    # 5. Check <amp-img> tag requirements
    amp_img_matches = re.findall(r'<amp-img\b([^>]*)>', html_content, re.IGNORECASE)
    for idx, attrs in enumerate(amp_img_matches):
        if 'width=' not in attrs.lower():
            errors.append(f"<amp-img> #{idx + 1} is missing required 'width' attribute.")
        if 'height=' not in attrs.lower():
            errors.append(f"<amp-img> #{idx + 1} is missing required 'height' attribute.")

    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <filepath_or_html_str>")
        sys.exit(1)

    path_or_str = sys.argv[1]
    try:
        with open(path_or_str, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        content = path_or_str

    is_valid, errors = validate_amp_html(content)
    if is_valid:
        print("✅ AMP HTML Validation Passed: Content complies with Blogger AMP standards & disclaimer requirements.")
        sys.exit(0)
    else:
        print("❌ AMP HTML Validation Failed:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
