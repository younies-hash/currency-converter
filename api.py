import requests, json

def fetch_data():
    url = 'https://api.frankfurter.dev/v2/rates'
    response = requests.get(url)
    data = response.json()
    with open('rates.json', 'w') as FILE:
        json.dump(data, FILE, indent=4)
        FILE.close()
    return data