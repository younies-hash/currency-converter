import requests, json

def fetch_data():
    url = 'https://api.frankfurter.dev/v2/rates'
    response = requests.get(url)
    data = response.json()
    with open('rates.json', 'w') as FILE:
        json.dump(data, FILE, indent=4)
        FILE.close()
    return data

def get_rate(rates, from_currency, to_currency):
    try:
        for rate in rates:
            print (rate['base'], rate['quote'])
            if rate['base'] == from_currency and rate['quote'] == to_currency:
                return float(rate['rate'])
        print('Currency not found')
        return None
    except ValueError:
        print('Invalid currency')
        return None
    