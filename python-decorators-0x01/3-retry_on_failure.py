#!/usr/bin/env python3

import time
import sqlite3 
import functools

#### paste your with_db_decorator here

def with_db_connection(func):
    """
    Decorator to manage SQLite database connections.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None  # Initialize conn outside the try block
        try:
            conn = sqlite3.connect('users.db')
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()  # Rollback changes if an error occurred
            raise  # Re-raise the exception to be handled by retry_on_failure
        finally:
            if conn:
                conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator to retry a function upon failure.

    Args:
        retries (int): Number of times to retry the function.
        delay (int): Delay in seconds between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts <= retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed: {e}")
                    if attempts <= retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("Max retries reached.  Raising the exception.")
                        raise  # Re-raise the exception after all retries fail
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)