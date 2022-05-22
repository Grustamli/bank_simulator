import socket
import threading

import globals
import bank_db
import json

import hasher


class Client:
    def __init__(self, id: int, secrets: {}):
        self.id = id
        self.secrets = secrets

    def start(self) -> None:
        self.simulate()

    def simulate(self):
        bank_id = input("Enter the bank id you wish to open account: ")
        self.request_account(bank_id)

    def request_account(self, bank_id: str):
        host, port = bank_db.get_bank(bank_id)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            request_data = self.acct_request_data()
            request_json = str.encode(json.dumps(request_data))
            s.sendall(request_json)
            rand_code = s.recv(1024)

            bank_id = request_data['existing_bank']
            secret = self.secrets[bank_id]
            hash = self._hash(secret, rand_code)
            s.sendall(str.encode(hash))
            response = s.recv(1024)
            print(response)

    def _hash(self, secret, random_code):
        code = bytes.decode(random_code, "ascii")
        return hasher.hash(secret, code)

    def get_any_registered_bank(self):
        return next(iter(self.secrets))

    def acct_request_data(self):
        req = {
            "code": globals.REQUEST_ACCT_CODE,
            "client_id": self.id,
            "existing_bank": self.get_any_registered_bank(),
        }
        return req
