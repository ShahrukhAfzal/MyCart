def get_login_query(username, password):

    login_query = f"""  SELECT *
                        FROM User
                        WHERE (user_name='{username}'
                        and password='{password}');
                    """

    return login_query
