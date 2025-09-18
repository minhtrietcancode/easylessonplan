import psycopg2
from dotenv import load_dotenv
import os

class DatabaseHandler:
    def __init__(self):
        # Load environment variables from .env
        load_dotenv()
        self.USER = os.getenv("user")
        self.PASSWORD = os.getenv("password")
        self.HOST = os.getenv("host")
        self.PORT = os.getenv("port")
        self.DBNAME = os.getenv("dbname")

        try:
            self.connection = psycopg2.connect(
                user=self.USER,
                password=self.PASSWORD,
                host=self.HOST,
                port=self.PORT,
                dbname=self.DBNAME,
                sslmode='require'
            )
            self.cursor = self.connection.cursor()
            print("✅ Database connection established")
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            self.connection = None
            self.cursor = None

    def insert_user(self, email, first_name):
        """Insert a new user into the database"""
        if not self.cursor:
            print("❌ No database connection")
            return None
        
        try:
            query = """
                INSERT INTO users (email, first_name)
                VALUES (%s, %s)
                RETURNING id, email, first_name, created_at;
            """
            self.cursor.execute(query, (email, first_name))
            new_user = self.cursor.fetchone()
            self.connection.commit()
            print("✅ Inserted user:", new_user)
            return new_user
        except Exception as e:
            print(f"❌ Failed to insert user: {e}")
            self.connection.rollback()
            return None

    def check_exist_user(self, email, first_name):
        """Check if a user exists by email and first_name"""
        if not self.cursor:
            print("❌ No database connection")
            return False
        
        try:
            query = """
                SELECT id, email, first_name, created_at
                FROM users
                WHERE email = %s AND first_name = %s;
            """
            self.cursor.execute(query, (email, first_name))
            user = self.cursor.fetchone()
            if user:
                print("✅ User exists:", user)
                return True
            else:
                print("ℹ️ User not found")
                return False
        except Exception as e:
            print(f"❌ Failed to check user: {e}")
            return False

    def close(self):
        """Close cursor and connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("🔒 Database connection closed")


# Example usage
if __name__ == "__main__":
    db = DatabaseHandler()

    # Check if user exists first
    exists = db.check_exist_user("sample@gmail.com", "Sample")
    if not exists:
        db.insert_user("sample@gmail.com", "Sample")

    # Close connection
    db.close()
