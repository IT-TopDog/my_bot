import requests
import json


API_ID = '801fc23bf8ea459bb6310b9ade965065'


def exchanger_currency():
    response = requests.get(f'https://openexchangerates.org/api/latest.json?app_id={API_ID}')

    data = json.loads(response.text)
    rates = data['rates']
    filter_rates = {
        'RUB': rates['RUB'],
        'KGS': rates['KGS'],
        'EUR': rates['EUR'],
        'KZT': rates['KZT'],
        'TRY': rates['TRY'],
        'CNY': rates['CNY'],
        'AED': rates['AED']
    }


    return filter_rates

# exchanger_currency()