from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import sqlite3


class dataBaseManager:
    def __init__(self, db: str):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            username text PRIMARY KEY,
            passwordHash text,
            wins int DEFAULT 0,
            losses int DEFAULT 0,
            draws int DEFAULT 0,
            totalGames int DEFAULT 0,
            roundsPlayed int DEFAULT 0,
            timePlayed float DEFAULT 0
            )"""
        )
        self.conn.commit()

    def register(self, username: str, password: str) -> bool:
        """
        Takes a username and password and adds them to the database.
        Returns True if the registration works, False if the username is already taken
        """
        hashedPassword = sha256(password.encode()).hexdigest()
        try:
            self.cur.execute(
                "INSERT INTO users (username, passwordHash) VALUES (?, ?)",
                (username, hashedPassword),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login(self, username: str, password: str) -> bool:
        """
        Checks if the username and password are correct and returns True if they are
        """
        # hash the password
        hashedPassword = sha256(password.encode()).hexdigest()
        # select the password hash from the database where the username is the one entered
        self.cur.execute(
            "SELECT passwordHash FROM users WHERE username = ?", (username,)
        )
        # get the password hash from the database
        hashedPasswordFromDB = self.cur.fetchone()[0]
        # check if the password hashes match
        if hashedPassword == hashedPasswordFromDB:
            return True
        else:
            return False

    def createStatsTable(self, username: str) -> Statistics:
        """
        Reads the statistics for the user from the database
        """
        self.cur.execute(
            """SELECT username, wins, losses, draws, totalGames, roundsPlayed, timePlayed FROM users WHERE username = ?""",
            (username,),
        )
        stats = Statistics(*self.cur.fetchone())
        return stats

    def __del__(self):
        self.conn.close()


@dataclass
class Statistics:
    """
    Statistics class that stores the statistics of a human player
    """

    username: str
    wins: int
    losses: int
    draws: int
    totalGames: int
    roundsPlayed: int
    timePlayed: float


def main():
    db = "test.db"
    dbm = dataBaseManager(db)
    x = dbm.register("test", "test123")
    if x:
        print("Registered")
    else:
        print("Username already taken")
    x = dbm.register("rufus2", "password")
    if x:
        print("Registered")
    else:
        print("Username already taken")

    y = dbm.createStatsTable("test")
    print(y)
    # choice = input("Register or Login? (1/2): ")
    # if choice == "1":
    #     x = dbm.register("test", "test")
    #     if x:
    #         print("Registered!")
    #     else:
    #         print("There was an unexpected error")
    # else:
    #     user = input("Username: ")
    #     password = input("Password: ")
    #     if dbm.login(user, password):
    #         print("Logged in!")
    #     else:
    #         print("Incorrect username or password")


if __name__ == "__main__":
    main()
