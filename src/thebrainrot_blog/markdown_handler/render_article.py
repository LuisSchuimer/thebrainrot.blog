from os import path
from typing import Union

from thebrainrot_blog.markdown_handler.parse_markdown import parse, article
from thebrainrot_blog.markdown_handler.handler_config import (
    piece_styles,
    piece_types,
    styling_types
)

def render(markdown_path: str) -> None | str:
    html_out: str = str()
    if not path.isfile(markdown_path): return None

    article_out: Union[article, None] = parse(markdown_article_path=markdown_path)
    if article_out is None: return article_out

    for line in article_out.lines:
        open_styles: dict[styling_types, list[piece_types]] = {
            styling_types.GLOBAL: list(),
            styling_types.SPECIFIC: list()
        }

        # Start with global styling types
        for current_style_type, (element, style_class) in piece_styles[styling_types.GLOBAL].items():
            for global_styling in line.styling[styling_types.GLOBAL]:
                if global_styling.style_type is current_style_type:
                    open_styles[styling_types.GLOBAL].append(global_styling.style_type)
                    html_out += f"<{element} {f"class='{style_class}'>" if style_class else ">"}"

        html_out += line.content

        for to_close in list(reversed(open_styles[styling_types.GLOBAL])):
            html_out += f"</{piece_styles[styling_types.GLOBAL][to_close][0]}>"

        open_styles[styling_types.GLOBAL].clear()

    return html_out

if __name__ == "__main__":
    print(render("./test.md"))