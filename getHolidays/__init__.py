import logging

import azure.functions as func
import holidays
from datetime import datetime, timedelta
import json
import io
import csv

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    country = req.params.get('country')
    query_date = req.params.get('date')
    include_weekends = req.params.get('includeWeekends')
    response_type = req.headers.get('Content-Type')

    if not query_date:
        logging.error('No dates specified, use a single date or a date range. In ISO 8601 format.')
        return func.HttpResponse(
             'No dates specified, use a single date or a date range. In ISO 8601 format.',
             status_code=400
        )
    if not country:
        logging.error('No country specified.')
        return func.HttpResponse(
             'No country specified.',
             status_code=400
        )
    try:
        country_holidays = holidays.CountryHoliday(country)
        country_holidays.include_sundays = False
    except KeyError:
        logging.error('Invalid country "{}" specified.'.format(country))
        return func.HttpResponse(
             'Invalid country "{}" specified.'.format(country),
             status_code=400
        )
    else:
        pass

    if not response_type:
        response_type = 'application/json'
    else:
        if response_type not in ['application/json', 'text/csv']:
            logging.error('Unknown content type "{}", choose json or csv.'.format(response_type))
            return func.HttpResponse(
                'Unknown content type "{}", choose json or csv.'.format(response_type),
                status_code=400
            )

    if not include_weekends:
        include_weekends = False
    dict_holidays = []
    if len(query_date) > 10: #Dealing with a date range
        for day in daterange(datetime.strptime(query_date[:10], '%Y-%m-%d').date(), datetime.strptime(query_date[11:], '%Y-%m-%d').date()):
            if day in country_holidays:
                dict_holidays.append(
                    {
                        'Date': day.isoformat(),
                        'Holiday': True,
                        'Name': country_holidays.get(day)
                    }
                )
            elif include_weekends and day.weekday() > 5:
                dict_holidays.append(
                    {
                        'Date': day.isoformat(),
                        'Holiday': True,
                        'Name': 'Weekend'
                    }
                )
    else:
        if query_date in country_holidays:
            dict_holidays.append(
                {
                    'Date': query_date,
                    'Holiday': True,
                    'Name': country_holidays.get(query_date)
                }
            )
        elif include_weekends and query_date.weekday() > 5:
            dict_holidays.append(
                {
                    'Date': query_date,
                    'Holiday': True,
                    'Name': 'Weekend'
                }
            )
    
    if response_type == 'application/json':
        logging.info('Finished processing output succesfully, responding with JSON')
        return func.HttpResponse(
            json.dumps(dict_holidays),
            headers={'Content-Type': 'application/json'},
            status_code=200
        )
    else:
        logging.info('Finished processing output succesfully, responding with CSV')
        output_csv = io.StringIO()
        headernames = ['Date', 'Holiday', 'Name']
        csv_writer = csv.DictWriter(output_csv, fieldnames=headernames, delimiter=';')
        csv_writer.writeheader()
        csv_writer.writerows(dict_holidays)
        return func.HttpResponse(
            output_csv.getvalue(),
            headers={'Content-Type': 'text/csv'},
            status_code=200
        )
    