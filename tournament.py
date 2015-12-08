#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    SQL = "DELETE FROM matches;"
    cursor.execute(SQL)

    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    SQL = "DELETE FROM players;"
    cursor.execute(SQL)

    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    SQL = "SELECT COUNT(*) FROM players AS integer;"
    cursor.execute(SQL)

    numberOfPlayers = cursor.fetchone()
    db.close()

    return numberOfPlayers[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    db, cursor = connect()
    SQL = ("INSERT INTO players (player_name) VALUES (%s)")

    playerName = bleach.clean(name)
    data = (playerName, )
    cursor.execute(SQL, data)

    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db, cursor = connect()

    SQL = "SELECT * FROM standings;"
    cursor.execute(SQL)

    player_standings = cursor.fetchall()
    db.close()

    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db, cursor = connect()

    SQL = """
        INSERT INTO
            matches (match_id, winner, loser)
        VALUES
            (DEFAULT, %s, %s)
    """
    cursor.execute(SQL, (winner, loser))

    db.commit()
    db.close()


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

    player_lineup = playerStandings()

    if len(player_lineup) % 2 == 0:
        list_ordered_by_rank = []

        for player in player_lineup:
            list_ordered_by_rank.append(player[0])
            list_ordered_by_rank.append(player[1])

        # I found this code here:
        # http://stackoverflow.com/questions/1624883/alternative-way-to-split-a-list-into-groups-of-n
        grouped_list = zip(*(iter(list_ordered_by_rank),) * 4)

        return grouped_list
    else:
        print "Number of players should be even."
        return False
