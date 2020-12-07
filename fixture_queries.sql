-- create admin user
INSERT INTO User (user_name, user_email, password, is_admin)
VALUES ('new-admin', 'admin@gmail.com', '123456', true);

-- create customers
INSERT INTO User (user_name, user_email, password, is_admin)
VALUES ('customer-1', 'customer-1@gmail.com', '123456', false);

INSERT INTO User (user_name, user_email, password, is_admin)
VALUES ('customer-2', 'customer-2@gmail.com', '123456', false);


-- create new categories
INSERT INTO Categories (category_name, category_description)
VALUES ('ELECTRONICS', 'LIKE T.V., Laptop, PC, Mobile');

INSERT INTO Categories (category_name, category_description)
VALUES ('Beverages', 'Soft drinks, coffees, teas, beers, and ales');

INSERT INTO Categories (category_name, category_description)
VALUES ('Condiments', 'Sweet and savory sauces, relishes, spreads, and seasonings');

INSERT INTO Categories (category_name, category_description)
VALUES ('Confections', 'Desserts, candies, and sweet breads');

INSERT INTO Categories (category_name, category_description)
VALUES ('Dairy Products', 'Milk, Cheeses, and other dairy items.');

SELECT * FROM Categories;

-- create new product
INSERT INTO Product (product_name, product_price, category_id)
VALUES ('MOTO X-Play', 13500, 1);

INSERT INTO Product (product_name, product_price, category_id)
VALUES ('LENOVO ideapad 320', 27499, 1);

INSERT INTO Product (product_name, product_price, category_id)
VALUES ('Samsung Galaxy S4', 17689, 1);

INSERT INTO Product (product_name, product_price, category_id)
VALUES ('COCA-COLA (2 ltr)', 89, 2);

INSERT INTO Product (product_name, product_price, category_id)
VALUES ('Mirinda (2 ltr)', 78, 2);

INSERT INTO Product (product_name, product_price, category_id)
VALUES ('SOAN-PAPDI', 250, 3);

INSERT INTO Product (product_name, product_price, category_id)
VALUES ('GULAB JAMUN', 450, 3);

INSERT INTO Product (product_name, product_price, category_id)
VALUES ('RASGULLA', 500, 3);


INSERT INTO Product (product_name, product_price, category_id)
VALUES ('Queso Cabrales', 210, 4);

INSERT INTO Product (product_name, product_price, category_id)
VALUES ('Geitost', 450, 4);

INSERT INTO Product (product_name, product_price, category_id)
VALUES ('Cheese', 150, 5);

SELECT * FROM Product;
