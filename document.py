import uuid


class Token:
    """ Represents a plain text word. """

    def __init__(self):
        self.text = ""
        self.position = -1
        self.document_guid = None

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text

    def __eq__(self, other):
        return self.text == other.text


class Document:
    """ Represents a crawled HTML document. """

    def __init__(self, url):
        self.guid = uuid.uuid4()
        self.url = url
        self.links = []
        self.crawled_links = []
        self.tokens = []

    def __eq__(self, other):
        return self.url == other.url or self.guid == other.guid
