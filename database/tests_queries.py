def drop_db_query(DB_NAME):
    drop_db_query = f"""DROP DATABASE IF EXISTS {DB_NAME}"""

    return drop_db_query

def create_db_query(DB_NAME):
    create_db_query = f"""create DATABASE IF NOT EXISTS {DB_NAME}"""

    return create_db_query

