#!/usr/bin/env python3

import sqlite3

def create_users_table(db_name="users.db"):
    """
    Creates a SQLite3 database with a 'users' table if it doesn't exist.
    Args:
        db_name (str): The name of the SQLite3 database file. Defaults to "test.db".
    """

    try:
        # Connect to the SQLite database (creates it if it doesn't exist)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create the 'users' table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Commit the changes and close the connection
        conn.commit()
        print(f"Database '{db_name}' created successfully with 'users' table.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


def populate_users_table(db_name="users.db"):
  """
  Populates the users table with some example data.

  Args:
        db_name (str): The name of the SQLite3 database file. Defaults to "test.db".
  """
  try:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert some sample data
    users_data = [
        ("john_doe", "password123", "john.doe@example.com"),
        ("jane_smith", "securepass", "jane.smith@example.org"),
        ("peter_jones", "p@$$wOrd", "peter.jones@example.net"),
    ]

    cursor.executemany("""
        INSERT INTO users (username, password, email)
        VALUES (?, ?, ?)
    """, users_data)

    conn.commit()
    print("Users table populated with sample data.")

  except sqlite3.Error as e:
    print(f"An error occurred: {e}")
  finally:
    if conn:
      conn.close()



if __name__ == "__main__":
    # Create the database and users table
    create_users_table()

    # Populate the table with sample data
    populate_users_table()

    # Optional: Verify the data
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        print("\nData in the 'users' table:")
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print(f"An error occurred while reading data: {e}")
    finally:
        if conn:
            conn.close()
