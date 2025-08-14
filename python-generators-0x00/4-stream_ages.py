from decimal import Decimal
from seed import connect_to_prodev

def stream_user_ages():
    """Generator that yields user ages one at a time from the database."""
    connection = connect_to_prodev()
    cursor = connection.cursor()

    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        if isinstance(age, Decimal):
            yield int(age)
        else:
            yield age

    cursor.close()
    connection.close()

def compute_average_age():
    """
    Computes and prints the average age of users by iterating over a stream of user ages.
    If no users are found, it prints a message indicating this.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    compute_average_age()
