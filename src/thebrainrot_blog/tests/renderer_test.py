import unittest

from thebrainrot_blog.markdown_handler.render_article import render

class RendererTester(unittest.TestCase):
    def shortDescription(self) -> None:
        return None

    # Basic .md file handling checks
    def test_invalid_file(self): self.assertIs(render("./"), None)
    def test_valid_file(self): self.assertIsNot(render("./README.md"), None)