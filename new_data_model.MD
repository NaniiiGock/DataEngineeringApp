```mermaid
erDiagram
    BusinessFACT }|--|| BusinessDIM : ranks
    BusinessFACT {
        int ID PK
        int BUSINESSID FK
        int RANK
        int EMPLOYEES
        int REVENUES
        int PROFIT
    }
    CountyDIM ||--|{ BusinessDIM : contains
    CountyDIM {
        int COUNTYFIPS PK
        string COUNTY
        string STATE
    }
    BusinessDIM{
        int ID PK
        string NAME
        int COUNTYFIPS FK
    }
    WeatherFACT }|--|| CountyDIM : occurs_in
    WeatherFACT {
        int ID PK
        int COUNTYFIPS FK
        date DATE
        int TMIN
        int TMAX
        int TAV
        int PRCP
    }
```