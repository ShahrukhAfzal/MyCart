import shutil
import click
from tests.fixtures import (categories_fixtures, products_fixtures,
    users_fixtures, add_to_cart_fixture, remove_from_cart_fixture)

WELCOME_MESSAGE = 'Welcome to MyCart App'
UNSUCCESSFULL_LOGIN_MESASAGE = '!!! Wrong credentials. !!!'


def align_center(text):
    return text.center(shutil.get_terminal_size().columns)

def print_welcome_string():
    click.secho(align_center(WELCOME_MESSAGE), bold=True, fg='cyan', reverse=True, nl=True)
    print('\n')

def print_successful_login_message(user_name):
    SUCCESSFULL_LOGIN_MESASAGE = 'You are successfully logged in. !'
    WELCOME_USER_MESSAGE = f' Welcome {user_name}'
    click.secho(align_center(SUCCESSFULL_LOGIN_MESASAGE), bold=True, fg='green', reverse=True)
    click.secho(align_center(WELCOME_USER_MESSAGE), bold=True, fg='green')
    print('\n')

def clear_screen():
    click.clear()
    print_welcome_string()

def print_unsuccessful_login_message():
    click.secho(UNSUCCESSFULL_LOGIN_MESASAGE, fg='red')

def retry():
    return click.confirm('Do you want to retry ?', default=True)

def get_username():
    return click.prompt(click.style('Username ??', fg='cyan'), type=str, prompt_suffix='\t')

def get_password():
    return click.prompt(click.style('Password ??', fg='cyan'), type=str, hide_input=True, prompt_suffix='\t')

def get_choice(choice_list):
    choice_message = 'Please enter your choice (e.g. 1 or 2)'
    choice_option_string = '\n'
    for number, choice in enumerate(choice_list, 1):
        choice_option_string += f'{number}. '+ choice + '\t'

    choice_option_string += '\n'

    return click.prompt(click.style(choice_message, fg='yellow'), prompt_suffix=choice_option_string, type=int)

"""
used in testing
"""
def get_category_test_data():
    data = list()
    for row in categories_fixtures:
        obj = (row['category_id'], row['category_name'], row['category_description'])
        data.append(obj)

    return data

def get_products_test_data():
    data = list()
    for row in products_fixtures:
        obj = (row['product_id'], row['product_name'], row['product_price'], row['category_id'])
        data.append(obj)

    return data

def get_user_test_data(admin=False):
    if admin:
        test_user = users_fixtures['admin_user'][0]
    else:
        test_user = users_fixtures['customer_user'][0]

    return test_user


def get_add_to_cart_with_coupon_fixture():
    return add_to_cart_fixture[:2]

def get_add_to_cart_without_coupon_fixture():
    return add_to_cart_fixture[2:]


def get_remove_from_cart_fixture():
    return remove_from_cart_fixture
