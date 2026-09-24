import unittest
from typing import Tuple, Union
from thebrainrot_blog.markdown_handler.parse_markdown import (
    parse, 
    construct_line, 
    line, 
    piece
)
from thebrainrot_blog.markdown_handler.piece_types import (
    piece_types, 
    styling_types, 
    data_types
)

class ParserTester(unittest.TestCase):
    def shortDescription(self):
        # Turn of stupid short descriptions of tests
        return None

    # Basic .md file handling checks
    def test_invalid_file(self): self.assertIs(parse("./"), None)
    def test_valid_file(self): self.assertIsNot("./README.md", None)

    # global styling translation checks
    def test_global_styling(self):
        """
        Tests the parser to correctly detect global styling patterns and to 
        proberly append those to the styling list and remove them out of the content
        """

        # input_content, output_content : expected detected global piece types (in order)
        styling_tests: dict[Tuple[str, str], list[piece_types]] = {
            ("- Test", "Test"): [piece_types.BULLET],
            ("# Test", "Test"): [piece_types.TITLE],
            ("# > - Test", "> - Test"): [piece_types.TITLE],
            ("> ## > - Test", "> - Test"): [piece_types.BLOCKQUOTE, piece_types.TITLE],
            ("- ### > - Test", "> - Test"): [piece_types.BULLET, piece_types.TITLE],
            ("- ### Test", "Test"): [piece_types.BULLET, piece_types.TITLE],
            ("#### -Test", "-Test"): [piece_types.TITLE],
            ("> # Test", "Test"): [ piece_types.BLOCKQUOTE, piece_types.TITLE],
            (">> - ## Test", "Test"): [piece_types.BLOCKQUOTE, piece_types.BLOCKQUOTE, piece_types.BULLET, piece_types.TITLE],
            ("*** ", ""): [piece_types.HORIZONTAL_RULES]
        }

        for content, expected_styling_pieces in styling_tests.items():
            out = construct_line(content[0])
            out_styling: list[piece_types] = [elem.style_type for elem in out.styling[styling_types.GLOBAL]]

            self.assertEqual(out.content, content[1], "Content expected and output mismatch")
            for i, styling_piece in enumerate(expected_styling_pieces):
                self.assertEqual(out_styling[i], styling_piece, "Global styling type mismatch between expected and output")
            self.assertIs(len(out_styling), len(styling_tests[content]), "Number of global styling mismatch between expected and output")

    def test_specific_styling(self):
        """
        Test the detection of specific styling types and deletion of required 
        detection patterns. Additionally it checks if indexes of start and end of styling is correct
        """

        #! More tests
        styling_tests: dict[Tuple[str, str], list[dict[str, Union[piece_types, Tuple[int, int]]]]] = {
            ("**This is** a test", "This is a test"): [
                {
                    "styling_piece": piece_types.BOLD,
                    "index": (0,6)
                },
            ],
            ("**ToDo List**", "ToDo List"): [
                {
                    "styling_piece": piece_types.BOLD,
                    "index": (0,8)
                }
            ],
            ("**Tests** are very **important** for *software*", "Tests are very important for software"): [
                {
                    "styling_piece": piece_types.BOLD,
                    "index": (0,4),
                },
                {
                    "styling_piece": piece_types.BOLD,
                    "index": (15,23)
                },
                {
                    "styling_piece": piece_types.ITALIC,
                    "index": (29,36)
                }
            ],
            ("Tests are ~~not~~ ==important==", "Tests are not important"): [
                {
                    "styling_piece": piece_types.STRIKETHROUGH,
                    "index": (10,12)
                },
                {
                    "styling_piece": piece_types.HIGHLIGHT,
                    "index": (14,22)
                }
            ]
        }

        for content, expected_pieces in styling_tests.items():
            out = construct_line(line_content=content[0])

            self.assertEqual(out.content, content[1], "Content mismatch between out and expected")
            for i, styling_piece in enumerate(out.styling[styling_types.SPECIFIC]):
                self.assertEqual(expected_pieces[i]["styling_piece"], styling_piece.style_type, "Specific styling type mismatch")
                self.assertEqual(expected_pieces[i]["index"], styling_piece.index, "Specific styling index mismatch")

    #! Currently only for title pieces, later also for images, links etc. 
    def test_piece_data(self):
        """
        Tests if the parser correctly identifies and saves piece data correctly
        """

        # (Content, type of used styling for test, styling type), data for detected style
        test_cases: dict[Tuple[str, styling_types, piece_types], dict[data_types, Union[piece_types, str]]] = {
            ("# Test", styling_types.GLOBAL, piece_types.TITLE): {
                data_types.TITLE_SIZE: "1"
            },
            ("### Test Case here", styling_types.GLOBAL, piece_types.TITLE): {
                data_types.TITLE_SIZE: "3"
            },
            ("###### Test Case here", styling_types.GLOBAL, piece_types.TITLE): {
                data_types.TITLE_SIZE: "6"
            }
        }

        for test, expected in test_cases.items():
            out = construct_line(line_content=test[0]).styling[test[1]][0]

            self.assertEqual(out.style_type, test[2], "Styling type mismatch between output and expected")
            self.assertEqual(out.data, expected, "Data mismatch between output and expected")

    def test_appending_style(self):
        """
        Tests if the parser appends specific and global styling types correctly into each 
        assined lists inside the line class
        """

        # Piece type, styling_type, start index, end_index
        appending_tests: list[Tuple[piece_types, styling_types, Tuple[int, int]]] = [
            (piece_types.BOLD, styling_types.SPECIFIC, (1, 4)),
            (piece_types.ITALIC, styling_types.SPECIFIC, (3,2)),
            (piece_types.TITLE, styling_types.GLOBAL, (2,4))
        ]

        for params in appending_tests:
            out = line()
            self.assertEqual(out.append_styling_piece(
                piece_type=params[0],
                index=params[2],
            ), True, "Operation of appending specific style on line failed")
            if params[1] is styling_types.GLOBAL: self.assertEqual(out.styling[styling_types.GLOBAL][0].style_type, params[0], "Styling not apppended to GLOBAL")
            elif params[1] is styling_types.SPECIFIC:
                styling_obj = out.styling[styling_types.SPECIFIC][0]
                self.assertEqual(styling_obj.style_type, params[0], "Styling not appended to SPECIFIC")
                self.assertEqual(styling_obj.index, params[2], "Styling sindex mismatch")

    def left_opened_styling(self):
        """
        Test that the program keeps a styling sequence in the content as long as
        it has not been closed yet
        """
        
        # input content, output content
        tests: list[Tuple[str, str]] = [
            ("This stying pattern (**) is nice", "This stying pattern (**) is nice"),
            ("I **love** this pattern *", "I love this pattern *"),
            ("~~ Check out those lines", "~~ Check out those lines")
        ]

        for test in tests: self.assertEqual(construct_line(test[0]).content, test[1])

    def test_updated_indexes(self):
        """
        Test if the function for deleting indexes from lines content
        is correctly updating the indexes of existing styling pieces
        """

        # Test text, indexes to be deleted (2 items a start and end value), potential styling indexes, expected change through deletion
        test_cases: dict[Tuple[str, Tuple[Tuple[int, int], Tuple[int,int]]], list[Tuple[Tuple[int,int], Tuple[int,int]]]] = {
            ("**Test*are*hot**yeaa", ((0,2), (15,17))): [((7,9), (5,7)), ((10,12), (8,10))],
            ("**I love tests**", ((0,2), (11,13))): [((3,11), (1,9))]
        }

        for test_params, expected in test_cases.items():
            out = line(test_params[0])
            for params in expected:
                out.styling[styling_types.SPECIFIC].append(piece(
                    style_type=piece_types.BOLD,
                    index=params[0]
                ))
            out.delete_indexes_from_content(
                (test_params[1][0], test_params[1][1])
            )

            for count, params in enumerate(expected):
                self.assertEqual(out.styling[styling_types.SPECIFIC][count].index, params[1])
