#!/usr/bin/env python3
"""
AMP Validator Script for IDE Guide Blog Posts.
Validates that generated HTML files adhere to AMP (Accelerated Mobile Pages) standards
and include mandatory requirements such as non-sponsorship disclaimers.
"""

import re
import sys
from typing import List, Tuple

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

REQUIRED_TAGS = [
    r"<html\s+[^>]*amp[^>]*>",
    r'<meta\s+charset=["\']utf-8["\']',
    r'<script\s+async\s+src=["\']https://cdn\.ampproject\.org/v0\.js["\']>',
    r'<meta\s+name=["\']viewport["\']',
    r"<style\s+amp-boilerplate>",
    r"<style\s+amp-custom>",
]

DISALLOWED_TAGS = [
    r"<img\s+",
    r"<iframe\s+",
    r"<video\s+",
    r"<audio\s+",
    r'style=["\'][^"\']*["\']',  # Inline style attributes
]


def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    errors = []

    # Check required tags
    for tag_pattern in REQUIRED_TAGS:
        if not re.search(tag_pattern, html_content, re.IGNORECASE):
            errors.append(f"Missing required AMP tag matching pattern: {tag_pattern}")

    # Check disallowed tags
    for tag_pattern in DISALLOWED_TAGS:
        matches = re.findall(tag_pattern, html_content, re.IGNORECASE)
        if matches:
            errors.append(f"Found disallowed HTML construct matching pattern '{tag_pattern}': {matches[:3]}")

    # Check disclaimer
    if DISCLAIMER_TEXT not in html_content:
        errors.append("Missing required non-sponsorship disclaimer text.")

    return (len(errors) == 0, errors)


def validate_file(filepath: str) -> bool:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        is_valid, errors = validate_amp_html(content)
        if is_valid:
            print(f"[SUCCESS] {filepath} is valid AMP HTML.")
            return True
        else:
            print(f"[FAILURE] {filepath} failed AMP validation:")
            for err in errors:
                print(f"  - {err}")
            return False
    except Exception as e:
        print(f"[ERROR] Could not read file {filepath}: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 amp_validator.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    success = validate_file(file_path)
    sys.exit(0 if success else 1)
