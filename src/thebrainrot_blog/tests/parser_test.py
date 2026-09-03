import unittest
from thebrainrot_blog.markdown_handler.parse_markdown import parse, construct_line
from thebrainrot_blog.markdown_handler.piece_types import piece_types, styling_types

class ParserTester(unittest.TestCase):
    # Basic .md file handling checks
    def test_invalid_file(self): self.assertIs(parse("./"), None)
    def test_valid_file(self): self.assertIsNot("./README.md", None)

    # global styling translation checks
    def test_global_styling(self):
        styling_tests: dict[str, list[piece_types]] = {
            "- Test": [
                piece_types.BULLET
            ],
            "# Test": [
                piece_types.TITLE1
            ],
            "- ### Test": [
                piece_types.BULLET,
                piece_types.TITLE3
            ],
            "> # Test": [
                piece_types.BLOCKQUOTE,
                piece_types.TITLE1
            ],
            ">> - ## Test": [
                piece_types.BLOCKQUOTE,
                piece_types.BLOCKQUOTE,
                piece_types.BULLET,
                piece_types.TITLE2
            ]
        }

        for test in styling_tests.keys():
            out = construct_line(test)
            out_styling: list[piece_types] = [elem.style_type for elem in out.styling[styling_types.GLOBAL]]

            for i in range(len(styling_tests[test])):
                self.assertEqual(out_styling[i], styling_tests[test][i], "Global styling type missmatch between expected and output")
            self.assertIs(len(out_styling), len(styling_tests[test]), "Number of global styling missmatch between expected and output")
