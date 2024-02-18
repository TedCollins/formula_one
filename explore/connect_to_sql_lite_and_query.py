import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('cache/fastf1_http_cache.sqlite')

cursor = conn.cursor()

# Query to select all table names in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all results from the executed command
tables = cursor.fetchall()

# Print the names of the tables
for table in tables:
    print(table[0])


cursor.execute("PRAGMA table_info(responses);")

# Fetch and print all the rows
columns = cursor.fetchall()
for column in columns:
    print(column)


# Don't forget to close the connection when you're done
conn.close()