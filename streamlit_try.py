
import pandas as pd
import streamlit as st
import altair as alt
import requests

api_url = "http://127.0.0.1:5001"

class APIConnector:

    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, q_number, payload):
        response = requests.post(f"{self.api_url}/api/get-data-q{q_number}", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def fetch_data_get_request(self, q_number):
        response = requests.get(f"{self.api_url}/api/get-data-q{q_number}")
        if response.status_code == 200:
            return response.json()
        else:
            return None

        
api_connector = APIConnector(api_url)


json_of_companies = requests.get(f"{api_url}/api/get/companies").json()
list_of_companies = [company["NAME"] for company in json_of_companies]
        
st.title("DELTA/TERMINAL")

st.subheader("User Dashboard")
    
st.subheader("Explore the data")

tab1, tab2, tab3 = st.tabs(["📈 Temp & Revenue", "📊 Company Revenue Development", "🔍 Countries & Revenues"])


if "df1" not in st.session_state:
    st.session_state["df1"] = None
if "df2" not in st.session_state:
    st.session_state["df2"] = None
if "df3" not in st.session_state:
    st.session_state["df3"] = None

import pandas as pd
import altair as alt
import streamlit as st

# Initialize session state for df1
if "df1" not in st.session_state:
    st.session_state["df1"] = None

with tab1:
    st.write("How temperature influence revenues of companies ?")

    # start_year1 = st.selectbox("Observed Year", options=[i for i in range(2015, 2020)], key="year1")
    start_year1 = st.text_input("Start year", value='2016-01-01', key="year1")
    # end_year1 = st.selectbox("End Year", options=[i for i in range(2015, 2020)], key="end_year1")
    end_year1 = st.text_input("End year", value='2016-12-31', key="end_year1")
    dependent_variable1 = st.selectbox("Dependent Variable", options=["REVENUES", "profit", "sales"], key="dependent_var1")
    predictors1 = st.selectbox("Predictors", options=["TAVG"], key="predictors1")
    instruments1 = st.multiselect("Instruments", options=list_of_companies, key="instruments1")

    if st.button("Generate Chart", key="generate_chart1"):
        # Fetch data from API
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

            # Save DataFrame to session state
            st.session_state["df1"] = df

            st.write("### Data Overview")
            st.dataframe(df)

    # Access df1 from session state
    if st.session_state["df1"] is not None:
        df = st.session_state["df1"]

        # User-defined sorting
        sort_column = st.selectbox("Sort by column:", options=["NAME", "REVENUES", "TAVG"])
        ascending = st.radio("Sort order:", options=["Ascending", "Descending"]) == "Ascending"

        # Sort DataFrame
        df = df.sort_values(by=sort_column, ascending=ascending)

        # Visualization with Altair
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

    st.write("How the revenue of companies develops over time?")
    # start_year2 = st.selectbox("Start Year", options=[i for i in range(2019, 2025)], key="start_year2")
    start_year2 = st.text_input("Start year", value='2016-01-01', key="start_year2")
    # end_year2 = st.selectbox("End Year", options=[i for i in range(2019, 2025)], key="end_year2")
    end_year2 = st.text_input("End year", value='2016-12-31', key="end_year2")
    dependent_variable2 = st.selectbox("Dependent Variable", options=["REVENUES"], key="dependent_var2", disabled=True)
    # companies2 = st.multiselect("Companies", options=["apple", "google", "microsoft"], key="companies2")
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

            # Save DataFrame to session state
            st.session_state["df2"] = df

            st.write("### Data Overview")
            st.dataframe(df)
        else:
            st.write(f'No data returned from API: {data}')

    # Access df2 from session state
    if st.session_state["df2"] is not None:
        df = st.session_state["df2"]

        # Visualization with Altair
        st.write("### Interactive Visualization with Date")
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("NAME:N", title="Company"),
            y=alt.Y("REVENUES:Q", title="Revenues"),
            color=alt.Color("NAME:N", scale=alt.Scale(scheme="category10"), title="Company"),
            tooltip=["NAME", "REVENUES"],
        ).properties(
            width=800,
            height=400,
            title="Revenues by Company Over Time",
        )

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

    st.write("What is the sum of revenues for each country over the year?")

    if st.button("Generate Chart", key="generate_chart3"):
        data = api_connector.fetch_data_get_request("3")

        if data:
            df = pd.DataFrame(data)
            df.dropna(inplace=True)
            df['COUNTYFIPS'] = df['COUNTYFIPS'].astype(str).apply(format_fips)

            # Save DataFrame to session state
            st.session_state["df3"] = df

            st.write("### Data Overview")
            st.dataframe(df)
        else:
            st.write(f'No data returned from API: {data}')


