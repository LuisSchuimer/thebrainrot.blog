from os import path
from typing import Union, Tuple

from thebrainrot_blog.backend.markdown_handler.parse_markdown import (
    parse, 
    article,
    line
)
from thebrainrot_blog.backend.markdown_handler.handler_config import (
    piece_styles,
    piece_types,
    styling_types,
    data_types,
    styling_association
)

def render(markdown_path: str) -> None | str:
    html_out: str = str()
    if not path.isfile(markdown_path): return None

    article_out: Union[article, None] = parse(markdown_article_path=markdown_path)
    if article_out is None: return article_out

    open_styles: dict[styling_types, list[Tuple[piece_types, int]]] = {
        styling_types.GLOBAL: list(),
        styling_types.SPECIFIC: list()
    }

    return html_out