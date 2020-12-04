def get_login_query(username, password):

    query = f"""SELECT *
                FROM User
                WHERE (user_name='{username}'
                and password='{password}');
            """

    return query
