import shutil

import click
import mysql.connector

from prettytable import PrettyTable, from_db_cursor

from config import DB_USER, DB_PASSWORD, DB_NAME

from database.user_query import get_login_query

from database.product_queries import (get_categories_query, get_products_query,
    get_product_detail_query, get_last_insert_id, add_category_query,
    add_product_query)
from database.new_tables import (create_user_table,
    create_category_table, create_product_table, create_cart_table,
    create_cart_product_table, create_order_table,
    create_order_details_table)
from database.cart_queries import (create_cart_query, get_cart_id_query,
    get_cart_prod_details_query, update_cart_product_query,
    create_cart_product_query, view_cart_query, delete_from_cart_query,
    get_total_amount_of_cart_query, buy_from_cart_query,
    get_order_details_query, create_into_order_details_query, delete_from_cart
    )


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

        username = 'shahrukh'
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


class MyCart(DB_set_up):

    def list_all_categories(self):
        cursor = self.connection.cursor()
        cursor.execute(get_categories_query())
        mytable = from_db_cursor(cursor)
        mytable.title = click.style('LIST OF ALL CATEGORIES', fg='yellow', bold=True)
        print(mytable)

    def list_all_products(self, category_id):
        cursor = self.connection.cursor()
        cursor.execute(get_products_query(category_id))
        mytable = from_db_cursor(cursor)
        if cursor.rowcount:
            mytable.title = f'LIST OF ALL Product of category {category_id}'
            print(mytable)
        else:
            cursor.fetchone()
            click.secho("\n\nNo Product exist for this category.\n\n", fg='red')
            return self.main()

    def detail_product(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute(get_product_detail_query(product_id))
        mytable = from_db_cursor(cursor)
        mytable.title = 'Product detail'
        print(mytable)

    def add_to_cart(self, product_id):
        prompt_suffix = "(default is" + click.style(" 1", fg='magenta') + ')\t'
        quantity = click.prompt("Quantity???", type=int, default=1,
                        show_default=False, prompt_suffix=prompt_suffix)
        cursor = self.connection.cursor()
        cursor.execute(get_cart_id_query(self.user_id))
        result = cursor.fetchone()

        if result:
            cart_id = result[0]
        else:
            #create a cart for the user if not exist
            cursor.execute(create_cart_query(self.user_id))
            self.connection.commit()
            cart_id = cursor.lastrowid

        cursor.execute(get_cart_prod_details_query(cart_id, product_id))
        result = cursor.fetchone()

        if result:
            # already have a cart add the product to it
            cart_prod_id = result[0]
            available_quantity = result[1]
            cursor.execute(update_cart_product_query(
                            cart_prod_id, available_quantity + quantity)
                        )
            self.connection.commit()
        else:
            cursor.execute(create_cart_product_query(cart_id, product_id, quantity))
            self.connection.commit()

    def view_cart(self):
        cursor = self.connection.cursor()
        cursor.execute(view_cart_query(self.user_id))
        mytable = from_db_cursor(cursor)
        # mytable.hrules = 1
        mytable.title = click.style('CART', fg='yellow', bold=True)
        total_amount = self.get_total_amount_of_cart()
        discounted_amount = self.get_discounted_amount(total_amount)
        net_amount = total_amount - discounted_amount

        total_row = ['']*(len(mytable.field_names)-2)
        total_text = click.style('TOTAL', fg='green')
        total_amount = click.style(str(total_amount), fg='green')
        total_row.extend([total_text, total_amount ])
        mytable.add_row(total_row)

        if discounted_amount:
            discount_row = ['']*(len(mytable.field_names)-2)
            discount_text = click.style('DISCOUNT', fg='magenta')
            discounted_amount = click.style(str(-discounted_amount), fg='magenta')
            discount_row.extend([discount_text, discounted_amount ])
            mytable.add_row(discount_row)

        net_row = ['']*(len(mytable.field_names)-2)
        net_text = click.style('NET TO PAY', fg='green')
        net_amount = click.style(str(net_amount), fg='green')
        net_row.extend([net_text, net_amount ])
        mytable.add_row(net_row)
        print(mytable)

    def remove_from_cart(self, **kwargs):
        cart_id = kwargs.get('cart_id')
        product_id = kwargs.get('product_id')

        if not (cart_id and product_id):
            cart_id = click.prompt("Enter the cart_id", type=int)
            product_id = click.prompt("Enter the product_id", type=int)

        cursor = self.connection.cursor()
        cursor.execute(delete_from_cart_query(cart_id, product_id))
        self.connection.commit()

    def get_total_amount_of_cart(self):
        cursor = self.connection.cursor()
        cursor.execute(get_total_amount_of_cart_query(self.user_id))
        final_amount = cursor.fetchone()

        if not final_amount or not final_amount[0]:
            return 0

        return final_amount[0]

    def get_discounted_amount(self, total_amount):
        DISCOUNT_ON = 10000
        MAX_DISCOUNT = 500

        if total_amount >= DISCOUNT_ON:
            return MAX_DISCOUNT

        return 0

    def buy_from_cart(self):
        total_amount = self.get_total_amount_of_cart()
        discounted_amount = self.get_discounted_amount(total_amount)

        confirm = click.confirm('Are you sure want to buy this ?', default=True)
        if not confirm:
            return self.customer()
        else:
            cursor = self.connection.cursor()
            cursor.execute(buy_from_cart_query(self.user_id, total_amount, discounted_amount))
            self.connection.commit()

            cursor = self.connection.cursor()
            cursor.execute(get_last_insert_id())
            order_id = cursor.fetchone()[0]

            cursor = self.connection.cursor()
            cursor.execute(get_order_details_query(self.user_id))
            all_rows = cursor.fetchall()
            data_to_be_inserted = list()

            cart_id = -1
            if len(all_rows):
                cart_id = all_rows[0][0]

            for row in all_rows:
                row = list(row)
                row[0] = order_id
                row = tuple(row)
                data_to_be_inserted.append(row)

            #insert the product details
            cursor = self.connection.cursor()
            cursor.executemany(create_into_order_details_query(), data_to_be_inserted)
            self.connection.commit()

            cursor = self.connection.cursor()
            cursor.execute(delete_from_cart(cart_id))
            self.connection.commit()

            print("\nThank you for shopping at MyCart.")
            print("Have a Good Day.")

    def get_ui(self):
        ui_dict = {
            'welcome': {
                    'message': 'Welcome to MyCart App'
                },

        }
        return ui_dict

    def main(self):
        ui_dict = self.get_ui()
        welcome_string = ui_dict['welcome']['message'].center(shutil.get_terminal_size().columns)
        click.secho(welcome_string, bold=True, fg='yellow', bg='white')

        if self.is_admin:
            self.admin()
        else:
            self.customer()

    def customer(self):
        choice_list = '\n1.Show category list\t2.Show Cart\t3.exit\n'
        choice = click.prompt(click.style('Please enter your choice (e.g. 1 or 2)', fg='yellow'), prompt_suffix=choice_list, type=int)

        if choice == 1:
            self.list_all_categories()
            choice_list = '\n1.Show Products\t 2.Main Menu\t 3.exit\n'
            choice = click.prompt(click.style('Please enter your choice (e.g. 1 or 2)', fg='yellow'), prompt_suffix=choice_list, type=int)

            if choice == 1:
                category_id = click.prompt(click.style('Enter category id to see list of products', fg='yellow'), type=int)
                self.list_all_products(category_id)
                choice_list = '\n1.Detail of product\t2.Main Menu\n'
                choice = click.prompt(click.style('Please enter your choice (e.g. 1 or 2)', fg='blue'), prompt_suffix=choice_list, type=int)

                if choice == 1:
                    product_id = click.prompt(click.style('Enter product id to see its details', fg='bright_blue'), type=int)
                    self.detail_product(product_id)
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
                            self.remove_from_cart()
                            self.view_cart()
                            return self.customer()
                        else:
                            return self.customer()
                    else:
                        return self.customer()
                elif choice == 2:
                    return self.customer()
                else:
                    return self.customer()

            elif choice == 2:
                return self.customer()
            else:
                exit()

        elif choice == 2:
            self.view_cart()
            choice_list = '\n1.Buy\t2.Remove item from the cart\t3.main_menu\n'
            choice = click.prompt(click.style('Please enter your choice (e.g. 1 or 2)', fg='blue'), prompt_suffix=choice_list, type=int)

            if choice == 1:
                return self.buy_from_cart()
            elif choice == 2:
                self.remove_from_cart()
                self.view_cart()

                return self.customer()
            else:
                self.customer()

        else:
            exit()

    def admin(self):
        choice_list = '\n1.Add Category\t2.Add Product\t3.Show cart of the user\t4.Orders of User\t5.exit\n'
        choice = click.prompt(click.style('Please enter your choice (e.g. 1 or 2)', fg='yellow'), prompt_suffix=choice_list, type=int)

        if choice == 1:
            self.add_category()
            return self.admin()

        elif choice == 2:
            self.add_product()
            return self.admin()

        elif choice == 3:
            pass

        elif choice == 4:
            pass

        else:
            exit()

    def add_category(self):
        click.secho('Add category', fg='green')
        category_name = click.prompt(click.style('Add category name', fg='yellow'), type=str)
        category_description = click.prompt(click.style(
                                text='Add category description (Not required)', fg='yellow'
                                ), type=str, default='', show_default=False)

        if (len(category_name.strip()) < 3):
            click.secho('Error: Category name should be greater than 3 characters', fg='red')
            return self.add_category()

        confirm = click.confirm(click.style('Are you sure want to add this category?', fg='yellow', blink=True), default=True)
        cursor = self.connection.cursor()
        cursor.execute(add_category_query(category_name, category_description))
        self.connection.commit()
        click.secho(f"Added {category_name}", fg='blue')
        self.list_all_categories()

    def add_product(self):
        click.secho('Add product', fg='green')
        product_name = click.prompt(click.style('Product name ?', fg='yellow'), type=str)
        product_price = click.prompt(click.style('Price ?', fg='yellow' ), type=float)
        category_id = click.prompt(click.style('Category ID ?', fg='yellow'), type=int)

        if (len(product_name.strip()) < 3):
            click.secho('Error: Product name should be greater than 3 characters', fg='red')
            return self.add_product()

        confirm = click.confirm(click.style('Are you sure want to add this product?', fg='yellow', blink=True), default=True)
        cursor = self.connection.cursor()
        cursor.execute(add_product_query(product_name, product_price, category_id))
        self.connection.commit()
        click.secho(f"Added {product_name}", fg='blue')
        self.list_all_products(category_id)

if __name__ == "__main__":
    start = MyCart()
    start.main()

