from flask import Flask, render_template, request
from converter import *

app = Flask(__name__)

rates = fetch_data()
currencies = ['EUR']

@app.route('/')
def index():
    for rate in rates:
        currencies.append(rate['quote'])
    return render_template('index.html', currencies=currencies)

@app.route('/select-currency')
def select():
    pass

@app.route('/convert', methods=['GET', 'POST'])
def convert_currency():
    data = request.form
    try:
        if request.method == 'POST':
            amount = float(data.get('amount'))
            from_currency = data.get('from_currency')
            to_currency = data.get('to_currency')
            result = convert(amount, from_currency, to_currency, rates)
            return render_template('partials/conversion_result.html', result=result)
    except ValueError:
        return render_template('index.html', error='ERROR: invalid currency or amount')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)