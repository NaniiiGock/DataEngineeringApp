import streamlit as st
import pandas as pd
import altair as alt


q1_data = pd.read_csv("q1.csv")
q2_data = pd.read_csv("q2.csv")
q3_data = pd.read_csv("q3.csv")


st.title("Interactive Data Visualization for q1, q2, and q3 Datasets")


tab1, tab2, tab3 = st.tabs(["State Revenues (q1)", "Company Data (q2)", "Revenues by Name (q3)"])


with tab1:
    st.header("State Revenues (q1.csv)")
    st.write("### Data Overview")
    st.dataframe(q1_data)

    min_revenue = int(q1_data["REVENUES"].min())
    max_revenue = int(q1_data["REVENUES"].max())
    revenue_range = st.slider(
        "Filter by Revenue Range", min_value=min_revenue, max_value=max_revenue, value=(min_revenue, max_revenue)
    )

    filtered_q1 = q1_data[(q1_data["REVENUES"] >= revenue_range[0]) & (q1_data["REVENUES"] <= revenue_range[1])]
    sort_option = st.radio("Sort by", ["Ascending", "Descending"], key="q1_sort")
    ascending = sort_option == "Ascending"
    filtered_q1 = filtered_q1.sort_values(by="REVENUES", ascending=ascending)
    st.write("### Filtered and Sorted Data")
    st.dataframe(filtered_q1)

    st.write("### Revenue by State (Filtered)")
    q1_chart = alt.Chart(filtered_q1).mark_bar().encode(
        x=alt.X("STATE", sort="-y", title="State"),
        y=alt.Y("REVENUES", title="Revenues"),
        color=alt.Color("REVENUES", scale=alt.Scale(scheme="blues"), title="Revenues"),
        tooltip=["STATE", "REVENUES"]
    ).properties(
        width=800,
        height=400,
        title="Filtered and Sorted Revenues by State (2017)"
    )
    st.altair_chart(q1_chart, use_container_width=True)

# Tab 2: Company Data (q2)
with tab2:
    st.header("Company Data (q2.csv)")
    st.write("### Data Overview")
    st.dataframe(q2_data)

    min_revenue = int(q2_data["REVENUES"].min())
    max_revenue = int(q2_data["REVENUES"].max())
    revenue_range = st.slider(
        "Filter by Revenue Range", min_value=min_revenue, max_value=max_revenue, value=(min_revenue, max_revenue),
        key="q2_slider"
    )

    filtered_q2 = q2_data[(q2_data["REVENUES"] >= revenue_range[0]) & (q2_data["REVENUES"] <= revenue_range[1])]

    # Sort the filtered data
    sort_option = st.radio("Sort by", ["Ascending", "Descending"], key="q2_sort")
    ascending = sort_option == "Ascending"
    filtered_q2 = filtered_q2.sort_values(by="REVENUES", ascending=ascending)

    st.write("### Filtered and Sorted Data")
    st.dataframe(filtered_q2)

    # Create a bar chart for the filtered data
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

# Tab 3: Revenues by Name (q3)
with tab3:
    st.header("Revenues by Name (q3.csv)")
    st.write("### Data Overview")
    st.dataframe(q3_data)

    # Add a slider to filter by revenue range
    min_revenue = int(q3_data["REVENUES"].min())
    max_revenue = int(q3_data["REVENUES"].max())
    revenue_range = st.slider(
        "Filter by Revenue Range", min_value=min_revenue, max_value=max_revenue, value=(min_revenue, max_revenue),
        key="q3_slider"
    )

    # Filter data based on slider input
    filtered_q3 = q3_data[(q3_data["REVENUES"] >= revenue_range[0]) & (q3_data["REVENUES"] <= revenue_range[1])]

    # Sort the filtered data
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
