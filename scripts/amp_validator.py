#!/usr/bin/env python3
"""
AMP Validator & Disclaimer Compliance Checker for IDE Guide Blogger Posts.
"""

import re
import sys
import argparse
from typing import List, Tuple

MANDATORY_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

FORBIDDEN_TAGS = [
    r'<img\b',
    r'<video\b',
    r'<audio\b',
    r'<iframe\b(?!.*data-amp-3p-sentinel)',
    r'<script\b(?!.*src="https://cdn\.ampproject\.org/)'
]

FORBIDDEN_ATTRIBUTES = [
    r'\bonclick\s*=',
    r'\bonload\s*=',
    r'\bonerror\s*=',
    r'\bstyle\s*=\s*"[^"]*!important[^"]*"',
]

def validate_amp_html(content: str) -> Tuple[bool, List[str]]:
    errors = []

    # Check non-sponsorship disclaimer
    if MANDATORY_DISCLAIMER not in content:
        errors.append("Missing or incomplete mandatory non-sponsorship disclaimer.")

    # Check forbidden HTML tags
    for pattern in FORBIDDEN_TAGS:
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(f"Forbidden tag matching pattern '{pattern}' found. Use AMP equivalents (e.g. <amp-img>, <amp-youtube>).")

    # Check forbidden inline event handlers / attributes
    for pattern in FORBIDDEN_ATTRIBUTES:
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(f"Forbidden attribute pattern '{pattern}' found.")

    # Check style tags
    style_tags = re.findall(r'<style\b([^>]*)>', content, re.IGNORECASE)
    for style_attr in style_tags:
        if 'amp-custom' not in style_attr and 'amp-boilerplate' not in style_attr:
            errors.append(f"Style tag <style {style_attr}> must be 'amp-custom' or 'amp-boilerplate'.")

    return len(errors) == 0, errors

def main():
    parser = argparse.ArgumentParser(description="Validate AMP HTML & Disclaimer compliance for IDE Guide blog posts.")
    parser.add_argument("file", nargs="?", help="Path to AMP HTML file to validate")
    args = parser.parse_args()

    if not args.file:
        print("AMP Validator CLI tool ready.")
        sys.exit(0)

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            html_content = f.read()
    except Exception as e:
        print(f"Error reading file {args.file}: {e}")
        sys.exit(1)

    is_valid, errors = validate_amp_html(html_content)
    if is_valid:
        print(f"✅ AMP Validation SUCCESS: {args.file} is AMP-compliant and contains required disclaimers.")
        sys.exit(0)
    else:
        print(f"❌ AMP Validation FAILED for {args.file}:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
