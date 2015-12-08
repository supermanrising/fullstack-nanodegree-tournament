# Tournament Database & Python Module

This is a database schema to store the game matches between players.  It includes a Python module which uses a swiss tournaments system (non elimination style) to rank the players and pair them up in matches based on current standings.

## Quick Setup

To use the app, clone this repository onto your local machine.

To test the app, you'll need to use a virtual linux machine.  I recommend installing and running Vagrant on your computer.  For complete directions on how to install and setup Vagrant, please refer to this [helpful guide](https://www.udacity.com/wiki/ud197/install-vagrant).

## Create The Database & Import The Database Schema.

Use terminal to navigate to the project directory.  Once vagrant has been initiated using `vagrant up`, you can use the one step command `psql -f tournament.sql` to create the database and import the database schema

## Testing The App

To test the app use the command `python tournament_test.py`.  This will run the python code included in the tournament_test.py file, which will test each of the tournament.py functions individually.