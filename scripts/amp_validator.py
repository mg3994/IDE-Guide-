#!/usr/bin/env python3
"""
AMP HTML Validator for Blogger Posts (IDE Guide)
Validates whether an HTML document adheres to mandatory AMP HTML specs and IDE Guide rules.
"""

import sys
import re
from typing import List, Tuple

REQUIRED_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    errors = []

    # 1. Check root html tag for ⚡ or amp attribute
    if not re.search(r'<html\b[^>]*?\bamp\b', html_content, re.IGNORECASE) and not re.search(r'<html\b[^>]*?⚡', html_content, re.IGNORECASE):
        errors.append("Missing '<html ⚡>' or '<html amp>' root tag.")

    # 2. Check charset meta tag
    if not re.search(r'<meta\s+charset=["\']?utf-8["\']?', html_content, re.IGNORECASE):
        errors.append("Missing '<meta charset=\"utf-8\">' tag.")

    # 3. Check AMP JS runtime
    if 'src="https://cdn.ampproject.org/v0.js"' not in html_content:
        errors.append("Missing AMP runtime script '<script async src=\"https://cdn.ampproject.org/v0.js\"></script>'.")

    # 4. Check canonical link
    if not re.search(r'<link\s+rel=["\']canonical["\']', html_content, re.IGNORECASE):
        errors.append("Missing '<link rel=\"canonical\" ...>' tag.")

    # 5. Check viewport tag
    if not re.search(r'<meta\s+name=["\']viewport["\']', html_content, re.IGNORECASE):
        errors.append("Missing '<meta name=\"viewport\" ...>' tag.")

    # 6. Check amp-boilerplate
    if '<style amp-boilerplate>' not in html_content:
        errors.append("Missing '<style amp-boilerplate>' element.")

    # 7. Check amp-custom
    if '<style amp-custom>' not in html_content:
        errors.append("Missing '<style amp-custom>' element.")

    # 8. Check for forbidden standard img tags outside noscript
    # Strip <noscript> blocks for img check
    content_no_noscript = re.sub(r'<noscript>.*?</noscript>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    if re.search(r'<img\s+[^>]*>', content_no_noscript, re.IGNORECASE):
        errors.append("Found standard <img> tag. Use <amp-img> instead for AMP compatibility.")

    # 9. Check for inline style attributes on standard HTML elements
    # Matches style="..." not inside <style> tags
    content_no_style_tags = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    if re.search(r'<\w+\s+[^>]*?\bstyle=["\'][^"\']*["\']', content_no_style_tags, re.IGNORECASE):
        errors.append("Inline style attribute found on tag. Inline styles are disallowed in AMP HTML.")

    # 10. Check non-sponsorship disclaimer
    # Normalize whitespaces for checking disclaimer
    normalized_content = " ".join(html_content.split())
    normalized_disclaimer = " ".join(REQUIRED_DISCLAIMER.split())
    if normalized_disclaimer not in normalized_content:
        errors.append("Missing required non-sponsorship disclaimer text.")

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
        print(f"Error reading file {filepath}: {e}")
        sys.exit(1)

    is_valid, errors = validate_amp_html(content)
    if is_valid:
        print(f"SUCCESS: {filepath} is valid AMP HTML for Blogger!")
        sys.exit(0)
    else:
        print(f"FAILURE: {filepath} failed AMP HTML validation:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
