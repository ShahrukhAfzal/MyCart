import shutil

import click
import mysql.connector

from prettytable import PrettyTable, from_db_cursor

from database.product_query import (get_categories_query, get_products_query)
from config import DB_USER, DB_PASSWORD, DB_NAME
from database.user_query import get_login_query
from database.new_tables import (create_user_table,
    create_category_table, create_product_table, create_cart_table,
    create_cart_product_table, create_order_table,
    create_order_details_table)


class DB_set_up:
    def __init__(self):
        connection = mysql.connector.connect(user=DB_USER,
                                            password=DB_PASSWORD,
                                            database=DB_NAME
                                        )

        self.connection = connection
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
            self.username = username
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


class Buy(DB_set_up):

    def list_all_categories(self):
        cursor = self.connection.cursor()
        cursor.execute(get_categories_query())

        x = PrettyTable()
        mytable = from_db_cursor(cursor)
        mytable.title = 'LIST OF ALL CATEGORIES'
        print(mytable)

    def list_all_products(self, category_id):
        cursor = self.connection.cursor()
        cursor.execute(get_products_query(category_id))
        mytable = from_db_cursor(cursor)
        mytable.title = f'LIST OF ALL Product of category {category_id}'
        print(mytable)

        # if cursor.rowcount == 0:
        #     print("No Product exists for this category.")
        #     print("Do you want to continue?")
        #     c = input("Y for yes and N for no...\n")
        #     if c.lower() in ["y", "yes", "yaa"]:
        #         self.list_all_products(self.list_all_categories())
        #     else:
        #         quit()
        # else:
        #     prod_id = int(input("Enter the product id to see it details  "))
        #     self.detail_product(prod_id, category_id)

    def detail_product(self, product_id, category_id):
        cursor = self.connection.cursor()
        query = """ SELECT *
                    FROM Product
                    WHERE product_id={}
                """.format(product_id)
        cursor.execute(query)
        mytable = from_db_cursor(cursor)
        mytable.title = 'Product detail'
        print(mytable)

        # print(f'ID = {r[0]}, NAME = {r[1]}, price = {r[2]}')
        # c = input("Do you want to add this item cart.")

        # if c.lower() in ['y', 'yes', 'yaa']:
        #     print("\nCURRENT ITEMS IN CART::")
        #     self.view_cart()
        #     quantity = int(input("Quantity ??"))
        #     self.add_to_cart(product_id, quantity)
        # else:
        #     self.list_all_products(category_id)

    def add_to_cart(self, product_id, quantity=1):
        prompt_suffix = "(default is" + click.style(" 1", fg='magenta') + ')\t'
        quantity = click.prompt("Quantity???", type=int, default=1, show_default=False, prompt_suffix=prompt_suffix)
        cursor = self.connection.cursor()
        query = f"""SELECT cart_id FROM Cart WHERE user_id='{self.user_id}'"""
        cursor.execute(query)
        r = cursor.fetchone()

        if r:
            cart_id = r[0]
        else:
            #create a cart for the user if not exist
            query = f"""INSERT INTO Cart (user_id) VALUES ({self.user_id})"""
            cursor.execute(query)
            self.connection.commit()
            cart_id = cursor.lastrowid

        query = f"""SELECT cart_prod_id, quantity
                    FROM cart_product
                    WHERE cart_id='{cart_id}'
                    AND product_id='{product_id}'
                """
        cursor.execute(query)
        r = cursor.fetchone()

        if r:
            # already have a cart add the product to it
            cart_prod_id = r[0]
            available_quantity = r[1]
            query = f"""UPDATE cart_product
                        SET quantity='{available_quantity + quantity}'
                        WHERE cart_prod_id='{cart_prod_id}'
                    """
            cursor.execute(query)
            self.connection.commit()
        else:
            query = f"""INSERT INTO cart_product (cart_id, product_id, quantity)
                        VALUES ({cart_id}, {product_id}, {quantity} )"""
            cursor.execute(query)
            self.connection.commit()
        # self.buy_from_cart()

    def view_cart(self):
        print("\nHello, This is your Cart.")
        cursor = self.connection.cursor()
        query = f"""SELECT c.cart_id,
                    p.product_id, p.product_name, p.product_price,
                    cp.quantity,
                    (p.product_price * cp.quantity) AS total_price
                    FROM Cart as c
                    JOIN cart_product as cp ON c.cart_id=cp.cart_id
                    JOIN Product as p ON cp.product_id=p.product_id
                    WHERE c.user_id={self.user_id}
                """
        cursor.execute(query)
        mytable = from_db_cursor(cursor)
        mytable.title = 'Cart'
        print(mytable)

        choice_list = '\n1.Buy\t2.Remove item from the cart\t3.main_menu\n'
        # choice = click.prompt(click.style('Please enter your choice (e.g. 1 or 2)', fg='yellow'), prompt_suffix=choice_list, type=int)
        # if choice == '1':
        #     pass
        # elif choice == '2':
        #     pass
        # elif choice == '3':
        #     self.main()

        # cursor.execute(query)

        # is_empty = True
        # for row in cursor:
        #     is_empty = False
        #     print(row)

        # self.buy_from_cart()
        # if not is_empty:
        #     cart_id = row[0]
        #     print("Do you want to remove any item from the Cart ??")
        #     c = input("Press y for yes... else for no")

        #     if c.lower() in ['y', 'yes', 'yaa']:
        #         product_id = int(input("Enter the product id to remove"))
        #         self.remove_from_cart(cart_id, product_id)

    def remove_from_cart(self, cart_id, product_id):
        cursor = self.connection.cursor()
        query = f"""DELETE FROM cart_product
                    WHERE cart_id={cart_id}
                    AND product_id={product_id};
                """
        cursor.execute(query)
        self.connection.commit()
        self.view_cart()

    def get_total_amount_of_cart(self):
        cursor = self.connection.cursor()
        query = f"""SELECT SUM(p.product_price * cp.quantity)
                    AS total_price FROM Cart as c
                    JOIN cart_product as cp ON c.cart_id=cp.cart_id
                    JOIN Product as p ON cp.product_id=p.product_id
                    where c.user_id={self.user_id};"""
        cursor.execute(query)
        final_amount = cursor.fetchone()

        if not final_amount:
            return 0

        return final_amount[0]

    def get_discounted_amount(self, total_amount):
        DISCOUNT_ON = 10000
        MAX_DISCOUNT = 500

        if total_amount >= DISCOUNT_ON:
            return MAX_DISCOUNT

        return 0

    def buy_from_cart(self):
        # self.view_cart()
        total_amount = self.get_total_amount_of_cart()
        discounted_amount = self.get_discounted_amount(total_amount)

        print(f"TOTAL PRICE = {total_amount}\nDiscount = -{discounted_amount}")
        print(f"To pay = {total_amount - discounted_amount}")

        confirm = click.confirm('Are you sure want to buy this ?')
        if not confirm:
            return self.main()
        else:
            cursor = self.connection.cursor()
            query = f"""INSERT INTO Orders
                        (user_id, actual_amount, discounted_amount)
                        VALUES ({self.user_id}, {total_amount},
                                {discounted_amount});
                    """
            cursor.execute(query)
            self.connection.commit()

            cursor = self.connection.cursor()
            query = "SELECT LAST_INSERT_ID();"
            cursor.execute(query)
            order_id = cursor.fetchone()[0]

            cursor = self.connection.cursor()
            query = f"""SELECT c.cart_id, p.product_id, cp.quantity
                        FROM Cart as c
                        JOIN cart_product as cp ON c.cart_id=cp.cart_id
                        JOIN Product as p ON cp.product_id=p.product_id
                        WHERE c.user_id={self.user_id};
                    """
            cursor.execute(query)
            all_rows = cursor.fetchall()
            data_to_be_inserted = list()

            if len(all_rows):
                cart_id = all_rows[0][0]

            for row in all_rows:
                row = list(row)
                print(row)
                row[0] = order_id
                row = tuple(row)
                data_to_be_inserted.append(row)

            #insert the product details
            cursor = self.connection.cursor()
            query = """INSERT INTO OrderDetails
                        (order_id, product_id, quantity)
                        VALUES (%s, %s, %s)
                    """

            cursor.executemany(query, data_to_be_inserted)
            self.connection.commit()

            query = f"DELETE FROM cart_product WHERE cart_id={cart_id};"
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()

            print("\nThank you for shopping at MyCart.")
            print("Have a Good Day.")

    def get_ui(self):
        ui_dict = {
            'welcome': {
                    'message': 'Welcome to MyCart'
                },

        }
        return ui_dict

    def main(self):
        ui_dict = self.get_ui()
        welcome_string = ui_dict['welcome']['message'].center(shutil.get_terminal_size().columns)
        click.secho(welcome_string, bold=True, fg='yellow', bg='white')

        choice_list = '\n1.Show category list\t2.Show Cart\n'
        choice = click.prompt(click.style('Please enter your choice (e.g. 1 or 2)', fg='yellow'), prompt_suffix=choice_list, type=int)

        if choice == 1:
            self.list_all_categories()
            choice_list = '\n1.Show Products\t 2.Main Menu\t 3.exit\n'
            choice = click.prompt(click.style('Please enter your choice (e.g. 1 or 2)', fg='yellow'), prompt_suffix=choice_list, type=int)

            if choice == 1:
                # self.list_all_categories()
                category_id = click.prompt(click.style('Enter category id to see list of products', fg='yellow'), type=int)
                self.list_all_products(category_id)
                choice_list = '\n1.Detail of product\t2.Main Menu\n'
                choice = click.prompt(click.style('Please enter your choice (e.g. 1 or 2)', fg='blue'), prompt_suffix=choice_list, type=int)

                if choice == 1:
                    product_id = click.prompt(click.style('Enter product id to see its details', fg='bright_blue'))
                    self.detail_product(product_id, category_id)
                    choice_list = '\n1.Do you want to add this item to the cart\t2.Main Menu\n'
                    choice = click.prompt(click.style('Please enter your choice (e.g. 1 or 2)', fg='blue'), prompt_suffix=choice_list, type=int)

                    if choice == 1:
                        self.add_to_cart(product_id)
                        click.secho('Product successfully added to cart', fg='green')
                        self.view_cart()
                        choice_list = '\n1.Buy\t2.Remove item from the cart\t3.main_menu\n'
                        choice = click.prompt(click.style('Please enter your choice (e.g. 1 or 2)', fg='blue'), prompt_suffix=choice_list, type=int)

                        if choice == 1:
                            self.buy_from_cart()



        elif choice == 2:
            self.view_cart()
            choice_list = '\n1.Buy\t2.Remove item from the cart\t3.main_menu\n'
            choice = click.prompt(click.style('Please enter your choice (e.g. 1 or 2)', fg='blue'), prompt_suffix=choice_list, type=int)

            self.main()


o = Buy()
if o.is_admin:
    pass
else:
    o.main()
    # category_id = o.list_all_categories()
    # o.list_all_products(category_id)
