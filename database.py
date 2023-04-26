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
    if maxSourceID == None:
        sourceID = 0
    else:
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
    if maxEntryID == None:
        entryID = 0
    else:
        entryID = maxEntryID + 1

    if datadict["data_types"][0]:
        for index, entry in entries.iterrows():
            date = next(datefinder.find_dates(entry.loc[cols[0]]))
            type = entry.loc[cols[4]]
            cur.execute("INSERT INTO Entry VALUES (?, ?, ?, ?)", (entryID, sourceID, date, type))
            entryID += 1

    # TODO data_types[1] and data_types[2]


    con.commit()
    con.close()
