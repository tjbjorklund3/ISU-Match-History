import sqlite3
from config import db_file_path

# Connect to the database and list the tables
def list_tables():
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()

    print("Tables in the database:")
    for table in tables:
        print(table[0])

if __name__ == "__main__":
    list_tables()
