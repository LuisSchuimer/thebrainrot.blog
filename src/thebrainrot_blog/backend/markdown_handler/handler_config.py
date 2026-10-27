from enum import Enum
from typing import Tuple, Union
class piece_types(Enum):
    """
    piece_types defines the global and specific types of applied styling
    """

    TITLE = "title"
    BLOCKQUOTE = "blockquote"
    BULLET = "bullet"
    HORIZONTAL_RULES = "horizontal rules"

    BOLD = "bold"
    ITALIC = "italic"
    STRIKETHROUGH = "strikethrough"
    HIGHLIGHT = "highlight"
    URL = "url"
    TITLE_ID = "title id"
    HREF = "href"
    TASK = "task"

    DUMMY = "dummy"

class styling_types(Enum):
    """
        styling types defines the scope where styling is applied at

        Global: styling applied on the entire line
        Specific: styling only applied on surtain parts of a line
    """

    GLOBAL = "global"
    SPECIFIC = "specific"

class styling_association(Enum):
    """
        Defines the association a piece of text has to a styling type
    """

    STARTS = "starts"
    ENDS = "ends"
    CONTAINS = "contains"

class data_types(Enum):
    """
        data types that can be used on specific styling types that 
        may include image urls or links
    """

    REFERENCE = "reference"
    CHECKED = "checked"
    HAS_TASK = "has_tast"
    TITLE_SIZE = "title_size"
    BLOCKQUOTE_DEEPNESS = "blockquote_deepness"


"Regex identification codes for all piece types"
piece_seqences: dict[styling_types, dict[piece_types, str]] = {
    styling_types.GLOBAL: {
        piece_types.BLOCKQUOTE: r"^>.*",
        piece_types.TITLE: r"^[#]{1,6}$",
        piece_types.BULLET: r"^-",
        piece_types.HORIZONTAL_RULES: r"^\*\*\*$"
    },
    styling_types.SPECIFIC: {
        piece_types.BOLD: r"[\*]{2}",
        piece_types.TITLE_ID: r"{(#[a-zA-Z0-9_]+)}",
        piece_types.ITALIC: r"(?<!\*)\*(?!\*)",
        piece_types.STRIKETHROUGH: r"[~]{2}",
        piece_types.HIGHLIGHT: r"[=]{2}",
        piece_types.URL: r"(?<!\]\()https?:\/\/[\da-z\.-]+\.[a-z]{2,6}[\/\w\.-]*\/?",
        piece_types.HREF: r"(\[)([a-zA-Z0-9\s.]+)(\]\((https?:\/\/?[\da-z\.-]+\.[a-z]{2,6}[\/\w\.-]*\/??|#[a-zA-Z0-9_]+)\))",
        piece_types.TASK: r'\[([x ])\]\s'
    }
}

# global or specific styling -> (piece type, (element, styling, if needed condition))
piece_styles: dict[styling_types, dict[piece_types, list[Tuple[str, Union[str, None], Union[Tuple[data_types, int], None]]]]] = {
    styling_types.GLOBAL: {
        piece_types.BLOCKQUOTE: [('div', 'p-4 bg-neutral-400 border border-solid rounded', None)],
        piece_types.TITLE: [
            ('div', "text-3xl font-bold", (data_types.TITLE_SIZE, 1)),
            ("div", "text-2xl font-bold", (data_types.TITLE_SIZE, 2)),
            ("div", "text-xl font-bold", (data_types.TITLE_SIZE, 3)),
            ("div", "text-lg font-bold", (data_types.TITLE_SIZE, 4)),
            ("div", "font-extrabold", (data_types.TITLE_SIZE, 5)),
            ("div", "font-bold", (data_types.TITLE_SIZE, 6)),
        ]
    },
    styling_types.SPECIFIC: {
        piece_types.BOLD: [("span", "font-bold", None)],
        piece_types.ITALIC: [("span", "italic", None)],
        piece_types.STRIKETHROUGH: [("span", "line-through", None)],
        piece_types.HIGHLIGHT: [("span", "text-yellow-600", None)]
    }
}