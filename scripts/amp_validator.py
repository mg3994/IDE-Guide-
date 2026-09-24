#!/usr/bin/env python3
"""
AMP HTML Validator for IDE Guide Blogger Posts
Validates HTML strings or files to ensure compliance with Blogger AMP (Accelerated Mobile Pages) rules.
"""

import re
import sys
from typing import List, Tuple

DISCLAIMER_TEXT = "Disclaimer: IDE Guide is an independent technical publication."

def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    """
    Validates AMP HTML content for Blogger compatibility.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    # 1. AMP runtime script presence
    if 'https://cdn.ampproject.org/v0.js' not in html_content:
        errors.append("Missing standard AMP script: https://cdn.ampproject.org/v0.js")

    # 2. Boilerplate style presence
    if 'amp-boilerplate' not in html_content:
        errors.append("Missing required AMP boilerplate CSS.")

    # 3. Canonical link tag presence
    if not re.search(r'<link\s+rel=["\']canonical["\']', html_content):
        errors.append("Missing canonical link tag (<link rel=\"canonical\" href=\"...\">).")

    # 4. Prohibit forbidden tags like standard <img> or inline styles with style attribute
    if re.search(r'<img\s+[^>]*>', html_content):
        errors.append("Forbidden tag <img ...> found. AMP requires <amp-img ...></amp-img>.")

    if re.search(r'<style>(?!.*amp-custom)', html_content) and 'amp-custom' not in html_content:
        errors.append("Custom CSS must use <style amp-custom>.")

    # 5. Check inline style attributes (style="...")
    if re.search(r'\sstyle=["\'][^"\'\>]+["\']', html_content):
        errors.append("Inline style attribute (style=\"...\") is forbidden in AMP HTML.")

    # 6. Check custom CSS size limit (under 75KB)
    css_match = re.search(r'<style\s+amp-custom[^>]*>(.*?)</style>', html_content, re.DOTALL)
    if css_match:
        css_size = len(css_match.group(1).encode('utf-8'))
        if css_size > 75000:
            errors.append(f"Custom CSS size ({css_size} bytes) exceeds AMP limit of 75,000 bytes.")

    # 7. Non-sponsorship disclaimer presence
    if DISCLAIMER_TEXT not in html_content:
        errors.append("Missing mandatory non-sponsorship disclaimer.")

    is_valid = len(errors) == 0
    return is_valid, errors

def validate_file(filepath: str) -> bool:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        valid, errors = validate_amp_html(content)
        if valid:
            print(f"✅ {filepath} is valid Blogger AMP HTML.")
            return True
        else:
            print(f"❌ {filepath} failed Blogger AMP HTML validation:")
            for err in errors:
                print(f"   - {err}")
            return False
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        success = validate_file(sys.argv[1])
        sys.exit(0 if success else 1)
    else:
        print("Usage: python3 scripts/amp_validator.py <path_to_amp_html_file>")
        sys.exit(1)
