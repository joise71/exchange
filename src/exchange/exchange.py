import csv
from datetime import datetime
from bank import Bank


class Exchange:

    def __init__(self):
        self.balance = self.get_wallet_balance('wallet.csv')
        self.rate = None
        self.command = None
        self.splitted_command = None
        self.currency_rcvd = None
        self.amount_rcvd = None
        self.amount_to_give = None
        self.currency_to_give = None
        self.exchange_success = False

    def get_wallet_balance(self, filename):
        self.balance = {}
        with open(filename, 'r') as file:
            wallet_csv = csv.reader(file)
            next(wallet_csv)
            for line in wallet_csv:
                try:
                    self.balance[line[0]] = float(line[1])
                except IndexError:
                    break
            return self.balance

    def get_command(self):
        self.command = input('COMMAND?').strip().upper()
        self.splitted_command = self.command.split(' ')
        if len(self.splitted_command) > 1:
            self.currency_rcvd = self.splitted_command[1]
            if len(self.splitted_command) > 2:
                try:
                    self.amount_rcvd = float(self.splitted_command[2])
                except ValueError:
                    print('INVALID COMMAND FORMAT')
        return self.splitted_command, self.currency_rcvd, self.amount_rcvd

    def get_operation_rate(self, bank=Bank()):
        if bank.get_rates() is not None:
            try:
                assert self.currency_rcvd in self.balance.keys()
                match self.currency_rcvd:
                    case 'USD':
                        self.rate = float(list(filter(lambda x: x['ccy'] == 'USD', bank.get_rates()))[0]['buy'])
                        self.currency_to_give = 'UAH'
                    case 'UAH':
                        self.rate = float(list(filter(lambda x: x['ccy'] == 'USD', bank.get_rates()))[0]['sale'])
                        self.currency_to_give = 'USD'
                    case _:
                        self.rate = float(list(filter(lambda x: x['ccy'] == self.currency_rcvd,
                                                      bank.get_rates()))[0]['buy'])
                        self.currency_to_give = 'USD'
            except AssertionError:
                print(f'INVALID CURRENCY {self.currency_rcvd}\n')
        else:
            print('ERROR. SERVICE NOT RESPONDING')

    def exchange(self):
        if (self.rate and self.amount_rcvd) is not None:
            if self.currency_rcvd == 'UAH':
                self.amount_to_give = round(self.amount_rcvd / self.rate, 2)
            else:
                self.amount_to_give = round(self.amount_rcvd * self.rate, 2)
            if self.amount_to_give <= self.balance[self.currency_to_give]:
                self.exchange_success = True

    def update_balance(self):
        if self.exchange_success is True:
            with open('wallet.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)
                dict_from_csv = dict((rows[0], rows[1]) for rows in reader)
            dict_from_csv[self.currency_rcvd] = float(dict_from_csv[self.currency_rcvd]) + self.amount_rcvd
            dict_from_csv[self.currency_to_give] = float(dict_from_csv[self.currency_to_give]) - self.amount_to_give
            with open('wallet.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                header = ['currency', 'amount']
                writer.writerow(header)
                for key, value in dict_from_csv.items():
                    writer.writerow([key, value])

    def print_rate(self):
        if self.rate is not None:
            print(f'RATE {self.rate}, AVAILABLE {self.balance[self.currency_rcvd]}\n')

    def print_operation(self):
        if (self.rate and self.amount_rcvd) is not None:
            if self.amount_to_give % round(self.amount_to_give) == 0:
                self.amount_to_give = int(self.amount_to_give)
            if self.exchange_success is not True:
                print(f'UNAVAILABLE, REQUIRED BALANCE {self.currency_to_give} {self.amount_to_give}, AVAILABLE '
                      f'{self.balance[self.currency_to_give]}\n')
            else:
                print(f'{self.currency_to_give} {self.amount_to_give}, RATE {self.rate}\n')

    def update_values(self):
        self.__init__()

    def write_log(self):
        if self.exchange_success is True:
            with open('wallet.log', 'a', newline='') as file:
                now = datetime.now()
                time = now.strftime('%Y-%m-%d %H:%M:%S')
                string = (
                    f'{time} - {self.amount_rcvd} {self.currency_rcvd} to {self.amount_to_give} {self.currency_to_give},'
                    f'bal {self.balance[self.currency_rcvd]:>.2f}{self.currency_rcvd} '
                    f'{self.balance[self.currency_to_give]:>.2f}{self.currency_to_give}\n')
                file.write(string)

