import mysql.connector
from mysql.connector import errorcode
import csv

def connect_db():
    """Connect to MySQL server (without specifying DB)"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if not exists"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    cursor.close()

def connect_to_prodev():
    """Connect to ALX_prodev database"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # change as needed
            database="ALX_prodev"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Create user_data table if not exists"""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX(user_id)
    )
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    cursor.close()

def insert_data(connection, csv_file):
    """Insert data from CSV into user_data table if not exists"""
    cursor = connection.cursor()
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check if user_id already exists
            cursor.execute("SELECT 1 FROM user_data WHERE user_id = %s", (row['user_id'],))
            if cursor.fetchone():
                continue  # skip existing

            insert_query = """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """
            try:
                cursor.execute(insert_query, (row['user_id'], row['name'], row['email'], row['age']))
            except mysql.connector.Error as err:
                print(f"Error inserting row {row}: {err}")
    connection.commit()
    cursor.close()
