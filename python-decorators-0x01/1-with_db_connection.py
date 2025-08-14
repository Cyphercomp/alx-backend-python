import sqlite3
import functools


# Decorator that opens and closes a database connection automatically
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")  # Open a new database connection
        try:
            # Inject the connection as the first argument to the function
            return func(conn, *args, **kwargs)
        finally:
            conn.close()  # Ensure the connection is closed even if an error occurs

    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    )  # Execute parameterized query
    return cursor.fetchone()  # Fetch and return the first result row


# Fetch a user by ID with automatic DB connection handling
user = get_user_by_id(user_id=1)
print(user)
