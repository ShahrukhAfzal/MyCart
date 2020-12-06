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


def add_category_query(category_name, category_description):
    add_category_query = f"""   INSERT INTO Categories (category_name, category_description)
                                VALUES ('{category_name}', '{category_description}');
                            """
    print(add_category_query)
    return add_category_query


def add_product_query(product_name, product_price, category_id):
    add_product_query = f"""INSERT INTO Product (product_name, product_price, category_id)
                            VALUES ('{product_name}', '{product_price}', '{category_id}');
                        """
    return add_product_query


def get_last_insert_id():
    return "SELECT LAST_INSERT_ID();"
