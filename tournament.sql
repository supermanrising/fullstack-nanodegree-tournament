-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players (
	player_id		serial PRIMARY KEY,
	player_name 	text NOT NULL
);

CREATE TABLE matches (
	match_id		serial PRIMARY KEY,
	winner			integer REFERENCES players(player_id) ON DELETE CASCADE,
	loser			integer REFERENCES players(player_id) ON DELETE CASCADE,
	CONSTRAINT check_players_are_not_identical
    	CHECK (winner <> loser)
);

-- I read through this Udacity forum page for tips on how to implement views here
-- https://discussions.udacity.com/t/views-playerstandings/15415/11

CREATE VIEW wincounts AS
	SELECT
        player_id, player_name, count(winner)::integer AS wins
    FROM
        players
    LEFT JOIN
        matches ON player_id = winner
    GROUP BY player_id
    ORDER BY wins DESC;

CREATE VIEW totalmatches AS
	SELECT
        player_id, player_name, count(match_id)::integer AS games
    FROM
        players
    LEFT JOIN
        matches
    ON
        player_id = winner OR player_id = loser
    GROUP BY
        player_id;

CREATE VIEW standings AS
    SELECT
    	wincounts.player_id, wincounts.player_name, wincounts.wins, totalmatches.games
    FROM
    	wincounts
    LEFT JOIN
    	totalmatches
    ON
    	wincounts.player_id = totalmatches.player_id
    ORDER BY
    	wincounts.wins DESC
