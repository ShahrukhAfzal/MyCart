def get_login_query(username, password):

	login_query = f"""  SELECT *
						FROM User
						WHERE (user_name='{username}'
						and password='{password}');
					"""

	return login_query


def get_all_user_query():
	return "SELECT user_id, user_name FROM User WHERE is_admin=false;"


def get_all_bill_by_user_query(user):
	get_all_bill_by_user = f""" SELECT user.user_id,
								user.user_name,
								ord.order_id,
								ord.order_date,
								(ord.actual_amount - ord.discounted_amount) AS Bill
								FROM Orders AS ord
								NATURAL JOIN User AS user
								WHERE user.user_id={user};
								"""

	return get_all_bill_by_user


def create_user_query(**user_dict):
	user_id = user_dict['user_id']
	user_name = user_dict['user_name']
	user_email = user_dict['user_email']
	password = user_dict['password']
	is_admin = user_dict['is_admin']

	create_user_query = f"""INSERT INTO User (user_id, user_name, user_email, password, is_admin)
                            VALUES ('{user_id}', '{user_name}', '{user_email}', '{password}', '{is_admin}');
                        """

	return create_user_query

