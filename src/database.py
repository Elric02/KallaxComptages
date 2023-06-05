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
    # connect to database
    con = sqlite3.connect('db/database.db')
    cur = con.cursor()


    # Source

    # set source ID based on current maximum ID + 1
    cur.execute("SELECT max(sourceID) FROM Source")
    maxSourceID = cur.fetchall()[0][0]
    sourceID = 0
    if maxSourceID != None:
        sourceID = maxSourceID + 1
    # set filename and location based on data inputs
    file = datadict["filename"]
    place = str(datadict["location"])
    cur.execute("INSERT INTO Source VALUES (?, ?, ?)", (file, sourceID, place))


    # Entry and its subobjects

    cols = {}
    entries = pd.DataFrame()

    # set entry ID based on current maximum ID + 1
    cur.execute("SELECT max(entryID) FROM Entry")
    maxEntryID = cur.fetchall()[0][0]
    entryID = 0
    if maxEntryID is not None:
        entryID = maxEntryID + 1

    # the following lines are only if data type is unique, aggregated types come later
    if datadict["data_types"][0]:
        # for each data column
        for i, elem in enumerate(datadict["data_columns"][0]):
            # if the value is set to the placeholder, consider that no data needs to be stored for this element
            if elem == main.optionmenu_with_none or elem == main.optionmenu_with_other_date:
                cols[i] = None
            else:
                # select only the column identifier (taking out the first value of the column)
                if datadict["filetype"] == ".xlsx":
                    cols[i] = openpyxl.utils.column_index_from_string(elem.split(" (")[0]) - 1
                else:
                    cols[i] = int(elem.split(" (")[0]) - 1
        # generate a list containing every non-null column identifier
        cols_list = list(filter(lambda item: item is not None, cols.values()))
        # update the entries dataframe with the correct data area, taking into account working rows and columns
        entries = datadict["df"].iloc[int(datadict["working_rows"][0][0])-1:int(datadict["working_rows"][0][1]), cols_list]

        # iterate over every entry to create an object to insert in the db for each of them
        for index, entry in entries.iterrows():
            # Entry
            # generate automatically the date based on the provided string from the data (next() is to take the first found value)
            date = next(datefinder.find_dates(str(entry.loc[cols[0]])))
            # if there is a separated column for the time of the entry, take it and combine with the date it in the "date" variable
            if cols[1] is not None:
                hour = next(datefinder.find_dates(str(entry.loc[cols[1]])))
                date = datetime.datetime.combine(date.date(), hour.time())
            # set vehicle type based on data input
            vehicletype = entry.loc[cols[4]]
            # prepare SQL statement to create object in the database
            cur.execute("INSERT INTO Entry VALUES (?, ?, ?, ?)", (entryID, sourceID, date, vehicletype))

            # Unique
            # set speed and noise based on data input, stick with None if values aren't defined
            speed = entry.loc[cols[2]] if cols[2] is not None else None
            noise = entry.loc[cols[3]] if cols[3] is not None else None
            # prepare SQL statement to create object in the database
            cur.execute("INSERT INTO 'Unique' VALUES (?, ?, ?)", (entryID, speed, noise))

            # prepare the ID for the next entry
            entryID += 1

    if datadict["data_types"][1]:
        # add date and hour columns to the data columns
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

        # find timespan by taking the first date value of the column (firstdate) and the second date value of the column and substracting them
        firstdate = next(datefinder.find_dates(str(entries.loc[int(datadict["working_rows"][1][0]), cols[0]])))
        # take into account if the time of the day is defined in a separate column
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
            # no support for the vehicle type (yet)
            vehicletype = None
            cur.execute("INSERT INTO Entry VALUES (?, ?, ?, ?)", (entryID, sourceID, date, vehicletype))

            # AggregatedTime
            # set entry values based on data input, stick with None if values aren't defined
            nb = entry.loc[cols[2]] if cols[2] is not None else None
            vmean = entry.loc[cols[3]] if cols[3] is not None else None
            vmax = entry.loc[cols[4]] if cols[4] is not None else None
            v85 = entry.loc[cols[5]] if cols[5] is not None else None
            v50 = entry.loc[cols[6]] if cols[6] is not None else None
            v30 = entry.loc[cols[7]] if cols[7] is not None else None
            v10 = entry.loc[cols[8]] if cols[8] is not None else None
            cur.execute("INSERT INTO 'AggregatedTime' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (entryID, str(timespan), nb,
                                                                                            vmean, vmax, v85, v50, v30, v10))

            # prepare the ID for the next entry
            entryID += 1

        # reset cols in case there is also speed-aggregated data
        cols = {}

    if datadict["data_types"][2]:
        # add speed and speedspan columns to the data columns
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

        # find speedspan if a beginning value and an end value were provided and are not difficulty-readable strings
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
            # find date based on the data input
            date = datetime.datetime.strptime(str(datadict["data_columns"][2][1]), '%m/%d/%y')
            # no support for the vehicle type (yet)
            vehicletype = None
            cur.execute("INSERT INTO Entry VALUES (?, ?, ?, ?)", (entryID, sourceID, date, vehicletype))

            # AggregatedSpeed
            # set entry values based on data input, stick with None if values aren't defined
            speed = entry.loc[cols[0]] if cols[0] is not None else None
            nb = entry.loc[cols[2]] if cols[2] is not None else None
            cur.execute("INSERT INTO 'AggregatedSpeed' VALUES (?, ?, ?, ?)", (entryID, speed, speedspan, nb))

            # prepare the ID for the next entry
            entryID += 1


    # commit SQL statements to database and then close it
    con.commit()
    con.close()
    print("Transfer to database completed!")