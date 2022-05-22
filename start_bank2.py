import bank
import globals


def start_bank():
    bank2 = bank.Bank(globals.BANK2_ID)
    bank2.start()


if __name__ == "__main__":
    start_bank()
