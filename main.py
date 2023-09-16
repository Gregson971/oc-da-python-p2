from utils import load_product_page_data, parse_category_page, parse_all_categories_pages

# URL to be scraped
url = "http://books.toscrape.com/index.html"

# Parse all categories pages
categories_urls = parse_all_categories_pages(url)

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

# Load categories product page data
for category_url in categories_urls:
    category_name, product_page_infos = parse_category_page(category_url)

    csv_file_name = category_name.replace(" ", "_").lower() + ".csv"

    # Load category product page data
    if __name__ == '__main__':
        load_product_page_data(
            csv_file_name, product_page_headers, product_page_infos)
