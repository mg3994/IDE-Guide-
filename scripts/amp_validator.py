#!/usr/bin/env python3
"""
AMP HTML & Compliance Validator for IDE Guide Blog Posts.
Ensures generated HTML conforms to AMP rules for Blogger and contains mandatory non-sponsorship disclaimers.
"""

import sys
import re

REQUIRED_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

FORBIDDEN_TAGS = ['<img ', '<video ', '<picture ']
FORBIDDEN_ATTRIBUTES = [' style=']


def validate_amp_html(html_content: str) -> tuple[bool, list[str]]:
    """
    Validates AMP HTML string content for Blogger requirements.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    # 1. Check for forbidden tags (<img ...> should be <amp-img ...>)
    for tag in FORBIDDEN_TAGS:
        if tag in html_content.lower():
            errors.append(f"Forbidden standard tag '{tag.strip()}' found. Use corresponding <amp-*> component.")

    # 2. Check for inline style attributes
    for attr in FORBIDDEN_ATTRIBUTES:
        if attr in html_content.lower():
            errors.append(f"Forbidden inline attribute '{attr.strip()}' found. Use <style amp-custom> instead.")

    # 3. Check for amp-img layout and dimensions if amp-img present
    if '<amp-img' in html_content.lower():
        if 'width=' not in html_content.lower() or 'height=' not in html_content.lower():
            errors.append("<amp-img> tag missing required width or height attributes.")

    # 4. Check for mandatory non-sponsorship disclaimer
    # Normalize whitespaces for exact disclaimer comparison
    normalized_content = " ".join(html_content.split())
    normalized_disclaimer = " ".join(REQUIRED_DISCLAIMER.split())
    if normalized_disclaimer not in normalized_content:
        errors.append("Mandatory non-sponsorship disclaimer missing or modified.")

    return len(errors) == 0, errors


def validate_file(filepath: str) -> bool:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        is_valid, errors = validate_amp_html(content)
        if is_valid:
            print(f"✅ {filepath} passed AMP HTML & compliance validation.")
            return True
        else:
            print(f"❌ {filepath} failed validation:")
            for err in errors:
                print(f"  - {err}")
            return False
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 amp_validator.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    success = validate_file(file_path)
    sys.exit(0 if success else 1)
