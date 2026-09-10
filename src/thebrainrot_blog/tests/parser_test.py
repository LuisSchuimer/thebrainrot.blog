import unittest
from typing import Tuple, Union
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
        appending_tests: dict[Tuple[Tuple[str, ...],piece_types,int], list[Union[str, piece_types]]] = {
            (("Test", "Test2"), piece_types.BOLD, 1): ["Test", piece_types.BOLD, "Test2"],
            (("I", "love", "Tests"), piece_types.ITALIC, 3): ["I", "love", "Tests", piece_types.ITALIC],
            (("Test3", "python"), piece_types.BOLD, 0): [piece_types.BOLD, "Test3", "python"]
        }

        for params, expect in appending_tests.items():
            out = line(content=list(params[0]))
            self.assertEqual(out.append_styling_piece(
                piece_type=params[1],
                start_index=params[2]
            ), True, "Operation of appending specific style on line failed")
            self.assertEqual(out.content, expect, "Content mismatch between expected and function output")