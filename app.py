import streamlit as st
from streamlit_google_auth import Authenticate
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "lilianahotsko",      
    "password": "passpost", 
    "database": "postgres" 
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
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT r.role_name FROM user_dim u JOIN role_dim r ON u.role_id = r.role_id WHERE u.email = %s", (email,))
        result = cursor.fetchone()
        return result['role_name'] if result else None
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

def ensure_user_exists(email, name):
    """Ensure the user exists in the database with the Regular User role."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_id FROM user_dim WHERE email = %s", (email,))
        result = cursor.fetchone()

        if not result:
            cursor.execute(
                """
                INSERT INTO user_dim (email, name, role_id)
                VALUES (%s, %s, (SELECT role_id FROM role_dim WHERE role_name = 'user'))
                """,
                (email, name)
            )
            conn.commit()
            print(f"New user {email} added to Regular User role.")
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

st.title("Streamlit Google Auth Example with Database Viewer")

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
        tab1, tab2, tab3 = st.tabs(["📈 Sales Trend", "📊 Product Sales", "🔍 Ad Campaign ROI"])

        with tab1:
            st.write("Monthly Sales Trends")
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
            st.write("Sales by Product Category")
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
            st.write("Advertising Investment vs. ROI")
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
        st.warning("Your role is undefined. Contact an admin.")

else:
    st.write('You are not connected')
    authorization_url = authenticator.get_authorization_url()
    st.link_button('Login', authorization_url)

if st.session_state.get('connected') and st.button('Log out'):
    authenticator.logout()
