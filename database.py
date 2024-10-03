import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect('history.db')
c = conn.cursor()

# Create table for storing prompts and generated content
c.execute('''CREATE TABLE IF NOT EXISTS history
             (id INTEGER PRIMARY KEY, prompt TEXT, tone TEXT, content TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

# Function to save generated content and prompt into the database
def save_to_db(prompt, tone, content):
    c.execute("INSERT INTO history (prompt, tone, content) VALUES (?, ?, ?)", (prompt, tone, content))
    conn.commit()

# Function to retrieve content history
def get_history():
    c.execute("SELECT prompt, tone, content, date FROM history ORDER BY date DESC")
    return c.fetchall()

# Close the database connection when done (optional, can also be done in a separate function)
def close_connection():
    conn.close()
