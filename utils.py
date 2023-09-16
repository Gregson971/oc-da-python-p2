import requests
from bs4 import BeautifulSoup
import csv
import os

# Parse product page informations


def parse_product_page_infos(url):
    # Make a GET request to fetch the raw HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse the html content
    soup = BeautifulSoup(html_content, "html.parser")

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

def parse_category_page(category_page_url):
    books_urls = []
    product_page_infos = []

    response = requests.get(category_page_url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

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
            response = requests.get(
                category_page_url.replace("index.html", pagination))
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")
            books = soup.find_all("h3")
            for book in books:
                books_urls.append(book.find_next("a")["href"].replace(
                    "../../../", "http://books.toscrape.com/catalogue/"))

    # Parse product page informations
    for book_url in books_urls:
        product_page_infos.append(parse_product_page_infos(book_url))

    return category_name, product_page_infos


# Parse all categories pages


def parse_all_categories_pages(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    # Get all categories URLs
    categories_urls = []
    categories = soup.find(
        "ul", {"class": "nav nav-list"}).find("ul").find_all("a")
    for category in categories:
        categories_urls.append(category["href"].replace(
            "catalogue/category/books/", "http://books.toscrape.com/catalogue/category/books/"))

    return categories_urls


# Download images


def download_image(url, path_name, file_name):
    # Get the directory of the currently running script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Specify the destination directory relative to the script directory
    path_directory = os.path.join(script_directory, path_name)
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)

    full_file_name = os.path.join(path_directory, file_name)

    file_image = open(full_file_name, 'wb')
    response = requests.get(url)
    file_image.write(response.content)
    file_image.close()
    print("Successful download of image: " + file_name + "")


# Load product page infos into a CSV file


def load_product_page_data(file_name, row_headers, product_page_infos):
    # Get the directory of the currently running script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Specify the destination directory relative to the script directory
    path_directory = os.path.join(script_directory, "csv_files")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)

    full_file_name = os.path.join(path_directory, file_name)

    with open(full_file_name, 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(row_headers)
        for product_page_info in product_page_infos:
            writer.writerow(product_page_info)
    print("Product page data loaded into: " + file_name + "")
