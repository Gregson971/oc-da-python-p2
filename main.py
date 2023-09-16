from utils import load_product_page_data, parse_category_page

# URL to be scraped
category_page_url = "http://books.toscrape.com/catalogue/category/books/default_15/index.html"

# Define product page headers
product_page_headers = (
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
)

category_name, product_page_infos = parse_category_page(category_page_url)

csv_file_name = category_name.replace(" ", "_").lower() + ".csv"

# Load category product page data
if __name__ == '__main__':
    load_product_page_data(
        csv_file_name, product_page_headers, product_page_infos)
