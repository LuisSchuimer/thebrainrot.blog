from enum import Enum
class piece_types(Enum):
    """
    piece_types defines the global and specific types of applied styling
    """

    TITLE1 = "title1"
    TITLE2 = "title2"
    TITLE3 = "title3"
    BULLET = "bullet"
    BOLD = "bold"
    ITALIC = "italic"
    BLOCKQUOTE = "blockquote"
    STRIKETHROUGH = "strikethrough"
    HIGHLIGHT = "highlight"

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


"Regex identification codes for all piece types"
piece_seqences = {
    styling_types.GLOBAL: {
        piece_types.BLOCKQUOTE: r"^>.*",
        piece_types.TITLE1: r"^[#]{1}$",
        piece_types.TITLE2: r"^[#]{2}$",
        piece_types.TITLE3: r"^[#]{3}$",
        piece_types.BULLET: r"^-",
    },
    styling_types.SPECIFIC: {
        piece_types.BOLD: r"[\*]{2}",
        piece_types.ITALIC: r"(?<!\*)\*(?!\*)",
        piece_types.STRIKETHROUGH: r"[~]{2}",
        piece_types.HIGHLIGHT: r"[=]{2}"
    }
}
