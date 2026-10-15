#!/usr/bin/env python3
"""
AMP Validator Utility for IDE Guide Blogger Content.
Validates AMP HTML content against standard Blogger AMP rules and verifies presence of non-sponsorship disclaimers.
"""

import re
import sys
from typing import List, Tuple

MANDATORY_DISCLAIMER_PHRASE = "IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."

DISALLOWED_TAGS = ["<img ", "<video ", "<audio ", "<iframe "]

def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    """
    Validates AMP HTML string for disallowed tags, required AMP components/structure, and mandatory disclaimer.
    """
    errors = []

    # Check for disallowed tags
    for tag in DISALLOWED_TAGS:
        if tag.lower() in html_content.lower():
            errors.append(f"Disallowed tag found: '{tag.strip()}'. Use appropriate <amp-*> tags instead.")

    # Check for disallowed inline scripts (script tags without type=application/ld+json or custom-element)
    script_matches = re.findall(r'<script\b[^>]*>(.*?)</script>', html_content, re.IGNORECASE | re.DOTALL)
    for match in script_matches:
        if "type=\"application/ld+json\"" not in match and "custom-element" not in match:
            # Let's check tag header directly
            pass

    raw_script_tags = re.findall(r'<script\b[^>]*>', html_content, re.IGNORECASE)
    for script_tag in raw_script_tags:
        if 'type="application/ld+json"' not in script_tag and 'custom-element' not in script_tag and 'src=' in script_tag:
            if not any(amp_lib in script_tag for amp_lib in ['cdn.ampproject.org']):
                errors.append(f"Non-AMP script tag found: {script_tag}")

    # Check for mandatory non-sponsorship disclaimer
    if MANDATORY_DISCLAIMER_PHRASE not in html_content:
        errors.append("Missing or modified mandatory non-sponsorship disclaimer.")

    # Check for basic required sections
    required_sections = ["<h2>Overview</h2>", "<h2>Pros & Cons</h2>", "<h2>Pricing Model", "<h2>Verdict"]
    for section in required_sections:
        if section.lower() not in html_content.lower():
            errors.append(f"Missing recommended post section matching header: '{section}'")

    is_valid = len(errors) == 0
    return is_valid, errors

def validate_file(filepath: str) -> bool:
    """Reads a file and validates its AMP content."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        is_valid, errors = validate_amp_html(content)
        if is_valid:
            print(f"SUCCESS: '{filepath}' is valid AMP HTML for Blogger.")
            return True
        else:
            print(f"FAILED validation for '{filepath}':")
            for err in errors:
                print(f"  - {err}")
            return False
    except Exception as e:
        print(f"ERROR reading '{filepath}': {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <path_to_html_file>")
        sys.exit(1)
    success = validate_file(sys.argv[1])
    sys.exit(0 if success else 1)
