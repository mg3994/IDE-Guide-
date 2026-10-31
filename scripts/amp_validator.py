#!/usr/bin/env python3
"""
AMP HTML Validator for Blogger Post Content Snippets
Validates that generated HTML strictly adheres to AMP standards for blog post content.
"""

import re
import sys
from typing import List, Tuple

MANDATORY_DISCLAIMER_SNIPPET = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

DISALLOWED_TAGS = [
    r"<script\b",
    r"<style(?! amp-custom\b)",  # style without amp-custom
    r"<link\b",
    r"<iframe(?!.*amp-youtube\b)",
    r"<img\b",                   # must use <amp-img>
    r"<video\b",                 # must use <amp-video>
    r"<audio\b",                 # must use <amp-audio>
    r"<frame\b",
    r"<frameset\b",
    r"<object\b",
    r"<embed\b",
    r"<applet\b"
]

DISALLOWED_ATTRIBUTES = [
    r'\bonclick\s*=',
    r'\bonmouseover\s*=',
    r'\bonload\s*=',
    r'\bonerror\s*=',
    r'\bstyle\s*=\s*["\'][^"\']*["\']',  # inline style attributes forbidden in AMP
]


def validate_amp_html(html_content: str, require_disclaimer: bool = True) -> Tuple[bool, List[str]]:
    """
    Validates AMP HTML for Blogger post body content.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    # Check for disallowed tags
    for tag_pattern in DISALLOWED_TAGS:
        matches = re.findall(tag_pattern, html_content, re.IGNORECASE)
        if matches:
            errors.append(f"Disallowed tag detected: {matches[0]} (use AMP component equivalent instead)")

    # Check for disallowed attributes (inline JS, inline style)
    for attr_pattern in DISALLOWED_ATTRIBUTES:
        matches = re.findall(attr_pattern, html_content, re.IGNORECASE)
        if matches:
            errors.append(f"Disallowed inline attribute found: '{matches[0]}'")

    # Validate <amp-img> has required layout attributes
    amp_img_pattern = re.compile(r"<amp-img\b([^>]*)>", re.IGNORECASE)
    for match in amp_img_pattern.finditer(html_content):
        attrs = match.group(1)
        if "width=" not in attrs or "height=" not in attrs:
            errors.append(f"<amp-img> missing required width/height attribute: {match.group(0)}")
        if "layout=" not in attrs:
            errors.append(f"<amp-img> should specify layout attribute (e.g. layout=\"responsive\"): {match.group(0)}")
        if "alt=" not in attrs:
            errors.append(f"<amp-img> missing accessibility alt attribute: {match.group(0)}")

    # Verify style amp-custom size if present
    style_match = re.search(r"<style amp-custom>(.*?)</style>", html_content, re.DOTALL | re.IGNORECASE)
    if style_match:
        css = style_match.group(1)
        if "!important" in css:
            errors.append("AMP CSS contains forbidden '!important' directive")
        if len(css.encode("utf-8")) > 75000:
            errors.append("AMP CSS exceeds maximum permitted size of 75KB")

    # Verify non-sponsorship disclaimer presence
    if require_disclaimer:
        clean_content = " ".join(html_content.split())
        clean_disclaimer = " ".join(MANDATORY_DISCLAIMER_SNIPPET.split())
        if clean_disclaimer not in clean_content:
            errors.append("Mandatory non-sponsorship disclaimer is missing or altered")

    return (len(errors) == 0, errors)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python3 amp_validator.py <path-to-html-file>")
        sys.exit(0 if (len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help")) else 1)

    filepath = sys.argv[1]
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error opening file {filepath}: {e}")
        sys.exit(1)

    is_valid, errors = validate_amp_html(content)
    if is_valid:
        print(f"AMP HTML Validation PASSED: {filepath}")
        sys.exit(0)
    else:
        print(f"AMP HTML Validation FAILED for {filepath} with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
