#!/usr/bin/env python3
"""
Custom class-based context manager for MySQL database connection
"""

import mysql.connector


class DatabaseConnection:
    def __init__(self, host="localhost", user="root", password="", database="alx_prodev"
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Connect to the database and return the cursor"""
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Close cursor and connection on exit"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Use the context manager to run SELECT query
    with DatabaseConnection(database="your_database_name") as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
