from os import path
import re

from thebrainrot_blog.markdown_handler.piece_types import (
    piece_types,
    piece_seqences,
    styling_types
)

class line:
    def __init__(self,
        content: str = ""
    ):
        self.content: str = content
        self.styling = {
            styling_types.GLOBAL: [],
            styling_types.SPECIFIC: [] 
        }

    def append_styling_piece(self, piece_type: piece_types, start_end_index: tuple[int, int] = []):
        if piece_type in piece_seqences[styling_types.GLOBAL].keys():
            self.styling[styling_types.GLOBAL].append(piece(style_type=piece_type))
        else: 
            self.styling[styling_types.SPECIFIC].append(piece(style_type=piece_type, start_end_index=start_end_index))

class piece:
    def __init__(self,
        style_type: piece_types,
        start_end_index: tuple[int, int] = []
    ):
        self.style_type: piece_types = style_type
        self.start_end_index: tuple[int, int] = start_end_index

def update_locked_styling_types(found_styling_sequence: piece_types) -> list[piece_types]:
    # Markdown styling syntax enforcer

    match found_styling_sequence:
        # Sequences that where used
        case piece_types.TITLE1 | piece_types.TITLE2 | piece_types.TITLE3:
            # Sequences that can not be used anymore after this point 
            return [
                piece_types.BULLET, 
                piece_types.BLOCKQUOTE,
                piece_types.TITLE1,
                piece_types.TITLE2,
                piece_types.TITLE3,
            ]

    return []


def _construct_line(line_content: str):
    current_line = line(content=line_content)

    locked_styling_types: list = []
    for seq in current_line.content.split():
        # Set value to detect if no styling pattern matches
        seq_valid = False
        for current_styling_pattern in piece_seqences[styling_types.GLOBAL]:
            # If styling is locked, continue to next
            if current_styling_pattern in locked_styling_types: continue
            found_pattern = re.search(piece_seqences[styling_types.GLOBAL][current_styling_pattern], seq)

            if found_pattern: 
                seq_valid = True
                locked_styling_types.extend(update_locked_styling_types(found_styling_sequence=current_styling_pattern))

                match current_styling_pattern:
                    case piece_types.BLOCKQUOTE: 
                        for _ in range(len(seq)): current_line.append_styling_piece(piece_type=piece_types.BLOCKQUOTE)#
                    case _: current_line.append_styling_piece(piece_type=current_styling_pattern)

        # If no valid pattern found: stop searching global styling
        if not seq_valid: break


    # Specific styling detection

    return current_line

def parse(markdown_article_path: str) -> None:
    if not path.isfile(markdown_article_path): return None

    output: list = []
    with open(markdown_article_path, encoding="utf8", mode="r") as article_file:
        article: list = [line_content.strip() for line_content in article_file]

    for line_content in article:
        output.append(_construct_line(line_content))

    return output

if __name__ == "__main__":
    #parse("./test2.md")
    _construct_line(">>> - # Test")