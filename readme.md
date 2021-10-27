# Holidays API
Using an azure function a basic API is created for returning holidays on a given date or in a date range.

## Input
The required input to the Azure function is a country, and a date or daterange in ISO 8601 format.

### Parameters
Parameter       | Required | Type           | Examples
---             | ---      | ---            | ---
country         | *        | string         | NO, NOR, Norway, UK
date            | *        | date/daterange | 2021-01-01, 2021-01-01-2022-01-01
inlcudeWeekends |          | boolean        | true, false 

### Headers
Header          | Required | Type           | Examples
---             | ---      | ---            | ---
Content-Type    |          | string         | application/json, text/csv

## Example output
### csv
`functionURL/api/getHolidays?date=2021-01-01-2021-04-01&country=UK` with header `Content-Type: text/csv`
```CSV
Date;Holiday;Name
2021-01-01;True;New Year's Day
2021-01-02;True;New Year Holiday [Scotland]
2021-01-04;True;New Year Holiday [Scotland] (Observed)
2021-03-17;True;St. Patrick's Day [Northern Ireland]
```
### json
`functionURL/api/getHolidays?date=2021-01-01-2021-04-01&country=UK` with header `Content-Type: application/json`
```JSON
[
    {
        "Date": "2021-01-01",
        "Holiday": true,
        "Name": "New Year's Day"
    },
    {
        "Date": "2021-01-02",
        "Holiday": true,
        "Name": "New Year Holiday [Scotland]"
    },
    {
        "Date": "2021-01-04",
        "Holiday": true,
        "Name": "New Year Holiday [Scotland] (Observed)"
    },
    {
        "Date": "2021-03-17",
        "Holiday": true,
        "Name": "St. Patrick's Day [Northern Ireland]"
    }
]
```
#### Credits
Uses the python-holidays library: https://github.com/dr-prodigy/python-holidays 