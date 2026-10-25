#!/usr/bin/env python3
"""
AMP HTML Validator script for Blogger Posts.
Validates required AMP boilerplate tags, style constraints, amp-img tags, and disclaimer presence.
"""

import re
import sys
from typing import List, Tuple

NON_SPONSORSHIP_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    """
    Validates AMP HTML string against required specifications for Blogger posts.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    # 1. DOCTYPE check
    if not re.search(r'<!doctype\s+html>', html_content, re.IGNORECASE):
        errors.append("Missing <!doctype html> declaration.")

    # 2. <html ⚡> or <html amp> check
    if not re.search(r'<html\s+[^>]*(⚡|\bamp\b)[^>]*>', html_content, re.IGNORECASE):
        errors.append("Missing ⚡ or amp attribute on <html> tag.")

    # 3. AMP JS runtime check
    if not re.search(r'<script\s+async\s+src="https://cdn\.ampproject\.org/v0\.js"></script>', html_content, re.IGNORECASE):
        errors.append("Missing required AMP runtime script: <script async src=\"https://cdn.ampproject.org/v0.js\"></script>")

    # 4. Meta viewport check
    if not re.search(r'<meta\s+name="viewport"\s+content="[^"]*width=device-width[^"]*"[^>]*>', html_content, re.IGNORECASE):
        errors.append("Missing or invalid <meta name=\"viewport\"> tag.")

    # 5. Canonical link check
    if not re.search(r'<link\s+rel="canonical"\s+href="[^"]+"[^>]*>', html_content, re.IGNORECASE):
        errors.append("Missing <link rel=\"canonical\"> tag.")

    # 6. AMP Boilerplate CSS check
    if "amp-boilerplate" not in html_content:
        errors.append("Missing required AMP boilerplate CSS block (<style amp-boilerplate>).")

    # 7. Disallow standard <img> tags (must use <amp-img>)
    if re.search(r'<img\s+', html_content, re.IGNORECASE):
        errors.append("Standard <img> tag found. AMP HTML requires <amp-img> instead.")

    # 8. Check for disallowed inline style attributes on tags
    if re.search(r'<\w+[^>]*\bstyle="[^"]*"[^>]*>', html_content, re.IGNORECASE):
        errors.append("Inline style attribute found. Custom CSS must be placed in <style amp-custom>.")

    # 9. Verify <style amp-custom> tag presence and size limit (75KB max)
    custom_style_match = re.search(r'<style\s+amp-custom\b[^>]*>(.*?)</style>', html_content, re.DOTALL | re.IGNORECASE)
    if custom_style_match:
        css_content = custom_style_match.group(1)
        if len(css_content.encode('utf-8')) > 75000:
            errors.append(f"Custom CSS in <style amp-custom> exceeds 75KB limit ({len(css_content.encode('utf-8'))} bytes).")

    # 10. Non-sponsorship disclaimer check
    if "Disclaimer:" not in html_content or "not sponsored" not in html_content.lower():
        errors.append("Missing required non-sponsorship disclaimer.")

    return (len(errors) == 0, errors)


def validate_file(filepath: str) -> bool:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        is_valid, errors = validate_amp_html(content)
        if is_valid:
            print(f"✅ {filepath}: Valid AMP HTML.")
            return True
        else:
            print(f"❌ {filepath}: AMP Validation Failed:")
            for err in errors:
                print(f"  - {err}")
            return False
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <path_to_amp_file.html>")
        sys.exit(1)

    file_path = sys.argv[1]
    success = validate_file(file_path)
    sys.exit(0 if success else 1)
