import unittest
from scripts.amp_validator import validate_amp_html, DISCLAIMER_TEXT

class TestAMPValidator(unittest.TestCase):

    def setUp(self):
        self.valid_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Title</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both}}</style>
  <noscript><style amp-boilerplate>body{{-webkit-animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: sans-serif; }}
  </style>
</head>
<body>
  <article>
    <h1>Test Article</h1>
    <amp-img src="https://example.com/image.jpg" width="800" height="450" layout="responsive" alt="Test"></amp-img>
    <p>{DISCLAIMER_TEXT}</p>
  </article>
</body>
</html>"""

    def test_valid_amp_html(self):
        is_valid, errors = validate_amp_html(self.valid_html)
        self.assertTrue(is_valid, f"Expected valid AMP HTML, but got errors: {errors}")
        self.assertEqual(len(errors), 0)

    def test_missing_amp_declaration(self):
        invalid_html = self.valid_html.replace("<html ⚡ lang=\"en\">", "<html lang=\"en\">")
        is_valid, errors = validate_amp_html(invalid_html)
        self.assertFalse(is_valid)
        self.assertTrue(any("Missing <html ⚡>" in err for err in errors))

    def test_forbidden_img_tag(self):
        invalid_html = self.valid_html.replace("<amp-img", "<img")
        is_valid, errors = validate_amp_html(invalid_html)
        self.assertFalse(is_valid)
        self.assertTrue(any("Forbidden standard <img>" in err for err in errors))

    def test_missing_disclaimer(self):
        invalid_html = self.valid_html.replace(DISCLAIMER_TEXT, "")
        is_valid, errors = validate_amp_html(invalid_html)
        self.assertFalse(is_valid)
        self.assertTrue(any("non-sponsorship disclaimer" in err for err in errors))

if __name__ == "__main__":
    unittest.main()
