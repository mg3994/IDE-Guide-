#!/usr/bin/env python3
"""
AMP Validator for Blogger Content (IDE Guide)

Validates HTML blog posts against AMP HTML rules and channel compliance
(e.g., non-sponsorship disclaimer, no standard img tags, proper AMP boilerplate).
"""

import sys
import re

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or "
    "editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
)

def validate_amp_html(html_content: str) -> tuple[bool, list[str]]:
    """
    Validates AMP HTML string.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    # 1. AMP declaration
    if not (re.search(r'<html\s+⚡', html_content, re.IGNORECASE) or re.search(r'<html\s+amp', html_content, re.IGNORECASE)):
        errors.append("Missing <html ⚡> or <html amp> declaration.")

    # 2. Canonical link
    if not re.search(r'<link\s+rel=["\']canonical["\']', html_content, re.IGNORECASE):
        errors.append("Missing <link rel=\"canonical\" href=\"...\"> tag.")

    # 3. AMP runtime script
    if 'https://cdn.ampproject.org/v0.js' not in html_content:
        errors.append("Missing AMP JS runtime script (https://cdn.ampproject.org/v0.js).")

    # 4. AMP Boilerplate CSS
    if 'style amp-boilerplate' not in html_content:
        errors.append("Missing <style amp-boilerplate> element.")

    # 5. Check for prohibited standard <img> tag
    # Allow <amp-img> but reject raw <img> tags
    raw_img_matches = re.findall(r'<img\s+[^>]*>', html_content, re.IGNORECASE)
    if raw_img_matches:
        errors.append(f"Forbidden standard <img> tag found ({len(raw_img_matches)} instance(s)). Use <amp-img> instead.")

    # 6. Check for inline style attributes on html elements (forbidden in strict AMP HTML)
    inline_style_matches = re.findall(r'<[a-z1-6]+\s+[^>]*style=["\'][^"\'\>]+["\'][^>]*>', html_content, re.IGNORECASE)
    # Ignore <style> tags themselves
    filtered_inline_styles = [m for m in inline_style_matches if not m.startswith('<style')]
    if filtered_inline_styles:
        errors.append(f"Forbidden inline style attribute found ({len(filtered_inline_styles)} instance(s)). All styling must be inside <style amp-custom>.")

    # 7. Check for Non-sponsorship Disclaimer
    if DISCLAIMER_TEXT not in html_content:
        errors.append("Missing exact mandatory non-sponsorship disclaimer text.")

    return (len(errors) == 0, errors)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 amp_validator.py <file.html>")
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        sys.exit(1)

    is_valid, errors = validate_amp_html(content)
    if is_valid:
        print(f"✅ SUCCESS: {filepath} is valid AMP HTML for Blogger.")
        sys.exit(0)
    else:
        print(f"❌ VALIDATION ERRORS in {filepath}:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

if __name__ == '__main__':
    main()
