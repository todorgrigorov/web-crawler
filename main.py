from urllib.parse import urlparse
from crawler import Crawler
from termcolor import colored


def main():
    # REQUEST A ROOT STARTING POINT
    root_link = input("Enter the address of the root document: ")
    while not root_link:
        root_link = input("Enter the address of the root document: ")

    # VALIDATE THE INPUT
    if not urlparse(root_link).scheme:
        root_link = '{0}://{1}'.format('http', root_link)

    if not root_link.endswith('/'):
        root_link += '/'

    # START THE CRAWLING PROCESS
    crawler = Crawler()
    crawler.crawl(root_link)

    size = len(crawler.documents)
    if size > 0:
        # SOME DOCUMENTS WERE CRAWLED
        print(colored('Crawling successful.', 'green'))
        print('Documents: %s' % (len(crawler.documents)))

        # OUTPUT DEPENDENCIES BETWEEN DOCUMENTS (BY LINKS)
        for document in crawler.documents:
            if document.crawled_links:
                print('\n')
                print(colored(document.url, 'blue'))

                for link in document.crawled_links:
                    print(colored(link, 'cyan'))

        while True:
            # SEARCH BY INPUT WORDS UNTIL TERMINATED
            print('\n')
            search = input('Search: ')
            if search:
                print(colored('Searching for %s...' % (search), 'green'))
                print('\n')
                values = crawler.tree.find(search.upper())

                if values:
                    for value in values:
                        document = crawler.get_document_by_guid(
                            value.document_guid)

                        print('%s at position %s' %
                              (document.url, value.position))
                else:
                    print(colored('No results found for %s...' % (search), 'red'))


main()
