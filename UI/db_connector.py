import os
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "mydatabase"),
}

class DBConnector:

    def get_db_connection(self):
        return psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )

    def get_user_role(self, email):
        """Fetch the user's role based on their email."""
        conn = self.get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SELECT r.role_name
            FROM user_dim u
            JOIN role_dim r ON u.role_id = r.role_id
            WHERE u.email = %s
            """
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result:
                return result['role_name']
            else:
                print(f"User with email {email} not found or no role assigned.")
                return None
        except Exception as e:
            print(f"Error fetching user role for email {email}: {e}")
            return None
        finally:
            cursor.close()
            conn.close()


    def fetch_table_data(self, table_name):
        conn = self.get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            return pd.DataFrame(data) if data else pd.DataFrame()
        finally:
            cursor.close()
            conn.close()

    def ensure_user_exists(self, email, name):
        """Ensure the user exists in the database with the Regular User role, excluding predefined users."""
        predefined_users = {
            'nanigock@gmail.com': 'admin',
            'liliana.hotsko@ucu.edu.ua': 'user'
        }
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            if email in predefined_users:
                print(f"User {email} is predefined with role '{predefined_users[email]}'. Skipping creation.")
                return

            cursor.execute("SELECT role_id FROM role_dim WHERE role_name = 'user'")
            user_role = cursor.fetchone()

            if not user_role:
                print("Error: 'user' role not found in role_dim. Check database initialization.")
                return

            user_role_id = user_role[0]

            cursor.execute("SELECT user_id FROM user_dim WHERE email = %s", (email,))
            result = cursor.fetchone()

            if not result:
                cursor.execute(
                    """
                    INSERT INTO user_dim (email, name, role_id)
                    VALUES (%s, %s, %s)
                    """,
                    (email, name, user_role_id)
                )
                conn.commit()
                print(f"New user {email} added with role 'user'.")
        except Exception as e:
            print(f"Error ensuring user exists: {e}")
        finally:
            cursor.close()
            conn.close()