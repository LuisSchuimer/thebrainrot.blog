from os import path
from typing import Union

from thebrainrot_blog.markdown_handler.parse_markdown import parse, article
from thebrainrot_blog.markdown_handler.handler_config import (
    piece_styles,
    #piece_types,
    styling_types
)

def render(markdown_path: str) -> None | str:
    html_out: str = ""
    if not path.isfile(markdown_path): return None

    article_out: Union[article, None] = parse(markdown_article_path=markdown_path)
    if article_out is None: return article_out

    for line in article_out.lines:
        # Start with global styling types
        for html_style in piece_styles[styling_types.GLOBAL].keys():
            for global_styling in line.styling[styling_types.GLOBAL]:
                if global_styling.style_type is html_style:
                    pass

    return html_out