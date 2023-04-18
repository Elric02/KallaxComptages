import sqlite3
import pandas as pd


# MAIN PROCESS

def main(datadict):
    con = sqlite3.connect('db/database.db')
    cur = con.cursor()
    print("Starting transfer to database with datadict", datadict)

    # TODO

    con.commit()
    con.close()
