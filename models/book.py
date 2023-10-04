class Book:
    """Book model"""

    def __init__(self, product_page_infos):
        """Initialize the Book class"""
        self.product_page_infos = product_page_infos

    def __repr__(self):
        """Return a string representation of the Book class"""
        return f"Book: {self.product_page_infos}"
