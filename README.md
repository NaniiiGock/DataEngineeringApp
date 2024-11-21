# DataEngineeringApp


# Plan:


**Q1: How the weather affects employees' productivity?**

Filters: start_date, end_date, location (country, city)

Charts:

-> heatmap which compares correlation between temperature and 
productivity over the time

-> list of countries + correlation (map where each country is colored 
into different colors based on the correlation)

-> temperature and productivity over the time in the country -> for each country NUMBER
-> estonia: 6.5, france 4.5


**Q2: How the weather affects the rank?**
Filters: start_date, end_date, companies list
Chart:
correlation separatly for each company over the same time period
-> list of companies + correlation 
Google - 0.5, Apple - 0.3, Microsoft - 0.7


**Q3: yearly average temperature correlation with revenue?**
Filters: start_date, end_date, companies list
Chart:
correlation separatly for each company over the same time period
-> list of companies + correlation
Google 1, Apple 0.5, Microsoft 0.7



## Tasks:

### Gustav:
1) scrapping the data from APIS/DataBases
2) pushing needed data into the database
*) Apache Airflow, dbt, data governance, duck db, iceberg 

### Simon:
3) Write templates for queries for 3 questions
4) for each question do correlation calculations
5) form dataframes for UI for each question
6) implement service with endpoints to get filters and return results
*) Flask, Swagger - API documentation

### Liliana:
7) Users managements(roles, login, security of the app, UI, filters, plotting, manage sessions)
8) get filters from the user
9) implement service with requests to the data analysis service
10) plot on UI
*) Streamlit, Google Auth, flask, postgres, secrets manager


### General:
*) Docker compose - mesh of services: 
1) datascrapping(everyone is waiting for it)
2) data analysis service
3) db for users
4) ui service
'''



