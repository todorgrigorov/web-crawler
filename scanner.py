class Scanner:
    """ Provides reading of HTML content, represented as string. """

    def __init__(self, html):
        self.html = html
        self.char = ""
        self.index = -1
        self.set_next_char()

    def get_position(self):
        return self.index + 1

    def can_seek(self):
        return self.index < len(self.html)

    def set_next_char(self):
        self.index += 1
        if self.can_seek():
            self.char = self.html[self.index]

    def get_char(self):
        return self.char

    def skip_spaces(self):
        while self.can_seek() and self.char.isspace():
            self.set_next_char()

    def skip_to_letter(self):
        while self.can_seek() and not self.char.isalpha() and self.char != '>':
            self.set_next_char()

    def skip_to_char(self, char):
        while self.can_seek() and self.char.upper() != char.upper() and self.char != '>':
            self.set_next_char()

    def peek_next_char(self):
        return self.html[self.index + 1]
