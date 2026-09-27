"Markdown to HTML parser as part of thebrainrot.blog written by Luis Schuimer"

from os import path
import re
from typing import Union, Tuple

from thebrainrot_blog.markdown_handler.piece_types import (
    piece_types,
    piece_seqences,
    styling_types,
    data_types
)
from thebrainrot_blog.utils import index_offset

class piece:
    def __init__(self,
        style_type: piece_types,
        index: Union[Tuple[int, int], None] = None,
        data: dict[data_types, str] = {}
    ):
        self.style_type: piece_types = style_type
        self.index: Union[Tuple[int, int], None] = index
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

    def delete_indexes_from_content(self, *indexes: Tuple[int,int]) -> None:
        for index in indexes: 
            for styling_type in self.styling[styling_types.SPECIFIC]:
                if styling_type.index is None: continue
                styling_type.index = index_offset(styling_type.index, indexes_to_be_removed=[index])

            self.content = self.content[:index[0]] + self.content[index[1]:]

    def append_styling_piece(self, 
            piece_type: piece_types, 
            index: Union[Tuple[int, int], None] = None, 
            data: dict[data_types, str] = {}) -> bool:
        
        if piece_type in piece_seqences[styling_types.GLOBAL].keys():
            self.styling[styling_types.GLOBAL].append(piece(style_type=piece_type, data=data))
            return True
        else:
            if index is not None:
                self.styling[styling_types.SPECIFIC].append(piece(
                    style_type=piece_type,
                    index=index,
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

    current_line.content = " ".join(current_line_content_list)

    # Specific styling detection
    for current_styling_pattern in piece_seqences[styling_types.SPECIFIC]:
        matches: list[re.Match[str]] = [match for match in re.finditer(piece_seqences[styling_types.SPECIFIC][current_styling_pattern], current_line.content)]

        match current_styling_pattern:
            # If url type seen continue with only adding a styling type to it
            case piece_types.URL:
                for match in matches:
                    current_line.append_styling_piece(
                        piece_type=current_styling_pattern,
                        index=(match.start(), match.end()-1)
                    )
                continue

            # If title id (like {#test}) is seen continue with this
            case piece_types.TITLE_ID:
                if not matches: continue

                for styling_type in current_line.styling[styling_types.GLOBAL]:
                    if styling_type.style_type is piece_types.TITLE: 
                        styling_type.append_data_to_piece(data_type=data_types.TITLE_ID, value=matches[0].group(1))

                        current_line.delete_indexes_from_content(
                            (matches[0].start(), matches[0].end()), 
                        )
                continue

            case piece_types.HREF:
                prev_seq: list[Tuple[int,int]] = []
                for match in matches:
                    prev_seq.append(index_offset((match.start(1), match.end(1)), indexes_to_be_removed=prev_seq))
                    prev_seq.append(index_offset((match.start(3), match.end(3)), indexes_to_be_removed=prev_seq))

                    current_line.append_styling_piece(
                        piece_type=piece_types.HREF,
                        index=(match.start(2), match.end(2) -1),
                        data={data_types.URL: match.group(4)}
                    )

                    current_line.delete_indexes_from_content(
                        prev_seq[-2],
                        prev_seq[-1]
                    )
                continue

            case _:
                prev_seq: list[Tuple[int, int]] = []
                for group in [(matches[i-1], matches[i]) for i in range(1, len(matches), 2)]:
                    prev_seq.append(index_offset((group[0].start(), group[0].end()), indexes_to_be_removed=prev_seq))
                    prev_seq.append(index_offset((group[1].start(), group[1].end()), indexes_to_be_removed=prev_seq))

                    current_line.append_styling_piece(
                        piece_type=current_styling_pattern,
                        index=(prev_seq[-2][0], prev_seq[-1][0] -1)
                    )

                    current_line.delete_indexes_from_content(
                        prev_seq[-2], 
                        prev_seq[-1]
                    )
                continue

    return current_line

def parse(markdown_article_path: str) -> list[line] | None:
    if not path.isfile(markdown_article_path): return None

    with open(markdown_article_path, encoding="utf8", mode="r") as article_file:
        article: list[str] = [line_content.strip() for line_content in article_file]

    return [construct_line(content) for content in article]

if __name__ == "__main__":
    #out = parse("./README.md")
    #print(out)
    out = construct_line("**hello from** [test link](https://google.com)")
    print(out.content)
    print([styling.index for styling in out.styling[styling_types.SPECIFIC]])