#!/usr/bin/env python3

import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            kwargs['conn'] = conn
            result = func(*args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    return wrapper
    
    
def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = kwargs.get('conn')
        if not conn:
            raise ValueError("Database connection 'conn' not found in keyword arguments.  Ensure with_db_connection decorator is applied first.")
        try:
            result = func(*args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            print(f"Transaction failed, rolling back: {e}")
            conn.rollback()
            raise  # Re-raise the exception to propagate it
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
