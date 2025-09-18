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
    
except Exception as e:
    print(f"❌ Failed to connect: {e}")