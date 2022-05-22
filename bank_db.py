import sqlite3
import os

DB_FILE = "banks.db"


def delete_db():
    try:
        os.remove(DB_FILE)
    except:
        pass


def init_db():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE banks 
                (id text, host text, port integer)"""
    )


def get_bank(id: str):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    row = cur.execute("SELECT host, port FROM banks WHERE id = ?", (id,)).fetchone()
    con.close()
    return row


def register_bank(id: str, host: str, port: int):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    row = cur.execute("SELECT host, port FROM banks WHERE id = ?", (id,)).fetchone()
    if row is None:
        cur.execute(
            "INSERT INTO banks (id, host, port) VALUES (?, ?, ?)", (id, host, port)
        )
    else:
        cur.execute(
            "UPDATE banks SET host = ?, port = ? WHERE id = ?", (host, port, id)
        )
    con.commit()
    con.close()
