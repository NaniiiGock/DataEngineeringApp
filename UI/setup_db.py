import psycopg2
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "mydatabase"),
}

CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS role_dim (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    role_description TEXT
);

CREATE TABLE IF NOT EXISTS user_dim (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    role_id INT REFERENCES role_dim(role_id)
);

CREATE TABLE IF NOT EXISTS action_dim (
    action_id SERIAL PRIMARY KEY,
    action_name VARCHAR(50) UNIQUE NOT NULL,
    action_description TEXT
);

CREATE TABLE IF NOT EXISTS activity_fact (
    activity_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES user_dim(user_id),
    action_id INT REFERENCES action_dim(action_id),
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INSERT_INITIAL_DATA = """
INSERT INTO role_dim (role_name, role_description)
VALUES 
    ('admin', 'Administrator with full privileges'),
    ('user', 'Regular user with limited access')
ON CONFLICT (role_name) DO NOTHING;

INSERT INTO action_dim (action_name, action_description)
VALUES 
    ('login', 'User logged into the system'),
    ('update_role', 'Admin updated a user role'),
    ('view_dashboard', 'User viewed the dashboard')
ON CONFLICT (action_name) DO NOTHING;

INSERT INTO user_dim (email, name, role_id)
VALUES 
    ('nanigock@gmail.com', 'Admin User', (SELECT role_id FROM role_dim WHERE role_name = 'admin')),
    ('liliana.hotsko@ucu.edu.ua', 'Liliana Hotsko', (SELECT role_id FROM role_dim WHERE role_name = 'user'))
ON CONFLICT (email) DO NOTHING;
"""

def setup_database():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        print("Creating tables...")
        cursor.execute(CREATE_TABLES)
        print("Inserting initial data...")
        cursor.execute(INSERT_INITIAL_DATA)
        conn.commit()
        print("Database setup complete.")
    except Exception as e:
        print(f"Error setting up the database: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    setup_database()
