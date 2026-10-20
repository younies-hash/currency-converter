from flask import Flask, render_template, request
from converter import *

app = Flask(__name__)

@app.route('/convert', methods=['GET', 'POST'])
def index():
    data = request.form
    rates = fetch_data()
    try:
        if request.method == 'POST':
            amount = float(data.get('amount'))
            from_currency = data.get('from_currency')
            to_currency = data.get('to_currency')
            rate = get_rate(rates, from_currency, to_currency)
            result = convert(amount, rate)
            return render_template('index.html', result=result)
    except ValueError:
        return render_template('index.html', error='ERROR: invalid currency or amount')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)