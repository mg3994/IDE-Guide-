#!/usr/bin/env python3
"""
AMP HTML Validator for IDE Guide Blogger Posts
Checks HTML strings or files for compliance with standard AMP rules and IDE Guide publishing guidelines.
"""

import re
import sys
from typing import List, Tuple

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    errors = []

    # 1. Check root html tag for ⚡ or amp attribute
    if not re.search(r'<html\s+[^>]*?\b(⚡|\bamp\b)[^>]*?>', html_content, re.IGNORECASE | re.UNICODE):
        errors.append("Missing '<html ⚡>' or '<html amp>' tag declaration.")

    # 2. Check head & body tags
    if "<head>" not in html_content or "</head>" not in html_content:
        errors.append("Missing <head> or </head> tags.")
    if "<body>" not in html_content or "</body>" not in html_content:
        errors.append("Missing <body> or </body> tags.")

    # 3. Check utf-8 charset
    if not re.search(r'<meta\s+charset=["\']utf-8["\']\s*/?>', html_content, re.IGNORECASE):
        errors.append("Missing '<meta charset=\"utf-8\">'.")

    # 4. Check viewport meta tag
    if not re.search(r'<meta\s+name=["\']viewport["\']', html_content, re.IGNORECASE):
        errors.append("Missing viewport meta tag.")

    # 5. Check AMP v0.js script
    if 'https://cdn.ampproject.org/v0.js' not in html_content:
        errors.append("Missing AMP JS runtime script 'https://cdn.ampproject.org/v0.js'.")

    # 6. Check canonical link
    if not re.search(r'<link\s+rel=["\']canonical["\']', html_content, re.IGNORECASE):
        errors.append("Missing '<link rel=\"canonical\" href=\"...\">' tag.")

    # 7. Check amp-boilerplate style
    if 'style amp-boilerplate' not in html_content:
        errors.append("Missing '<style amp-boilerplate>' tag.")

    # 8. Check for illegal <img> tags
    if re.search(r'<img\s+[^>]*?>', html_content, re.IGNORECASE):
        errors.append("Forbidden <img> tag found. Must use <amp-img> tag instead.")

    # 9. Check for forbidden inline style attributes
    if re.search(r'<\w+\s+[^>]*?\bstyle=["\'][^"\'\>]+["\']', html_content, re.IGNORECASE):
        errors.append("Forbidden inline 'style=\"...\"' attribute found. Use <style amp-custom> instead.")

    # 10. Check amp-custom style size (< 75KB)
    custom_styles = re.findall(r'<style amp-custom>(.*?)</style>', html_content, re.DOTALL)
    for css in custom_styles:
        if len(css.encode('utf-8')) > 75 * 1024:
            errors.append("AMP custom style exceeds 75KB size limit.")

    # 11. Check mandatory disclaimer
    if DISCLAIMER_TEXT not in html_content:
        errors.append("Missing mandatory non-sponsorship disclaimer text.")

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_file(filepath: str) -> bool:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    is_valid, errors = validate_amp_html(content)
    if is_valid:
        print(f"SUCCESS: {filepath} is valid AMP HTML.")
        return True
    else:
        print(f"FAILED: {filepath} has AMP validation errors:")
        for err in errors:
            print(f" - {err}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 amp_validator.py <file.html>")
        sys.exit(1)

    success = validate_file(sys.argv[1])
    sys.exit(0 if success else 1)
