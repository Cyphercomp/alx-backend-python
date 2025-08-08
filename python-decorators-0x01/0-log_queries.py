#!/usr/bin/env python3

import sqlite3
import functools
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel('INFO')
handler = logging.FileHandler("query.log", mode="a")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s : %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

#### decorator to log SQL queries

def log_queries(func):
    @functools.wraps(func)    
    def log_queries_wrapper(*args, **kwargs):
        arg = [v for v in args]
        kwarg = [f"{k}={v}" for k,v in kwargs.items()]
        query = "Executing: {} - {}".format(arg, kwarg)
        print(query)
        logger.info(query)
        return func(*args,**kwargs)
    return log_queries_wrapper
         
         

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
