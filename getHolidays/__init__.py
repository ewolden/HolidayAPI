import logging

import azure.functions as func
import holidays
from datetime import date
from datetime import datetime
import json
import io
import csv


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    country = req.params.get('country')
    query_date = req.params.get('date')
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
    except ImportError:
        logging.error('Invalid country specified.')
        return func.HttpResponse(
             'Invalid country specified.',
             status_code=400
        )
    else:
        pass

    if not response_type:
        response_type = 'application/json'
    else:
        if response_type not in ['application/json', 'application/csv']:
            logging.error('Unknown content type, choose json or csv.')
            return func.HttpResponse(
                'Unknown content type, choose json or csv.',
                status_code=400
            )
    
    if len(query_date) > 10: #Dealing with a date range
        list_of_holidays = country_holidays[query_date[:10]: query_date[10:]]
    else:
        if query_date in country_holidays:
            list_of_holidays = date(datetime.strptime(query_date, '%Y-%m-%d'))
    dict_holidays = []
    if list_of_holidays:
        for day in list_of_holidays:
            dict_holidays.append(
                {
                    'Date': day.isoformat(),
                    'Holiday': True
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
        headernames = ['Date', 'Holiday']
        csv_writer = csv.DictWriter(output_csv, fieldnames=headernames, delimiter=';')
        csv_writer.writeheader()
        csv_writer.writerows(dict_holidays)
        return func.HttpResponse(
            output_csv.getvalue(),
            headers={'Content-Type': 'application/csv'},
            status_code=200
        )
    