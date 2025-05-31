#!/usr/bin/python3
import mysql.connector

def stream_users():
    """Generator that streams rows from user_data one by one"""
    # Connect to the ALX_prodev database
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # change this accordingly
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return  # Exit generator if connection fails

    cursor = conn.cursor(dictionary=True)  # dictionary=True to get rows as dicts

    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        # Single loop to fetch and yield rows one at a time
        for row in cursor:
            yield row
    finally:
        cursor.close()
        conn.close()
