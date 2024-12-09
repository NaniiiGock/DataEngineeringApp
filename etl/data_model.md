```mermaid
erDiagram
    BusinessFACT }|--|| BusinessDIM : ranks
    BusinessFACT {
        int id PK
        int business_id FK
        int rank
        int employees
        int revenues
        int profit
    }
    CountyDIM ||--|{ BusinessDIM : contains
    CountyDIM {
        int county_fips PK
        string state
    }
    BusinessDIM{
        int id PK
        string name
        int county_fips FK
    }
    WeatherFACT }|--|| CountyDIM : occurs_in
    WeatherFACT {
        int id PK
        int county_fips FK
        date date
        int tmin
        int tmax
        int tavg
        int prcp
    }
```