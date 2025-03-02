import requests
from bs4 import BeautifulSoup

from models.book import Book


class Category:
    """Class to create a category object"""

    def __init__(self, category_page_url):
        """Initialize the Categories class"""
        self.category_page_url = category_page_url
        self.category_name = ""
        self.categories_urls = []
        self.product_page_infos = []

        """Parse category page informations"""
        books_urls = []
        product_page_infos = []

        soup = self.get_soup(category_page_url)

        category_name = soup.find("h1").text.strip()

        books = soup.find_all("h3")
        for book in books:
            books_urls.append(book.find_next("a")["href"].replace("../../../", "http://books.toscrape.com/catalogue/"))

        # Check if there is a next page
        next_page = soup.find("li", {"class": "next"})

        if next_page:
            total_pages = soup.find("li", {"class": "current"}).text.strip().split(" ")[3]
            for i in range(2, int(total_pages) + 1):
                pagination = "page-" + str(i) + ".html"
                soup = self.get_soup(category_page_url.replace("index.html", pagination))
                books = soup.find_all("h3")
                for book in books:
                    books_urls.append(
                        book.find_next("a")["href"].replace("../../../", "http://books.toscrape.com/catalogue/")
                    )

        # Parse product page informations
        for book_url in books_urls:
            book_informations = Book(book_url).book_informations
            product_page_infos.append(book_informations)

        self.category_name = category_name
        self.product_page_infos = product_page_infos

    def get_soup(self, url: str):
        """Get the html content of a page"""
        response = requests.get(url)
        return BeautifulSoup(response.content, "html.parser")

    def __repr__(self):
        """Return a string representation of the Category class"""
        return f"Category: {self.category_name}"
