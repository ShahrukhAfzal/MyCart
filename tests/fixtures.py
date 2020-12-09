users_fixtures = {
    'admin_user': [{
        'user_id' : 1,
        'user_name' : 'admin',
        'user_email' : 'admin@gmail.com',
        'is_admin': 1,
        'password':'123456'

    }],
    'customer_user': [{
        'user_id' : 2,
        'user_name' : 'shahrukh',
        'user_email' : 'shoaibtayyab121@gmail.com',
        'is_admin': 0,
        'password':'123456'

    }]

}


categories_fixtures =  [
        {
            'category_id': 1,
            'category_name': 'ELECTRONICS',
            'category_description': 'T.V., Laptop, PC, Mobile etc.'
        },
        {
            'category_id': 2,
            'category_name': 'Beverages',
            'category_description': 'Soft drinks, coffees, teas, beers, and ales.'
        },
        {
            'category_id': 3,
            'category_name': 'Condiments',
            'category_description': 'Sweet and savory sauces, relishes, spreads, and seasonings'
        },
        {
            'category_id': 4,
            'category_name': 'HOME & KITCHEN APPLIANCES',
            'category_description': 'Water Purifiers, Inverters, Geyser etc.'
        }
    ]


products_fixtures = [
        {
            'product_id': 1,
            'product_name': 'MOTO X-Play',
            'product_price': '13500.00',
            'category_id': 1
        },
        {
            'product_id': 2,
            'product_name': 'LENOVO ideapad 320',
            'product_price': '27499.00',
            'category_id': 1
        },
        {
            'product_id': 3,
            'product_name': 'Samsung Galaxy S4',
            'product_price': '17689.00',
            'category_id': 1
        },
        {
            'product_id': 4,
            'product_name': 'COCA-COLA (2 ltr)',
            'product_price': '89.00',
            'category_id': 2
        },
        {
            'product_id': 5,
            'product_name': 'Mirinda (2 ltr)',
            'product_price': '78.00',
            'category_id': 2
        },
        {
            'product_id': 6,
            'product_name': 'SOAN-PAPDI',
            'product_price': '250.00',
            'category_id': 3
        },
        {
            'product_id': 7,
            'product_name': 'GULAB JAMUN',
            'product_price': '450.00',
            'category_id': 3
        },
        {
            'product_id': 8,
            'product_name': 'RASGULLA',
            'product_price': '500.00',
            'category_id': 3
        }

    ]
