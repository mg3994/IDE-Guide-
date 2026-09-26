#!/usr/bin/env python3
"""
AMP Validator Utility for IDE Guide Blogger Posts.
Checks HTML files for AMP specification compliance and required disclaimers.
"""

import sys
import re
from pathlib import Path

REQUIRED_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

def validate_amp_html(html_content: str) -> tuple[bool, list[str]]:
    errors = []

    # 1. Check for standard <img> tag (Must use <amp-img>)
    if re.search(r'<img\s+[^>]*>', html_content, re.IGNORECASE):
        errors.append("Forbidden standard HTML <img> tag found. Use <amp-img> instead.")

    # 2. Check <amp-img> tags for required attributes width, height, layout
    amp_imgs = re.findall(r'<amp-img\s+[^>]*>', html_content, re.IGNORECASE)
    for tag in amp_imgs:
        if 'width=' not in tag or 'height=' not in tag:
            errors.append(f"<amp-img> tag missing required width or height attribute: {tag}")
        if 'layout=' not in tag:
            errors.append(f"<amp-img> tag missing layout attribute: {tag}")

    # 3. Check for inline style="..." attributes (Forbidden in AMP HTML)
    if re.search(r'\sstyle=["\'][^"\']*["\']', html_content, re.IGNORECASE):
        errors.append("Forbidden inline style attribute found. Use <style amp-custom> CSS rules instead.")

    # 4. Check for forbidden inline JavaScript (<script> tags without amp src)
    scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', html_content, re.DOTALL | re.IGNORECASE)
    for script_match in re.finditer(r'<script\b([^>]*)>', html_content, re.IGNORECASE):
        attrs = script_match.group(1)
        if 'ampproject.org' not in attrs:
            errors.append(f"Forbidden inline or custom <script> tag found: {script_match.group(0)}")

    # 5. Check for Non-Sponsorship Disclaimer
    if REQUIRED_DISCLAIMER not in html_content:
        errors.append("Mandatory Non-Sponsorship Disclaimer missing or modified.")

    is_valid = len(errors) == 0
    return is_valid, errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <path_to_html_file>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    content = file_path.read_text(encoding='utf-8')
    is_valid, errors = validate_amp_html(content)

    if is_valid:
        print(f"SUCCESS: '{file_path}' is valid AMP HTML for IDE Guide Blogger publication.")
        sys.exit(0)
    else:
        print(f"VALIDATION ERROR in '{file_path}':")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
