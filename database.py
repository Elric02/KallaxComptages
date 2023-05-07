import sqlite3
import pandas as pd
import openpyxl
import datefinder
import datetime

import main


# MAIN PROCESS

def insert_db(datadict):

    # Initializing

    print("Starting transfer to database with datadict", datadict)
    con = sqlite3.connect('db/database.db')
    cur = con.cursor()


    # Source

    cur.execute("SELECT max(sourceID) FROM Source")
    maxSourceID = cur.fetchall()[0][0]
    sourceID = 0
    if maxSourceID != None:
        sourceID = maxSourceID + 1
    file = datadict["filename"]
    place = str(datadict["location"])
    cur.execute("INSERT INTO Source VALUES (?, ?, ?)", (file, sourceID, place))


    # Entry and its subobjects

    cols = {}
    entries = pd.DataFrame()

    cur.execute("SELECT max(entryID) FROM Entry")
    maxEntryID = cur.fetchall()[0][0]
    entryID = 0
    if maxEntryID is not None:
        entryID = maxEntryID + 1

    if datadict["data_types"][0]:
        for i, elem in enumerate(datadict["data_columns"][0]):
            if elem == main.optionmenu_with_none or elem == main.optionmenu_with_other:
                cols[i] = None
            else:
                if datadict["filetype"] == ".xlsx":
                    cols[i] = openpyxl.utils.column_index_from_string(elem) - 1
                else:
                    cols[i] = int(datadict["data_columns"][0][i].split(" (")[0]) - 1
        cols_list = list(filter(lambda item: item is not None, cols.values()))
        entries = datadict["df"].iloc[int(datadict["working_rows"][0][0])-1:int(datadict["working_rows"][0][1]), cols_list]

        for index, entry in entries.iterrows():
            # Entry
            date = next(datefinder.find_dates(entry.loc[cols[0]]))
            if cols[1] is not None:
                hour = next(datefinder.find_dates(entry.loc[cols[1]]))
                date = datetime.datetime.combine(date.date(), hour.time())
            type = entry.loc[cols[4]]
            cur.execute("INSERT INTO Entry VALUES (?, ?, ?, ?)", (entryID, sourceID, date, type))

            # Unique
            speed = entry.loc[cols[2]] if cols[2] is not None else None
            noise = entry.loc[cols[3]] if cols[3] is not None else None
            cur.execute("INSERT INTO 'Unique' VALUES (?, ?, ?)", (entryID, speed, noise))

            entryID += 1

    elif datadict["data_types"][1]:
        print("not supported yet")
    # TODO data_types[1] and data_types[2]






    con.commit()
    con.close()
