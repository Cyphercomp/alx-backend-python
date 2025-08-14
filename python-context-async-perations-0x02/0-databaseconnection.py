import sqlite3


class DatabaseConnection:
    def __init__(self, db_name):
        # Store the database name
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Establish a connection to the database
        self.connection = sqlite3.connect(self.db_name)
        # Create a cursor to execute queries
        self.cursor = self.connection.cursor()
        return self.cursor  # Return the cursor to be used inside the 'with' block

    def __exit__(self, exc_type, exc_value, traceback):
        # Commit any changes
        if self.connection:
            self.connection.commit()
            self.connection.close()  # Close the connection
        # Handle exceptions (if any occurred in the 'with' block)
        if exc_type:
            print(f"An error occurred: {exc_value}")
        return False  # Do not suppress exceptions


# ----- Example usage -----


# Create a test database and table if not exists (for demonstration)
def setup_demo_data():
    with DatabaseConnection("0-example.db") as cursor:
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """
        )
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Peter",))
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Anne",))
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Martin",))
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Jane",))


setup_demo_data()

# Use the custom context manager to fetch data
with DatabaseConnection("0-example.db") as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)
