#!/usr/bin/env python3
import sys
import re
import os

REQUIRED_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

def validate_amp_html(html_content: str) -> tuple[bool, list[str]]:
    """
    Validates HTML content against AMP Blogger standards and IDE Guide requirements.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    # 1. Check for forbidden standard <img> tags
    if re.search(r'<img\s', html_content, re.IGNORECASE):
        errors.append("Forbidden <img> tag found. Use <amp-img> instead.")

    # 2. Check for inline style attributes: style="..."
    if re.search(r'\sstyle=["\'][^"\']*["\']', html_content, re.IGNORECASE):
        errors.append("Forbidden inline style attribute found. Style elements via <style amp-custom>.")

    # 3. Check for disallowed script tags (must be AMP scripts or none)
    script_tags = re.findall(r'<script\b[^>]*>(.*?)</script>', html_content, re.IGNORECASE | re.DOTALL)
    for script in re.finditer(r'<script\b([^>]*)>', html_content, re.IGNORECASE):
        attrs = script.group(1)
        if "cdn.ampproject.org" not in attrs and 'type="application/ld+json"' not in attrs:
            errors.append(f"Disallowed <script> tag attributes: {attrs}")

    # 4. Validate <amp-img> layout and attributes
    amp_imgs = re.findall(r'<amp-img\b([^>]*)>', html_content, re.IGNORECASE)
    if not amp_imgs and "<amp-img" in html_content:
        errors.append("Malformed <amp-img> tag found.")
    for attrs in amp_imgs:
        if "width=" not in attrs or "height=" not in attrs:
            errors.append("amp-img tag missing required 'width' or 'height' attribute.")

    # 5. Check mandatory disclaimer presence
    # Normalize whitespace for comparison
    normalized_content = " ".join(html_content.split())
    normalized_disclaimer = " ".join(REQUIRED_DISCLAIMER.split())
    if normalized_disclaimer not in normalized_content:
        errors.append("Mandatory non-sponsorship disclaimer missing or modified.")

    is_valid = len(errors) == 0
    return is_valid, errors

def validate_file(filepath: str) -> bool:
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} does not exist.")
        return False
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    is_valid, errors = validate_amp_html(content)
    if is_valid:
        print(f"✅ {filepath}: AMP HTML compliant.")
        return True
    else:
        print(f"❌ {filepath}: AMP HTML validation failed:")
        for err in errors:
            print(f"   - {err}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/amp_validator.py <filepath_or_directory>")
        sys.exit(1)

    target = sys.argv[1]
    all_valid = True

    if os.path.isdir(target):
        for root, _, files in os.walk(target):
            for file in files:
                if file.endswith('.html') or file.endswith('.amp.html'):
                    filepath = os.path.join(root, file)
                    if not validate_file(filepath):
                        all_valid = False
    else:
        all_valid = validate_file(target)

    sys.exit(0 if all_valid else 1)

if __name__ == "__main__":
    main()
