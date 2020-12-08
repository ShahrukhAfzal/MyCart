import click
import mysql.connector

from prettytable import PrettyTable, from_db_cursor

from config import DB_USER, DB_PASSWORD, DB_NAME

from utils import (clear_screen, print_welcome_string,
    print_successful_login_message, print_unsuccessful_login_message, retry,
    get_username, get_password, get_choice)

from database.user_query import (get_login_query, get_all_user_query,
    get_all_bill_by_user_query)
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
        self.create_db_connection()
        self.create_all_table_if_not_exists()

    def create_db_connection(self):
        self.connection = mysql.connector.connect(user=DB_USER,
                                                password=DB_PASSWORD,
                                                database=DB_NAME
                                            )

    def create_all_table_if_not_exists(self):
        cursor = self.connection.cursor()
        cursor.execute(create_user_table)
        cursor.execute(create_category_table)
        cursor.execute(create_product_table)
        cursor.execute(create_cart_table)
        cursor.execute(create_cart_product_table)
        cursor.execute(create_order_table)
        cursor.execute(create_order_details_table)

    def execute_query(self, query, get_dictionary=False):
        cursor = self.connection.cursor(dictionary=get_dictionary)
        cursor.execute(query)
        return cursor


class User:

    def login(self, username=None, password=None):
        if not username:
            username = get_username()
        if not password:
            password = get_password()

        cursor = self.execute_query(get_login_query(username, password), get_dictionary=True)
        result = cursor.fetchone()
        return result

    def signup(self):
        pass

    def get_all_user(self):
        cursor = self.connection.cursor()
        cursor.execute(get_all_user_query())
        mytable = from_db_cursor(cursor)
        mytable.title = 'List of all the Customer'
        print(mytable)

    def get_all_bill_from_user(self, user_id=None):
        if not user_id:
            self.get_all_user()
            user_id = click.prompt(click.style('Enter the user_id to see its all bill', fg='yellow'), type=int)

        cursor = self.execute_query(get_all_bill_by_user_query(user_id))
        mytable = from_db_cursor(cursor)
        mytable.title = f"Bill of user {user_id}"
        print(mytable)

    def customer_flow(self):
        choice_list = ['Buy(Show category list)', 'Show Cart', 'exit']
        choice = get_choice(choice_list)
        if choice == 1:
            self.list_all_categories()
            choice_list = ['Show Products', 'Main Menu', 'exit']
            choice = get_choice(choice_list)

            if choice == 1:
                category_id = click.prompt(click.style('Enter category id to see list of products', fg='yellow'), type=int)
                self.list_all_products(category_id)
                choice_list = ['Detail of product', 'Main Menu', 'exit']
                choice = get_choice(choice_list)

                if choice == 1:
                    product_id = click.prompt(click.style('Enter product id to see its details', fg='bright_blue'), type=int)
                    self.detail_product(product_id)
                    choice_list = ['Do you want to add this item to the cart', 'Main Menu']
                    choice = get_choice(choice_list)

                    if choice == 1:
                        self.add_to_cart(product_id)
                        self.view_cart()
                        choice_list = ['Buy', 'Remove item from the cart', 'Main Menu']
                        choice = get_choice(choice_list)

                        if choice == 1:
                            self.buy_from_cart()
                        elif choice == 2:
                            self.remove_from_cart()
                            self.view_cart()
                            return self.customer_flow()
                        else:
                            return self.customer_flow()
                    else:
                        return self.customer_flow()
                elif choice == 2:
                    return self.customer_flow()
                else:
                    exit()

            elif choice == 2:
                return self.customer_flow()
            else:
                exit()

        elif choice == 2:
            self.view_cart()
            choice_list = ['Buy', 'Remove item from the cart', 'Main Menu']
            choice = get_choice(choice_list)

            if choice == 1:
                return self.buy_from_cart()
            elif choice == 2:
                self.remove_from_cart()
                self.view_cart()
                return self.customer_flow()
            else:
                return self.customer_flow()

        else:
            exit()

    def admin_flow(self):
        choice_list = ['Add Category', 'Add Product', 'Show cart of the user', 'Orders of User', 'exit']
        choice = get_choice(choice_list)

        if choice == 1:
            self.add_category()
            return self.admin_flow()

        elif choice == 2:
            self.add_product()
            return self.admin_flow()

        elif choice == 3:
            self.view_cart()
            return self.admin_flow()

        elif choice == 4:
            self.get_all_bill_from_user()
            return self.admin_flow()

        else:
            exit()


class Product:
    """
    """
    def list_all_categories(self):
        cursor = self.execute_query(get_categories_query())
        mytable = from_db_cursor(cursor)
        mytable.title = click.style('LIST OF ALL CATEGORIES', fg='yellow', bold=True)
        print(mytable)

    def list_all_products(self, category_id):
        cursor = self.execute_query(get_products_query(category_id))
        mytable = from_db_cursor(cursor)
        if cursor.rowcount:
            mytable.title = f'LIST OF ALL Product of category {category_id}'
            print(mytable)
        else:
            cursor.fetchone()
            click.secho("\n\nNo Product exist for this category.\n\n", fg='red')
            return self.main()

    def detail_product(self, product_id):
        cursor = self.execute_query(get_product_detail_query(product_id))
        mytable = from_db_cursor(cursor)
        mytable.title = 'Product detail'
        print(mytable)

    def add_category(self, category_name=None, category_description=None, ask_confirm=True, confirm=True):
        click.secho('Add category', fg='green')
        if not category_name:
            category_name = click.prompt(click.style('Add category name', fg='yellow'), type=str)

        if (len(category_name.strip()) < 3):
            click.secho('Error: Category name should be greater than 3 characters', fg='red')
            return self.add_category()

        if not category_description:
            category_description = click.prompt(click.style(text='Add category description (Not required)', fg='yellow'), type=str, default='', show_default=False)

        if ask_confirm:
            confirm = click.confirm(click.style('Are you sure want to add this category?', fg='yellow', blink=True), default=True)

        if confirm:
            self.execute_query(add_category_query(category_name, category_description))
            self.connection.commit()
            click.secho(f"Added {category_name}", fg='blue')
            self.list_all_categories()
        else:
            return self.admin_flow()

    def add_product(self, product_name=None, product_price=None, category_id=None, ask_confirm=True, confirm=True):
        click.secho('Add product', fg='green')
        if not product_name:
            product_name = click.prompt(click.style('Product name ?', fg='yellow'), type=str)
        if (len(product_name.strip()) < 3):
            click.secho('Error: Product name should be greater than 3 characters', fg='red')
            return self.add_product()

        if not product_price:
            product_price = click.prompt(click.style('Price ?', fg='yellow' ), type=float)

        if not category_id:
            self.list_all_categories()
            category_id = click.prompt(click.style('Category ID ?', fg='yellow'), type=int)

        if ask_confirm:
            confirm = click.confirm(click.style('Are you sure want to add this product?', fg='yellow', blink=True), default=True)

        if confirm:
            self.execute_query(add_product_query(product_name, product_price, category_id))
            self.connection.commit()
            click.secho(f"Added {product_name}", fg='blue')
            self.list_all_products(category_id)
        else:
            return self.admin_flow()


class Cart:

    def add_to_cart(self, product_id, new_quantity=None):
        if not new_quantity:
            prompt_suffix = "(default is" + click.style(" 1", fg='magenta') + ')\t'
            new_quantity = click.prompt("Quantity???", type=int, default=1,
                            show_default=False, prompt_suffix=prompt_suffix)

        cursor = self.execute_query(get_cart_id_query(self.user_id), get_dictionary=True)
        result = cursor.fetchone()
        if result:
            cart_id = result['cart_id']
        else:
            #create a cart for the user if not exist
            cursor = self.execute_query(create_cart_query(self.user_id))
            self.connection.commit()
            cart_id = cursor.lastrowid

        cursor = self.execute_query(get_cart_prod_details_query(cart_id, product_id), get_dictionary=True)
        result = cursor.fetchone()
        if result:
            # already have a cart add the product to it
            cart_prod_id = result['cart_prod_id']
            available_quantity = result['quantity']
            self.execute_query(update_cart_product_query(cart_prod_id, available_quantity + new_quantity))
            self.connection.commit()
        else:
            self.execute_query(create_cart_product_query(cart_id, product_id, new_quantity))
            self.connection.commit()
        click.secho('Product successfully added to cart', fg='green')

    def view_cart(self, user_id=None, ask_confirm=True):
        if not user_id:
            user_id = self.user_id
            if self.is_admin:
                self.get_all_user()
                user_id = click.prompt(click.style('Enter user_id to show its cart...', fg='yellow'), type=int)

        cursor = self.execute_query(view_cart_query(user_id))
        mytable = from_db_cursor(cursor)
        # mytable.hrules = 1
        if cursor.rowcount:
            mytable.title = click.style('CART', fg='yellow', bold=True)
            total_amount = self.get_total_amount_of_cart(user_id)
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
        else:
            click.secho('Your Cart is empty.', fg='magenta', reverse=True)

    def remove_from_cart(self, **kwargs):
        cart_id = kwargs.get('cart_id')
        product_id = kwargs.get('product_id')

        if not (cart_id and product_id):
            cart_id = click.prompt("Enter the cart_id", type=int)
            product_id = click.prompt("Enter the product_id", type=int)

        cursor = self.execute_query(delete_from_cart_query(cart_id, product_id))
        self.connection.commit()

    def get_total_amount_of_cart(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute(get_total_amount_of_cart_query(user_id))
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

    def buy_from_cart(self, ask_confirm=True, confirm=True):
        total_amount = self.get_total_amount_of_cart(self.user_id)
        discounted_amount = self.get_discounted_amount(total_amount)

        if ask_confirm:
            confirm = click.confirm('Are you sure want to buy this ?', default=True)
            if not confirm:
                return self.customer_flow()

        self.execute_query(buy_from_cart_query(self.user_id, total_amount, discounted_amount))
        self.connection.commit()

        cursor = self.execute_query(get_last_insert_id())
        order_id = cursor.fetchone()[0]

        cursor = self.execute_query(get_order_details_query(self.user_id))
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

        #emptying cart after buying the products
        cursor = self.execute_query(delete_from_cart(cart_id))
        self.connection.commit()

        print("\nThank you for shopping at MyCart.")
        print("Have a Good Day.")


class MyCart(DB_set_up, User, Product, Cart):

    def main(self):
        authentication_token = self.login()
        if authentication_token:
            self.user_id = authentication_token['user_id']
            self.is_admin = authentication_token['is_admin']
            user_name = authentication_token['user_name']
            print_successful_login_message(user_name)

            cart = Cart()

            if self.is_admin:
                self.admin_flow()
            else:
                self.customer_flow()
        else:
            print_unsuccessful_login_message()
            if retry():
                clear_screen()
                return self.main()
            else:
                quit()


if __name__ == "__main__":
    clear_screen()
    start = MyCart()
    start.main()

