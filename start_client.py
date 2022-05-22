import client
import globals


def start_client():
    cli = client.Client(
        globals.TEST_CLIENT_ID, {globals.BANK1_ID: globals.BANK1_EXISTING_SECRET}
    )
    cli.start()


if __name__ == "__main__":
    start_client()
