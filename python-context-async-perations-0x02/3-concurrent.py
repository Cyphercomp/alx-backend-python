import asyncio
import aiosqlite


# --------- Example Usage ---------
async def setup_demo_data():
    async with aiosqlite.connect("3-example.db") as db:
        await db.execute("DROP TABLE IF EXISTS users")
        await db.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """
        )
        await db.execute("DELETE FROM users")  # Clear table before inserting
        await db.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [
                ("Peter", 22),
                ("Anne", 30),
                ("Martin", 27),
                ("Joy", 50),
                ("Diana", 19),
                ("Eve", 35),
                ("Jane", 15),
                ("Tim", 55),
                ("John", 40),
                ("Alice", 28),
                ("Simon", 20),
            ],
        )
        await db.commit()


# Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("3-example.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("\nAll Users:")
            for user in users:
                print(user)
            return users


# Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("3-example.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            users = await cursor.fetchall()
            print("\nUsers older than 40:")
            for user in users:
                print(user)
            return users


# Run both queries concurrently
async def fetch_concurrently():
    await setup_demo_data()
    await asyncio.gather(async_fetch_users(), async_fetch_older_users())


# Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
