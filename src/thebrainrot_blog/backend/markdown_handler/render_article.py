from os import path
from typing import Union, Tuple

from thebrainrot_blog.backend.markdown_handler.parse_markdown import (
    parse, 
    article,
    line,
    tree_node
)
from thebrainrot_blog.backend.markdown_handler.handler_config import (
    piece_styles,
    piece_types,
    styling_types,
    data_types
)
from thebrainrot_blog.utils import search_in_tree

def get_next_line(path: tree_node, index: int = 0) -> tuple[line | None, tree_node]:
    if (found_line := search_in_tree(path=path, to_find_index=index)) != None:
        return (found_line, path)
    
    return (None, path)

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