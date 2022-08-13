from exchange import Exchange


def main(exchange):
    commands = ['COURSE', 'EXCHANGE', 'STOP']
    while True:
        exchange.get_command()
        try:
            assert (exchange.splitted_command[0] in commands and ((len(exchange.splitted_command) > 1) or
                                                                  exchange.splitted_command[0] == 'STOP'))
            match exchange.splitted_command[0]:
                case 'COURSE':
                    exchange.get_operation_rate()
                    exchange.print_rate()
                    exchange.update_values()
                case 'EXCHANGE':
                    exchange.get_operation_rate()
                    exchange.exchange()
                    exchange.update_balance()
                    exchange.write_log()
                    exchange.print_operation()
                    exchange.update_values()
                case 'STOP':
                    print('SERVICE STOPPED')
                    break
                case _:
                    print('INVALID COMMAND')
        except AssertionError:
            print('INVALID COMMAND')


if __name__ == '__main__':
    exchange = Exchange()
    main(exchange)
