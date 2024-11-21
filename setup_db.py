import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "lilianahotsko",         
    "password": "passpost", 
    "database": "postgres"   
}

CREATE_ROLE_DIM = """
CREATE TABLE IF NOT EXISTS role_dim (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    role_description TEXT
);
"""

CREATE_USER_DIM = """
CREATE TABLE IF NOT EXISTS user_dim (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    role_id INT REFERENCES role_dim(role_id)
);
"""

CREATE_ACTION_DIM = """
CREATE TABLE IF NOT EXISTS action_dim (
    action_id SERIAL PRIMARY KEY,
    action_name VARCHAR(50) UNIQUE NOT NULL,
    action_description TEXT
);
"""

CREATE_ACTIVITY_FACT = """
CREATE TABLE IF NOT EXISTS activity_fact (
    activity_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES user_dim(user_id),
    action_id INT REFERENCES action_dim(action_id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INSERT_ROLES = """
INSERT INTO role_dim (role_name, role_description)
VALUES 
    ('admin', 'Administrator with full privileges'),
    ('user', 'Regular user with limited access')
ON CONFLICT (role_name) DO NOTHING;
"""

INSERT_ACTIONS = """
INSERT INTO action_dim (action_name, action_description)
VALUES 
    ('login', 'User logged into the system'),
    ('update_role', 'Admin updated a user role'),
    ('view_dashboard', 'User viewed the dashboard')
ON CONFLICT (action_name) DO NOTHING;
"""

INSERT_USERS = """
INSERT INTO user_dim (email, name, role_id)
VALUES 
    ('nanigock@gmail.com', 'Admin User', 1),
    ('liliana.hotsko@ucu.edu.ua', 'Regular User', 2)
ON CONFLICT (email) DO NOTHING;
"""

INSERT_ACTIVITIES = """
INSERT INTO activity_fact (user_id, action_id)
VALUES 
    (1, 1), -- Admin logs in
    (2, 3)  -- User views the dashboard
ON CONFLICT DO NOTHING;
"""

def connect_to_db():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

def create_tables():
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        print("Creating star schema tables...")
        cursor.execute(CREATE_ROLE_DIM)
        cursor.execute(CREATE_USER_DIM)
        cursor.execute(CREATE_ACTION_DIM)
        cursor.execute(CREATE_ACTIVITY_FACT)
        conn.commit()
        print("Tables created successfully.")
    except Exception as e:
        print("Error creating tables:", e)
    finally:
        cursor.close()
        conn.close()

def insert_sample_data():
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        print("Inserting sample data...")
        cursor.execute(INSERT_ROLES)
        cursor.execute(INSERT_ACTIONS)
        cursor.execute(INSERT_USERS)
        cursor.execute(INSERT_ACTIVITIES)
        conn.commit()
        print("Sample data inserted successfully.")
    except Exception as e:
        print("Error inserting sample data:", e)
    finally:
        cursor.close()
        conn.close()

def main():
    print("Setting up the star schema...")
    create_tables()
    insert_sample_data()
    print("Star schema setup and sample data insertion complete.")

if __name__ == "__main__":
    main()
