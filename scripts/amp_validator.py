#!/usr/bin/env python3
"""
AMP Validator for IDE Guide Blogger Posts
Validates HTML strings and files for AMP compliance and required disclaimer.
"""

import sys
import re
from html.parser import HTMLParser

REQUIRED_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

class AMPHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.warnings = []
        self.has_amp_attr = False
        self.has_charset = False
        self.has_amp_js = False
        self.has_style_custom = False
        self.has_style_boilerplate = False
        self.amp_imgs = []

    def handle_starttag(self, tag, attrs):
        attr_dict = {k.lower(): v for k, v in attrs}

        if tag == "html":
            if "⚡" in attr_dict or "amp" in attr_dict or ("⚡", None) in attrs or ("amp", None) in attrs or any(k in ["⚡", "amp"] for k, _ in attrs):
                self.has_amp_attr = True

        if tag == "meta":
            if "charset" in attr_dict:
                self.has_charset = True

        if tag == "script":
            src = attr_dict.get("src", "")
            script_type = attr_dict.get("type", "")
            if src == "https://cdn.ampproject.org/v0.js":
                self.has_amp_js = True
            elif src.startswith("https://cdn.ampproject.org/v0/amp-"):
                pass # AMP component script
            elif script_type == "application/ld+json":
                pass # Structured data
            else:
                self.errors.append(f"Disallowed script tag: src='{src}', type='{script_type}'")

        if tag == "style":
            if "amp-custom" in attr_dict or ("amp-custom", None) in attrs or any(k == "amp-custom" for k, _ in attrs):
                self.has_style_custom = True
            if "amp-boilerplate" in attr_dict or ("amp-boilerplate", None) in attrs or any(k == "amp-boilerplate" for k, _ in attrs):
                self.has_style_boilerplate = True

        if tag == "img":
            self.errors.append("Standard <img> tag is forbidden in AMP. Use <amp-img> instead.")

        if tag == "amp-img":
            self.amp_imgs.append(attr_dict)
            if "src" not in attr_dict:
                self.errors.append("<amp-img> missing 'src' attribute.")
            if "width" not in attr_dict:
                self.errors.append("<amp-img> missing 'width' attribute.")
            if "height" not in attr_dict:
                self.errors.append("<amp-img> missing 'height' attribute.")
            if "alt" not in attr_dict:
                self.warnings.append("<amp-img> missing 'alt' attribute.")

        # Check inline styles on tags
        if "style" in attr_dict:
            self.errors.append(f"Inline style attribute found on <{tag}> element. AMP requires CSS in <style amp-custom>.")


def validate_amp_html(html_content: str) -> dict:
    """
    Validates an HTML string against AMP HTML standards and IDE Guide requirements.
    Returns a dict with status (bool), list of errors, and list of warnings.
    """
    errors = []
    warnings = []

    # Check for mandatory disclaimer
    normalized_content = " ".join(html_content.split())
    normalized_disclaimer = " ".join(REQUIRED_DISCLAIMER.split())
    if normalized_disclaimer not in normalized_content:
        errors.append("Mandatory non-sponsorship disclaimer missing or modified.")

    parser = AMPHTMLParser()
    try:
        parser.feed(html_content)
    except Exception as e:
        errors.append(f"HTML parsing error: {e}")

    # Root html ⚡/amp check
    if not parser.has_amp_attr:
        # Fallback check regex
        if not re.search(r'<html\s+[^>]*?\b(amp|⚡)\b', html_content, re.IGNORECASE):
            errors.append("Root <html> tag must contain '⚡' or 'amp' attribute.")

    if not parser.has_charset:
        errors.append("Missing <meta charset='utf-8'> tag.")

    if not parser.has_amp_js:
        errors.append("Missing AMP runtime script (<script async src='https://cdn.ampproject.org/v0.js'></script>).")

    if not parser.has_style_custom:
        errors.append("Missing <style amp-custom> tag for custom styles.")

    errors.extend(parser.errors)
    warnings.extend(parser.warnings)

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def validate_file(filepath: str) -> dict:
    """Reads a file and validates its AMP HTML contents."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return validate_amp_html(content)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 amp_validator.py <filepath>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = validate_file(file_path)

    if result["valid"]:
        print(f"SUCCESS: '{file_path}' is valid AMP HTML.")
        if result["warnings"]:
            print("Warnings:")
            for w in result["warnings"]:
                print(f" - {w}")
        sys.exit(0)
    else:
        print(f"FAILED: '{file_path}' failed AMP validation.")
        print("Errors:")
        for err in result["errors"]:
            print(f" - {err}")
        sys.exit(1)
