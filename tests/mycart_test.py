from task import MyCart

from test_config import DB_USER, DB_PASSWORD, DB_NAME

from database.tests_queries import (drop_db_query, create_db_query)
from database.user_query import create_user_query, get_login_query
from database.product_queries import (add_multiple_categories_query, add_multiple_products_query)

from utils import (get_user_test_data, get_category_test_data,
    get_products_test_data, get_add_to_cart_with_coupon_fixture,
    get_add_to_cart_without_coupon_fixture, get_remove_from_cart_fixture)


class TestMyCart(MyCart):

    def __init__(self):
        db_connection = {'DB_USER': DB_USER, 'DB_PASSWORD': DB_PASSWORD}
        print("creating database connection")
        self.create_db_connection(**db_connection)

        print("dropping old database")
        self.execute_query(drop_db_query(DB_NAME))

        print("creating new database")
        self.execute_query(create_db_query(DB_NAME))
        db_connection.update({
                'DB_NAME': DB_NAME
            })

        print("creating new database connection")
        self.create_db_connection(**db_connection)
        self.create_all_table_if_not_exists()

    def test_create_user(self, admin=False):
        user_data = get_user_test_data(admin)
        self.execute_query(create_user_query(**user_data))
        self.connection.commit()

        cursor = self.execute_query(get_login_query(user_data['user_name'], user_data['password']))
        cursor.fetchall()
        rowcount = cursor.rowcount

        if rowcount:
            print(f"passed test_create_user admin={admin}")
        else:
            print(f"failed test_create_user admin={admin}")

    def test_create_categories(self):
        cursor = self.connection.cursor()
        category_test_data =  get_category_test_data()
        cursor.executemany(add_multiple_categories_query(), category_test_data)
        self.connection.commit()
        print('passed test_create_categories')

    def test_create_products(self):
        cursor = self.connection.cursor()
        products_test_data = get_products_test_data()
        cursor.executemany(add_multiple_products_query(), products_test_data)
        self.connection.commit()
        print('passed test_create_products')

    def test_list_all_categories(self):
        self.list_all_categories()

    def test_list_all_products(self):
        self.list_all_products(category_id=1)
        self.list_all_products(category_id=10)

    def test_detail_product(self):
        self.detail_product(product_id=1)
        self.detail_product(product_id=2)
        self.detail_product(product_id=30)

    def test_add_to_cart_with_coupon(self):
        products = get_add_to_cart_with_coupon_fixture()
        for item in products:
            self.add_to_cart(item['product_id'],  item['new_quantity'], item['user_id'])

        test.view_cart(user_id=1)

    def test_add_to_cart_without_coupon(self):
        products = get_add_to_cart_without_coupon_fixture()
        for item in products:
            self.add_to_cart(item['product_id'],  item['new_quantity'], item['user_id'])

        test.view_cart(user_id=1)

    def test_remove_from_cart(self):
        data = get_remove_from_cart_fixture()
        for each in data:
            self.remove_from_cart(**each)

        test.view_cart(user_id=1)

test = TestMyCart()
test.test_create_user(admin=True)
test.test_create_user(admin=False)
test.test_create_categories()
test.test_create_products()
test.test_list_all_categories()
test.test_list_all_products()
test.test_detail_product()

test.test_add_to_cart_without_coupon()
test.test_add_to_cart_with_coupon()

test.test_remove_from_cart()



