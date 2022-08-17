import json
import requests


class Bank:

    def __init__(self):
        self.rates = self.get_rates()

    def get_rates(self):
        try:
            get_request = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
            if get_request.status_code == 200:
                self.rates = json.loads(get_request.content)
                return self.rates
            else:
                return None
        except requests.exceptions.ConnectionError:
            print('FIX YOUR INTERNET')
