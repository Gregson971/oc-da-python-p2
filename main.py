from utils import parse_product_page_infos, load_product_page_data

# URL to be scraped
url = 'http://books.toscrape.com/catalogue/wall-and-piece_971/index.html'

# Parse product page informations
product_page_infos = parse_product_page_infos(url)

# Define product page headers
product_page_headers = [
    "product_page_url",
    "universal_product_code",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"
]

# Load product page data
if __name__ == '__main__':
    load_product_page_data(
        "product_page.csv", product_page_headers, product_page_infos)
