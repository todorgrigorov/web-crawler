from symbol import Symbol
from symbol import SymbolType


class Tokenizer:
    """ Provides functionalities for splitting HTML document into string tokens. """

    def __init__(self, scanner):
        self.scanner = scanner

    def is_alphanumeric(self):
        return self.scanner.char.isalpha() or self.scanner.char.isdigit()

    def is_quote(self):
        return self.scanner.char == '\'' or self.scanner.char == '"'

    def is_open_tag(self):
        return self.scanner.char == '<'

    def is_close_tag(self):
        return self.scanner.char == '>'

    def set_tag(self, symbol):
        while self.scanner.can_seek() and self.is_alphanumeric():
            symbol.name += self.scanner.char.lower()
            self.scanner.set_next_char()

    def set_text(self, symbol):
        while self.scanner.can_seek() and not self.is_open_tag():
            symbol.content += self.scanner.char
            self.scanner.set_next_char()

    def set_attributes(self, symbol):
        self.scanner.skip_to_letter()

        if not self.is_close_tag():
            attribute_name = ""
            attribute_value = ""

            while self.scanner.can_seek() and self.scanner.char != '=' and not self.scanner.char.isspace():
                attribute_name += self.scanner.char
                self.scanner.set_next_char()

            self.scanner.set_next_char()

            if self.is_quote():
                next_char = self.scanner.peek_next_char()
                if next_char == '#':
                    self.scanner.skip_to_char('#')
                elif next_char == '/':
                    self.scanner.skip_to_char('/')
                else:
                    self.scanner.skip_to_letter_or_digit()

                while self.scanner.can_seek() and not self.is_quote() and not self.is_close_tag():
                    attribute_value += self.scanner.char
                    self.scanner.set_next_char()

            symbol.attributes[attribute_name] = attribute_value

            self.set_attributes(symbol)

    def set_start_tag_type(self, tag):
        try:
            tag.type = SymbolType['%s_START' % (tag.name.upper())]
        except KeyError:
            try:
                tag.type = SymbolType[tag.name.upper()]
            except KeyError:
                tag.type = SymbolType.UNKNOWN

    def set_end_tag_type(self, tag):
        try:
            tag.type = SymbolType['%s_END' % (tag.name.upper())]
        except KeyError:
            tag.type = SymbolType.UNKNOWN

    def get_next_symbol(self):
        symbol = Symbol()
        symbol.type = SymbolType.UNKNOWN

        self.scanner.skip_spaces()

        if self.is_open_tag():
            self.scanner.set_next_char()

            if self.scanner.char == '!':
                next_char = self.scanner.peek_next_char()

                if next_char.upper() == 'D':
                    symbol.type = SymbolType.DOCTYPE

                    self.scanner.skip_to_char('>')
                    self.scanner.set_next_char()
                elif next_char == '-':
                    symbol.type = SymbolType.COMMENT

                    while self.scanner.char != '-' and next_char != '>':
                        self.scanner.skip_to_char('-')
                        next_char = self.scanner.peek_next_char()

                    self.scanner.set_next_char()

            elif self.scanner.char == '/':
                self.scanner.set_next_char()

                self.set_tag(symbol)
                self.set_end_tag_type(symbol)

                self.scanner.skip_to_char('>')
                self.scanner.set_next_char()
            else:
                self.set_tag(symbol)
                self.set_start_tag_type(symbol)

                self.set_attributes(symbol)

                self.scanner.skip_to_char('>')
                self.scanner.set_next_char()
        else:
            self.set_text(symbol)
            symbol.type = SymbolType.PLAIN_TEXT

            self.scanner.skip_to_char('<')

        return symbol
