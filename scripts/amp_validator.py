#!/usr/bin/env python3
"""
AMP HTML Validator for IDE Guide Blogger Posts.
Ensures that generated blog post HTML meets basic AMP (Accelerated Mobile Pages) requirements
and contains the mandatory non-sponsorship disclaimer.
"""

import sys
import re
import argparse

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

def validate_amp_html(html_content: str) -> tuple[bool, list[str]]:
    errors = []

    # Check AMP root html tag (matches <html amp ...> or <html ⚡ ...>)
    if not (re.search(r"<html\b[^>]*\bamp\b[^>]*>", html_content, re.IGNORECASE) or re.search(r"<html\b[^>]*⚡[^>]*>", html_content, re.IGNORECASE)):
        errors.append("Missing <html ⚡> or <html amp> root element.")

    # Check utf-8 charset
    if not re.search(r'<meta\s+charset=["\']utf-8["\']\s*/?>', html_content, re.IGNORECASE):
        errors.append("Missing <meta charset=\"utf-8\"> tag.")

    # Check AMP v0 runtime script
    if not re.search(r'<script\s+async\s+src=["\']https://cdn\.ampproject\.org/v0\.js["\']></script>', html_content, re.IGNORECASE):
        errors.append("Missing AMP v0 JS runtime script (<script async src=\"https://cdn.ampproject.org/v0.js\"></script>).")

    # Check canonical link
    if not re.search(r'<link\s+rel=["\']canonical["\']\s+href=', html_content, re.IGNORECASE):
        errors.append("Missing <link rel=\"canonical\" href=\"...\"> link.")

    # Check viewport tag
    if not re.search(r'<meta\s+name=["\']viewport["\']\s+content=', html_content, re.IGNORECASE):
        errors.append("Missing <meta name=\"viewport\" ...> tag.")

    # Check AMP boilerplate
    if "amp-boilerplate" not in html_content:
        errors.append("Missing <style amp-boilerplate> tag.")

    # Check for forbidden <img> tags (should use <amp-img>)
    if re.search(r'<img\s+[^>]*>', html_content, re.IGNORECASE):
        errors.append("Forbidden <img> tag found. Use <amp-img> instead for AMP compliance.")

    # Check for unauthorized inline scripts
    scripts = re.findall(r'<script\b([^>]*)>', html_content, re.IGNORECASE)
    for script_attrs in scripts:
        if 'src="https://cdn.ampproject.org/' in script_attrs or "src='https://cdn.ampproject.org/" in script_attrs:
            continue
        if 'type="application/ld+json"' in script_attrs:
            continue
        errors.append(f"Disallowed <script> tag detected: attrs='{script_attrs}'")

    # Check non-sponsorship disclaimer
    if DISCLAIMER_TEXT not in html_content:
        errors.append("Missing or modified non-sponsorship disclaimer.")

    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    parser = argparse.ArgumentParser(description="Validate AMP HTML for IDE Guide Blogger posts.")
    parser.add_argument("--file", required=True, help="Path to the AMP HTML file to validate")
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {args.file}: {e}")
        sys.exit(1)

    is_valid, errors = validate_amp_html(content)
    if is_valid:
        print(f"✅ SUCCESS: {args.file} is fully AMP compliant.")
        sys.exit(0)
    else:
        print(f"❌ AMP VALIDATION ERROR(S) in {args.file}:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
