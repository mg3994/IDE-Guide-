#!/usr/bin/env python3
"""
AMP HTML Validator for IDE Guide Blogger Posts.
Ensures AMP HTML compliance and non-sponsorship disclaimer presence.
"""

import sys
import re

REQUIRED_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

def validate_amp_html(html_content: str) -> tuple[bool, list[str]]:
    errors = []

    # Check boilerplate requirements
    if not re.search(r"<!doctype\s+html>", html_content, re.IGNORECASE):
        errors.append("Missing <!doctype html>")

    if not re.search(r"<html\s+([^>]*\s+)?(⚡|amp)(\s+|>)", html_content, re.IGNORECASE):
        errors.append("Missing ⚡ or amp attribute on <html> tag")

    if '<meta charset="utf-8"' not in html_content and '<meta charset="UTF-8"' not in html_content:
        errors.append("Missing <meta charset=\"utf-8\">")

    if 'https://cdn.ampproject.org/v0.js' not in html_content:
        errors.append("Missing AMP runtime script (v0.js)")

    if '<style amp-boilerplate' not in html_content:
        errors.append("Missing <style amp-boilerplate>")

    if '<style amp-custom' not in html_content:
        errors.append("Missing <style amp-custom>")

    # Check for forbidden <img> tags
    if re.search(r"<img\b", html_content, re.IGNORECASE):
        errors.append("Forbidden <img> tag found. Use <amp-img> instead.")

    # Check for inline style attributes
    if re.search(r'\bstyle\s*=\s*["\']', html_content, re.IGNORECASE):
        errors.append("Forbidden inline style attribute found. All CSS must be in <style amp-custom>.")

    # Check for unapproved <script> tags
    scripts = re.findall(r'<script\b[^>]*>', html_content, re.IGNORECASE)
    for script in scripts:
        if 'cdn.ampproject.org' not in script and 'type="application/ld+json"' not in script:
            errors.append(f"Forbidden <script> tag found: {script}")

    # Check CSS size limit in <style amp-custom>
    custom_css_match = re.search(r'<style amp-custom>(.*?)</style>', html_content, re.DOTALL)
    if custom_css_match:
        css_size = len(custom_css_match.group(1).encode('utf-8'))
        if css_size > 75 * 1024:
            errors.append(f"Custom CSS size exceeds 75KB limit ({css_size} bytes)")

    # Check non-sponsorship disclaimer
    if REQUIRED_DISCLAIMER not in html_content:
        errors.append("Missing or incorrect non-sponsorship disclaimer.")

    return len(errors) == 0, errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <file_path>")
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
        print(f"✅ AMP Validation Passed for {filepath}")
        sys.exit(0)
    else:
        print(f"❌ AMP Validation Failed for {filepath}:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
