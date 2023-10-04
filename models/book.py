import requests
from bs4 import BeautifulSoup


class Book:
    """Book model"""

    def __init__(self, url):
        """Initialize the Book class"""
        self.url = url
        self.book_informations = []

        """Parse product page informations"""
        # Parse the html content
        soup = self.get_soup(url)

        # Get product page informations
        product_page_url = url
        universal_product_code = soup.find(string="UPC").next_element.text
        title = soup.find("h1").text
        price_including_tax = soup.find(string="Price (incl. tax)").next_element.text
        price_excluding_tax = soup.find(string="Price (excl. tax)").next_element.text
        number_available = soup.find(string="Availability").next_element.next_element.text
        product_description = soup.find(id="product_description")

        if product_description:
            product_description = product_description.next_sibling.next_sibling.text
        else:
            product_description = "No description available"

        category = soup.find("ul", {"class": "breadcrumb"}).find_all("li")[-2].text.strip()
        review_rating = soup.find("p", {"class": "star-rating"})["class"][1]
        image_url = (
            soup.find("div", class_="carousel-inner")
            .find_next("img")["src"]
            .replace("../../", "http://books.toscrape.com/")
        )

        product_page_infos = [
            product_page_url,
            universal_product_code,
            title,
            price_including_tax,
            price_excluding_tax,
            number_available,
            product_description,
            category,
            review_rating,
            image_url,
        ]

        self.book_informations = product_page_infos

    def get_soup(self, url: str):
        """Get the html content of a page"""
        response = requests.get(url)
        return BeautifulSoup(response.content, "html.parser")

    def __repr__(self):
        """Return a string representation of the Book class"""
        return f"Book: {self.book_informations}"
