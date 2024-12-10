# Tables and fields

The tables are described: what does the data mean, how did the data come to be, how to read and interpret it.

The field descriptions include datatype and meaning and primary/foreign key mention if applies.

## WeatherFACT Table
Contains weather observations. Each row is a single day in a single county. The measurements are averaged for that day accross different weather stations in the county.
This table records the daily average, minimum and maximum temperatures, and the amount of precipitation.
There are missing values - in some counties, only the precipitations are measured, while in others, only the minimum and maximum temperature are stored.
<br>All temperatures are in **Celsius**, and
<br>all precipitations are in **Millimeters**.

### Field descriptions

**ID**
* INTEGER
* PRIMARY KEY

**COUNTYFIPS**
* INTEGER
* FOREIGN KEY
* Unique identifier for the county in which the measurements were made. It is a standard US county identifier.


**DATE**
* DATETIME
* Format: YYYY-MM-DDTHH:MM:SS
* The date when the measurements were made

**TMIN**
* INTEGER
* Minimum recorded temperature

**TAVG**
* INTEGER
* Average recorded temperature

**TMAX**
* Maximum recorded temperature

**PRCP**
* INTEGER
* Amount of precipitations for whole day

## BusinessFACT Table
Contains, in essence, the measurables for the Forbes 500 businesses. The table does not contain data about the locations of the corporations, nor does it include the name of any other identifier except for the business id.
<br>The business id can be in turn used, to get more data about the business from the BusinessDIM table which also includes the county identifier COUNTYFIPS.
<br>Monetary values like REVENUES and PROFIT are in **millions of dollars**.

### Field descriptions

**ID**
* INTEGER 
* PRIMARY KEY

**BUSINESSID**
* INTEGER
* FOREIGN KEY
* Maps the business fact to the dimensions of BusinessDIM

**RANK**
* INTEGER
* The ranking of the business on the 2017 Fortune 500

**EMPLOYEES**
* INTEGER
* Number of employees in the company.

**REVENUES**
* INTEGER
* Business revenues (income before costs) in the year 2016
* In millions of dollars

**PROFIT**
* INTEGER
* Business profits (income after costs) in the year 2016
* In millions of dollars

## BusinessDIM Table

This table complements the BusinessFACT table with the name of the business and the business's home county identifier (COUNTYFIPS).

### Field descriptions

**ID**
* INTEGER
* PRIMARY KEY

**NAME**
* STRING
* Name of the company

**COUNTYFIPS**
* INTEGER
* FOREIGN KEY
* Unique identifier across all counties in the US. Maps the BusinessDIM table to CountyDIM table.

## CountyDIM Table

This table contains the name of each county in which a Fortune 500 company's headquarter resideds, along with that county's parent state.

Some distinct counties share a name but reside in different states - they are identified by the Countyfips

### Field descriptions

**COUNTYFIPS**
* INTEGER
* PRIMARY KEY
* Unique identifier across all US counties, US standard identifier.

**COUNTY**
* STRING
* Name of the county.

**STATE**
* STRING
* Name of the state in which the county is situated.