from os import path
from typing import Union, Tuple

from thebrainrot_blog.markdown_handler.parse_markdown import (
    parse, 
    article,
    line
)
from thebrainrot_blog.markdown_handler.handler_config import (
    piece_styles,
    piece_types,
    styling_types,
    data_types,
    styling_association
)

#! Rewrite because O(c*l)
def _check_associated_styling(current_line: line, char_index: int) -> list[Tuple[piece_types, styling_association]]:
    associated_styling: list[Tuple[piece_types, styling_association]] = list()
    for styling_type in current_line.styling[styling_types.SPECIFIC]:
        if styling_type.index is None: continue

        if char_index == styling_type.index[0]: associated_styling.append((styling_type.style_type, styling_association.STARTS))
        elif char_index < styling_type.index[1] and char_index > styling_type.index[0]: associated_styling.append((styling_type.style_type, styling_association.CONTAINS))
        elif char_index == styling_type.index[1]: associated_styling.append((styling_type.style_type, styling_association.ENDS))

    return associated_styling

def render(markdown_path: str) -> None | str:
    html_out: str = str()
    if not path.isfile(markdown_path): return None

    article_out: Union[article, None] = parse(markdown_article_path=markdown_path)
    if article_out is None: return article_out

    open_styles: dict[styling_types, list[Tuple[piece_types, int]]] = {
        styling_types.GLOBAL: list(),
        styling_types.SPECIFIC: list()
    }

    for line_count, line in enumerate(article_out.lines):

        # Start with global styling types
        for current_style_type, styling_options in piece_styles[styling_types.GLOBAL].items():
            for global_styling in line.styling[styling_types.GLOBAL]:
                if global_styling.style_type is current_style_type:

                    match global_styling.style_type:
                        case piece_types.BLOCKQUOTE:
                            if (
                                line_count != 0 
                                and data_types.BLOCKQUOTE_DEEPNESS in article_out.lines[line_count-1].data.keys()
                                and article_out.lines[line_count-1].data[data_types.BLOCKQUOTE_DEEPNESS] is line.data[data_types.BLOCKQUOTE_DEEPNESS]
                            ): continue

                        case _: pass

                    for count, (element, style_class, condition) in enumerate(styling_options):
                        if condition is None or condition[0] in global_styling.data.keys() and condition[1] == global_styling.data[condition[0]]:
                            open_styles[styling_types.GLOBAL].append((global_styling.style_type, count))
                            html_out += f"<{element} {f"class='{style_class}'>" if style_class else ">"}"
                            break

        if len(line.content) == 0: html_out += "<br>"
        else:
            html_out += "<p>"
            for count, char in enumerate(line.content):
                char_written: bool = False
                associated_styling_pieces = _check_associated_styling(current_line=line, char_index=count)

                if len(associated_styling_pieces) == 0:
                    html_out += char
                    continue

                for styling_piece, association in associated_styling_pieces:
                        if association in [styling_association.ENDS, styling_association.STARTS]:
                            if association is styling_association.ENDS: html_out += char; char_written = True
                            html_out += f"<{"/" if association is styling_association.ENDS else ""}{piece_styles[styling_types.SPECIFIC][styling_piece][0][0]}{f" class='{piece_styles[styling_types.SPECIFIC][styling_piece][0][1]}'" if association is not styling_association.ENDS else ""}>"

                if not char_written: html_out += char

            html_out += "</p>"

        indexes_removed: list[int] = list()
        index: int = len(open_styles[styling_types.GLOBAL]) -1
        for to_close, styling_option_index in list(reversed(open_styles[styling_types.GLOBAL])):
            match to_close:
                case piece_types.BLOCKQUOTE:
                    if (
                        line_count != len(article_out.lines)
                        and data_types.BLOCKQUOTE_DEEPNESS in line.data.keys()
                        and data_types.BLOCKQUOTE_DEEPNESS in article_out.lines[line_count+1].data.keys()

                        and line.data[data_types.BLOCKQUOTE_DEEPNESS] is article_out.lines[line_count+1].data[data_types.BLOCKQUOTE_DEEPNESS]
                    ): continue
                case _: pass

            html_out += f"</{piece_styles[styling_types.GLOBAL][to_close][styling_option_index][0]}>"
            indexes_removed.append(index)
            index -= 1

        for index in indexes_removed: open_styles[styling_types.GLOBAL].pop(index)

    return html_out

if __name__ == "__main__":
    print(open("./src/thebrainrot_blog/templates/components/test.html", "w").write(str(render("./test.md"))))