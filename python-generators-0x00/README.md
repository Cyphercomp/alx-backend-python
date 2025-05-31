# python-generators-0x00

## Overview

This project demonstrates how to efficiently interact with a MySQL database in Python using generators. It covers setting up a MySQL database, creating tables, seeding data from a CSV file, and implementing memory-efficient data streaming and processing using Python generators.

Generators are used throughout the project to stream rows from the database, handle large datasets in batches, lazily paginate data, and perform aggregation operations without loading all data into memory.

---

## Files and Exercises

- **seed.py**  
  Contains functions to connect to the MySQL server, create the `ALX_prodev` database and `user_data` table, and insert user data from `user_data.csv`.

- **user_data.csv**  
  Sample CSV file containing user records used to populate the database.

- **0-stream_users.py**  
  Implements `stream_users()` — a generator function that streams user rows one by one from the database using Python’s `yield`.

- **1-batch_processing.py**  
  Implements:
  - `stream_users_in_batches(batch_size)`: generator that fetches user rows in batches.
  - `batch_processing(batch_size)`: processes batches to filter users older than 25 years.

- **2-lazy_paginate.py**  
  Implements:
  - `paginate_users(page_size, offset)`: fetches a single page of users.
  - `lazy_pagination(page_size)`: generator that lazily fetches pages of users on demand.

- **4-stream_ages.py**  
  Implements:
  - `stream_user_ages()`: generator yielding user ages one by one.
  - `average_age()`: calculates average user age using the generator without loading all data into memory or using SQL’s AVG.

---

## Database Schema

**Database:** `ALX_prodev`

**Table:** `user_data`

| Column  | Type     | Constraints                 |
| ------- | -------- | ---------------------------|
| user_id | CHAR(36) | PRIMARY KEY, UUID, Indexed |
| name    | VARCHAR  | NOT NULL                   |
| email   | VARCHAR  | NOT NULL                   |
| age     | DECIMAL  | NOT NULL                   |

---

## Setup and Usage

### 1. Configure MySQL Connection

Update the MySQL connection details (username, password) in `seed.py` to match your environment.

### 2. Initialize Database and Seed Data

Run `0-main.py` to:

- Connect to the MySQL server.
- Create the `ALX_prodev` database if it does not exist.
- Connect to the `ALX_prodev` database.
- Create the `user_data` table if it does not exist.
- Insert data from `user_data.csv` into the table.
- Verify the database and table contents.

```

