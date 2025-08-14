import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

DB_NAME = "ALX_prodev"

TABLES = {
    "user_data": (
        "CREATE TABLE IF NOT EXISTS user_data ("
        "  user_id CHAR(36) PRIMARY KEY,"
        "  name VARCHAR(255) NOT NULL,"
        "  email VARCHAR(255) NOT NULL,"
        "  age DECIMAL NOT NULL,"
        "  INDEX(user_id)"
        ") ENGINE=InnoDB"
    )
}


def connect_db():
    """Connects to MySQL server (no database yet)"""
    try:
        return mysql.connector.connect(user='root', password='Habakkuk')
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None


def create_database(connection):
    """Creates the ALX_prodev database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")


def connect_to_prodev():
    """Connects to the ALX_prodev database"""
    try:
        return mysql.connector.connect(user='root', password='Habakkuk', database=DB_NAME)
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        return None


def create_table(connection):
    """Creates the user_data table if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute(TABLES['user_data'])
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    finally:
        cursor.close()


def insert_data(connection, csv_file):
    """Inserts data from CSV into user_data table with generated UUIDs"""
    cursor = connection.cursor()
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age),
                )
        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()