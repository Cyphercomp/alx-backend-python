import mysql.connector
from decimal import Decimal

def stream_users():
    # Connect to the ALX_prodev database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Habakkuk",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    # Execute query
    cursor.execute("SELECT * FROM user_data")

    # Fetch and yield one row at a time
    for row in cursor:
        # Convert Decimal to int for age
        if isinstance(row['age'], Decimal):
            row['age'] = int(row['age'])
        yield row

    # Close resources
    cursor.close()
    connection.close()

__all__ = ['stream_users']