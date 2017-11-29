class NotFoundException(Exception):
    """ Error which indicates a missing web document (HTTP 404 code). """

    def __init__(self, message, url):
        super(NotFoundException, self).__init__(message)

        self.url = url
