"""
contains all the category related queries
"""

def get_categories_query():
    categories_query = "SELECT * FROM Categories;"

    return categories_query


def get_products_query(category_id):
    products_query = f"""   SELECT product_id, product_name, product_price, category_id
                            FROM Product
                            WHERE category_id={category_id};
                        """
    return products_query


def get_product_detail_query(product_id):
    product_detail_query = f""" SELECT *
                                FROM Product
                                WHERE product_id={product_id}
                            """

    return product_detail_query


def get_last_insert_id():
    return "SELECT LAST_INSERT_ID();"
