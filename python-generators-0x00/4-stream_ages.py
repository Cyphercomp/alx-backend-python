#!/usr/bin/python3
import mysql.connector

def stream_user_ages():
    """Generator to yield user ages one by one from the database"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # update accordingly
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT age FROM user_data")
        for (age,) in cursor:
            yield age
    finally:
        cursor.close()
        conn.close()


def average_age():
    """Calculates average age using stream_user_ages generator without loading all data at once"""
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    if count == 0:
        print("No users found.")
        return
    avg = total_age / count
    print(f"Average age of users: {avg:.2f}")


if __name__ == "__main__":
    average_age()
