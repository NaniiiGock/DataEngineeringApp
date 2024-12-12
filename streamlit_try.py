
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
        
api_connector = APIConnector(api_url)


json_of_companies = requests.get(f"{api_url}/api/get/companies").json()
list_of_companies = [company["NAME"] for company in json_of_companies]
        
st.title("REVENUE INSIGHTS DASHBOARD")

st.subheader("User Dashboard")
    
st.subheader("Explore the data")

tab1, tab2, tab3 = st.tabs(["📈 Temp & Revenue", "📊 Company Revenue Development", "🔍 Countries & Revenues"])

with tab1:
    st.write("How the temperature influenced revenues of the companies")

    start_year1 = st.selectbox("Observed Year", options=[i for i in range(2015, 2020)], key="year1")
    end_year1 = st.selectbox("End Year", options=[i for i in range(2015, 2020)], key="end_year1")
    dependent_variable1 = st.selectbox("Dependent Variable", options=["REVENUES", "profit", "sales"], key="dependent_var1")
    predictors1 = st.selectbox("Predictors", options=["TAVG"], key="predictors1")
    instruments1 = st.multiselect("Instruments", options=list_of_companies, key="instruments1")
    
    select_all = st.button("Select All Instruments")
    if select_all:
        instruments = st.multiselect("Instruments", options=list_of_companies, default=list_of_companies)
    else:
        instruments = st.multiselect("Instruments", options=list_of_companies)

    if st.button("Generate Chart", key="generate_chart1"):

        payload = {
            "start_year": start_year1,
            "end_year": end_year1,
            "dependent_variable": dependent_variable1,
            "predictors": predictors1,
            "instruments": instruments1
        }
        data_json = api_connector.fetch_data("1", payload)

        st.write("### Data Overview")
        st.dataframe(data_json)
        # min_revenue = int(q1_data["REVENUES"].min())
        # max_revenue = int(q1_data["REVENUES"].max())
        # revenue_range = st.slider(
        #     "Filter by Revenue Range", min_value=min_revenue, max_value=max_revenue, value=(min_revenue, max_revenue)
        # )

        # filtered_q1 = q1_data[(q1_data["REVENUES"] >= revenue_range[0]) & (q1_data["REVENUES"] <= revenue_range[1])]
        # sort_option = st.radio("Sort by", ["Ascending", "Descending"], key="q1_sort")
        # ascending = sort_option == "Ascending"
        # filtered_q1 = filtered_q1.sort_values(by="REVENUES", ascending=ascending)
        # st.write("### Filtered and Sorted Data")
        # st.dataframe(filtered_q1)

        # st.write("### Revenue by State (Filtered)")
        # q1_chart = alt.Chart(filtered_q1).mark_bar().encode(
        #     x=alt.X("STATE", sort="-y", title="State"),
        #     y=alt.Y("REVENUES", title="Revenues"),
        #     color=alt.Color("REVENUES", scale=alt.Scale(scheme="blues"), title="Revenues"),
        #     tooltip=["STATE", "REVENUES"]
        # ).properties(
        #     width=800,
        #     height=400,
        #     title="Filtered and Sorted Revenues by State (2017)"
        # )
        # st.altair_chart(q1_chart, use_container_width=True)

with tab2:

    st.write("How the revenue of companies has been developing over the years")
    start_year2 = st.selectbox("Start Year", options=[i for i in range(2019, 2025)], key="start_year2")
    end_year2 = st.selectbox("End Year", options=[i for i in range(2019, 2025)], key="end_year2")
    dependent_variable2 = st.selectbox("Dependent Variable", options=["revenue"], key="dependent_var2")
    companies2 = st.multiselect("Companies", options=["apple", "google", "microsoft"], key="companies2")

    if st.button("Generate Chart", key="generate_chart2"):
        payload = {
            "start_year": start_year2,
            "end_year": end_year2,
            "dependent_variable": dependent_variable2,
            "companies": companies2
        }
        data = api_connector.fetch_data("chart2", payload)

        if data:
            q2_data = pd.DataFrame(data)
        else:
            q2_data = pd.read_csv("data/q2.csv")

        st.dataframe(q2_data)

        min_revenue = int(q2_data["REVENUES"].min())
        max_revenue = int(q2_data["REVENUES"].max())
        revenue_range = st.slider(
            "Filter by Revenue Range", min_value=min_revenue, max_value=max_revenue, value=(min_revenue, max_revenue),
            key="q2_slider"
        )
        filtered_q2 = q2_data[(q2_data["REVENUES"] >= revenue_range[0]) & (q2_data["REVENUES"] <= revenue_range[1])]
        sort_option = st.radio("Sort by", ["Ascending", "Descending"], key="q2_sort")
        ascending = sort_option == "Ascending"
        filtered_q2 = filtered_q2.sort_values(by="REVENUES", ascending=ascending)

        st.write("### Filtered and Sorted Data")
        st.dataframe(filtered_q2)

        st.write("### Top Companies by Revenue (Filtered)")
        q2_bar = alt.Chart(filtered_q2).mark_bar().encode(
            x=alt.X("NAME", sort="-y", title="Company"),
            y=alt.Y("REVENUES", title="Revenues"),
            color=alt.Color("REVENUES", scale=alt.Scale(scheme="greens"), title="Revenues"),
            tooltip=["NAME", "REVENUES"]
        ).properties(
            width=800,
            height=400,
            title="Filtered and Sorted Top Companies by Revenue (2017)"
        )
        st.altair_chart(q2_bar, use_container_width=True)

with tab3:
    st.write("What is the sum of revenues for each country over the year?")
    year3 = st.selectbox("Observed Year", options=[i for i in range(2019, 2025)], key="year3")
    dependent_variable3 = st.selectbox("Dependent Variable", options=["revenue"], key="dependent_var3")
    instruments3 = st.multiselect("Instruments", options=["forbes500", "nasdaq", "s&p500"], key="instruments3")

    if st.button("Generate Chart", key="generate_chart3"):
        payload = {
            "year": year3,
            "dependent_variable": dependent_variable3,
            "instruments": instruments3
        }
        data = api_connector.fetch_data("data/chart3", payload)

        if data:
            q3_data = pd.DataFrame(data)
        else:
            q3_data = pd.read_csv("q3.csv")

        st.write("### Data Overview")
        st.dataframe(q3_data)
        min_revenue = int(q3_data["REVENUES"].min())
        max_revenue = int(q3_data["REVENUES"].max())
        revenue_range = st.slider(
            "Filter by Revenue Range", min_value=min_revenue, max_value=max_revenue, value=(min_revenue, max_revenue),
            key="q3_slider"
        )

        filtered_q3 = q3_data[(q3_data["REVENUES"] >= revenue_range[0]) & (q3_data["REVENUES"] <= revenue_range[1])]
        sort_option = st.radio("Sort by", ["Ascending", "Descending"], key="q3_sort")
        ascending = sort_option == "Ascending"
        filtered_q3 = filtered_q3.sort_values(by="REVENUES", ascending=ascending)

        st.write("### Filtered and Sorted Data")
        st.dataframe(filtered_q3)

        st.write("### Revenue Distribution by Name (Filtered)")
        q3_chart = alt.Chart(filtered_q3).mark_bar().encode(
            x=alt.X("NAME", sort=None, title="Name"),
            y=alt.Y("REVENUES", title="Revenues"),
            color=alt.Color("REVENUES", scale=alt.Scale(scheme="purples"), title="Revenues"),
            tooltip=["NAME", "REVENUES"]
        ).properties(
            width=800,
            height=400,
            title="Filtered and Sorted Revenues by Name (2017)"
        )
        st.altair_chart(q3_chart, use_container_width=True)
