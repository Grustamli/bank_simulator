import json
import random
import secrets
import socket

import bank_db
import globals
import hasher


class Bank:
    def __init__(
        self, id: str, host: str = "localhost", port: int = 0, clients: dict = {}
    ):
        self.id = id
        self.host = host or "localhost"
        self.port = port
        self.clients = clients

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            port = s.getsockname()[1]
            bank_db.register_bank(self.id, self.host, port)
            s.listen()
            print("listening")
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                self._process_request(conn, data)

    def _process_request(self, conn, data):
        data = json.loads(data)
        if data:
            code = data["code"]
            if code == globals.REQUEST_ACCT_CODE:
                client_id = int(data["client_id"])
                existing_bank = data["existing_bank"]
                self._handle_acct_request(conn, client_id, existing_bank)
            elif code == globals.VERIFY_ACCT_CODE:
                client_id = int(data["client_id"])
                random_key = data["random"]
                hash = self._get_hash(client_id, random_key)
                conn.sendall(str.encode(hash))

    def _handle_acct_request(self, conn, client_id: int, existing_bank_id: str):
        code = self._generate_code()
        conn.sendall(code)
        client_hash = conn.recv(1024)
        bank_hash = self._verify_with_bank(existing_bank_id, client_id, code)

        if client_hash == bank_hash:
            self._create_account(client_id)
            conn.sendall(str.encode(self._create_account(client_id)))
        else:
            print("Hash mismatch!")
            conn.sendall(b"New account cannot be created.")

    def _create_account(self, client_id):
        secret = secrets.token_hex(16)
        self.clients[client_id] = secret
        return secret

    def _get_hash(self, client_id, random_key):
        secret = self.clients.get(client_id, "")
        return hasher.hash(secret, random_key)

    def _verify_with_bank(self, bank_id, client_id, code):
        host, port = bank_db.get_bank(bank_id)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            request_data = self._verification_request(client_id, code)
            request_json = str.encode(json.dumps(request_data))
            s.sendall(request_json)
            bank_hash = s.recv(1024)
            return bank_hash

    def _verification_request(self, client_id, code):
        return {
            "code": globals.VERIFY_ACCT_CODE,
            "client_id": client_id,
            "random": bytes.decode(code),
        }

    def _generate_code(self):
        return str.encode(secrets.token_hex(16), "ascii")
