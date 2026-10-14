import unittest
from typing import Tuple

from thebrainrot_blog.markdown_handler.render_article import render

from thebrainrot_blog.markdown_handler.handler_config import (
    piece_styles,
    styling_types,
    piece_types
)

class RendererTester(unittest.TestCase):
    def shortDescription(self) -> None:
        return None

    # Basic .md file handling checks
    def test_invalid_file(self): self.assertIs(render("./"), None)
    def test_valid_file(self): self.assertIsNot(render("./README.md"), None)

    def test_rendering(self):
        test_cases: list[Tuple[str, str]] = [
            ("./src/thebrainrot_blog/tests/testdata/test.md", 
                f"<p><{piece_styles[styling_types.SPECIFIC][piece_types.BOLD][0][0]} class='{piece_styles[styling_types.SPECIFIC][piece_types.BOLD][0][1]}'>Hello World</{piece_styles[styling_types.SPECIFIC][piece_types.BOLD][0][0]}></p>"
            )
        ] 

        for markdown_path, expected_out in test_cases:
            self.assertEqual(render(markdown_path=markdown_path), expected_out)