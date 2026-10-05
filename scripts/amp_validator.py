#!/usr/bin/env python3
"""
AMP HTML Validator for Blogger posts (IDE Guide).
Validates HTML content against strict Blogger AMP requirements.
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


def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    """
    Validates AMP HTML string for compliance with Blogger AMP rules and IDE Guide guidelines.
    Returns (is_valid, errors).
    """
    errors: List[str] = []

    # 1. Check Doctype
    if not re.search(r"<!doctype\s+html>", html_content, re.IGNORECASE):
        errors.append("Missing or invalid <!doctype html> declaration.")

    # 2. Check <html ⚡> or <html amp>
    if not re.search(r"<html\s+[^>]*?\b(amp)\b[^>]*>", html_content, re.IGNORECASE) and not re.search(r"<html\s+[^>]*?⚡[^>]*>", html_content, re.IGNORECASE):
        errors.append("Missing '⚡' or 'amp' attribute on <html> element.")

    # 3. Check <meta charset="utf-8">
    if not re.search(r'<meta\s+charset=["\']utf-8["\']\s*/?>', html_content, re.IGNORECASE):
        errors.append("Missing <meta charset=\"utf-8\"> tag.")

    # 4. Check Viewport
    if not re.search(r'<meta\s+name=["\']viewport["\'][^>]*content=["\'][^"\']*width=device-width[^"\']*["\']', html_content, re.IGNORECASE):
        errors.append("Missing valid AMP <meta name=\"viewport\"> tag.")

    # 5. Check Canonical link
    if not re.search(r'<link\s+rel=["\']canonical["\'][^>]*href=["\'][^"\']+["\']', html_content, re.IGNORECASE):
        errors.append("Missing valid <link rel=\"canonical\" href=\"...\"> tag.")

    # 6. Check AMP Runtime script
    if "https://cdn.ampproject.org/v0.js" not in html_content:
        errors.append("Missing AMP runtime script (https://cdn.ampproject.org/v0.js).")

    # 7. Check AMP boilerplate
    if "style amp-boilerplate" not in html_content:
        errors.append("Missing <style amp-boilerplate> tag.")

    # 8. Check <style amp-custom>
    if "<style amp-custom>" not in html_content:
        errors.append("Missing <style amp-custom> tag for inline CSS.")

    # 9. Forbidden <img> tags
    if re.search(r"<img\b[^>]*>", html_content, re.IGNORECASE):
        errors.append("Forbidden <img> tag found. Use <amp-img> instead.")

    # 10. Forbidden unapproved <script> tags
    for script_tag in re.finditer(r"<script\b([^>]*)>", html_content, re.IGNORECASE):
        attrs = script_tag.group(1)
        if "src=" in attrs and "cdn.ampproject.org" not in attrs:
            errors.append(f"Forbidden external script detected: {script_tag.group(0)}")
        elif "src=" not in attrs and "application/json" not in attrs and "application/ld+json" not in attrs:
            errors.append("Forbidden inline custom JavaScript detected.")

    # 11. Check Non-sponsorship disclaimer
    if DISCLAIMER_TEXT not in html_content:
        errors.append("Missing mandatory non-sponsorship disclaimer in HTML content.")

    return (len(errors) == 0, errors)


def validate_file(filepath: str) -> bool:
    """Reads file and validates its AMP HTML structure."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        is_valid, errors = validate_amp_html(content)
        if is_valid:
            print(f"✓ {filepath} is valid Blogger AMP HTML!")
            return True
        else:
            print(f"✗ {filepath} failed AMP HTML validation:")
            for err in errors:
                print(f"  - {err}")
            return False
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        success = validate_file(sys.argv[1])
        sys.exit(0 if success else 1)
    else:
        print("Usage: python3 scripts/amp_validator.py <path_to_html_file>")
        sys.exit(1)
