from enum import Enum


class SymbolType(Enum):
    UNKNOWN = 0
    PLAIN_TEXT = 1
    A_START = 2
    A_END = 3
    HTML_START = 4
    HTML_END = 5
    HEAD_START = 6
    HEAD_END = 7
    BODY_START = 8
    BODY_END = 9
    DOCTYPE = 10
    META = 11
    TITLE_START = 12
    TITLE_END = 13
    STYLE_START = 14
    STYLE_END = 15
    SCRIPT_START = 16
    SCRIPT_END = 17
    LINK = 18
    DIV_START = 19
    DIV_END = 20
    TABLE_START = 21
    TABLE_END = 22
    P_START = 23
    P_END = 24
    SPAN_START = 25
    SPAN_END = 26
    IMG = 27
    HEADER_START = 28
    HEADER_END = 29
    UL_START = 30
    UL_END = 31
    OL_START = 32
    OL_END = 33
    LI_START = 34
    LI_END = 35
    NAV_START = 36
    NAV_END = 37
    NOSCRIPT_START = 38
    NOSCRIPT_END = 39
    H1_START = 40
    H2_START = 41
    H3_START = 42
    H4_START = 43
    H5_START = 44
    H6_START = 45
    H1_END = 46
    H2_END = 47
    H3_END = 48
    H4_END = 49
    H5_END = 50
    H6_END = 51
    INPUT = 52
    SVG_START = 53
    SVG_END = 53
    TR_START = 54
    TR_END = 55
    TD_START = 56
    TD_END = 57
    TBODY_START = 58
    TBODY_END = 59
    CODE_START = 60
    CODE_END = 61
    PRE_START = 62
    PRE_END = 63
    FOOTER_START = 64
    FOOTER_END = 65
    FORM_START = 66
    FORM_END = 67
    BUTTON_START = 68
    BUTTON_END = 69
    THEAD_START = 70
    THEAD_END = 71
    TFOOT_START = 72
    TFOOT_END = 73
    COMMENT = 74
    SELECT_START = 75
    SELECT_END = 76
    OPTION_START = 77
    OPTION_END = 78
    BR = 79


class Symbol:
    def __init__(self):
        self.name = ""
        self.type = SymbolType.UNKNOWN
        self.attributes = {}
        self.content = ""
        self.position = -1

    def is_empty(self):
        return not self.name and not self.content and self.type == SymbolType.UNKNOWN
