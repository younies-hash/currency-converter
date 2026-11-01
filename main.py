from flask import Flask, render_template, request
from converter import convert
from api import fetch_data
from db import DataBase, Conversion
from datetime import datetime

app = Flask(__name__)

db = DataBase()
rates = fetch_data()
db.update_rates(rates)
currencies = []

@app.route('/')
def index():
    currencies = ['EUR']
    for rate in rates:
        currencies.append(rate['quote'])
    return render_template('index.html', currencies=currencies)

@app.route('/convert', methods=['GET', 'POST'])
def convert_currency():
    data = request.form
    try:
        if request.method == 'POST':
            
            amount = float(data.get('amount'))
            base_currency = data.get('base_currency')
            target_currency = data.get('target_currency')
            
            rate, result = convert(amount, base_currency, target_currency, rates)
            
    except ValueError:
        return render_template('index.html', error='ERROR: invalid currency or amount')

    cnvrsn = Conversion(
        datetime.now().isoformat(timespec='seconds'),
        amount,
        base_currency,
        target_currency,
        rate,
        result
    )
    db.add_conversion(cnvrsn)
    return render_template('partials/conversion_result.html', result=result)

@app.route('/history', methods=['GET'])
def show_history():
    return
        

if __name__ == '__main__':
    app.run(debug=True)