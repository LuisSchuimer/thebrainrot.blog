from os import path
import re
from typing import Union

from thebrainrot_blog.markdown_handler.piece_types import (
    piece_types,
    piece_seqences,
    styling_types,
    data_types
)

class piece:
    def __init__(self,
        style_type: piece_types,
        start_index: Union[int,None] = None,
        end_index: Union[int,None] = None,
        data: dict[data_types, str] = {}
    ):
        self.style_type: piece_types = style_type
        self.start_index: Union[int,None] = start_index
        self.end_index: Union[int,None] = end_index
        self.data: dict[data_types, str] = data

    def append_data_to_piece(self, data_type: data_types, value: str) -> None: self.data[data_type] = value
class line:
    def __init__(self,
        content: str = ""
    ):
        self.content: str = content
        self.styling: dict[styling_types, list[piece]] = {
            styling_types.GLOBAL: [],
            styling_types.SPECIFIC: [],
        }

    def open_specific_styling(self, style_type: piece_types) -> piece|bool:
        open_styling_types = [
            elem 
            for elem in self.styling[styling_types.SPECIFIC]
            if elem.style_type == style_type and elem.end_index is None
        ]
        if open_styling_types:
            return open_styling_types[0]
        else: return False

    def append_styling_piece(self, piece_type: piece_types, start_index: int|None = None, end_index: int|None = None) -> bool:
        if piece_type in piece_seqences[styling_types.GLOBAL].keys():
            self.styling[styling_types.GLOBAL].append(piece(style_type=piece_type))
            return True
        else:
            # Ensure that no new styling type is opened when the same one is still opened
            if start_index is not None and self.open_specific_styling(piece_type) is False:
                self.styling[styling_types.SPECIFIC].append(piece(
                    style_type=piece_type,
                    start_index=start_index,
                    end_index=end_index
                ))
                return True
            elif end_index is not None and isinstance((open_obj := self.open_specific_styling(piece_type)), piece): 
                open_obj.end_index = end_index
                return True
        return False

    # Looks at previous styling sequences used and evaluates which styling types are not further usable in a line
    def invalid_global_styling_sequences(self) -> list[piece_types]:
        for styling_type in [elem.style_type for elem in self.styling[styling_types.GLOBAL]]:
            match styling_type:
                case piece_types.TITLE1 | piece_types.TITLE2 | piece_types.TITLE3:
                    return [
                        piece_types.TITLE1,
                        piece_types.TITLE2,
                        piece_types.TITLE3,
                        piece_types.BLOCKQUOTE
                    ]

                case _: return []
        return []

def construct_line(line_content: str) -> line:
    current_line: line = line()

    current_line_content_list: list[str] = line_content.split()
    for seq in line_content.split():
        # Set value to detect if no styling pattern matches
        seq_valid = False
        for current_styling_pattern in piece_seqences[styling_types.GLOBAL]:
            # If styling is locked, continue to next
            if current_styling_pattern in current_line.invalid_global_styling_sequences(): continue
            found_pattern = re.search(piece_seqences[styling_types.GLOBAL][current_styling_pattern], seq)

            if found_pattern: 
                seq_valid = True
                current_line_content_list.pop(0)

                match current_styling_pattern:
                    case piece_types.BLOCKQUOTE: 
                        for _ in range(len(seq)): current_line.append_styling_piece(piece_type=piece_types.BLOCKQUOTE)#
                    case _: current_line.append_styling_piece(piece_type=current_styling_pattern)

        # If no valid pattern found: stop searching global styling
        if not seq_valid: break

    current_line.content = " ".join(current_line_content_list)

    # Specific styling detection
    for line_piece in current_line.content.split():

        for current_styling_pattern in piece_seqences[styling_types.SPECIFIC]:
            found_patterns = re.search(piece_seqences[styling_types.SPECIFIC][current_styling_pattern], line_piece)
            if found_patterns: print(f"{found_patterns =}, {current_styling_pattern =}")

    #! TEST FOR THIS
    current_line.append_styling_piece(piece_type=piece_types.BOLD, start_index=3)
    current_line.append_styling_piece(piece_type=piece_types.BOLD, end_index=5)

    return current_line

def parse(markdown_article_path: str) -> list[line] | None:
    if not path.isfile(markdown_article_path): return None

    output: list[line] = []
    with open(markdown_article_path, encoding="utf8", mode="r") as article_file:
        article: list[str] = [line_content.strip() for line_content in article_file]

    for line_content in article:
        output.append(construct_line(line_content))

    return output

if __name__ == "__main__":
    #parse("./test2.md")
    construct_line(">>> **Tests** are great")