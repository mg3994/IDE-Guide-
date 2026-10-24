#!/usr/bin/env python3
"""
AMP Validator module for verifying AMP HTML post compliance for Blogger.
Checks for mandatory tags, scripts, boilerplate, prohibited elements, and disclaimers.
"""

import re
from typing import List, Tuple

REQUIRED_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)


def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    """
    Validates HTML string against core AMP requirements for Blogger posts.

    Returns:
        (is_valid: bool, errors: List[str])
    """
    errors = []

    # 1. Doctype check
    if not re.search(r'<!doctype\s+html>', html_content, re.IGNORECASE):
        errors.append("Missing <!doctype html> declaration.")

    # 2. <html ⚡> or <html amp> tag check
    if not re.search(r'<html\s+[^>]*\b(⚡|amp)\b[^>]*>', html_content, re.IGNORECASE):
        errors.append("Missing ⚡ or amp attribute in <html> tag.")

    # 3. <head> and <body> check
    if "<head>" not in html_content.lower() or "</head>" not in html_content.lower():
        errors.append("Missing <head> tag structure.")
    if "<body>" not in html_content.lower() or "</body>" not in html_content.lower():
        errors.append("Missing <body> tag structure.")

    # 4. Meta charset utf-8
    if not re.search(r'<meta\s+charset=["\']utf-8["\']\s*/?>', html_content, re.IGNORECASE):
        errors.append("Missing <meta charset=\"utf-8\"> tag.")

    # 5. AMP JS runtime script
    if 'src="https://cdn.ampproject.org/v0.js"' not in html_content and "src='https://cdn.ampproject.org/v0.js'" not in html_content:
        errors.append("Missing AMP JS runtime CDN script tag.")

    # 6. Canonical link
    if not re.search(r'<link\s+rel=["\']canonical["\']', html_content, re.IGNORECASE):
        errors.append("Missing <link rel=\"canonical\"> tag.")

    # 7. Viewport meta tag
    if 'name="viewport"' not in html_content and "name='viewport'" not in html_content:
        errors.append("Missing viewport <meta> tag.")

    # 8. AMP Boilerplate style
    if 'amp-boilerplate' not in html_content:
        errors.append("Missing <style amp-boilerplate> tag.")

    # 9. No forbidden custom javascript script tags (excluding v0.js and amp extensions)
    script_tags = re.findall(r'<script\b[^>]*>(.*?)</script>', html_content, re.DOTALL | re.IGNORECASE)
    for tag in re.findall(r'<script\b[^>]*>', html_content, re.IGNORECASE):
        if 'cdn.ampproject.org' not in tag and 'type="application/ld+json"' not in tag and "type='application/ld+json'" not in tag:
            errors.append(f"Forbidden <script> tag found: {tag}")

    # 10. Check for plain <img> tags (must use <amp-img>)
    if re.search(r'<img\s+[^>]*>', html_content, re.IGNORECASE):
        errors.append("Prohibited <img> tag found; AMP requires <amp-img>.")

    # 11. Check inline style attributes (disallowed in AMP)
    if re.search(r'<[a-zA-Z0-9]+\s+[^>]*style=["\'][^"\'"]*["\']', html_content, re.IGNORECASE):
        errors.append("Inline style attribute detected; disallowed in AMP (use <style amp-custom>).")

    # 12. Non-sponsorship disclaimer check
    if REQUIRED_DISCLAIMER not in html_content:
        errors.append("Missing mandatory non-sponsorship disclaimer text.")

    return len(errors) == 0, errors


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        valid, errs = validate_amp_html(content)
        if valid:
            print(f"✅ {filepath} is valid AMP HTML.")
        else:
            print(f"❌ {filepath} failed AMP HTML validation:")
            for e in errs:
                print(f"  - {e}")
            sys.exit(1)
    else:
        print("Usage: python3 amp_validator.py <file.html>")
