#conversion 
#id, timestamp, amount, base_currency, target_currency, rate, result

#rates
#id, date, target_currency, base_currency, rate

# from currency = base
# to currency = quote 

import sqlite3
from contextlib import contextmanager

class DataBase:
    def __init__(self, path='conversions.db'):
        self.path = path
        self._create_tables()
        
    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
        
    def _create_tables(self):
        with self._connect() as conn:
            conn.execute('''
                            CREATE TABLE IF NOT EXISTS conversions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp TEXT,
                                amount REAL NOT NULL,
                                base_currency TEXT NOT NULL,
                                target_currency TEXT NOT NULL,
                                rate REAL NOT NULL, 
                                result REAL NOT NULL)
                            ''')
        
            conn.execute('''
                            CREATE TABLE IF NOT EXISTS rates (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                date TEXT,
                                base_currency TEXT NOT NULL,
                                target_currency TEXT NOT NULL,
                                rate REAL NOT NULL)
                                UNIQUE (date, base_currency, target_currency
                                )
                            ''')
        
    def update_rates(self, rates):
        with self._connect() as conn:
            for rate in rates:
                conn.execute('''
                    INSERT INTO rates 
                    (date, base_currency, target_currency, rate) 
                    VALUES (NULL, ?, ?, ?, ?)
                    ON CONFLICT (date, base_currency, target_currency)
                    DO UPDATE SET rate = excluded.rate
                    ''',(
                        rate['date'], 
                        rate['base'], 
                        rate['quote'], 
                        rate['rate']
                        )
                    )
        
    def add_conversion(self, conversion):
        with self._connect() as conn:
            conn.execute('''
                INSERT INTO conversion 
                (timestamp, amount, base_currency, target_currency, rate, result) 
                VALUES (NULL, ?, ?, ?, ?, ?, ?)
                ''', (
                    conversion.timestamp, 
                    conversion.amount, 
                    conversion.base_currency, 
                    conversion.target_currency, 
                    conversion.rate, 
                    conversion.result
                    ))
        
    def get_rates(self, base_currency=None, target_currency=None):
        sql = 'SELECT * FROM rates'
        clauses, params = [], []
        
        if base_currency is not None:
            clauses.append('base_currency = ?')
            params.append(base_currency)
        if target_currency is not None:
            clauses.append('target_currency = ?')
            params.append(target_currency
                          )
        if clauses:
            sql += 'WHERE ' + ' AND '.join(clauses)
        with self._connect() as conn:
            return conn.execute(sql,params).fetchall()
    
    def get_conversion(self, limit=50):
        with self._connect() as conn:
            return conn.execute(
                'SELECT * FROM conversion ORDER BY id DESC LIMIT ?', (limit,)
            ).fetchall()
        
    
class Conversion:
    def __init__(self, timestamp, amount, base_currency, target_currency, rate, result):
        self.timestamp = timestamp
        self.amount = amount
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.rate = rate
        self.result = result
        
    def __str__(self):
        return f'conversion: {self.timestamp}, {self.amount}, {self.base_currency}, {self.target_currency}, {self.rate}, {self.result}'