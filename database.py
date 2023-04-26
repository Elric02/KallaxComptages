import sqlite3
import pandas as pd
import openpyxl


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


    # Entry

    cur.execute("SELECT max(entryID) FROM Entry")
    cols = []
    if datadict["data_types"][0]:
        cols += [openpyxl.utils.column_index_from_string(datadict["data_columns"][0][0]) - 1]
        if len(datadict["data_columns"][0][1]) <= 3:
            cols += [openpyxl.utils.column_index_from_string(datadict["data_columns"][0][1]) - 1]
        cols += [openpyxl.utils.column_index_from_string(datadict["data_columns"][0][2]) - 1, openpyxl.utils.column_index_from_string(datadict["data_columns"][0][3]) - 1]
        print(cols)
        entries = datadict["df"].iloc[int(datadict["working_rows"][0][0])-1:int(datadict["working_rows"][0][1]), cols]
        print(entries)
    # TODO data_types[1] and data_types[2]


    con.commit()
    con.close()
