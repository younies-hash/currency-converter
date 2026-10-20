#conversations
#id, timesatmp, amount, from_currency, to_currency, rate, result

#rates
#id, date, base, quote, rate

import mysql
from api import fetch_data

class DB:
    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database='currency_converter'
        )
        self.curser = self.db.cursor()
        self.curser.execute('CREATE TABLE IF NOT EXISTS conversations (id INT AUTO_INCREMENT, timesatmp TIMESTAMP, amount INT, from_currency VARCHAR(3), to_currency VARCHAR(3), rate FLOAT, result FLOAT, PRIMARY KEY (id))')
        self.curser.execute('CREATE TABLE IF NOT EXISTS rates (id INT AUTO_INCREMENT, date DATE, base VARCHAR(3), quote VARCHAR(3), rate FLOAT, PRIMARY KEY (id))')
        
    def upodate_rates(self, rates):
        for rate in rates:
            self.curser.execute('INSERT INTO rates VALUES (NULL, ?, ?, ?, ?)', (rate['date'], rate['base'], rate['quote'], rate['rate']))
        self.db.commit()
        
    def add_conversation(self, conversation):
        sql = f'INSERT INTO conversations VALUES (NULL, {conversation.timesatmp}, {conversation.amount}, {conversation.from_currency}, {conversation.to_currency}, {conversation.rate}, {conversation.result})'
        self.curser.execute(sql)
        self.db.commit()
        
    def get_rates(self, from_currency=None, to_currency=None):
        if from_currency is None or to_currency is None:
            self.curser.execute('SELECT * FROM rates')
            return
        self.curser.execute(f'SELECT * FROM rates WHERE BASE = {from_currency} AND QUOTE = {to_currency}')
    
    def get_conversations(self, condition=None):
        if condition is None:
            self.curser.execute('SELECT * FROM conversations')
            return
        self.curser.execute('SELECT * FROM conversations WHERE ' + condition)
    
class conversations:
    def __init__(self, timesatmp, amount, from_currency, to_currency, rate, result):
        self.timesatmp = timesatmp
        self.amount = amount
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.rate = rate
        self.result = result
        
    def __str__(self):
        return f'conversation: {self.timesatmp}, {self.amount}, {self.from_currency}, {self.to_currency}, {self.rate}, {self.result}'