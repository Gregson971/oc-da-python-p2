from utils import load_product_page_data, parse_category_page, parse_all_categories_pages, download_image


# URL to be scraped
url = "http://books.toscrape.com/index.html"

# Get all categories urls
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

if __name__ == '__main__':
    for category_url in categories_urls:
        # Parse categories product page data
        category_name, product_page_infos = parse_category_page(category_url)

        # Load category product page data
        load_product_page_data(
            category_name, product_page_headers, product_page_infos)

        # Download images
        for product_page_info in product_page_infos:
            image_url = product_page_info[-1]
            universal_product_code = product_page_info[1]
            file_name = universal_product_code + ".jpg"
            download_image(
                image_url, category_name, file_name)
