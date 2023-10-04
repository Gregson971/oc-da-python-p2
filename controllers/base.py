import requests
from bs4 import BeautifulSoup
import os
from pandas import DataFrame as df

from models.category import Category

# Define product page headers
PRODUCT_PAGE_HEADERS = (
    "product_page_url",
    "universal_product_code",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url",
)


class Controller:
    """Controller class"""

    def __init__(self, url: str, view):
        """Initialize the Controller class"""
        self.url = url
        self.view = view

    def get_soup(self, url: str):
        """Get the html content of a page"""
        response = requests.get(url)
        return BeautifulSoup(response.content, "html.parser")

    def parse_all_categories_pages(self, url: str):
        """Parse all categories pages"""
        soup = self.get_soup(url)

        # Get all categories URLs
        categories_urls = []
        categories = soup.find("ul", {"class": "nav nav-list"}).find("ul").find_all("a")
        for category in categories:
            categories_urls.append(
                category["href"].replace(
                    "catalogue/category/books/", "http://books.toscrape.com/catalogue/category/books/"
                )
            )

        return categories_urls

    def load_product_page_data(self, category_name: str, row_headers: tuple, product_page_infos: list):
        """Load product page data into a CSV file"""
        format_category_name = category_name.replace(" ", "_").lower()
        path_directory = os.path.join("data", format_category_name)
        os.makedirs(path_directory, exist_ok=True)
        csv_file_name = os.path.join(path_directory, f'{format_category_name}.csv')

        csv_data = df(product_page_infos, columns=row_headers)
        csv_data.to_csv(csv_file_name, index=False, header=True)

        self.view.show_message(f'Product page data loaded into: {csv_file_name}')

    def download_image(self, url: str, category_name: str, file_name: str):
        """Download image from a URL"""
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

        self.view.show_message(f'Downloading image: {file_name}')

    def run(self):
        """Run the main program"""
        # Get all categories urls
        categories_urls = self.parse_all_categories_pages(self.url)

        for category_url in categories_urls:
            category = Category(category_url)
            self.view.show_message(f"Successful parsing of category: {category.category_name}")

            # Load category product page data
            self.load_product_page_data(category.category_name, PRODUCT_PAGE_HEADERS, category.product_page_infos)

            # Download images
            for product_page_info in category.product_page_infos:
                image_url = product_page_info[-1]
                universal_product_code = product_page_info[1]
                file_name = universal_product_code + ".jpg"
                self.download_image(image_url, category.category_name, file_name)
