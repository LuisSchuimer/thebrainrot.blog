from enum import Enum
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

class styling_types(Enum):
    """
        styling types defines the scope where styling is applied at

        Global: styling applied on the entire line
        Specific: styling only applied on surtain parts of a line
    """

    GLOBAL = "global"
    SPECIFIC = "specific"

class data_types(Enum):
    """
        data types that can be used on specific styling types that 
        may include image urls or links
    """

    URL = "url"
    LINKTO = "linkto"
    TITLE_SIZE = "title size"
    TITLE_ID = "title_id"


"Regex identification codes for all piece types"
piece_seqences = {
    styling_types.GLOBAL: {
        piece_types.BLOCKQUOTE: r"^>.*",
        piece_types.TITLE: r"^[#]{1,6}$",
        piece_types.BULLET: r"^-",
        piece_types.HORIZONTAL_RULES: r"^\s*\*\*\*\s*$"
    },
    styling_types.SPECIFIC: {
        piece_types.BOLD: r"[\*]{2}",
        piece_types.TITLE_ID: r"{(#[a-zA-Z0-9_]+)}",
        piece_types.ITALIC: r"(?<!\*)\*(?!\*)",
        piece_types.STRIKETHROUGH: r"[~]{2}",
        piece_types.HIGHLIGHT: r"[=]{2}",
        piece_types.URL: r"(https)?:\/\/?[\da-z\.-]+\.[a-z]{2,6}[\/\w\.-]*\/?",
        piece_types.HREF: r"(\[)([a-zA-Z0-9\s.]+)(\]\((https?:\/\/?[\da-z\.-]+\.[a-z]{2,6}[\/\w\.-]*\/?)?\))"
    }
}
