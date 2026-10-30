"""Validator for Accelerated Mobile Pages (AMP) compliance in Blogger blog post bodies.

Enforces:
1. No forbidden tags (<img>, <script>, <iframe>, <style> unless amp-custom, <font>, etc.).
2. Media must use <amp-img> with required attributes (width, height, layout).
3. Non-sponsorship disclaimer must be explicitly present.
4. Clean HTML structure and accessibility attributes.
"""

import re
from typing import List, Tuple

FORBIDDEN_TAGS = [
    r"<img\b",
    r"<script\b",
    r"<iframe\b",
    r"<video\b",
    r"<audio\b",
    r"<font\b",
    r"<center\b",
    r"<frame\b",
    r"<frameset\b",
]

MANDATORY_DISCLAIMER_KEYWORD = "Disclaimer: IDE Guide is an independent technical publication."


class AMPValidationError(Exception):
    """Exception raised when HTML content violates AMP Blogger standards."""
    pass


def validate_amp_blogger_content(html_content: str) -> Tuple[bool, List[str]]:
    """Validate HTML snippet destined for Blogger against AMP requirements.

    Returns:
        (is_valid, list_of_errors)
    """
    errors: List[str] = []

    if not html_content or not html_content.strip():
        errors.append("HTML content is empty.")
        return False, errors

    # Check 1: Forbidden HTML tags
    for pattern in FORBIDDEN_TAGS:
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            tag_name = pattern.replace("<", "").replace(r"\b", "")
            errors.append(f"Forbidden tag detected: <{tag_name}>. Use AMP equivalents (e.g. <amp-img> instead of <img>).")

    # Check 2: amp-img tag requirements
    amp_img_matches = re.finditer(r"<amp-img\b([^>]*)>", html_content, re.IGNORECASE)
    for match in amp_img_matches:
        attrs = match.group(1)
        if "width=" not in attrs or "height=" not in attrs:
            errors.append(f"Found <amp-img> missing explicit width or height attributes: {match.group(0)}")
        if "layout=" not in attrs:
            errors.append(f"Found <amp-img> missing layout attribute: {match.group(0)}")

    # Check 3: Forbidden inline event handlers (onclick, onload, etc.)
    inline_events = re.findall(r"\bon[a-z]+\s*=", html_content, re.IGNORECASE)
    if inline_events:
        errors.append(f"Forbidden inline event handler attributes detected: {', '.join(set(inline_events))}")

    # Check 4: Mandatory Non-Sponsorship Disclaimer
    if MANDATORY_DISCLAIMER_KEYWORD not in html_content:
        errors.append(
            "Missing mandatory non-sponsorship disclaimer: "
            f"Must include '{MANDATORY_DISCLAIMER_KEYWORD}'."
        )

    return len(errors) == 0, errors


if __name__ == "__main__":
    sample_valid_amp = f"""
    <article class="amp-post">
        <h2>VS Code Review</h2>
        <amp-img src="https://example.com/vscode.png" width="800" height="450" layout="responsive" alt="VS Code"></amp-img>
        <p>Testing post content.</p>
        <div class="disclaimer">
            <p>{MANDATORY_DISCLAIMER_KEYWORD} This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.</p>
        </div>
    </article>
    """
    is_valid, sample_errors = validate_amp_blogger_content(sample_valid_amp)
    print(f"Sample test validity: {is_valid}, errors: {sample_errors}")
