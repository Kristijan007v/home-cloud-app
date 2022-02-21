import sqlite3

# Connecting to sqlite
# connection object
connection_obj = sqlite3.connect('db.sqlite')

# cursor object
cursor_obj = connection_obj.cursor()

# Drop the GEEK table if already exists.
cursor_obj.execute("DROP TABLE IF EXISTS notes")

command = """DROP TABLE IF EXISTS NOTES"""

# Creating table
table = """ CREATE TABLE notes (
            noteId INTEGER PRIMARY KEY,
            note VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ); """

cursor_obj.execute(table)

print("Table is Ready")

# Close the connection
connection_obj.close()
