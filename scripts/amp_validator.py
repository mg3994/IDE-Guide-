#!/usr/bin/env python3
"""
AMP Validator Utility for IDE Guide Blogger Posts.
Checks HTML content for compliance with Accelerated Mobile Pages (AMP) standards
and mandatory non-sponsorship disclaimer requirements.
"""

import sys
import re
from typing import Tuple, List

MANDATORY_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    """
    Validates AMP HTML rules and disclaimer presence.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    if not re.search(r"<!doctype\s+html>", html_content, re.IGNORECASE):
        errors.append("Missing <!doctype html> declaration.")

    if not re.search(r"<html\s+[^>]*(⚡|amp)[^>]*>", html_content, re.IGNORECASE):
        errors.append("Missing <html ⚡> or <html amp> attribute.")

    if not re.search(r'<meta\s+charset=["\']?utf-8["\']?', html_content, re.IGNORECASE):
        errors.append("Missing <meta charset=\"utf-8\"> tag.")

    if "https://cdn.ampproject.org/v0.js" not in html_content:
        errors.append("Missing AMP runtime script (https://cdn.ampproject.org/v0.js).")

    if "<style amp-boilerplate>" not in html_content:
        errors.append("Missing <style amp-boilerplate> block.")

    if "<noscript><style amp-boilerplate>" not in html_content:
        errors.append("Missing <noscript><style amp-boilerplate> block.")

    if re.search(r"<img\s+", html_content, re.IGNORECASE) and not re.search(r"<amp-img\s+", html_content, re.IGNORECASE):
        errors.append("Found standard <img> tag instead of <amp-img> tag.")

    if MANDATORY_DISCLAIMER not in html_content:
        errors.append("Missing required exact non-sponsorship disclaimer text.")

    is_valid = len(errors) == 0
    return is_valid, errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <path_to_html_file>")
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
        print(f"SUCCESS: {filepath} is valid AMP HTML for Blogger with mandatory disclaimer.")
        sys.exit(0)
    else:
        print(f"FAILED: {filepath} has AMP validation errors:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
