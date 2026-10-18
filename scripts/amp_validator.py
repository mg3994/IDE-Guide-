#!/usr/bin/env python3
"""
AMP HTML Validator for IDE Guide Blogger Posts.
Validates AMP HTML files for compliance with AMP specification rules:
1. <html ⚡> or <html amp> attribute.
2. Mandatory AMP boilerplate script and style tags.
3. Canonical link present.
4. Viewport meta tag present.
5. Absence of forbidden <img> tags (must use <amp-img>).
6. Non-sponsorship disclaimer present.
"""

import sys
import re
from typing import List, Tuple

REQUIRED_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

class AmpValidator:
    def __init__(self, html_content: str):
        self.html = html_content
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        self.errors.clear()
        self.warnings.clear()

        # Check html tag for amp attribute
        if not re.search(r'<html\s+[^>]*\b(amp|⚡)\b[^>]*>', self.html, re.IGNORECASE):
            self.errors.append("Missing <html ⚡> or <html amp> root tag attribute.")

        # Check for required AMP JS script tag
        if not re.search(r'<script\s+async\s+src=["\']https://cdn\.ampproject\.org/v0\.js["\']\s*></script>', self.html):
            self.errors.append("Missing mandatory AMP v0.js script tag: https://cdn.ampproject.org/v0.js")

        # Check for viewport meta tag
        if not re.search(r'<meta\s+name=["\']viewport["\']\s+content=["\'][^"\']*width=device-width[^"\']*["\']', self.html, re.IGNORECASE):
            self.errors.append("Missing or invalid viewport meta tag.")

        # Check for canonical link tag
        if not re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']+["\']', self.html, re.IGNORECASE):
            self.errors.append("Missing canonical link tag (<link rel=\"canonical\" href=\"...\">).")

        # Check for AMP boilerplate style
        if "amp-boilerplate" not in self.html:
            self.errors.append("Missing mandatory <style amp-boilerplate> tag.")

        # Check for forbidden <img> tags
        img_matches = re.findall(r'<img\b[^>]*>', self.html, re.IGNORECASE)
        if img_matches:
            self.errors.append(f"Forbidden <img> tags found ({len(img_matches)} count). Use <amp-img> instead.")

        # Check for <amp-img> layout and dimension attributes
        amp_imgs = re.findall(r'<amp-img\b([^>]*)>', self.html, re.IGNORECASE)
        for idx, img_attrs in enumerate(amp_imgs, 1):
            if "width=" not in img_attrs or "height=" not in img_attrs:
                self.errors.append(f"<amp-img> element #{idx} is missing required width and/or height attributes.")

        # Check for non-sponsorship disclaimer
        if REQUIRED_DISCLAIMER not in self.html:
            self.errors.append("Missing exact required non-sponsorship disclaimer.")

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings


def validate_file(filepath: str) -> bool:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return False

    validator = AmpValidator(content)
    is_valid, errors, warnings = validator.validate()

    if is_valid:
        print(f"✅ SUCCESS: {filepath} is valid AMP HTML.")
        return True
    else:
        print(f"❌ VALIDATION ERROR(S) in {filepath}:")
        for err in errors:
            print(f"  - {err}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <path_to_amp_html_file>")
        sys.exit(1)

    filepath_arg = sys.argv[1]
    success = validate_file(filepath_arg)
    sys.exit(0 if success else 1)
