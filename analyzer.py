from symbol import Symbol
from symbol import SymbolType


class Analyzer:
    """ Analyzes the correctness of recieved HTML tokens. """

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.symbols = []

        size = len(self.symbols)
        while size == 0:
            # try adding symbols until the collection is not empty
            self.add_symbol()
            size = len(self.symbols)

    def analyze(self):
        while self.last_symbol_type() != SymbolType.HTML_END:
            self.add_symbol()

    def add_symbol(self):
        symbol = Symbol()
        size = len(self.symbols)

        if size > 0:
            last = self.symbols[-1]

            # if the previous tag has started a script or a style,
            # do not include the contents of those tags as they
            # are large and unnecessary
            # NOTE: this does not skip inline tags
            if last.type == SymbolType.SCRIPT_START or last.type == SymbolType.STYLE_START:
                symbol = self.tokenizer.get_next_symbol()

                while (symbol.type == SymbolType.SCRIPT_START or
                       symbol.type == SymbolType.STYLE_START or
                       symbol.type == SymbolType.SCRIPT_END or
                       symbol.type == SymbolType.STYLE_END or
                       symbol.type == SymbolType.PLAIN_TEXT):
                    symbol = self.tokenizer.get_next_symbol()
            else:
                symbol = self.tokenizer.get_next_symbol()
        else:
            symbol = self.tokenizer.get_next_symbol()

            # do not add symbols until a start of the document has been reached
            # the start it represented as DOCTYPE tag
            if symbol.type != SymbolType.DOCTYPE:
                symbol = Symbol.empty()

        if not symbol.is_empty():
            # might be empty when the end of the HTML has been reached
            self.symbols.append(symbol)

    def last_symbol_type(self):
        return self.symbols[-1].type
