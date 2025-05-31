#!/usr/bin/env python3
"""
Reusable Query Context Manager for executing SQL queries with parameters
"""

import mysql.connector


class ExecuteQuery:
    def __init__(self, query, params=None,
                 host="localhost", user="root", password="", database="alx_prodev"):
        """
        Initialize with query, parameters, and connection settings
        """
        self.query = query
        self.params = params or ()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        Connect to the database, execute the query and return results
        """
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the cursor and connection
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Example: select users where age > 25
    query = "SELECT * FROM users WHERE age > %s"
    param = (25,)

    with ExecuteQuery(query, param, database="your_database_name") as results:
        for row in results:
            print(row)
