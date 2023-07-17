import sqlite3


# Connect to the database
conn = sqlite3.connect('webui/GPT4_summaries.db')
cursor = conn.cursor()

# Execute a SELECT query
cursor.execute("SELECT * FROM Summaries")

# Fetch all the rows
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

# get the number of rows in the cursor object
num_rows = cursor.execute("SELECT COUNT(*) FROM Summaries").fetchone()[0]
print(f"\nNumber of rows: {num_rows}")
# Close the connection
conn.close()
