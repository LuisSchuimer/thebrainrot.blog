import unittest
from typing import Tuple
from thebrainrot_blog.markdown_handler.parse_markdown import parse, construct_line, line
from thebrainrot_blog.markdown_handler.piece_types import piece_types, styling_types

class ParserTester(unittest.TestCase):
    # Basic .md file handling checks
    def test_invalid_file(self): self.assertIs(parse("./"), None)
    def test_valid_file(self): self.assertIsNot("./README.md", None)

    # global styling translation checks
    def test_global_styling(self):
        styling_tests: dict[str, list[piece_types]] = {
            "- Test": [piece_types.BULLET],
            "# Test": [piece_types.TITLE1],
            "# > - Test": [piece_types.TITLE1],
            "- ### Test": [piece_types.BULLET, piece_types.TITLE3],
            "> # Test": [ piece_types.BLOCKQUOTE, piece_types.TITLE1],
            ">> - ## Test": [piece_types.BLOCKQUOTE, piece_types.BLOCKQUOTE, piece_types.BULLET, piece_types.TITLE2]
        }

        for test in styling_tests.keys():
            out = construct_line(test)
            out_styling: list[piece_types] = [elem.style_type for elem in out.styling[styling_types.GLOBAL]]

            for i in range(len(styling_tests[test])):
                self.assertEqual(out_styling[i], styling_tests[test][i], "Global styling type mismatch between expected and output")
            self.assertIs(len(out_styling), len(styling_tests[test]), "Number of global styling mismatch between expected and output")

    def test_appending_style(self):
        appending_tests: list[Tuple[piece_types, styling_types, int, int]] = [
            (piece_types.BOLD, styling_types.SPECIFIC, 1, 4),
            (piece_types.ITALIC, styling_types.SPECIFIC, 3, 5),
            (piece_types.TITLE1, styling_types.GLOBAL, 0, 0)
        ]

        for params in appending_tests:
            out = line()
            self.assertEqual(out.append_styling_piece(
                piece_type=params[0],
                start_index=params[2],
                end_index=params[3]
            ), True, "Operation of appending specific style on line failed")
            if params[1] is styling_types.GLOBAL: self.assertEqual(out.styling[styling_types.GLOBAL][0].style_type, params[0], "Styling not apppended to GLOBAL")
            elif params[1] is styling_types.SPECIFIC:
                styling_obj = out.styling[styling_types.SPECIFIC][0]
                self.assertEqual(styling_obj.style_type, params[0], "Styling not appended to SPECIFIC")
                self.assertEqual(styling_obj.start_index, params[2], "Styling start index mismatch")
                self.assertEqual(styling_obj.end_index, params[3], "Styling end index mismatch")