import bank
import globals


def start_bank():
    bank1 = bank.Bank(globals.BANK1_ID, clients={globals.TEST_CLIENT_ID: globals.BANK1_EXISTING_SECRET})
    bank1.start()

if __name__ == '__main__':
    start_bank()
