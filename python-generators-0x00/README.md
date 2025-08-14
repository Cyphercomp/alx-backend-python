# Python Generators: Streaming, Batching, and Pagination with SQL

This project demonstrates how to use **Python generators** to efficiently stream and process data from a MySQL database. It focuses on lazy loading, batching, pagination, and memory-efficient aggregation, all without loading the entire dataset into memory.

---

## 📁 Files

| File Name             | Description |
|----------------------|-------------|
| `0-stream_users.py`  | Contains a generator function `stream_users()` that connects to a MySQL database and lazily yields user records one at a time from the `user_data` table. |
| `1-batch_processing.py` | Implements `stream_users_in_batches(batch_size)` to fetch user data in batches, and `batch_processing(batch_size)` to filter users older than 25 using a generator. |
| `2-lazy_paginate.py` | Contains `lazy_pagination(page_size)` which uses a generator to simulate pagination — it lazily loads user records page-by-page from the database. |
| `4-stream_ages.py`   | Contains a generator `stream_user_ages()` that yields user ages one by one, and a function to compute the average user age without loading the full dataset into memory. |
| `seed.py`            | Utility module to establish a MySQL database connection (typically via `connect_to_prodev()`), used by other scripts for database access. |

---

## 🛠 Requirements

- Python 3.x
- `mysql-connector-python`
- Access to a MySQL database with a `user_data` table

---

## 🚀 Running the Examples

Activate your virtual environment and use the provided `main.py` scripts to test functionality. Example:

```bash
python3 1-main.py
python3 3-main.py | head -n 7
python3 4-stream_ages.py
```

---

## 📚 Key Concepts Demonstrated

- Generators for lazy data loading
- Streaming database rows without full memory load
- Batching records from SQL queries
- Pagination via `LIMIT` and `OFFSET`
- Aggregation (average) using a generator


