import sqlite3

# Step 1: Connect to a database or create one if it doesn't exist
conn = sqlite3.connect('example.db')

# Step 2: Create a cursor object to interact with the database
cursor = conn.cursor()

# Step 3: Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL
                )''')

# Step 4: Insert data into the table
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('John', 'John@example.com'))
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('Doe', 'Doe@example.com'))

# Step 5: Save (commit) the changes
conn.commit()

# Step 6: Retrieve data from the table
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# Step 7: Display the retrieved data
for row in rows:
    print(row)

# Step 8: Close the connection
conn.close()