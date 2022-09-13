from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass
from hashlib import sha256
import sqlite3


@contextmanager
def openDB(db: str) -> sqlite3.Cursor:
    """
    A context manager that yields the db cursor and commits the changes.
    """
    conn = sqlite3.connect(db)
    try:
        cur = conn.cursor()
        yield cur
    finally:
        conn.commit()
        conn.close()


class dataBaseManager:
    """
    A class that contains functions required to interact with the statistics database
    """

    def __init__(self, db: str):
        self.db = db
        # create the database if it doesn't exist
        with openDB(self.db) as cur:
            cur.execute(
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

    def register(self, username: str, password: str) -> bool:
        """
        Takes a username and password and adds them to the database.
        Returns True if the registration works, False if the username is already taken
        """
        # hash the password
        hashedPassword = sha256(password.encode()).hexdigest()
        try:
            with openDB(self.db) as cur:
                # insert the username and password hash into the database
                cur.execute(
                    "INSERT INTO users (username, passwordHash) VALUES (?, ?)",
                    (username, hashedPassword),
                )
            return True
        except sqlite3.IntegrityError:  # if the username is already taken
            return False

    def login(self, username: str, password: str) -> bool:
        """
        Checks if the username and password are correct and returns True if they are
        """
        # hash the password
        hashedPassword = sha256(password.encode()).hexdigest()
        # select the password hash from the database where the username is the one entered
        with openDB(self.db) as cur:
            cur.execute(
                "SELECT passwordHash FROM users WHERE username = ?", (username,)
            )
            # fetch the password hash
            passwordHash = cur.fetchone()
        if passwordHash and passwordHash[0] == hashedPassword:
            # if the password hashes match, return True
            return True
        return False

    def createStatsTable(self, username: str) -> Statistics:
        """
        Reads the statistics for the user from the database
        """
        with openDB(self.db) as cur:
            cur.execute(
                "SELECT username, wins, losses, draws, totalGames, roundsPlayed, timePlayed FROM users WHERE username = ?",
                (username,),
            )
            stats = cur.fetchone()
        return Statistics(*stats)

    def createEmptyStatsTable(self, username: str) -> Statistics:
        """
        Creates a new empty stats table
        """
        return Statistics(username)

    def saveStatsTable(self, stats: Statistics):
        with openDB(self.db) as cur:
            cur.execute(
                """UPDATE users SET wins = ?, losses = ?, draws = ?, totalGames = ?, roundsPlayed = ?, timePlayed = ? WHERE username = ?""",
                (
                    stats.wins,
                    stats.losses,
                    stats.draws,
                    stats.totalGames,
                    stats.roundsPlayed,
                    stats.timePlayed,
                    stats.username,
                ),
            )


@dataclass
class Statistics:
    """
    Statistics class that stores the statistics of a human player
    """

    username: str
    wins: int = 0
    losses: int = 0
    draws: int = 0
    totalGames: int = 0
    roundsPlayed: int = 0
    timePlayed: float = 0.0
