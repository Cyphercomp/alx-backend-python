import time
import sqlite3
import functools

query_cache = {}  # Dictionary to store query results


# Decorator to handle opening and closing a database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()

    return wrapper


# Decorator to cache query results based on the query string
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract the SQL query string from either args or kwargs
        if "query" in kwargs:
            query = kwargs["query"]
        else:
            # Assume the second argument is the query if unnamed
            query = args[0] if len(args) > 0 else None

        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for: {query}")
            return query_cache[query]
        else:
            print(f"[CACHE MISS] Executing and caching result for: {query}")
            result = func(conn, *args, **kwargs)
            query_cache[query] = result  # Store result in cache
            return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
