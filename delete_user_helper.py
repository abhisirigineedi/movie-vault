import sqlite3
import sys

def delete_user_account(identifier):
    db_path = 'movies.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys so movies are deleted automatically
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Delete by ID if numeric, otherwise by username
    if identifier.isdigit():
        print(f"--- Deleting user with ID: {identifier} ---")
        cursor.execute("DELETE FROM users WHERE id = ?", (int(identifier),))
    else:
        print(f"--- Deleting user with username: {identifier} ---")
        cursor.execute("DELETE FROM users WHERE username = ?", (identifier,))
    
    if cursor.rowcount > 0:
        print(f"SUCCESS: User and all their associated data have been deleted.")
    else:
        print(f"FAILED: No user found with that identifier.")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python delete_user_helper.py <username>")
    else:
        delete_user_account(sys.argv[1])
