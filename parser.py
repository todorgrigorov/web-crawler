from urllib.parse import urlparse
from urllib.parse import urlsplit
from symbol import SymbolType
from scanner import Scanner
from tokenizer import Tokenizer
from analyzer import Analyzer
from document import Document
from document import Token
from timeout import Timeout


class Parser:
    """ Provides HTML document parsing functionalities. """

    MAX_ANALYZE_TIMEOUT = 5

    def __init__(self, url, html):
        self.document = Document(url)
        self.scanner = Scanner(html)
        self.tokenizer = Tokenizer(self.scanner)
        self.analyzer = Analyzer(self.tokenizer)
        self.symbol_position = 0

    def parse(self):
        analyzed = False
        with Timeout(Parser.MAX_ANALYZE_TIMEOUT):
            # stop if the analyze takes too long
            self.analyzer.analyze()
            analyzed = True

        if analyzed:
            for symbol in self.analyzer.symbols:
                if symbol.type == SymbolType.PLAIN_TEXT:
                    self.extract_text(symbol.content)
                elif symbol.type == SymbolType.META:
                    self.extract_meta(symbol)
                elif symbol.type == SymbolType.A_START:
                    self.extract_link(symbol)

    def is_punctuation(self, char):
        return char == '?' or char == '!' or char == '.' or char == ',' or char == '-' or char == ':'

    def extract_text(self, symbol_content):
        text = ""

        for char in symbol_content:
            if not char.isspace():
                if not self.is_punctuation(char):
                    # skip punctuation signs as they are not important
                    text += char.upper()
            elif text:
                # text might be empty if 2 or more spaces are next to each other
                self.symbol_position += 1
                self.add_token(self.symbol_position, text)
                text = ""

        if text:
            # also add the last token in the sequence as it might not end with space
            self.symbol_position += 1
            self.add_token(self.symbol_position, text)

    def add_token(self, position, text):
        token = Token()
        token.position = position
        token.text = text
        token.document_guid = self.document.guid
        self.document.tokens.append(token)

    def extract_meta(self, symbol):
        if 'name' in symbol.attributes:
            name = symbol.attributes['name']

            if name == 'keywords' and 'content' in symbol.attributes:
                self.extract_text(symbol.attributes['content'])

            if name == 'description' and 'content' in symbol.attributes:
                self.extract_text(symbol.attributes['content'])

    def link_valid(self, link):
        return ('#' not in link and
                'javascript:' not in link and
                not link.endswith('.jpg') and
                not link.endswith('.jpeg') and
                not link.endswith('.pptx') and
                not link.endswith('.ppt') and
                not link.endswith('.png') and
                not link.endswith('.pdf') and
                not link.endswith('.ppsx'))

    def extract_link(self, symbol):
        if 'href' in symbol.attributes:
            url = symbol.attributes['href']

            if self.link_valid(url):
                if not urlparse(url).netloc:
                    # url is relative
                    slash = '/'
                    if url.startswith('/'):
                        slash = ''

                    self.document.links.append(
                        '{0.scheme}://{0.netloc}{1}{2}'.format(
                            urlsplit(self.document.url),
                            slash,
                            url))
                else:
                    # url is absolute
                    if not urlparse(url).scheme:
                        self.document.links.append(
                            '{0.scheme}:{1}'.format(urlsplit(self.document.url), url))
                    else:
                        self.document.links.append(url)
