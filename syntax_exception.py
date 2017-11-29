class SyntaxException(Exception):
    """ Error which indicates a syntax error in HTML document. """

    def __init__(self, position):
        super(SyntaxException, self).__init__(
            'Syntax error at position: %s' % position)
