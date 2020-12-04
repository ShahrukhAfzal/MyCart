print("Welcome to my app")

import mysql.connector

class DB_set_up:
    def __init__(self):
        connection = mysql.connector.connect(user='test-user',
                                            password='12345678',
                                            database='temp_db')

        self.connection = connection
        self.create_all_table_if_not_exists()
        self.is_admin = self.login()

    def create_all_table_if_not_exists(self):
        cursor = self.connection.cursor()
        create_user_table = """
                    CREATE TABLE if not exists User(
                        user_id int AUTO_INCREMENT,
                        user_name varchar(255) NOT NULL,
                        user_email varchar(255) NOT NULL,
                        password varchar(10),
                        is_admin BOOLEAN,
                        PRIMARY KEY (user_id)
                    )
                    """

        create_category_table = """
                    CREATE TABLE if not exists Categories(
                        category_id int AUTO_INCREMENT,
                        category_name varchar(255) NOT NULL,
                        category_description varchar(255) NOT NULL,
                        PRIMARY KEY (category_id)
                    )
                    """

        create_product_table = """
                    CREATE TABLE if not exists Product(
                        product_id int AUTO_INCREMENT,
                        product_name varchar(255) NOT NULL,
                        product_price DECIMAL(10,2),
                        category_id int,
                        PRIMARY KEY (product_id),
                        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
                    )
                    """

        create_cart_table = """
                    CREATE TABLE if not exists Cart(
                        cart_id int AUTO_INCREMENT,
                        user_id int,
                        PRIMARY KEY (cart_id),
                        FOREIGN KEY (user_id) REFERENCES User(user_id)
                    )
                    """

        create_cart_product_table = """
                    CREATE TABLE if not exists cart_product(
                        cart_prod_id int AUTO_INCREMENT,
                        cart_id int,
                        product_id int,
                        quantity int default 0 CHECK (quantity >= 1),
                        PRIMARY KEY (cart_prod_id),
                        FOREIGN KEY (product_id) REFERENCES Product(product_id),
                        FOREIGN KEY (cart_id) REFERENCES Cart(cart_id)
                    )
                    """

        create_order_table = """
                    CREATE TABLE if not exists Orders(
                        order_id int AUTO_INCREMENT,
                        user_id int,
                        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        actual_amount DECIMAL CHECK (actual_amount >= 0) ,
                        discounted_amount DECIMAL CHECK (discounted_amount >= 0),
                        PRIMARY KEY (order_id),
                        FOREIGN KEY (user_id) REFERENCES User(user_id)
                    )
                    """

        create_order_details_table = """
                    CREATE TABLE if not exists OrderDetails(
                        order_details_id int AUTO_INCREMENT,
                        order_id int,
                        product_id int,
                        quantity int,
                        PRIMARY KEY (order_details_id),
                        FOREIGN KEY (order_id) REFERENCES Orders(order_id),
                        FOREIGN KEY (product_id) REFERENCES Product(product_id)
                    )
                    """

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
        print("All tables created successfully")

    def login(self):
        # username = input("Please enter your user_name\t")
        # password = input("Please enter your password\t")
        username = 'shoaib'
        password = '123456'
        cursor = self.connection.cursor()
        query = f"""SELECT *
                    FROM User
                    WHERE (user_name='{username}'
                    and password='{password}');
                """
        cursor.execute(query)
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

class Buy(DB_set_up):

    def list_all_categories(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM Categories;"
        cursor.execute(query)

        print("\nPlease select a category")
        print("category_id | category_name")
        for (cat_id, cat_name, _) in cursor:
            print(cat_id, cat_name)

        n = int(input("Please select the category number to view all the related products\n"))

        return n

    def list_all_products(self, category_id):
        cursor = self.connection.cursor()
        query = """ SELECT product_id, product_name, product_price, category_id
                    FROM Product
                    WHERE category_id={cat_id};
                """.format(cat_id=category_id)

        cursor.execute(query)
        is_empty = True
        print("ID | NAME | PRICE")
        for row_with_col in cursor:
            is_empty = False
            print("""{id} | '{name}' | ${price}""".format(id=row_with_col[0],
                                                name=row_with_col[1],
                                                price=row_with_col[2],
                                                )
            )

        if is_empty:
            print("No Product exists for this category.")
            print("Do you want to continue?")
            c = input("Y for yes and N for no...\n")
            if c.lower() in ["y", "yes", "yaa"]:
                self.list_all_products(self.list_all_categories())
            else:
                quit()
        else:
            prod_id = int(input("Enter the product id to see it details  "))
            self.detail_product(prod_id, category_id)

    def detail_product(self, product_id, category_id):
        cursor = self.connection.cursor()
        query = """ SELECT *
                    FROM Product
                    WHERE product_id={}
                """.format(product_id)
        cursor.execute(query)
        r = cursor.fetchone()
        print(f'ID = {r[0]}, NAME = {r[1]}, price = {r[2]}')
        c = input("Do you want to add this item cart.")

        if c.lower() in ['y', 'yes', 'yaa']:
            print("\nCURRENT ITEMS IN CART::")
            self.view_cart()
            quantity = int(input("Quantity ??"))
            self.add_to_cart(product_id, quantity)
        else:
            self.list_all_products(category_id)

    def add_to_cart(self, product_id, quantity=1):
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

    def view_cart(self):
        print("\nHello, This is your Cart.")
        cursor = self.connection.cursor()
        query = f"""SELECT c.cart_id,
                    p.product_id, p.product_name,
                    cp.quantity
                    FROM Cart as c
                    JOIN cart_product as cp ON c.cart_id=cp.cart_id
                    JOIN Product as p ON cp.product_id=p.product_id
                    WHERE c.user_id={self.user_id}
                """
        cursor.execute(query)

        is_empty = True
        for row in cursor:
            is_empty = False
            print(row)

        if not is_empty:
            cart_id = row[0]
            print("Do you want to remove any item from the Cart ??")
            c = input("Press y for yes... else for no")

            if c.lower() in ['y', 'yes', 'yaa']:
                product_id = int(input("Enter the product id to remove"))
                self.remove_from_cart(cart_id, product_id)

    def remove_from_cart(self, cart_id, product_id):
        cursor = self.connection.cursor()
        query = f"""DELETE FROM cart_product
                    WHERE cart_id={cart_id}
                    AND product_id={product_id};
                """
        cursor.execute(query)
        self.connection.commit()
        self.view_cart()


o = Buy()
if o.is_admin:
    pass
else:
    category_id = o.list_all_categories()
    o.list_all_products(category_id)
