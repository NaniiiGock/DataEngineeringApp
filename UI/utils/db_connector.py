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
            return result['role_name'] if result else None
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
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT user_id FROM user_dim WHERE email = %s", (email,))
            result = cursor.fetchone()
            if not result:
                cursor.execute(
                    """
                    INSERT INTO user_dim (email, name, role_id)
                    VALUES (%s, %s, (SELECT role_id FROM role_dim WHERE role_name = 'user'))
                    RETURNING user_id
                    """,
                    (email, name)
                )
                conn.commit()
                return cursor.fetchone()[0]
            return result[0]
        finally:
            cursor.close()
            conn.close()

    def get_action_id(self, action_name):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT action_id FROM action_dim WHERE action_name = %s", (action_name,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            cursor.close()
            conn.close()

    def log_activity(self, user_id, action_id, details=None):
        if not user_id or not action_id:
            print("Error: user_id or action_id is missing. Activity not logged.")
            return

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO activity_fact (user_id, action_id, details, timestamp)
            VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(query, (user_id, action_id, details))
            conn.commit()
        finally:
            cursor.close()
            conn.close()