from seed import connect_to_prodev
from decimal import Decimal

def paginate_users(page_size, offset):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()

    # Convert Decimal age to int
    for row in rows:
        if isinstance(row.get('age'), Decimal):
            row['age'] = int(row['age'])

    connection.close()
    return rows

def lazy_pagination(page_size):
    """
    Generator function that yields paginated user data in chunks of the specified page size.
    """
    offset = 0
    while True:
        users = paginate_users(page_size, offset)
        if not users:
            break
        # print(f"Fetched page at offset {offset}")
        yield users
        offset += page_size
