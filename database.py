import sqlite3
import pandas as pd
import openpyxl
import datefinder


# MAIN PROCESS

def main(datadict):

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


    # Entry

    cols = {}
    entries = pd.DataFrame()

    if datadict["data_types"][0]:
        cols[0] = openpyxl.utils.column_index_from_string(datadict["data_columns"][0][0]) - 1
        for i in range(1, len(datadict["data_columns"][0])):
            if len(datadict["data_columns"][0][i]) <= 3:
                cols[i] = openpyxl.utils.column_index_from_string(datadict["data_columns"][0][i]) - 1
            else:
                cols[i] = None
        cols_list = list(filter(lambda item: item is not None, cols.values()))
        entries = datadict["df"].iloc[int(datadict["working_rows"][0][0])-1:int(datadict["working_rows"][0][1]), cols_list]

    # TODO data_types[1] and data_types[2]

    cur.execute("SELECT max(entryID) FROM Entry")
    maxEntryID = cur.fetchall()[0][0]
    entryID = 0
    if maxEntryID != None:
        entryID = maxEntryID + 1

    if datadict["data_types"][0]:
        for index, entry in entries.iterrows():
            # Entry
            date = next(datefinder.find_dates(entry.loc[cols[0]]))
            type = entry.loc[cols[4]]
            cur.execute("INSERT INTO Entry VALUES (?, ?, ?, ?)", (entryID, sourceID, date, type))

            # Unique
            speed = entry.loc[cols[2]] if cols[2] is not None else None
            noise = entry.loc[cols[3]] if cols[3] is not None else None
            cur.execute("INSERT INTO 'Unique' VALUES (?, ?, ?)", (entryID, speed, noise))

            entryID += 1

    # TODO hour / date séparés
    # TODO CSV
    # TODO data_types[1] and data_types[2]




    con.commit()
    con.close()
