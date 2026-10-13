#!/usr/bin/env python3
"""
AMP Validator Script for IDE Guide Blog Posts.
Validates HTML string or file against AMP standards for Blogger.
"""

import sys
import re

REQUIRED_DISCLAIMER = "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."

def validate_amp_html(html_content: str) -> tuple[bool, list[str]]:
    """
    Validates AMP HTML content.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    # 1. Check doctype
    if not re.search(r'<!doctype\s+html>', html_content, re.IGNORECASE):
        errors.append("Missing <!doctype html> declaration.")

    # 2. Check <html> or <html ⚡> tag
    if not re.search(r'<html\s+(amp|⚡)[\s>]', html_content, re.IGNORECASE):
        errors.append("Missing <html amp> or <html ⚡> tag.")

    # 3. Check charset utf-8
    if not re.search(r'<meta\s+charset=["\']utf-8["\']', html_content, re.IGNORECASE):
        errors.append("Missing <meta charset=\"utf-8\"> tag.")

    # 4. Check canonical link
    if not re.search(r'<link\s+rel=["\']canonical["\']', html_content, re.IGNORECASE):
        errors.append("Missing <link rel=\"canonical\" href=\"...\"> tag.")

    # 5. Check viewport
    if not re.search(r'<meta\s+name=["\']viewport["\']', html_content, re.IGNORECASE):
        errors.append("Missing <meta name=\"viewport\" ...> tag.")

    # 6. Check AMP runtime script
    if 'https://cdn.ampproject.org/v0.js' not in html_content:
        errors.append("Missing AMP runtime script https://cdn.ampproject.org/v0.js.")

    # 7. Check AMP boilerplate
    if 'amp-boilerplate' not in html_content:
        errors.append("Missing <style amp-boilerplate> tag.")

    # 8. Check custom styles tag
    if 'style amp-custom' not in html_content:
        errors.append("Missing <style amp-custom> tag.")

    # 9. Disallow inline style attributes
    if re.search(r'\sstyle=["\'][^"\']*["\']', html_content, re.IGNORECASE):
        errors.append("Inline style attribute found (prohibited in AMP).")

    # 10. Disallow prohibited tags like <img> without amp-img, <script> outside head
    if re.search(r'<img\s', html_content, re.IGNORECASE):
        errors.append("Standard <img> tag found. Use <amp-img> instead.")

    if re.search(r'<iframe\s', html_content, re.IGNORECASE):
        errors.append("Forbidden <iframe> tag found.")

    # 11. Verify mandatory non-sponsorship disclaimer
    if REQUIRED_DISCLAIMER not in html_content:
        errors.append("Missing mandatory non-sponsorship disclaimer text.")

    is_valid = len(errors) == 0
    return is_valid, errors

def validate_file(filepath: str) -> bool:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        is_valid, errors = validate_amp_html(content)
        if is_valid:
            print(f"✅ SUCCESS: '{filepath}' is valid AMP HTML.")
            return True
        else:
            print(f"❌ ERROR: '{filepath}' failed AMP validation:")
            for err in errors:
                print(f"   - {err}")
            return False
    except Exception as e:
        print(f"❌ ERROR reading file {filepath}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    success = validate_file(file_path)
    sys.exit(0 if success else 1)
