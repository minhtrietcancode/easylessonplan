from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

PROJECT_REF = os.getenv("SUPABASE_PROJECT_REF")
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")

if not PROJECT_REF or not SUPABASE_PASSWORD:
    print("Please set SUPABASE_PROJECT_REF and SUPABASE_PASSWORD in your .env")
    raise SystemExit(1)

def test_connection():
    try:
        conn = psycopg2.connect(
            host=f"db.{PROJECT_REF}.supabase.co",
            port=5432,
            dbname="postgres",
            user="postgres",
            password=SUPABASE_PASSWORD,
            sslmode="require"   # Supabase requires TLS
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        print("✅ Connected. PostgreSQL version:", cur.fetchone()[0])
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Connection failed!")
        print(e)

if __name__ == "__main__":
    test_connection()
