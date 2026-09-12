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
        content: list[Union[str,piece_types]] = []
    ):
        self.content: list[Union[str,piece_types]] = content
        self.styling: dict[styling_types, list[piece]] = {
            styling_types.GLOBAL: [],
            styling_types.SPECIFIC: [],
        }

    def append_styling_piece(self, piece_type: piece_types, start_index: int|None = None, end_index: int|None = None) -> bool:
        if piece_type in piece_seqences[styling_types.GLOBAL].keys():
            self.styling[styling_types.GLOBAL].append(piece(style_type=piece_type))
        else:
            if start_index != None:
                self.styling[styling_types.SPECIFIC].append(piece(
                    style_type=piece_type,
                    start_index=start_index,
                    end_index=end_index
                ))
                self.content.insert(start_index, piece_type)
                if end_index != None: self.content.insert(end_index, piece_type)
            else: return False
        return True

    # Looks at previous styling sequences used and evaluates which styling types are not further usable in a line
    def invalid_styling_sequences(self) -> list[piece_types]:
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
            if current_styling_pattern in current_line.invalid_styling_sequences(): continue
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

    current_line.content = list[Union[str, piece_types]](current_line_content_list)

    # Specific styling detection
    print(current_line.content)
    for line_piece in current_line.content:
        if isinstance(line_piece, piece_types): continue

        for current_styling_pattern in piece_seqences[styling_types.SPECIFIC]:
            found_patterns = re.findall(piece_seqences[styling_types.SPECIFIC][current_styling_pattern], line_piece)
            if found_patterns: print(f"{found_patterns = }, {current_styling_pattern =}")


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