import sqlite3
import pandas as pd


# MAIN PROCESS

def main(datadict):

    # Initializing

    print("Starting transfer to database with datadict", datadict)
    con = sqlite3.connect('db/database.db')
    cur = con.cursor()

    # Source

    cur.execute("SELECT max(sourceID) FROM Source")
    maxSourceID = cur.fetchall()[0][0]
    if maxSourceID == None:
        sourceID = 0
    else:
        sourceID = maxSourceID + 1
    file = datadict["filename"]
    place = str(datadict["location"])
    cur.execute("INSERT INTO Source VALUES (?, ?, ?)", (file, sourceID, place))


    # TODO

    con.commit()
    con.close()
