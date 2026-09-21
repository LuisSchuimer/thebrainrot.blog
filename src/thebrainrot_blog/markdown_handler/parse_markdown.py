"Markdown to HTML parser as part of thebrainrot.blog by Luis Schuimer"

from os import path
import re
from typing import Union, Tuple

from thebrainrot_blog.markdown_handler.piece_types import (
    piece_types,
    piece_seqences,
    styling_types,
    data_types
)

class piece:
    def __init__(self,
        style_type: piece_types,
        start_index: Union[Tuple[int, int], None] = None,
        end_index: Union[Tuple[int, int], None] = None,
        data: dict[data_types, str] = {}
    ):
        self.style_type: piece_types = style_type
        self.start_index: Union[Tuple[int, int], None] = start_index
        self.end_index: Union[Tuple[int, int], None] = end_index
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

    def append_styling_piece(self, 
            piece_type: piece_types, 
            start_index: Union[Tuple[int, int], None] = None, 
            end_index: Union[Tuple[int, int], None] = None, 
            data: dict[data_types, str] = {}) -> bool:
        
        if piece_type in piece_seqences[styling_types.GLOBAL].keys():
            self.styling[styling_types.GLOBAL].append(piece(style_type=piece_type, data=data))
            return True
        else:
            if start_index is not None and end_index is not None:
                self.styling[styling_types.SPECIFIC].append(piece(
                    style_type=piece_type,
                    start_index=start_index,
                    end_index=end_index,
                    data=data
                ))
                return True
            return False

    # Looks at previous styling sequences used and evaluates which styling types are not further usable in a line
    def invalid_global_styling_sequences(self) -> list[Union[piece_types,None]]:
        for styling_type in [elem.style_type for elem in self.styling[styling_types.GLOBAL]]:
            match styling_type:
                case piece_types.TITLE:
                    return [
                        piece_types.TITLE,
                        piece_types.BLOCKQUOTE,
                        piece_types.BULLET
                    ]
                case _: continue
        return []

def construct_line(line_content: str) -> line:
    def delete_indexes_from_word(word: str, *indexes: Tuple[int,int]) -> str:
        for index in indexes: word = word[:index[0]] + word[index[1]:]
        return word
    
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
                        for _ in range(len(seq)): current_line.append_styling_piece(piece_type=piece_types.BLOCKQUOTE)
                    case piece_types.TITLE: current_line.append_styling_piece(piece_type=piece_types.TITLE, data={data_types.TITLE_SIZE: str(len(seq))})
                    
                    case _: current_line.append_styling_piece(piece_type=current_styling_pattern)

        # If no valid pattern found: stop searching global styling
        if not seq_valid: break

    # Specific styling detection
    unfinished_styling_pieces: dict[piece_types, Tuple[int,int,int]] = {} # Open piece type, index of word start and end that opended
    for word_count, line_piece in enumerate(current_line_content_list):
        for current_styling_pattern in piece_seqences[styling_types.SPECIFIC]:
            seq_found: bool = True
            while seq_found:
                seq_found = (found_pattern := re.search(piece_seqences[styling_types.SPECIFIC][current_styling_pattern], line_piece)) is not None

                if found_pattern and current_styling_pattern in unfinished_styling_pieces.keys(): 
                    # Delete both styling sequences
                    line_piece = delete_indexes_from_word(line_piece, 
                        (found_pattern.start(), found_pattern.end()
                    ))
                    current_line_content_list[word_count] = line_piece
                    current_line.append_styling_piece(
                        piece_type=current_styling_pattern,
                        start_index=(unfinished_styling_pieces[current_styling_pattern][0], unfinished_styling_pieces[current_styling_pattern][1]), # Start of styling piece (from unfinisched styling pieces)
                        end_index=(word_count, int(found_pattern.start() -1)) # End index (current piece discovered)
                    )
                    # Delete added styling pattern (because it was closed)
                    unfinished_styling_pieces.pop(current_styling_pattern)

                elif found_pattern: 
                    unfinished_styling_pieces[current_styling_pattern] = (word_count, found_pattern.start(), found_pattern.end())
                    line_piece = delete_indexes_from_word(line_piece, 
                        (found_pattern.start(), found_pattern.end()
                    ))

                else: seq_found = False

    current_line.content = " ".join(current_line_content_list)

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
    construct_line("#### -Test")