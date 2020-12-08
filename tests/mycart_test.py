from test_config import DB_USER, DB_PASSWORD, DB_NAME
from database.tests_queries import (drop_db_query, create_db_query)

from task import MyCart

class TestMyCart(MyCart):

    def __init__(self):
        db_connection = {'DB_USER': DB_USER, 'DB_PASSWORD': DB_PASSWORD}
        self.create_db_connection(**db_connection)
        print()
        self.execute_query(drop_db_query(DB_NAME))
        self.execute_query(create_db_query(DB_NAME))
        self.connection.close()
        print(self.connection)
        db_connection.update({
            'DB_NAME': DB_NAME
            })
        self.create_db_connection(**db_connection)
        self.create_all_table_if_not_exists()
        print(self.connection)


test = TestMyCart()

