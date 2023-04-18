import tkinter as tk
from tkinter import filedialog as tk_fd
import tkintermapview as tkmv
import pandas as pd
import openpyxl


# DATA SPECIFICATION

window = None
root = None
file = None
filetype = ''
xlsx_sheets = []
working_element = ''
df = None
data_types = [False, False, False] # raw, time-aggregated, speed-aggregated
working_rows = [[], [], []]
date_hour_columns = [0, 0]
speed_column = 0
data_columns = [[], [], []]
location = [0, 0]


# BEGIN AND END FUNCTION

def begin(newWindow, rootDef):
    global window, root, filetype, xlsx_sheets, working_element, df, data_types, working_rows, date_hour_columns, speed_column, data_columns, location
    window = newWindow
    root = rootDef
    print("Starting input process...")
    filetype = ''
    xlsx_sheets = []
    working_element = ''
    df = None
    data_types = [False, False, False] # raw, time-aggregated, speed-aggregated
    working_rows = [[], [], []]
    date_hour_columns = [0, 0]
    speed_column = 0
    data_columns = [[], [], []]
    location = [0, 0]
    pack_part1()

# Function to end the input process

def end_input(frame7):
    frame7.pack_forget()
    print("All necessary information gathered !")
    datadict = {
        "working_element": working_element,
        "df": df,
        "data_types": data_types,
        "working_rows": working_rows,
        "date_hour_columns": date_hour_columns,
        "speed_column": speed_column,
        "data_columns": data_columns,
        "location": location
    }
    import main
    global root
    main.receive_input(datadict, window, root)


# FUNCTIONS DEFINING DATA SPECIFICATIONS

# Function to open file and set file type
def choose_file(frame1):
    loc = tk_fd.askopenfilename(filetypes=(("fichier XLSX ou CSV", ["*.xlsx", "*.csv"]),))
    global filetype
    filetype = loc[loc.rindex('.'):]
    print("Importing", filetype, "located at", loc)
    global file, xlsx_sheets
    file = pd.ExcelFile(loc)
    xlsx_sheets = file.sheet_names
    pack_part2(frame1)


# Function to set working element (separator or working sheet)
def set_working_element(frame2, entry2a_var, entry2b):
    global working_element
    if filetype == ".xlsx":
        if entry2a_var.get() == "" or entry2a_var.get() == "Cliquez ici":
            return
        else:
            working_element = entry2a_var.get()
    else:
        if entry2b.get() == "":
            return
        else:
            working_element = entry2b.get()
    print("Working element set as", working_element)
    global file, df
    df = file.parse(sheet_name=working_element, header=None)
    pack_part3(frame2)


# Function to set data type(s)
def set_data_types(frame3, radio3var, check3var_1, check3var_2):
    global data_types
    if radio3var.get() == 1:
        data_types[0] = True
    else:
        if check3var_1.get() == 1:
            data_types[1] = True
        if check3var_2.get() == 1:
            data_types[2] = True
        if check3var_1.get() == 0 and check3var_2.get() == 0:
            return
    print("Data types set as... raw:", data_types[0], ", time-aggregated:", data_types[1], ", speed-aggregated:", data_types[2])
    pack_part4(frame3)


def set_working_rows(frame4, entry4a_1, entry4a_2, entry4b_1, entry4b_2, entry4c_1, entry4c_2):
    global working_rows
    if data_types[0]:
        working_rows[0] = [entry4a_1.get(), entry4a_2.get()]
        print("Working rows set for raw data as :", *working_rows[0])
    if data_types[1]:
        working_rows[1] = [entry4b_1.get(), entry4b_2.get()]
        print("Working rows set for time-aggregated data as :", *working_rows[1])
    if data_types[2]:
        working_rows[2] = [entry4c_1.get(), entry4c_2.get()]
        print("Working rows set for speed-aggregated data as :", *working_rows[2])
    print("Proceeding to part 5")
    pack_part5(frame4)


# Function to set date/hour and/or speed columns
def set_label_columns(frame5, entry5a_1, entry5a_2, entry5b):
    global date_hour_columns, speed_column
    if data_types[1]:
        date_hour_columns = [entry5a_1.get(), entry5a_2.get()]
        print("Date and hour columns set to :", *date_hour_columns)
    if data_types[2]:
        speed_column = entry5b.get()
        print("Speed column set to:", speed_column)
    print("Proceeding to part 6")
    pack_part6(frame5)


# Function to set actual data columns
def set_data_columns(frame6, entry6_1, entry6a_1, entry6a_2, entry6a_3, entry6a_4, entry6a_5, entry6a_6, entry6b_1, entry6a_7, entry6_2, ):
    global data_columns
    if data_types[0]:
        data_columns[0] = [entry6_1.get(), entry6_2.get()]
    else:
        if data_types[1]:
            data_columns[1] = [entry6a_1.get(), entry6a_2.get(), entry6a_3.get(), entry6a_4.get(), entry6a_5.get(), entry6a_6.get(), entry6a_7.get()]
        if data_types[2]:
            data_columns[2] = [entry6b_1.get()]
    print("Data received, proceeding to part 7")
    pack_part7(frame6)


# Function to set geolocation coordinates
def set_location(coords):
    global location
    location = coords
    print("Location set to :", location)


# PACKING FUNCTIONS

# PART 1 : CHOOSING FILE

def pack_part1():
    frame1 = tk.Frame(window)
    frame1.pack()

    label1 = tk.Label(frame1, text="1. Choisissez votre fichier d'entrée", font='Helvetica 16 bold')
    button1 = tk.Button(frame1, text="choisir", command= lambda: choose_file(frame1))

    label1.pack()
    button1.pack()


# PART 2 : DEFINING SEPARATORS/SHEET

def pack_part2(frame1):
    frame2 = tk.Frame(window)
    frame2.pack()

    label2a = tk.Label(frame2, text="2. Définissez la feuille à utiliser (par exemple feuille1)",
                       font='Helvetica 16 bold')
    entry2a_var = tk.StringVar()
    entry2a_var.set("Cliquez ici")
    entry2a = tk.OptionMenu(frame2, entry2a_var, *xlsx_sheets)

    label2b = tk.Label(frame2, text="2. Définissez le séparateur de colonnes (par exemple ;)",
                       font='Helvetica 16 bold')
    entry2b = tk.Entry(frame2, bd=5)

    button2 = tk.Button(frame2, text="valider", command= lambda: set_working_element(frame2, entry2a_var, entry2b))

    if filetype == ".xlsx":
        label2a.pack()
        entry2a.pack()
    else:
        label2b.pack()
        entry2b.pack()
    frame1.pack_forget()
    button2.pack()


# PART 3 : DEFINING DATA TYPE

def pack_part3(frame2):
    frame3 = tk.Frame(window)
    frame3.pack()

    def unpack_checkbox3():
        check3_1.pack_forget()
        check3_2.pack_forget()

    def pack_checkbox3():
        button3.pack_forget()
        check3_1.pack()
        check3_2.pack()
        button3.pack()

    label3 = tk.Label(frame3, text="2. Définissez le type de données disponibles", font='Helvetica 16 bold')
    radio3var = tk.IntVar()
    radio3_1 = tk.Radiobutton(frame3, text="données brutes", variable=radio3var, value=1, command=unpack_checkbox3)
    radio3_2 = tk.Radiobutton(frame3, text="données agrégées", variable=radio3var, value=2, command=pack_checkbox3)
    check3var_1 = tk.IntVar()
    check3var_2 = tk.IntVar()
    check3_1 = tk.Checkbutton(frame3, text="...par tranches de temps", variable=check3var_1, onvalue=1, offvalue=0)
    check3_2 = tk.Checkbutton(frame3, text="...par tranches de vitesse", variable=check3var_2, onvalue=1, offvalue=0)
    button3 = tk.Button(frame3, text="valider", command= lambda: set_data_types(frame3, radio3var, check3var_1, check3var_2))

    frame2.pack_forget()
    label3.pack()
    radio3_1.pack()
    radio3_2.pack()
    button3.pack()


# PART 4 : DEFINING WORKING ROWS

def pack_part4(frame3):
    frame4 = tk.Frame(window)
    frame4.pack()

    label4a = tk.Label(frame4, text="4a. Donnez les numéros des lignes utilisées",
                       font='Helvetica 16 bold')
    frame4a_1 = tk.Frame(frame4)
    label4a_1 = tk.Label(frame4a_1, text="Début (incluse) : ", font='Helvetica 10')
    entry4a_1 = tk.Entry(frame4a_1, bd=3)
    entry4a_1.insert(0, "0")
    frame4a_2 = tk.Frame(frame4)
    label4a_2 = tk.Label(frame4a_2, text="Fin (incluse) : ", font='Helvetica 10')
    entry4a_2 = tk.Entry(frame4a_2, bd=3)
    entry4a_2.insert(0, str(df.shape[0]))

    label4b = tk.Label(frame4, text="4b. Donnez les numéros des lignes utilisées pour les données agrégées par tranches de temps",
                       font='Helvetica 16 bold')
    frame4b_1 = tk.Frame(frame4)
    label4b_1 = tk.Label(frame4b_1, text="Début (incluse) : ", font='Helvetica 10')
    entry4b_1 = tk.Entry(frame4b_1, bd=3)
    entry4b_1.insert(0, "0")
    frame4b_2 = tk.Frame(frame4)
    label4b_2 = tk.Label(frame4b_2, text="Fin (incluse) : ", font='Helvetica 10')
    entry4b_2 = tk.Entry(frame4b_2, bd=3)
    entry4b_2.insert(0, str(df.shape[0]))

    label4c = tk.Label(frame4, text="4c. Donnez les numéros des lignes utilisées pour les données agrégées par tranches de vitesse",
                       font='Helvetica 16 bold')
    frame4c_1 = tk.Frame(frame4)
    label4c_1 = tk.Label(frame4c_1, text="Début (incluse) : ", font='Helvetica 10')
    entry4c_1 = tk.Entry(frame4c_1, bd=3)
    entry4c_1.insert(0, "0")
    frame4c_2 = tk.Frame(frame4)
    label4c_2 = tk.Label(frame4c_2, text="Fin (incluse) : ", font='Helvetica 10')
    entry4c_2 = tk.Entry(frame4c_2, bd=3)
    entry4c_2.insert(0, str(df.shape[0]))

    button4 = tk.Button(frame4, text="valider",
                        command=lambda: set_working_rows(frame4, entry4a_1, entry4a_2, entry4b_1, entry4b_2, entry4c_1, entry4c_2))

    frame3.pack_forget()
    if data_types[0]:
        label4a.pack()
        frame4a_1.pack()
        label4a_1.pack(side=tk.LEFT)
        entry4a_1.pack(side=tk.RIGHT)
        frame4a_2.pack()
        label4a_2.pack(side=tk.LEFT)
        entry4a_2.pack(side=tk.RIGHT)
    if data_types[1]:
        label4b.pack()
        frame4b_1.pack()
        label4b_1.pack(side=tk.LEFT)
        entry4b_1.pack(side=tk.RIGHT)
        frame4b_2.pack()
        label4b_2.pack(side=tk.LEFT)
        entry4b_2.pack(side=tk.RIGHT)
    if data_types[2]:
        label4c.pack()
        frame4c_1.pack()
        label4c_1.pack(side=tk.LEFT)
        entry4c_1.pack(side=tk.RIGHT)
        frame4c_2.pack()
        label4c_2.pack(side=tk.LEFT)
        entry4c_2.pack(side=tk.RIGHT)
    button4.pack()


# PART 5 : DEFINING DATE/HOUR AND/OR SPEED COLUMNS (AGGREGATED ONLY)

def pack_part5(frame4):
    frame5 = tk.Frame(window)
    frame5.pack()

    label5a = tk.Label(frame5, text="5a. Donnez les numéros des colonnes contenant les valeurs de date et d'heure",
                       font='Helvetica 16 bold')
    frame5a_1 = tk.Frame(frame5)
    label5a_1 = tk.Label(frame5a_1, text="Colonne de dates : ", font='Helvetica 10')
    entry5a_1 = tk.Entry(frame5a_1, bd=2)
    frame5a_2 = tk.Frame(frame5)
    label5a_2 = tk.Label(frame5a_2, text="Colonne d'heures : ", font='Helvetica 10')
    entry5a_2 = tk.Entry(frame5a_2, bd=2)

    label5b = tk.Label(frame5, text="5b. Donnez le numéro de la colonne contenant les valeurs de tranches de vitesse",
                       font='Helvetica 16 bold')
    entry5b = tk.Entry(frame5, bd=2)

    button5 = tk.Button(frame5, text="valider", command= lambda: set_label_columns(frame5, entry5a_1, entry5a_2, entry5b))

    frame4.pack_forget()
    if data_types[0]:
        set_label_columns(frame5, entry5a_1, entry5a_2, entry5b)
        return
    if data_types[1]:
        label5a.pack()
        frame5a_1.pack()
        label5a_1.pack(side=tk.LEFT)
        entry5a_1.pack(side=tk.RIGHT)
        frame5a_2.pack()
        label5a_2.pack(side=tk.LEFT)
        entry5a_2.pack(side=tk.RIGHT)
    if data_types[2]:
        label5b.pack()
        entry5b.pack()
    button5.pack()


# PART 6 : DEFINING USED COLUMNS

def pack_part6(frame5):
    frame6 = tk.Frame(window)
    frame6.pack()

    label6 = tk.Label(frame6,
                      text="6. Donnez les numéros des colonnes suivantes (laissez vide si colonne pas présente)",
                      font='Helvetica 16 bold')
    frame6_1 = tk.Frame(frame6)
    label6_1 = tk.Label(frame6_1, text="Vitesse : ", font='Helvetica 10')
    entry6_1 = tk.Entry(frame6_1, bd=2)
    frame6_2 = tk.Frame(frame6)
    label6_2 = tk.Label(frame6_2, text="Bruit : ", font='Helvetica 10')
    entry6_2 = tk.Entry(frame6_2, bd=2)

    label6a = tk.Label(frame6,
                       text="6a. Donnez les numéros des colonnes suivantes - données agrégées par heure (laissez vide si colonne pas présente)",
                       font='Helvetica 16 bold')
    frame6a_1 = tk.Frame(frame6)
    label6a_1 = tk.Label(frame6a_1, text="Nb de passages : ", font='Helvetica 10')
    entry6a_1 = tk.Entry(frame6a_1, bd=2)
    frame6a_2 = tk.Frame(frame6)
    label6a_2 = tk.Label(frame6a_2, text="Vmoyenne : ", font='Helvetica 10')
    entry6a_2 = tk.Entry(frame6a_2, bd=2)
    frame6a_3 = tk.Frame(frame6)
    label6a_3 = tk.Label(frame6a_3, text="Vmax : ", font='Helvetica 10')
    entry6a_3 = tk.Entry(frame6a_3, bd=2)
    frame6a_4 = tk.Frame(frame6)
    label6a_4 = tk.Label(frame6a_4, text="V85 : ", font='Helvetica 10')
    entry6a_4 = tk.Entry(frame6a_4, bd=2)
    frame6a_5 = tk.Frame(frame6)
    label6a_5 = tk.Label(frame6a_5, text="V50 : ", font='Helvetica 10')
    entry6a_5 = tk.Entry(frame6a_5, bd=2)
    frame6a_6 = tk.Frame(frame6)
    label6a_6 = tk.Label(frame6a_6, text="V30 : ", font='Helvetica 10')
    entry6a_6 = tk.Entry(frame6a_6, bd=2)
    frame6a_7 = tk.Frame(frame6)
    label6a_7 = tk.Label(frame6a_7, text="V10 : ", font='Helvetica 10')
    entry6a_7 = tk.Entry(frame6a_7, bd=2)

    label6b = tk.Label(frame6,
                       text="6b. Donnez les numéros des colonnes suivantes - données agrégées par vitesse (laissez vide si colonne pas présente)",
                       font='Helvetica 16 bold')
    frame6b_1 = tk.Frame(frame6)
    label6b_1 = tk.Label(frame6b_1, text="Nb de passages : ", font='Helvetica 10')
    entry6b_1 = tk.Entry(frame6b_1, bd=2)

    button6 = tk.Button(frame6, text="valider", command= lambda: set_data_columns(frame6, entry6_1, entry6a_1,
                                                                                  entry6a_2, entry6a_3, entry6a_4,
                                                                                  entry6a_5, entry6a_6, entry6a_7,
                                                                                  entry6b_1, entry6_2))

    frame5.pack_forget()
    if data_types[0]:
        for packing in [label6, frame6_1, label6_1, entry6_1, frame6_2, label6_2, entry6_2]:
            if type(packing) == tk.Frame or packing == label6:
                packing.pack()
            elif type(packing) == tk.Label:
                packing.pack(side=tk.LEFT)
            elif type(packing) == tk.Entry:
                packing.pack(side=tk.RIGHT)
    else:
        if data_types[1]:
            for packing in [label6a, frame6a_1, label6a_1, entry6a_1, frame6a_2, label6a_2, entry6a_2, frame6a_3,
                            label6a_3, entry6a_3, frame6a_4, label6a_4, entry6a_4, frame6a_5, label6a_5, entry6a_5,
                            frame6a_6, label6a_6, entry6a_6, frame6a_7, label6a_7, entry6a_7]:
                if type(packing) == tk.Frame or packing == label6a:
                    packing.pack()
                elif type(packing) == tk.Label:
                    packing.pack(side=tk.LEFT)
                elif type(packing) == tk.Entry:
                    packing.pack(side=tk.RIGHT)
        if data_types[2]:
            for packing in [label6b, frame6b_1, label6b_1, entry6b_1]:
                if type(packing) == tk.Frame or packing == label6b:
                    packing.pack()
                elif type(packing) == tk.Label:
                    packing.pack(side=tk.LEFT)
                elif type(packing) == tk.Entry:
                    packing.pack(side=tk.RIGHT)
    button6.pack()


# PART 7 : DEFINING LOCATION

def pack_part7(frame6):
    frame7 = tk.Frame(window)
    frame7.pack()

    def set_marker(coords):
        map7.delete_all_marker()
        map7.set_marker(coords[0], coords[1], text="Localisation du comptage")
        set_location(coords)

    label7 = tk.Label(frame6, text="7. Cliquez sur la localisation exacte du comptage", font='Helvetica 16 bold')
    map7 = tkmv.TkinterMapView(frame7, width=800, height=600)
    map7.set_position(46.521934, 6.626156)  # Lausanne, Switzerland
    map7.set_zoom(8)
    map7.add_left_click_map_command(set_marker)

    button7 = tk.Button(frame7, text="valider", command= lambda: end_input(frame7))

    frame6.pack_forget()
    label7.pack()
    map7.pack()
    button7.pack()

