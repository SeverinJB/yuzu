# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import csv
import pandas as pd

bar_dict = {   'close': 158.81,
    'high': 158.83,
    'low': 158.725,
    'open': 158.725,
    'symbol': 'AAPL',
    'timestamp': 1661879220000000000,
    'trade_count': 22,
    'volume': 1419,
    'vwap': 158.793961}

def on_bars(bar):
    print(f'received bar: {bar}')

    field_names = ['open','high','low','close','volume','timestamp']

    data = {'open': bar['open'],
            'high': bar['high'],
            'low': bar['low'],
            'close': bar['close'],
            'volume': bar['volume'],
            'timestamp': pd.Timestamp(bar['timestamp'])}

    print(f'received bar: {data}')

    with open(r'/data_sources/alpaca_data.csv', 'a') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writerow(data)
        file.close()

def get_latest_bars():
    data = []

    with open(r'/data_sources/alpaca_data.csv', 'r') as file:
        reader = csv.DictReader(file, skipinitialspace=True)

        for line in reader:
            data.append(line)

    return data

on_bars(bar_dict)

for bar in get_latest_bars():
    print(bar['timestamp'])