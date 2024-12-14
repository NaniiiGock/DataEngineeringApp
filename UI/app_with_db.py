import pandas as pd
import streamlit as st
import altair as alt
import logging
from logging.handlers import RotatingFileHandler
from utils.db_connector import DBConnector
from utils.db_api_requests import APIConnector
from streamlit_google_auth import Authenticate

LOG_FILE = "streamlit_app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=10**6, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

db_connector = DBConnector()
api_connector = APIConnector()

authenticator = Authenticate(
    secret_credentials_path='creds.json',
    cookie_name='my_cookie_name',
    cookie_key='this_is_secret',
    redirect_uri='http://localhost:8501',
)
authenticator.check_authentification()

json_of_companies = api_connector.fetch_companies()
list_of_companies = [company["NAME"] for company in json_of_companies]


st.title("DELTA/TERMINAL")


if st.session_state['connected']:
    user_info = st.session_state['user_info']
    email = user_info.get('email')
    name = user_info.get('name')

    user_id = db_connector.ensure_user_exists(email, name)

    login_action_id = db_connector.get_action_id("login")
    db_connector.log_activity(user_id, login_action_id, f"User {email} logged in.")

    role = db_connector.get_user_role(email)
    st.info(f"Your role: {role}")

    if role == "admin":
        st.subheader("Admin Panel: Database Viewer")
        table_options = ["role_dim", "user_dim", "action_dim", "activity_fact"]
        selected_table = st.selectbox("Select a table to view:", table_options)
        if st.button(f"Show contents of {selected_table}"):
            admin_action_id = db_connector.get_action_id("view_dashboard")
            db_connector.log_activity(user_id, admin_action_id, f"Viewed table {selected_table}.")
            table_data = db_connector.fetch_table_data(selected_table)
            if not table_data.empty:
                st.dataframe(table_data)
            else:
                st.write(f"No data found in `{selected_table}`.")
    else:
        st.subheader("User Dashboard")

    st.subheader("Explore the Data")
    tab1, tab2, tab3 = st.tabs(["📈 Temp & Revenue", "📊 Revenue Development", "🔍 Country Revenues"])

    for tab_key in ["df1", "df2", "df3"]:
        if tab_key not in st.session_state:
            st.session_state[tab_key] = None

    with tab1:
        st.write("How temperature influence revenues of companies ?")

        start_year1 = st.text_input("Start year", value='2016-01-01', key="year1")
        end_year1 = st.text_input("End year", value='2016-12-31', key="end_year1")
        dependent_variable1 = st.selectbox("Dependent Variable", options=["REVENUES", "profit", "sales"], key="dependent_var1")
        predictors1 = st.selectbox("Predictors", options=["TAVG"], key="predictors1")
        instruments1 = st.multiselect("Instruments", options=list_of_companies, key="instruments1")

        if st.button("Generate Chart", key="generate_chart1"):
            payload = {
                "start_year": str(start_year1),
                "end_year": str(end_year1),
                "dependent_variable": dependent_variable1,
                "predictors": predictors1,
                "instruments": instruments1,
            }
            data_json = api_connector.fetch_data("1", payload)
            if data_json:
                df = pd.DataFrame(data_json)
                df.dropna(inplace=True)
                st.session_state["df1"] = df

                st.write("### Data Overview")
                st.dataframe(df)

                chart_action_id = db_connector.get_action_id("view_dashboard")
                db_connector.log_activity(user_id, chart_action_id, f"Generated chart with payload: {payload}")



        if st.session_state["df1"] is not None:
            df = st.session_state["df1"]
            sort_column = st.selectbox("Sort by column:", options=["NAME", "REVENUES", "TAVG"])
            ascending = st.radio("Sort order:", options=["Ascending", "Descending"]) == "Ascending"

            df = df.sort_values(by=sort_column, ascending=ascending)

            st.write("### Interactive Visualization Without Date")
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X("NAME:N", title="Company"),
                y=alt.Y("REVENUES:Q", title="Revenues"),
                color=alt.Color("TAVG:Q", scale=alt.Scale(scheme="redyellowblue"), title="Avg Temp"),
                tooltip=["NAME", "REVENUES", "TAVG"],
            ).properties(
                width=800,
                height=400,
                title="Revenues by Company (Color-Coded by Temperature)",
            )

            st.altair_chart(chart, use_container_width=True)


    with tab2:
        st.write("How does company revenue develop over time?")
        start_year2 = st.text_input("Start Year", value='2016-01-01', key="start_year2")
        end_year2 = st.text_input("End Year", value='2016-12-31', key="end_year2")
        dependent_variable2 = st.selectbox("Dependent Variable", options=["REVENUES"], key="dependent_var2", disabled=True)
        companies2 = st.multiselect("Companies", options=list_of_companies, key="companies2")

        if st.button("Generate Chart", key="generate_chart2"):
            payload = {
                "start_year": start_year2,
                "end_year": end_year2,
                "dependent_variable": dependent_variable2,
                "instruments": companies2
            }
            data = api_connector.fetch_data("2", payload)
            if data:
                df = pd.DataFrame(data)
                df.dropna(inplace=True)
                st.session_state["df2"] = df
                st.write("### Data Overview")
                st.dataframe(df)

                chart_action_id = db_connector.get_action_id("view_dashboard")
                db_connector.log_activity(user_id, chart_action_id, f"Generated chart with payload: {payload}")

        if st.session_state["df2"] is not None:
            df = st.session_state["df2"]
            st.write("### Interactive Visualization")
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X("NAME:N", title="Company"),
                y=alt.Y("REVENUES:Q", title="Revenues"),
                color=alt.Color("NAME:N", scale=alt.Scale(scheme="category10"), title="Company"),
                tooltip=["NAME", "REVENUES"],
            ).properties(width=800, height=400, title="Revenues by Company Over Time")
            st.altair_chart(chart, use_container_width=True)

    with tab3:
        def format_fips(fips):
                fips_str = str(fips)
                if len(fips_str) == 4:
                    return f"0{fips_str}"
                elif len(fips_str) == 3:
                    return f"00{fips_str}"
                elif len(fips_str) == 2:
                    return f"000{fips_str}"
                else:
                    return fips_str
                
        st.write("What is the sum of revenues for each country?")
        if st.button("Generate Chart", key="generate_chart3"):
            data = api_connector.fetch_data_get_request("3")
            if data:
                df = pd.DataFrame(data)
                df['COUNTYFIPS'] = df['COUNTYFIPS'].astype(str).apply(format_fips)

                df.dropna(inplace=True)
                st.session_state["df3"] = df
                st.write("### Data Overview")
                st.dataframe(df)

    if st.session_state.get('connected') and st.button('Log out'):
        logout_action_id = db_connector.get_action_id("logout")
        db_connector.log_activity(user_id, logout_action_id, f"User {email} logged out.")
        authenticator.logout()
else:
    st.write('You are not connected')
    authorization_url = authenticator.get_authorization_url()
    st.link_button('Login', authorization_url)
