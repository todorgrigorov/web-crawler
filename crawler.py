from parser import Parser
from fetcher import Fetcher
from tree import Tree
from document import Document
from requests.exceptions import InvalidSchema
from requests.exceptions import ConnectionError
from requests.exceptions import MissingSchema
from not_found_exception import NotFoundException
from syntax_exception import SyntaxException
from termcolor import colored
from timeout_exception import TimeoutException


class Crawler:
    """ Scans through websites via HTTP GET requests and recursion.  """

    MAX_DEPTH = 1

    def __init__(self):
        self.fetcher = Fetcher()
        self.tree = Tree()
        self.documents = []

    def get_document_by_guid(self, guid):
        for document in self.documents:
            if document.guid == guid:
                return document

    def crawl(self, url, current_depth=0):
        if self.fetcher.url_valid(url):
            try:
                html = self.fetcher.fetch(url)
                parser = Parser(url, html)
                parser.parse()

                self.documents.append(parser.document)
                for token in parser.document.tokens:
                    self.tree.add(token.text, token)

                print(colored('Document crawled successfully.', 'green'))
                print('URL: %s' % (parser.document.url))
                print('Tokens: %s' % (len(parser.document.tokens)))
                print('Links: %s' % (len(parser.document.links)))
                print('\n')

                # the depth increases with each subsequent crawl call
                if current_depth <= Crawler.MAX_DEPTH:
                    for link in parser.document.links:
                        if Document(link) not in self.documents:
                            # NOTE: this is not 100% guarantee that the same document will not be crawled again,
                            #       as there are many ways to forward DNS to the same page...
                            self.crawl(link, current_depth + 1)

                            # if crawling has been successful, then append the link as crawled
                            parser.document.crawled_links.append(link)
            except (MissingSchema, InvalidSchema):
                print(colored('Invalid URL specified.', 'red'))
                print('URL: %s' % (url))
                print('\n')
            except NotFoundException:
                print(colored('Document not found.', 'red'))
                print('URL: %s' % (url))
                print('\n')
            except ConnectionError:
                print(colored('Error while crawling document.', 'red'))
                print('URL: %s' % (url))
                print('\n')
            except (SyntaxException, RecursionError):
                print(colored('Error while parsing document.', 'red'))
                print('URL: %s' % (url))
                print('\n')
            except TimeoutException:
                print(colored('Document took too long to process.', 'red'))
                print('URL: %s' % (url))
                print('\n')
        else:
            print(colored('Invalid URL specified.', 'red'))
            print('URL: %s' % (url))
            print('\n')
