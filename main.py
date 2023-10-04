from controllers.base import Controller
from views.base import View


def main():
    # URL to be scraped
    url = "http://books.toscrape.com/index.html"

    console_view = View()

    book_scraper = Controller(url, console_view)
    book_scraper.run()


if __name__ == '__main__':
    main()
