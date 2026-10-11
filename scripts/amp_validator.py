#!/usr/bin/env python3
"""
AMP HTML Validator for IDE Guide Blogger Posts.
Checks HTML content for common AMP compliance rules required for Blogger posts.
"""

import re
import sys
from typing import List, Tuple

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

def validate_amp_html(html_content: str) -> Tuple[bool, List[str]]:
    """
    Validates HTML content against AMP rules for Blogger posts.

    Returns:
        (is_valid, list_of_errors)
    """
    errors: List[str] = []

    # 1. Check for standard <img> tags (must use <amp-img>)
    if re.search(r'<img\b[^>]*>', html_content, re.IGNORECASE):
        errors.append("Prohibited element found: Standard <img> tags are not allowed in AMP HTML. Use <amp-img> instead.")

    # 2. Check for inline style attributes (style="...")
    if re.search(r'\bstyle\s*=\s*["\'][^"\']*["\']', html_content, re.IGNORECASE):
        errors.append("Prohibited attribute found: Inline 'style' attributes are not allowed in AMP HTML. Use <style amp-custom>.")

    # 3. Check for disallowed tags: <script>, <iframe>, <form>, <input>
    disallowed_tags = ['script', 'iframe', 'form', 'input', 'button']
    for tag in disallowed_tags:
        if re.search(rf'<{tag}\b[^>]*>', html_content, re.IGNORECASE):
            errors.append(f"Prohibited tag found: <{tag}> is not allowed in standard AMP post body.")

    # 4. Check for event handlers (e.g. onclick, onload)
    if re.search(r'\bon[a-z]+\s*=', html_content, re.IGNORECASE):
        errors.append("Prohibited inline event handler found (e.g. onclick, onload).")

    # 5. Check for disclaimer
    if DISCLAIMER_TEXT not in html_content:
        errors.append("Missing mandatory non-sponsorship disclaimer.")

    # 6. Verify <amp-img> tags have required attributes (width, height)
    amp_img_matches = re.findall(r'<amp-img\b([^>]*)>', html_content, re.IGNORECASE)
    for idx, attrs in enumerate(amp_img_matches, 1):
        if 'width=' not in attrs or 'height=' not in attrs:
            errors.append(f"<amp-img> #{idx} is missing required 'width' or 'height' attributes.")

    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 amp_validator.py <path_to_html_file>")
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
        print(f"SUCCESS: '{filepath}' is valid AMP HTML for IDE Guide Blogger posts.")
        sys.exit(0)
    else:
        print(f"FAILED: '{filepath}' contains AMP HTML validation errors:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
