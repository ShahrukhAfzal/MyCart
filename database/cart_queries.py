"""
contains all the cart related queries
"""

def create_cart_query(user_id):
    create_cart_query = f"""INSERT INTO Cart (user_id) VALUES ({user_id})"""

    return create_cart_query


def get_cart_id_query(user_id):
    cart_id_query = f"""SELECT cart_id FROM Cart WHERE user_id={user_id}"""

    return cart_id_query


def get_cart_prod_details_query(cart_id, product_id):
    cart_prod_details_query = f"""  SELECT cart_prod_id, quantity
                                    FROM cart_product
                                    WHERE cart_id={cart_id}
                                    AND product_id={product_id}
                                """

    return cart_prod_details_query


def update_cart_product_query(cart_prod_id, new_quantity):
    update_cart_product_query = f"""UPDATE cart_product
                                    SET quantity={new_quantity}
                                    WHERE cart_prod_id={cart_prod_id}
                                """

    return update_cart_product_query


def create_cart_product_query(cart_id, product_id, quantity):

    create_cart_product_query = f"""INSERT INTO cart_product
                                    (cart_id, product_id, quantity)
                                    VALUES ({cart_id}, {product_id}, {quantity} )
                                """

    return create_cart_product_query


def view_cart_query(user_id):
    view_cart_query = f"""  SELECT c.cart_id,
                            p.product_id, p.product_name, p.product_price,
                            cp.quantity,
                            (p.product_price * cp.quantity) AS total_price
                            FROM Cart as c
                            JOIN cart_product as cp ON c.cart_id=cp.cart_id
                            JOIN Product as p ON cp.product_id=p.product_id
                            WHERE c.user_id={user_id}
                        """
    return view_cart_query


def delete_from_cart_query(cart_id, product_id):
    delete_from_cart_query = f"""   DELETE FROM cart_product
                                    WHERE cart_id={cart_id}
                                    AND product_id={product_id};
                                """
    return delete_from_cart_query


def get_total_amount_of_cart_query(user_id):
    get_total_amount_of_cart_query = f"""   SELECT SUM(p.product_price * cp.quantity)
                                            AS total_price FROM Cart as c
                                            JOIN cart_product as cp ON c.cart_id=cp.cart_id
                                            JOIN Product as p ON cp.product_id=p.product_id
                                            where c.user_id={user_id};
                                        """
    return get_total_amount_of_cart_query


def buy_from_cart_query(user_id, total_amount, discounted_amount):
    buy_from_cart_query = f"""  INSERT INTO Orders
                                (user_id, actual_amount, discounted_amount)
                                VALUES ({user_id}, {total_amount}, {discounted_amount});
                            """
    return buy_from_cart_query


def get_order_details_query(user_id):
    get_order_details_query = f"""  SELECT c.cart_id, p.product_id, cp.quantity
                                    FROM Cart as c
                                    JOIN cart_product as cp ON c.cart_id=cp.cart_id
                                    JOIN Product as p ON cp.product_id=p.product_id
                                    WHERE c.user_id={user_id};
                                """
    return get_order_details_query


def delete_from_cart(cart_id):
    return f"DELETE FROM cart_product WHERE cart_id={cart_id};"


def create_into_order_details_query():
    create_into_order_details_query = """INSERT INTO OrderDetails
                                        (order_id, product_id, quantity)
                                        VALUES (%s, %s, %s)
                                        """
    return create_into_order_details_query

