import unittest
from scripts.ide_guide_agent_skill import (
    get_ide_info,
    generate_amp_html_blog_post,
    generate_google_flow_video_spec,
    DISCLAIMER_TEXT,
    BLOGGER_URL,
    YOUTUBE_URL
)

class TestAMPValidation(unittest.TestCase):
    def setUp(self):
        self.info = get_ide_info("Cursor")
        self.amp_html = generate_amp_html_blog_post(self.info)
        self.video_spec = generate_google_flow_video_spec(self.info)

    def test_amp_doctype_and_html_tag(self):
        self.assertTrue(self.amp_html.startswith("<!doctype html>"))
        self.assertIn('<html ⚡ lang="en">', self.amp_html)

    def test_amp_js_runtime_script(self):
        self.assertIn('<script async src="https://cdn.ampproject.org/v0.js"></script>', self.amp_html)

    def test_amp_boilerplate_and_custom_style(self):
        self.assertIn('<style amp-boilerplate>', self.amp_html)
        self.assertIn('<style amp-custom>', self.amp_html)

    def test_mandatory_disclaimer_in_blog_post(self):
        self.assertIn(DISCLAIMER_TEXT, self.amp_html)

    def test_mandatory_disclaimer_in_video_spec(self):
        self.assertIn(DISCLAIMER_TEXT, self.video_spec)

    def test_channel_urls_presence(self):
        self.assertIn(BLOGGER_URL, self.amp_html)
        self.assertIn(YOUTUBE_URL, self.amp_html)
        self.assertIn("ideguide.blogspot.com", self.video_spec)
        self.assertIn("@IDEguide", self.video_spec)

if __name__ == "__main__":
    unittest.main()
