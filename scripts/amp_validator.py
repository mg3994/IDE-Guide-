#!/usr/bin/env python3
"""
AMP HTML Validator script for IDE Guide Blogger posts.
Checks for required AMP Boilerplate, script tags, amp-img usage, CSS limits, and mandatory disclaimers.
"""

import sys
import re

DISCLAIMER_TEXT = "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."

def validate_amp_html(html_content: str) -> tuple[bool, list[str]]:
    errors = []

    # 1. Check <html ⚡> or <html amp>
    if not (re.search(r'<html\s+[^>]*\bamp\b[^>]*>', html_content, re.IGNORECASE) or '<html ⚡' in html_content or '<html amp' in html_content):
        errors.append("Missing `<html ⚡>` or `<html amp>` tag.")

    # 2. Check AMP runtime script
    if 'https://cdn.ampproject.org/v0.js' not in html_content:
        errors.append("Missing AMP runtime script `<script async src=\"https://cdn.ampproject.org/v0.js\"></script>`.")

    # 3. Check AMP boilerplate CSS
    if 'amp-boilerplate' not in html_content:
        errors.append("Missing `<style amp-boilerplate>` tag.")

    # 4. Check custom CSS tag
    if '<style amp-custom>' not in html_content:
        errors.append("Missing `<style amp-custom>` block.")

    # 5. Ensure no raw <img> tags (must use <amp-img>)
    img_matches = re.findall(r'<img\s+[^>]*>', html_content, re.IGNORECASE)
    if img_matches:
        errors.append(f"Disallowed <img> tag found ({len(img_matches)} occurrence(s)). Must use <amp-img> instead.")

    # 6. Ensure no forbidden inline style="..." attributes on non-AMP tags
    inline_styles = re.findall(r'<[a-zA-Z0-9]+[^>]*\bstyle\s*=\s*["\'][^"\']*["\'][^>]*>', html_content)
    if inline_styles:
        errors.append(f"Inline style attributes found ({len(inline_styles)} occurrence(s)). Inline style attributes are forbidden in AMP HTML.")

    # 7. Check for non-sponsorship disclaimer
    if DISCLAIMER_TEXT not in html_content:
        errors.append("Missing mandatory non-sponsorship disclaimer text.")

    is_valid = len(errors) == 0
    return is_valid, errors


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 amp_validator.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        sys.exit(1)

    valid, errors = validate_amp_html(content)
    if valid:
        print(f"SUCCESS: {filepath} is valid AMP HTML.")
        sys.exit(0)
    else:
        print(f"FAILED: {filepath} contains AMP validation errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
