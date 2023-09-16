import requests
from bs4 import BeautifulSoup
import csv

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
        id="product_description").next_sibling.next_sibling.text

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


# Load product page infos into a CSV file

def load_product_page_data(file_name, header, product_page_infos):
    with open(file_name, 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(header)
        writer.writerow(product_page_infos)
    print("Product page data loaded into a CSV file")
