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
            if elem == main.optionmenu_with_none or elem == main.optionmenu_with_other_date:
                cols[i] = None
            else:
                if datadict["filetype"] == ".xlsx":
                    cols[i] = openpyxl.utils.column_index_from_string(elem.split(" (")[0]) - 1
                else:
                    cols[i] = int(elem.split(" (")[0]) - 1
        cols_list = list(filter(lambda item: item is not None, cols.values()))
        entries = datadict["df"].iloc[int(datadict["working_rows"][0][0])-1:int(datadict["working_rows"][0][1]), cols_list]

        for index, entry in entries.iterrows():
            # Entry
            date = next(datefinder.find_dates(str(entry.loc[cols[0]])))
            if cols[1] is not None:
                hour = next(datefinder.find_dates(str(entry.loc[cols[1]])))
                date = datetime.datetime.combine(date.date(), hour.time())
            vehicletype = entry.loc[cols[4]]
            cur.execute("INSERT INTO Entry VALUES (?, ?, ?, ?)", (entryID, sourceID, date, vehicletype))

            # Unique
            speed = entry.loc[cols[2]] if cols[2] is not None else None
            noise = entry.loc[cols[3]] if cols[3] is not None else None
            cur.execute("INSERT INTO 'Unique' VALUES (?, ?, ?)", (entryID, speed, noise))

            entryID += 1

    if datadict["data_types"][1]:
        for i, elem in enumerate(datadict["date_hour_columns"] + datadict["data_columns"][1]):
            if elem == main.optionmenu_with_none or elem == main.optionmenu_with_other_begin:
                cols[i] = None
            else:
                if datadict["filetype"] == ".xlsx":
                    cols[i] = openpyxl.utils.column_index_from_string(elem.split(" (")[0]) - 1
                else:
                    cols[i] = int(elem.split(" (")[0]) - 1
        cols_list = list(filter(lambda item: item is not None, cols.values()))
        entries = datadict["df"].iloc[int(datadict["working_rows"][1][0]) - 1:int(datadict["working_rows"][1][1]), cols_list]

        # find timespan
        firstdate = next(datefinder.find_dates(str(entries.loc[int(datadict["working_rows"][1][0]), cols[0]])))
        if cols[1] is not None:
            hour = next(datefinder.find_dates(str(entries.loc[int(datadict["working_rows"][1][0]), cols[1]])))
            firstdate = datetime.datetime.combine(firstdate.date(), hour.time())
        seconddate = next(datefinder.find_dates(str(entries.loc[int(datadict["working_rows"][1][0])+1, cols[0]])))
        if cols[1] is not None:
            hour = next(datefinder.find_dates(str(entries.loc[int(datadict["working_rows"][1][0])+1, cols[1]])))
            seconddate = datetime.datetime.combine(seconddate.date(), hour.time())
        timespan = seconddate - firstdate

        for index, entry in entries.iterrows():
            # Entry
            date = next(datefinder.find_dates(str(entry.loc[cols[0]])))
            if cols[1] is not None:
                hour = next(datefinder.find_dates(str(entry.loc[cols[1]])))
                date = datetime.datetime.combine(date.date(), hour.time())
            vehicletype = None
            cur.execute("INSERT INTO Entry VALUES (?, ?, ?, ?)", (entryID, sourceID, date, vehicletype))

            # AggregatedTime
            nb = entry.loc[cols[2]] if cols[2] is not None else None
            vmean = entry.loc[cols[3]] if cols[3] is not None else None
            vmax = entry.loc[cols[4]] if cols[4] is not None else None
            v85 = entry.loc[cols[5]] if cols[5] is not None else None
            v50 = entry.loc[cols[6]] if cols[6] is not None else None
            v30 = entry.loc[cols[7]] if cols[7] is not None else None
            v10 = entry.loc[cols[8]] if cols[8] is not None else None
            cur.execute("INSERT INTO 'AggregatedTime' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (entryID, str(timespan), nb,
                                                                                            vmean, vmax, v85, v50, v30, v10))
            entryID += 1

        # Reset cols in case there is also speed-aggregated data
        cols = {}

    if datadict["data_types"][2]:
        for i, elem in enumerate([datadict["speed_column"]] + [datadict["speedspan_column"]] + [datadict["data_columns"][2][0]]):
            if elem == main.optionmenu_with_none or elem == main.optionmenu_with_other_begin:
                cols[i] = None
            else:
                if datadict["filetype"] == ".xlsx":
                    cols[i] = openpyxl.utils.column_index_from_string(elem.split(" (")[0]) - 1
                else:
                    cols[i] = int(elem.split(" (")[0]) - 1
        cols_list = list(filter(lambda item: item is not None, cols.values()))
        entries = datadict["df"].iloc[int(datadict["working_rows"][2][0]) - 1:int(datadict["working_rows"][2][1]), cols_list]

        # find speedspan
        if cols[1] is not None:
            endvalue = entries.loc[int(datadict["working_rows"][2][0]), cols[1]]
            startvalue = entries.loc[int(datadict["working_rows"][2][0]), cols[0]]
            if type(endvalue) != str and type(startvalue) != str:
                speedspan = endvalue - startvalue
            else:
                speedspan = None
        else:
            speedspan = None

        for index, entry in entries.iterrows():
            # Entry
            date = datetime.datetime.strptime(str(datadict["data_columns"][2][1]), '%m/%d/%y')
            vehicletype = None
            cur.execute("INSERT INTO Entry VALUES (?, ?, ?, ?)", (entryID, sourceID, date, vehicletype))

            # AggregatedSpeed
            speed = entry.loc[cols[0]] if cols[0] is not None else None
            nb = entry.loc[cols[2]] if cols[2] is not None else None
            cur.execute("INSERT INTO 'AggregatedSpeed' VALUES (?, ?, ?, ?)", (entryID, speed, speedspan, nb))

            entryID += 1


    con.commit()
    con.close()
    print("Transfer to database completed!")