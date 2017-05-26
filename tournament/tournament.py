#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM matches;")
    conn.commit()
    cur.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM players;")
    conn.commit()
    cur.close()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    #
    cur.execute("SELECT * FROM no_of_players;")
    num = cur.fetchall()
    cur.close()
    conn.close()
    if num:
        return num[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    if name:
        cur.execute("INSERT INTO players (player_name) VALUES(%s)",
                    (bleach.clean(name),))
    conn.commit()
    cur.close()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * from standings;")
    standings = cur.fetchall()
    cur.close()
    conn.close()
    if standings:
        return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    if winner and loser:
        cur.execute("INSERT INTO matches (winner, loser) VALUES(%s, %s)",
                    (bleach.clean(winner), bleach.clean(loser),))
    conn.commit()
    cur.close()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    pairs = []
    if standings and len(standings) % 2 == 0:
        for i in range(len(standings)):
            if i % 2 == 0:
                pairs.append([standings[i][0], standings[i][1],
                              standings[i + 1][0], standings[i + 1][1]])
    return pairs

# Code for testing
"""
if __name__ == '__main__':
    deleteMatches()
    deletePlayers()
    print countPlayers()
    registerPlayer("Madhu")
    registerPlayer("Bhargav")
    print countPlayers()
    standings = playerStandings()
    [id1, id2] = [row[0] for row in standings]
    reportMatch(id1, id2)
    print swissPairings()
    deleteMatches()
    deletePlayers()
"""
