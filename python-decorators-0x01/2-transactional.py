import sqlite3
import functools


# Decorator that opens and closes a database connection
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


# Decorator to wrap a DB operation in a transaction
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # Run the DB operation
            conn.commit()  # Commit if successful
            return result
        except Exception as e:
            conn.rollback()  # Roll back if there's an error
            raise e  # Re-raise the exception for visibility

    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Update user email with automatic connection and transaction handling
update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
