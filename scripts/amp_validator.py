#!/usr/bin/env python3
"""
AMP HTML Validator for IDE Guide Blogger Posts
Validates that generated HTML content follows AMP HTML requirements for Blogger.
"""

import sys
import re

REQUIRED_DISCLAIMER = (
    "IDE Guide is an independent technical publication. This content is not sponsored, "
    "endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

def validate_amp_html(html_content: str) -> tuple[bool, list[str]]:
    errors = []

    # Check 1: Doctype
    if not re.search(r"<!doctype\s+html>", html_content, re.IGNORECASE):
        errors.append("Missing or invalid <!doctype html> declaration.")

    # Check 2: <html ⚡> or <html amp> (using re.UNICODE / re.IGNORECASE)
    if not (re.search(r"<html\s+[^>]*\bamp\b[^>]*>", html_content, re.IGNORECASE) or
            re.search(r"<html\s+[^>]*⚡[^>]*>", html_content, re.IGNORECASE)):
        errors.append("HTML root element must include 'amp' or '⚡' attribute.")

    # Check 3: JS Library
    if "https://cdn.ampproject.org/v0.js" not in html_content:
        errors.append("Missing required AMP script tag (https://cdn.ampproject.org/v0.js).")

    # Check 4: Viewport
    if not re.search(r'<meta\s+name=["\']viewport["\']', html_content, re.IGNORECASE):
        errors.append("Missing <meta name=\"viewport\"> tag.")

    # Check 5: Canonical Link
    if not re.search(r'<link\s+rel=["\']canonical["\']', html_content, re.IGNORECASE):
        errors.append("Missing <link rel=\"canonical\"> tag.")

    # Check 6: AMP Boilerplate
    if "amp-boilerplate" not in html_content:
        errors.append("Missing AMP boilerplate style tag.")

    # Check 7: Custom Style tag
    if "<style amp-custom>" not in html_content:
        errors.append("Missing <style amp-custom> tag.")

    # Check 8: Disallowed tags (e.g. <img> instead of <amp-img>)
    if re.search(r"<img\s+", html_content, re.IGNORECASE):
        errors.append("Disallowed <img> tag found. Use <amp-img> instead for AMP compatibility.")

    # Check 9: Inline styles (disallowed style="..." attribute)
    if re.search(r'\sstyle=["\'][^"\']*["\']', html_content, re.IGNORECASE):
        errors.append("Inline style attribute found. Inline styles are disallowed in AMP HTML.")

    # Check 10: Non-sponsorship disclaimer presence
    if REQUIRED_DISCLAIMER not in html_content:
        errors.append("Missing required non-sponsorship disclaimer text.")

    return len(errors) == 0, errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 amp_validator.py <file.html>")
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        sys.exit(1)

    is_valid, errors = validate_amp_html(content)
    if is_valid:
        print(f"SUCCESS: {filepath} is valid AMP HTML for Blogger.")
        sys.exit(0)
    else:
        print(f"VALIDATION FAILED for {filepath}:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
