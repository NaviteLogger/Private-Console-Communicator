# The init_db.py file is used to initialize the database.
# It is used to create the database and the tables.

import sqlite3

# Connect to the database
conn = sqlite3.connect("../database/connections.db")

# Create the tables
