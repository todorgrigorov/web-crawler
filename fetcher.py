from urllib.parse import urlparse
import requests
from exceptions import NotFoundException


class Fetcher:
    """ Retrieves the HTML content of a page via HTTP requests. """

    def url_valid(self, url):
        return bool(urlparse(url).netloc)

    def fetch(self, url):
        """ Returns the HTML content of the URL. """
        response = requests.get(url)
        if response.status_code == 404:
            raise NotFoundException('URL not found: %s' % (url), url)
        else:
            return response.text
