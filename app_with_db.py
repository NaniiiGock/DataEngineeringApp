import streamlit as st
from streamlit_google_auth import Authenticate
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import altair as alt
import plotly.express as px
import os
import requests

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "mydatabase"),
}

def get_db_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

def get_user_role(email):
    """Fetch the user's role based on their email."""
    conn = get_db_connection()
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


def fetch_table_data(table_name):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        return pd.DataFrame(data) if data else pd.DataFrame()
    finally:
        cursor.close()
        conn.close()

API_URL = "http://localhost:5000/api"  # Update with your Flask API URL

def fetch_data(endpoint, payload):
    try:
        response = requests.post(f"{API_URL}/{endpoint}", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def ensure_user_exists(email, name):
    """Ensure the user exists in the database with the Regular User role, excluding predefined users."""
    predefined_users = {
        'nanigock@gmail.com': 'admin',
        'liliana.hotsko@ucu.edu.ua': 'user'
    }
    conn = get_db_connection()
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

authenticator = Authenticate(
    secret_credentials_path='creds.json',
    cookie_name='my_cookie_name',
    cookie_key='this_is_secret',
    redirect_uri='http://localhost:8501',
)

authenticator.check_authentification()

st.title("REVENUE INSIGHTS DASHBOARD")

if st.session_state['connected']:
    st.write('Hello, '+ st.session_state['user_info'].get('name'))
    user_info = st.session_state['user_info']
    email = user_info.get('email')
    name = user_info.get('name')

    ensure_user_exists(email, name)
    role = get_user_role(email)
    if role:
        st.info(f"Your role: {role}")

        if role == "admin":
            st.subheader("Admin Panel: Database Viewer")
            table_options = ["role_dim", "user_dim", "action_dim", "activity_fact"]
            selected_table = st.selectbox("Select a table to view:", table_options)
            if st.button(f"Show contents of {selected_table}"):
                table_data = fetch_table_data(selected_table)
                if not table_data.empty:
                    st.dataframe(table_data)
                else:
                    st.write(f"No data found in `{selected_table}`.")
            
        else:
            st.subheader("User Dashboard")
    
        st.subheader("Visualization from CSV Files")

        tab1, tab2, tab3 = st.tabs(["📈 Temp & Revenue", "📊 Company Revenue Development", "🔍 Countries & Revenues"])


        with tab1:
            st.write("How the temperature influenced revenues of the companies")
            year1 = st.selectbox("Observed Year", options=[i for i in range(2019, 2025)], key="year1")
            dependent_variable1 = st.selectbox("Dependent Variable", options=["revenue", "profit", "sales"], key="dependent_var1")
            predictors1 = st.selectbox("Predictors", options=["tavg"], key="predictors1")
            instruments1 = st.multiselect("Instruments", options=["forbes500", "nasdaq", "s&p500"], key="instruments1")

            if st.button("Generate Chart", key="generate_chart1"):
                payload1 = {
                    "start_year": year1,
                    "end_year": year1,
                    "dependent_variable": dependent_variable1,
                    "predictors": [predictors1],
                    "instruments": instruments1,
                }
                data1 = fetch_data("get-data-q1", payload1)

                if data1:
                    df1 = pd.DataFrame(data1)
                    line_chart1 = alt.Chart(df1).mark_line(point=True).encode(
                        x=alt.X('month', title="Month"),
                        y=alt.Y('sales', title="Sales (USD)", scale=alt.Scale(domain=[0, df1['sales'].max() + 2000])),
                        tooltip=['month', 'sales']
                    ).properties(
                        width=700,
                        height=400,
                        title="Sales Trend Over the Year"
                    )
                    st.altair_chart(line_chart1, use_container_width=True)

                df1 = pd.read_csv("file1.csv")
                line_chart = alt.Chart(df1).mark_line(point=True).encode(
                    x=alt.X('month', title="Month"),
                    y=alt.Y('sales', title="Sales (USD)", scale=alt.Scale(domain=[0, df1['sales'].max() + 2000])),
                    tooltip=['month', 'sales']
                ).properties(
                    width=700,
                    height=400,
                    title="Sales Trend Over the Year"
                ).configure_title(
                    fontSize=20,
                    font="Arial",
                    anchor="middle"
                ).configure_axis(
                    labelFontSize=12,
                    titleFontSize=14
                )
                st.altair_chart(line_chart, use_container_width=True)

        with tab2:
            st.write("How the revenue of companies has been developing over the years")
            start_year2 = st.selectbox("Start Year", options=[i for i in range(2019, 2025)], key="start_year2")
            end_year2 = st.selectbox("End Year", options=[i for i in range(2019, 2025)], key="end_year2")
            dependent_variable2 = st.selectbox("Dependent Variable", options=["revenue"], key="dependent_var2")
            companies2 = st.multiselect("Companies", options=["apple", "google", "microsoft"], key="companies2")


            if st.button("Generate Chart", key="generate_chart2"):
                df2 = pd.read_csv("file2.csv")
                bar_chart = alt.Chart(df2).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10).encode(
                    x=alt.X('product_category', title="Product Category", sort='-y'),
                    y=alt.Y('sales', title="Sales (USD)"),
                    color=alt.Color('product_category', legend=None),
                    tooltip=['product_category', 'sales']
                ).properties(
                    width=700,
                    height=400,
                    title="Product Category Sales"
                ).configure_title(
                    fontSize=20,
                    font="Arial",
                    anchor="middle"
                ).configure_axis(
                    labelFontSize=12,
                    titleFontSize=14
                )
                st.altair_chart(bar_chart, use_container_width=True)

        with tab3:
            st.write("What is the sum of revenues for each country over the year?")
            year3 = st.selectbox("Observed Year", options=[i for i in range(2019, 2025)], key="year3")
            dependent_variable3 = st.selectbox("Dependent Variable", options=["revenue"], key="dependent_var3")
            instruments3 = st.multiselect("Instruments", options=["forbes500", "nasdaq", "s&p500"], key="instruments3")

            if st.button("Generate Chart", key="generate_chart3"):
                df3 = pd.read_csv("file3.csv")
                scatter_chart = px.scatter(
                    df3,
                    x="investment",
                    y="roi",
                    labels={"investment": "Investment (USD)", "roi": "Return on Investment (USD)"},
                    title="Ad Campaign Performance",
                    color="investment",
                    size="roi",
                    hover_data={"investment": True, "roi": True},
                    template="plotly_dark",
                )
                scatter_chart.update_traces(marker=dict(size=12, line=dict(width=1, color="DarkSlateGrey")))
                scatter_chart.update_layout(
                    title_font_size=20,
                    font=dict(size=14),
                    height=500,
                    width=800,
                )
                st.plotly_chart(scatter_chart, use_container_width=True)

else:
    st.write('You are not connected')
    authorization_url = authenticator.get_authorization_url()
    st.link_button('Login', authorization_url)

if st.session_state.get('connected') and st.button('Log out'):
    authenticator.logout()
