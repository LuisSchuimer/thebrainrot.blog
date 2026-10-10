from os import path
from typing import Union

from thebrainrot_blog.markdown_handler.parse_markdown import parse, article
from thebrainrot_blog.markdown_handler.handler_config import (
    piece_styles,
    piece_types,
    styling_types,
    data_types
)

def render(markdown_path: str) -> None | str:
    html_out: str = str()
    if not path.isfile(markdown_path): return None

    article_out: Union[article, None] = parse(markdown_article_path=markdown_path)
    if article_out is None: return article_out

    open_styles: dict[styling_types, list[piece_types]] = {
        styling_types.GLOBAL: list(),
        styling_types.SPECIFIC: list()
    }

    for line_count, line in enumerate(article_out.lines):

        # Start with global styling types
        for current_style_type, (element, style_class) in piece_styles[styling_types.GLOBAL].items():
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

                    open_styles[styling_types.GLOBAL].append(global_styling.style_type)
                    html_out += f"<{element} {f"class='{style_class}'>" if style_class else ">"}"

        html_out += f"<p>{line.content}</p>"

        indexes_removed: list[int] = list()
        index: int = len(open_styles[styling_types.GLOBAL]) -1
        for to_close in list(reversed(open_styles[styling_types.GLOBAL])):
            match to_close:
                case piece_types.BLOCKQUOTE:
                    if (
                        line_count != len(article_out.lines)
                        and data_types.BLOCKQUOTE_DEEPNESS in line.data.keys()
                        and data_types.BLOCKQUOTE_DEEPNESS in article_out.lines[line_count+1].data.keys()

                        and line.data[data_types.BLOCKQUOTE_DEEPNESS] is article_out.lines[line_count+1].data[data_types.BLOCKQUOTE_DEEPNESS]
                    ): continue
                case _: pass

            html_out += f"</{piece_styles[styling_types.GLOBAL][to_close][0]}>"
            indexes_removed.append(index)
            index -= 1

        for index in indexes_removed: open_styles[styling_types.GLOBAL].pop(index)

    return html_out

if __name__ == "__main__":
    print(open("./src/thebrainrot_blog/templates/components/test.html", "w").write(str(render("./test.md"))))