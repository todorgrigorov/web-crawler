class NotFoundException(Exception):
    """ Error which indicates a missing web document (HTTP 404 code). """

    def __init__(self, message, url):
        super(NotFoundException, self).__init__(message)

        self.url = url


class SyntaxException(Exception):
    """ Error which indicates a syntax error in HTML document. """

    def __init__(self, position):
        super(SyntaxException, self).__init__(
            'Syntax error at position: %s' % position)


class TimeoutException(Exception):
    """ Error which indicates that a timeout has occurred. """
    pass
