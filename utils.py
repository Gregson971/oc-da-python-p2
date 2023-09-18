import requests
from bs4 import BeautifulSoup
import os
from pandas import DataFrame as df


class Book_Scraper:
    """Class to scrape books.toscrape.com"""

    def __init__(self):
        pass

    def get_soup(self, url: str):
        response = requests.get(url)
        return BeautifulSoup(response.content, "html.parser")

    # Parse product page informations

    def parse_product_page_infos(self, url: str):
        # Parse the html content
        soup = self.get_soup(url)

        # Get product page informations
        product_page_url = url
        universal_product_code = soup.find(string="UPC").next_element.text
        title = soup.find("h1").text
        price_including_tax = soup.find(
            string="Price (incl. tax)").next_element.text
        price_excluding_tax = soup.find(
            string="Price (excl. tax)").next_element.text
        number_available = soup.find(
            string="Availability").next_element.next_element.text
        product_description = soup.find(
            id="product_description")

        if product_description:
            product_description = product_description.next_sibling.next_sibling.text
        else:
            product_description = "No description available"

        category = soup.find("ul", {"class": "breadcrumb"}
                             ).find_all("li")[-2].text.strip()
        review_rating = soup.find("p", {"class": "star-rating"})["class"][1]
        image_url = soup.find("div", class_="carousel-inner").find_next(
            "img")["src"].replace("../../", "http://books.toscrape.com/")

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
            image_url
        ]

        return product_page_infos

    # Parse category page

    def parse_category_page(self, category_page_url: str):
        books_urls = []
        product_page_infos = []

        soup = self.get_soup(category_page_url)

        category_name = soup.find("h1").text.strip()

        books = soup.find_all("h3")
        for book in books:
            books_urls.append(book.find_next("a")["href"].replace(
                "../../../", "http://books.toscrape.com/catalogue/"))

        # Check if there is a next page
        next_page = soup.find("li", {"class": "next"})

        if next_page:
            total_pages = soup.find(
                "li", {"class": "current"}).text.strip().split(" ")[3]
            for i in range(2, int(total_pages) + 1):
                pagination = "page-" + str(i) + ".html"
                soup = self.get_soup(
                    category_page_url.replace("index.html", pagination))
                books = soup.find_all("h3")
                for book in books:
                    books_urls.append(book.find_next("a")["href"].replace(
                        "../../../", "http://books.toscrape.com/catalogue/"))

        # Parse product page informations
        for book_url in books_urls:
            product_page_infos.append(
                self.parse_product_page_infos(book_url))

        print("Successful parsing of category: " + category_name + "")

        return category_name, product_page_infos

    # Parse all categories pages

    def parse_all_categories_pages(self, url: str):
        soup = self.get_soup(url)

        # Get all categories URLs
        categories_urls = []
        categories = soup.find(
            "ul", {"class": "nav nav-list"}).find("ul").find_all("a")
        for category in categories:
            categories_urls.append(category["href"].replace(
                "catalogue/category/books/", "http://books.toscrape.com/catalogue/category/books/"))

        return categories_urls

    # Load product page infos into a CSV file

    def load_product_page_data(self, category_name: str, row_headers: tuple, product_page_infos: list):
        format_category_name = category_name.replace(" ", "_").lower()
        path_directory = os.path.join(
            "data", format_category_name)
        os.makedirs(path_directory, exist_ok=True)
        csv_file_name = os.path.join(
            path_directory, f'{format_category_name}.csv')

        csv_data = df(product_page_infos, columns=row_headers)
        csv_data.to_csv(csv_file_name, index=False, header=True)

        print(f'Product page data loaded into: {csv_file_name}')

    # Download images

    def download_image(self, url: str, category_name: str, file_name: str):
        format_category_name = category_name.replace(" ", "_").lower()

        # Get the directory of the currently running script
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Specify the destination directory relative to the script directory
        path_name = os.path.join("data", format_category_name, "images")
        path_directory = os.path.join(script_directory, path_name)
        os.makedirs(path_directory, exist_ok=True)
        full_file_name = os.path.join(path_directory, file_name)

        response = requests.get(url)
        with open(full_file_name, 'wb') as file_image:
            file_image.write(response.content)

        print(f'Downloading image: {file_name}')
