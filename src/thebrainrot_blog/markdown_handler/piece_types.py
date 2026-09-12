from enum import Enum

class piece_types(Enum):
    TITLE1 = "title1"
    TITLE2 = "title2"
    TITLE3 = "title3"
    BULLET = "bullet"
    BOLD = "bold"
    ITALIC = "italic"
    BLOCKQUOTE = "blockquote"

class styling_types(Enum):
    GLOBAL = "global"
    SPECIFIC = "specific"

class data_types(Enum):
    URL = "url"
    LINKTO = "linkto"

piece_seqences = {
    styling_types.GLOBAL: {
        piece_types.BLOCKQUOTE: r"^>.*",
        piece_types.TITLE1: r"^[#]{1}$",
        piece_types.TITLE2: r"^[#]{2}$",
        piece_types.TITLE3: r"^[#]{3}$",
        piece_types.BULLET: r"^-",
    },
    styling_types.SPECIFIC: {
        piece_types.BOLD: r"[*]{2}",
        piece_types.ITALIC: r"[1]{1}",
    }
}
