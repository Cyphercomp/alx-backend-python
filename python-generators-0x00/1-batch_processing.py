#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that fetches user_data rows from the database in batches of batch_size"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # update this
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return

    cursor = conn.cursor(dictionary=True)
    offset = 0

    try:
        while True:
            cursor.execute(
                "SELECT user_id, name, email, age FROM user_data "
                "ORDER BY user_id LIMIT %s OFFSET %s",
                (batch_size, offset)
            )
            batch = cursor.fetchall()
            if not batch:
                break
            yield batch
            offset += batch_size
    finally:
        cursor.close()
        conn.close()


def batch_processing(batch_size):
    """Process each batch and yield users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
