from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import sqlite3


class dataBaseManager:
    ################################################
    # TODO: REWRITE THIS CLASS TO USE WITH KEYWORD #
    ################################################
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
        result = self.cur.fetchone()
        if result and result[0] == hashedPassword:
            # if the password hashes match, return True
            return True
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

    def createEmptyStatsTable(self, username: str) -> Statistics:
        """
        Creates a new empty stats table
        """
        return Statistics(username)

    def saveStatsTable(self, stats: Statistics):
        self.cur.execute(
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
        self.conn.commit()

    def __del__(self):
        self.conn.close()


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
