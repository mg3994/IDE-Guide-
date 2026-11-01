"""
AMP Validator for Blogger Blog Posts.

Verifies that HTML content complies with AMP (Accelerated Mobile Pages) standards
appropriate for Google Blogger, ensuring:
1. No prohibited script tags or inline javascript event handlers (e.g. onclick, onerror).
2. Proper usage of <amp-img> instead of standard <img> tags with width, height, and layout.
3. No forbidden tags (<iframe> without amp, <embed>, <object>, <applet>).
4. Valid presence of the independent non-sponsorship disclaimer.
5. Presence of structured semantic headings (h1/h2/h3).
"""

from __future__ import annotations

import re
from typing import List, Tuple
from html.parser import HTMLParser

REQUIRED_DISCLAIMER_PHRASE = (
    "independent technical publication. This content is not sponsored, "
    "endorsed, or affiliated with any software vendor"
)

FORBIDDEN_TAGS = {"script", "iframe", "frame", "embed", "object", "applet", "form", "input"}
ALLOWED_AMP_TAGS = {"amp-img", "amp-video", "amp-youtube", "amp-iframe"}


class AMPHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.has_amp_img = False
        self.has_raw_img = False
        self.tags_seen: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]):
        tag_lower = tag.lower()
        self.tags_seen.append(tag_lower)
        attr_dict = {k.lower(): (v or "") for k, v in attrs}

        # Check for forbidden tags
        if tag_lower in FORBIDDEN_TAGS:
            self.errors.append(f"Forbidden tag detected: <{tag}>")

        # Check raw <img>
        if tag_lower == "img":
            self.has_raw_img = True
            self.errors.append("Standard <img> tag is forbidden in AMP. Use <amp-img> instead.")

        # Check <amp-img> attributes
        if tag_lower == "amp-img":
            self.has_amp_img = True
            if "width" not in attr_dict or "height" not in attr_dict:
                self.errors.append("<amp-img> must explicitly declare 'width' and 'height' attributes.")
            if "layout" not in attr_dict:
                self.warnings.append("<amp-img> recommended to include layout='responsive'.")
            if "alt" not in attr_dict or not attr_dict["alt"].strip():
                self.warnings.append("<amp-img> should include a non-empty 'alt' attribute for accessibility.")

        # Check for inline event handlers (onclick, onload, onerror, etc.)
        for attr_name in attr_dict:
            if attr_name.startswith("on"):
                self.errors.append(f"Inline JavaScript event handler '{attr_name}' is forbidden in AMP HTML.")
            if attr_name == "href" and attr_dict[attr_name].strip().lower().startswith("javascript:"):
                self.errors.append(f"Disallowed 'javascript:' URI detected in href.")


def validate_amp_blogger_content(html_content: str) -> Tuple[bool, List[str], List[str]]:
    """
    Validates AMP Blogger HTML content.
    Returns:
        (is_valid: bool, errors: list of error strings, warnings: list of warning strings)
    """
    errors: List[str] = []
    warnings: List[str] = []

    if not html_content or not html_content.strip():
        return False, ["HTML content is empty."], []

    # Check for disclaimer
    if REQUIRED_DISCLAIMER_PHRASE not in html_content:
        errors.append(
            f"Missing required independent disclaimer: '{REQUIRED_DISCLAIMER_PHRASE}' must appear in the post."
        )

    # Parse HTML
    parser = AMPHTMLParser()
    try:
        parser.feed(html_content)
    except Exception as e:
        errors.append(f"HTML parsing failure: {str(e)}")

    errors.extend(parser.errors)
    warnings.extend(parser.warnings)

    # Check for heading structure
    if not any(h in parser.tags_seen for h in ("h1", "h2")):
        warnings.append("Recommended to include at least one <h1> or <h2> tag for SEO structure.")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    valid, errs, warns = validate_amp_blogger_content(content)
    if warns:
        print("WARNINGS:")
        for w in warns:
            print(f"  - {w}")
    if not valid:
        print("ERRORS (Validation FAILED):")
        for e in errs:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"SUCCESS: '{file_path}' passed AMP Blogger validation.")
