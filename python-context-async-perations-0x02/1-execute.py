import sqlite3


class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name  # Database file name
        self.query = query  # SQL query string
        self.params = params or ()  # Parameters for the query
        self.connection = None  # Will hold the database connection
        self.cursor = None  # Will hold the cursor object
        self.result = None  # Will hold the result of the query

    def __enter__(self):
        # Open connection and execute the query
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result  # Return the result of the query

    def __exit__(self, exc_type, exc_value, traceback):
        # Close connection safely
        if self.connection:
            self.connection.commit()
            self.connection.close()
        if exc_type:
            print(f"An error occurred: {exc_value}")
        return False  # Propagate any exceptions


# --------- Example Usage ---------
def setup_demo_data():
    with sqlite3.connect("1-example.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """
        )
        cursor.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [
                ("Peter", 22),
                ("Anne", 30),
                ("Martin", 27),
                ("Diana", 19),
                ("Eve", 35),
                ("Jane", 15),
                ("John", 40),
                ("Alice", 28),
                ("Simon", 20),
            ],
        )
        conn.commit()


setup_demo_data()

# --------- Use the ExecuteQuery context manager ---------
query = "SELECT * FROM users WHERE age > ?"
param = (25,)

with ExecuteQuery("1-example.db", query, param) as results:
    for row in results:
        print(row)
