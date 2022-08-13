import csv
from datetime import datetime
import pandas as pd

from bank import Bank


class Exchange:

    def __init__(self):
        self.balance = self.get_wallet_balance('wallet.csv')
        self.rates = self.get_rates()
        self.rate = None
        self.command = None
        self.splitted_command = None
        self.currency_rcvd = None
        self.amount_rcvd = None
        self.amount_to_give = None
        self.currency_to_give = None

    def get_wallet_balance(self, filename):
        self.balance = {}
        with open(filename, 'r') as file:
            wallet_csv = csv.reader(file)
            header = next(wallet_csv)
            if header is not None:
                for line in wallet_csv:
                    self.balance[line[1]] = float(line[2])
                return self.balance

    def get_command(self):
        self.command = input('COMMAND?')
        self.splitted_command = self.command.split(' ')
        if len(self.splitted_command) > 1:
            self.currency_rcvd = self.splitted_command[1]
            if len(self.splitted_command) > 2:
                self.amount_rcvd = float(self.splitted_command[2])
        return self

    def get_rates(self):
        bank = Bank()
        self.rates = bank.rates
        return self.rates

    def get_operation_rate(self):
        try:
            assert self.currency_rcvd in self.balance.keys()
            for item in self.rates:
                match self.currency_rcvd:
                    case 'USD':
                        if item['ccy'] == 'USD':
                            self.rate = float(item['buy'])
                            self.currency_to_give = 'UAH'
                    case 'UAH':
                        if item['ccy'] == 'USD':
                            self.rate = float(item['sale'])
                            self.currency_to_give = 'USD'
                    case _:
                        if item['ccy'] == self.currency_rcvd:
                            self.rate = float(item['buy'])
                            self.currency_to_give = 'USD'
        except AssertionError:
            print(f'INVALID CURRENCY {self.currency_rcvd}\n')

    def exchange(self):
        if self.rate is not None:
            if self.currency_rcvd == 'UAH':
                self.rate = round((1 / self.rate), 6)
            self.amount_to_give = self.amount_rcvd * self.rate

    def update_balance(self):
        if self.amount_to_give is not None:
            if self.amount_to_give <= self.balance[self.currency_to_give]:
                with open('wallet.csv', 'r+', newline='') as file:
                    df = pd.read_csv('wallet.csv')
                    df.head()
                    df.loc[df['currency'] == self.currency_rcvd, 'amount'] = \
                        float(self.balance[self.currency_rcvd]) + self.amount_rcvd
                    df.loc[df['currency'] == self.currency_to_give, 'amount'] = \
                        float(self.balance[self.currency_to_give]) - self.amount_to_give
                    df.to_csv(file, index=False)

    def print_rate(self):
        if self.rate is not None:
            print(f'RATE {self.rate}, AVAILABLE {self.balance[self.currency_rcvd]}\n')

    def print_operation(self):
        if self.rate is not None:
            if self.amount_to_give % round(self.amount_to_give) == 0:
                self.amount_to_give = int(self.amount_to_give)
            if self.amount_to_give > self.balance[self.currency_to_give]:
                print(f'UNAVAILABLE, REQUIRED BALANCE {self.currency_to_give} {self.amount_to_give}, AVAILABLE '
                      f'{self.balance[self.currency_to_give]}\n')
            else:
                print(f'{self.currency_to_give} {self.amount_to_give}, RATE {self.rate}\n')

    def update_values(self):
        self.__init__()

    def write_log(self):
        with open('wallet.log', 'a', newline='') as file:
            now = datetime.now()
            time = now.strftime('%Y-%m-%d %H:%M:%S')
            string = (
                f'{time} - {self.amount_rcvd} {self.currency_rcvd} to {self.amount_to_give} {self.currency_to_give},'
                f'bal {self.balance[self.currency_rcvd]:>.2f}{self.currency_rcvd} '
                f'{self.balance[self.currency_to_give]:>.2f}{self.currency_to_give}\n')
            file.write(string)
            