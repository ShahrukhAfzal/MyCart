import mysql.connector

from config import DB_USER, DB_PASSWORD, DB_NAME
from database.new_tables import (create_user_table, create_category_table,
    create_product_table, create_cart_table, create_cart_product_table,
    create_order_table, create_order_details_table,)
from database.user_query import get_login_query


class DB_set_up:
    def __init__(self):
        self.connection = mysql.connector.connect(user=DB_USER,
                                                password=DB_PASSWORD,
                                                database=DB_NAME
                                            )

        self.create_all_table_if_not_exists()
        self.is_admin = self.login()

    def create_all_table_if_not_exists(self):
        cursor = self.connection.cursor()

        cursor.execute(create_user_table)
        # self.connection.commit()

        cursor.execute(create_category_table)
        # self.connection.commit()

        cursor.execute(create_product_table)
        # self.connection.commit()

        cursor.execute(create_cart_table)
        # self.connection.commit()

        cursor.execute(create_cart_product_table)
        # self.connection.commit()

        cursor.execute(create_order_table)
        # self.connection.commit()

        cursor.execute(create_order_details_table)
        # self.connection.commit()

    def login(self):
        # username = input("Please enter your user_name\t")
        # password = input("Please enter your password\t")
        username = 'shoaib'
        password = '123456'
        cursor = self.connection.cursor()
        login_query = get_login_query(username, password)
        cursor.execute(login_query)
        r = cursor.fetchone()
        if r:
            self.user_id = r[0]
            return r[-2]
        else:
            print("Wrong credentials")
            c = input("Do you want to retry, enter y for yes\n")
            if c.lower() in ['y', 'yes']:
                self.login()
            else:
                quit()

    def signup(self):
        pass
