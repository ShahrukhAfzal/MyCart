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
