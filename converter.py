from api import *

def convert(amount, from_currency, to_currency, rates):
    #rate from from_currency to EUR
    rate1 = get_rate(rates, from_currency)
    #rate from to_currency to EUR
    rate2 = get_rate(rates, to_currency)
    amount_in_eur = amount / rate1
    result = amount_in_eur * rate2
    return result

def get_rate(rates, from_currency):
    to_currency = 'EUR'
    if from_currency == to_currency:
        print(f"exchange rate for {from_currency} and {to_currency} = 1")
        return 1.0
    try:
        for rate in rates:
            if rate['quote'] == from_currency and rate['base'] == to_currency:
                print(f"exchange rate for {from_currency} and {to_currency} = {rate['rate']}")
                return float(rate['rate'])
        print(f"can't find exchange rate for {from_currency} and {to_currency}")
        return None
    except ValueError:
        print('Invalid currency')
        return None