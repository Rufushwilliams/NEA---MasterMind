from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass
from hashlib import sha256
from time import strftime
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
        # create the tables if they don't exist
        with openDB(self.db) as cur:
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                passwordHash TEXT,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                totalGames INTEGER DEFAULT 0,
                roundsPlayed INTEGER DEFAULT 0,
                timePlayed REAL DEFAULT 0
                )"""
            )
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS pastGames (
                gameID INTEGER PRIMARY KEY,
                player1 TEXT,
                player2 TEXT,
                winner TEXT,
                lengthOfCode INTEGER,
                numGuesses INTEGER,
                numRounds INTEGER,
                colourNum INTEGER,
                duplicatesAllowed INTEGER,
                date TEXT,
                timeTaken REAL,
                mode TEXT
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
        if stats:
            return Statistics(*stats)
        else:
            # if the user doesn't exist, create an empty stats table
            return self.createEmptyStatsTable(username)

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
                    round(stats.timePlayed, 2),
                    stats.username,
                ),
            )

    def getPlayerPosition(self, username: str) -> int:
        """
        Returns the position of the player in the leaderboard.
        The leaderboard is sorted by wins, then losses, then time played.
        """
        with openDB(self.db) as cur:
            # count the number of players with more wins than the player
            # select all players with the same number of wins as the player
            # count the number of players with less losses than the player from the previous selection
            # select all players with the same number of wins and losses as the player
            # count the number of players with more time played than the player from the previous selection
            # add up these values plus one to get the position
            cur.execute(
                """
                SELECT
                (SELECT COUNT(*) FROM users WHERE wins > (SELECT wins FROM users WHERE username = ?)) +
                (SELECT COUNT(*) FROM users WHERE wins = (SELECT wins FROM users WHERE username = ?) AND losses < (SELECT losses FROM users WHERE username = ?)) +
                (SELECT COUNT(*) FROM users WHERE wins = (SELECT wins FROM users WHERE username = ?) AND losses = (SELECT losses FROM users WHERE username = ?) AND timePlayed > (SELECT timePlayed FROM users WHERE username = ?)) + 1
                """,
                (username,) * 6,
            )
            position = cur.fetchone()
        return position[0]

    def getLeaderboard(self, numPlayers: int) -> list[Statistics]:
        """
        Gets the leaderboard for the given number of players.
        Returns a list of the Statistics objects for the players sorted by wins.
        If wins are equal, the player with the least losses is higher.
        If losses are equal, the player with the highest time played is higher.
        """
        with openDB(self.db) as cur:
            cur.execute(
                "SELECT username, wins, losses, draws, totalGames, roundsPlayed, timePlayed FROM users ORDER BY wins DESC, losses ASC, timePlayed DESC LIMIT ?",
                (numPlayers,),
            )
            stats = cur.fetchall()
        return [Statistics(*stat) for stat in stats]

    def savePastGame(
        self,
        pl1Username: str,
        pl2Username: str,
        winnerUsername: str,
        lengthOfCode: int,
        numGuesses: int,
        numRounds: int,
        colourNum: int,
        duplicatesAllowed: bool,
        timeTaken: float,
        mode: str,
    ):
        with openDB(self.db) as cur:
            cur.execute(
                """INSERT INTO pastGames (player1, player2, winner, lengthOfCode, numGuesses, numRounds, colourNum, duplicatesAllowed, date, timeTaken, mode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    pl1Username,
                    pl2Username,
                    winnerUsername,
                    lengthOfCode,
                    numGuesses,
                    numRounds,
                    colourNum,
                    duplicatesAllowed,
                    strftime("%d/%m/%Y"),
                    timeTaken,
                    mode,
                ),
            )

    def getPastGames(self, username: str) -> list[tuple]:
        with openDB(self.db) as cur:
            cur.execute(
                "SELECT gameID, player1, player2, winner, lengthOfCode, numGuesses, numRounds, colourNum, duplicatesAllowed, date, timeTaken, mode FROM pastGames WHERE player1 = ? OR player2 = ?",
                (username, username),
            )
            results = cur.fetchall()
        return results


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
