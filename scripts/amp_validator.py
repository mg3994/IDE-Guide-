#!/usr/bin/env python3
"""
AMP HTML & Disclaimer Validator for IDE Guide Blogger Posts.
Validates AMP compliance and presence of mandatory non-sponsorship disclaimer.
"""

import sys
import re
from pathlib import Path

MANDATORY_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

def validate_amp_html(html_content: str) -> tuple[bool, list[str]]:
    """
    Validates AMP HTML string. Returns (is_valid, list_of_errors).
    """
    errors = []

    # 1. Check for AMP html tag (<html ⚡ ...> or <html amp ...>)
    if not re.search(r'<html(?:\s+[^>]*)?\s+(⚡|amp)(?:[\s>])', html_content, re.IGNORECASE):
        errors.append("Missing <html ⚡> or <html amp> declaration.")

    # 2. Check for charset
    if not re.search(r'<meta\s+charset=["\']utf-8["\']', html_content, re.IGNORECASE):
        errors.append("Missing <meta charset=\"utf-8\"> tag.")

    # 3. Check for AMP runtime script
    if not re.search(r'<script\s+async\s+src=["\']https://cdn\.ampproject\.org/v0\.js["\']></script>', html_content):
        errors.append("Missing AMP runtime script (v0.js).")

    # 4. Check for forbidden standard <img> tags
    if re.search(r'<img\b[^>]*>', html_content, re.IGNORECASE):
        errors.append("Forbidden standard <img> tag found. Use <amp-img> instead.")

    # 5. Check for inline style attributes
    if re.search(r'\bstyle=["\'][^"\'`]*["\']', html_content, re.IGNORECASE):
        errors.append("Forbidden inline style attribute found. Custom CSS must be inside <style amp-custom>.")

    # 6. Check for non-AMP inline script tags
    scripts = re.findall(r'<script\b([^>]*)>(.*?)</script>', html_content, re.IGNORECASE | re.DOTALL)
    for attrs, _content in scripts:
        if 'src="https://cdn.ampproject.org' in attrs or "src='https://cdn.ampproject.org" in attrs:
            continue
        if 'type="application/json"' in attrs or 'type="application/ld+json"' in attrs:
            continue
        errors.append(f"Forbidden inline or custom JavaScript tag found: <script {attrs}>")

    # 7. Check for mandatory disclaimer
    # Normalize spaces in content and disclaimer for checking
    normalized_content = " ".join(html_content.split())
    normalized_disclaimer = " ".join(MANDATORY_DISCLAIMER.split())
    if normalized_disclaimer not in normalized_content:
        errors.append("Missing or modified mandatory non-sponsorship disclaimer.")

    return (len(errors) == 0, errors)


def validate_file(filepath: str) -> bool:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File '{filepath}' does not exist.")
        return False

    content = path.read_text(encoding="utf-8")
    is_valid, errors = validate_amp_html(content)

    if is_valid:
        print(f"✅ {filepath} is valid AMP HTML with mandatory disclaimer.")
        return True
    else:
        print(f"❌ {filepath} failed AMP validation with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    success = validate_file(file_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
