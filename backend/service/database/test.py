import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables from environment
USER = os.getenv("user")
PASSWORD = os.getenv("password") 
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Debug: Check if variables are loaded correctly
print(f"USER: {USER}")
print(f"PASSWORD: {PASSWORD[:3]}***{PASSWORD[-3:] if PASSWORD else 'None'}")  # Show first/last 3 chars
print(f"HOST: {HOST}")
print(f"PORT: {PORT}")
print(f"DBNAME: {DBNAME}")
print("-" * 40)

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME,
        sslmode='require'
    )
    print("✅ Connection successful!")

    # Create a cursor to execute SQL commands
    cursor = connection.cursor()

    try:
        # Insert a sample user
        insert_query = """
            INSERT INTO users (email, first_name)
            VALUES (%s, %s)
            RETURNING id, email, first_name, created_at;
        """
        cursor.execute(insert_query, ("sample@gmail.com", "Sample"))

        # Fetch the inserted row
        new_user = cursor.fetchone()
        print("✅ Inserted user:", new_user)

        # Commit the transaction so changes are saved
        connection.commit()

        # Select all users to verify
        cursor.execute("SELECT id, email, first_name, created_at FROM users;")
        all_users = cursor.fetchall()
        print("\n📋 All users in the database:")
        for user in all_users:
            print(user)

    except Exception as e:
        print(f"❌ Failed to insert/select user: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()
        print("🔒 Connection closed")

except Exception as e:
    print(f"❌ Failed to connect: {e}")
