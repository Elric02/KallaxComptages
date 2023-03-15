# TODO : renommer ce fichier en input.py ? et faire un autre fichier central main.py qui lance les différentes procédures
# TODO : ajouter champs pour préciser les lignes intéressantes des fichiers ? ou le faire automatiquement (et demander éventuellement une confirmaton de l'user)
# TODO : suite du travail : enregistrer le tout dans une base de données (probablement nouveau fichier .py pour faire ça)


import tkinter as tk
from tkinter import filedialog as tk_fd
import tkintermapview as tkmv


# WINDOWS AND FRAMES

window = None


# DATA SPECIFICATION

file = None
filetype = ''
working_element = ''
data_types = [False, False, False] # raw, speed-aggregated, time-aggregated
date_hour_columns = [0, 0]
speed_column = 0
data_columns = [[], [], []]
location = [0, 0]


# MAIN FUNCTION STARTING THE PROCESS

def main(newWindow):
    global window
    window = newWindow
    # PAS POSSIBLE DE CHANGER LE PARENT, FAUT REWORK LE RESTE DU CODE ET ENCAPSULER DANS DES FONCTIONS
    print(frame1.winfo_parent())
    print(frame1.master)
    pack_part1()


# FUNCTIONS DEFINING DATA SPECIFICATIONS

# Function to open file and set file type
def choose_file(_):
    loc = tk_fd.askopenfilename(filetypes=(("fichier XLSX ou CSV", ["*.xlsx", "*.csv"]),))
    global filetype
    filetype = loc[loc.rindex('.'):]
    print("Importing", filetype, "located at", loc)
    pack_part2()
    global file
    file = open(loc, 'r')
    file.close()


# Function to set working element (separator or working sheet)
def set_working_element(_):
    global working_element
    if filetype == ".xlsx":
        if entry2a.get() == "":
            return
        else:
            working_element = entry2a.get()
    else:
        if entry2b.get() == "":
            return
        else:
            working_element = entry2b.get()
    print("Working element set as", working_element)
    pack_part3()


# Function to set data type(s)
def set_data_types(_):
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
    print("Data types set as... raw:", data_types[0], ", speed-aggregated:", data_types[1], ", time-aggregated:", data_types[2])
    pack_part4()


# Function to set date/hour and/or speed columns
def set_label_columns(_):
    global date_hour_columns
    global speed_column
    if data_types[1]:
        date_hour_columns = [entry4a_1.get(), entry4a_2.get()]
        print("Date and hour columns set to :", *date_hour_columns)
    if data_types[2]:
        speed_column = entry4b.get()
        print("Speed column set to:", speed_column)
    print("Proceeding to part 5")
    pack_part5()


# Function to set actual data columns
def set_data_columns(_):
    global data_columns
    if data_types[0]:
        data_columns[0] = [entry5_1.get(), entry5_2.get()]
    else:
        if data_types[1]:
            data_columns[1] = [entry5a_1.get(), entry5a_2.get(), entry5a_3.get(), entry5a_4.get(), entry5a_5.get(), entry5a_6.get(), entry5a_7.get()]
        if data_types[2]:
            data_columns[2] = [entry5b_1.get()]
    print("Data received, proceeding to part 6")
    pack_part6()


# Function to set geolocation coordinates
def set_location(coords):
    global location
    location = coords
    print("Location set to :", location)


# Function to end the input process
def end_input(_):
    frame6.pack_forget()
    print("All necessary information gathered !")
    # TODO : lancer la suite depuis ici


# PART 1 : CHOOSING FILE

frame1 = tk.Frame()
frame1.pack()

label1 = tk.Label(frame1, text="1. Choisissez votre fichier d'entrée", font='Helvetica 16 bold')
button1 = tk.Button(frame1, text="choisir")
button1.bind("<Button-1>", choose_file)

def pack_part1():
    label1.pack()
    button1.pack()


# PART 2 : DEFINING SEPARATORS/SHEET

frame2 = tk.Frame(window)
frame2.pack()

label2a = tk.Label(frame2, text="2. Définissez la feuille à utiliser (par exemple feuille1)", font='Helvetica 16 bold')
entry2a = tk.Entry(frame2, bd=5)

label2b = tk.Label(frame2, text="2. Définissez le séparateur de colonnes (par exemple ;)", font='Helvetica 16 bold')
entry2b = tk.Entry(frame2, bd=5)

button2 = tk.Button(frame2, text="valider")
button2.bind("<Button-1>", set_working_element)

def pack_part2():
    if filetype == ".xlsx":
        label2a.pack()
        entry2a.pack()
    else:
        label2b.pack()
        entry2b.pack()
    frame1.pack_forget()
    button2.pack()


# PART 3 : DEFINING DATA TYPE

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
check3_1 = tk.Checkbutton(frame3, text="...par tranches d'heure", variable=check3var_1, onvalue=1, offvalue=0)
check3_2 = tk.Checkbutton(frame3, text="...par tranches de vitesse", variable=check3var_2, onvalue=1, offvalue=0)
button3 = tk.Button(frame3, text="valider")
button3.bind("<Button-1>", set_data_types)

def pack_part3():
    frame2.pack_forget()
    radio3_1.pack()
    radio3_2.pack()
    button3.pack()


# PART 4 : DEFINING DATE/HOUR AND/OR SPEED COLUMNS (AGGREGATED ONLY)

frame4 = tk.Frame(window)
frame4.pack()

label4a = tk.Label(frame4, text="4a. Donnez les numéros des colonnes contenant les valeurs de date et d'heure", font='Helvetica 16 bold')
frame4a_1 = tk.Frame(frame4)
label4a_1 = tk.Label(frame4a_1, text="Colonne de dates : ", font='Helvetica 10')
entry4a_1 = tk.Entry(frame4a_1, bd=2)
frame4a_2 = tk.Frame(frame4)
label4a_2 = tk.Label(frame4a_2, text="Colonne d'heures : ", font='Helvetica 10')
entry4a_2 = tk.Entry(frame4a_2, bd=2)

label4b = tk.Label(frame4, text="4b. Donnez le numéro de la colonne contenant les valeurs de tranches de vitesse", font='Helvetica 16 bold')
entry4b = tk.Entry(frame4, bd=2)

button4 = tk.Button(frame4, text="valider")
button4.bind("<Button-1>", set_label_columns)

def pack_part4():
    frame3.pack_forget()
    if data_types[0]:
        set_label_columns(None)
        return
    if data_types[1]:
        label4a.pack()
        frame4a_1.pack()
        label4a_1.pack(side=tk.LEFT)
        entry4a_1.pack(side=tk.RIGHT)
        frame4a_2.pack()
        label4a_2.pack(side=tk.LEFT)
        entry4a_2.pack(side=tk.RIGHT)
    if data_types[2]:
        label4b.pack()
        entry4b.pack()
    button4.pack()


# PART 5 : DEFINING USED COLUMNS

frame5 = tk.Frame(window)
frame5.pack()

label5 = tk.Label(frame5, text="5. Donnez les numéros des colonnes suivantes (laissez vide si colonne pas présente)", font='Helvetica 16 bold')
frame5_1 = tk.Frame(frame5)
label5_1 = tk.Label(frame5_1, text="Vitesse : ", font='Helvetica 10')
entry5_1 = tk.Entry(frame5_1, bd=2)
frame5_2 = tk.Frame(frame5)
label5_2 = tk.Label(frame5_2, text="Bruit : ", font='Helvetica 10')
entry5_2 = tk.Entry(frame5_2, bd=2)

label5a = tk.Label(frame5, text="5a. Donnez les numéros des colonnes suivantes - données agrégées par heure (laissez vide si colonne pas présente)", font='Helvetica 16 bold')
frame5a_1 = tk.Frame(frame5)
label5a_1 = tk.Label(frame5a_1, text="Nb de passages : ", font='Helvetica 10')
entry5a_1 = tk.Entry(frame5a_1, bd=2)
frame5a_2 = tk.Frame(frame5)
label5a_2 = tk.Label(frame5a_2, text="Vmoyenne : ", font='Helvetica 10')
entry5a_2 = tk.Entry(frame5a_2, bd=2)
frame5a_3 = tk.Frame(frame5)
label5a_3 = tk.Label(frame5a_3, text="Vmax : ", font='Helvetica 10')
entry5a_3 = tk.Entry(frame5a_3, bd=2)
frame5a_4 = tk.Frame(frame5)
label5a_4 = tk.Label(frame5a_4, text="V85 : ", font='Helvetica 10')
entry5a_4 = tk.Entry(frame5a_4, bd=2)
frame5a_5 = tk.Frame(frame5)
label5a_5 = tk.Label(frame5a_5, text="V50 : ", font='Helvetica 10')
entry5a_5 = tk.Entry(frame5a_5, bd=2)
frame5a_6 = tk.Frame(frame5)
label5a_6 = tk.Label(frame5a_6, text="V30 : ", font='Helvetica 10')
entry5a_6 = tk.Entry(frame5a_6, bd=2)
frame5a_7 = tk.Frame(frame5)
label5a_7 = tk.Label(frame5a_7, text="V10 : ", font='Helvetica 10')
entry5a_7 = tk.Entry(frame5a_7, bd=2)

label5b = tk.Label(frame5, text="5b. Donnez les numéros des colonnes suivantes - données agrégées par vitesse (laissez vide si colonne pas présente)", font='Helvetica 16 bold')
frame5b_1 = tk.Frame(frame5)
label5b_1 = tk.Label(frame5b_1, text="Nb de passages : ", font='Helvetica 10')
entry5b_1 = tk.Entry(frame5b_1, bd=2)

button5 = tk.Button(frame5, text="valider")
button5.bind("<Button-1>", set_data_columns)

def pack_part5():
    frame4.pack_forget()
    if data_types[0]:
        for packing in [label5, frame5_1, label5_1, entry5_1, frame5_2, label5_2, entry5_2]:
            if type(packing) == tk.Frame or packing == label5:
                packing.pack()
            elif type(packing) == tk.Label:
                packing.pack(side=tk.LEFT)
            elif type(packing) == tk.Entry:
                packing.pack(side=tk.RIGHT)
    else:
        if data_types[1]:
            for packing in [label5a, frame5a_1, label5a_1, entry5a_1, frame5a_2, label5a_2, entry5a_2, frame5a_3, label5a_3, entry5a_3, frame5a_4, label5a_4, entry5a_4, frame5a_5, label5a_5, entry5a_5, frame5a_6, label5a_6, entry5a_6, frame5a_7, label5a_7, entry5a_7]:
                if type(packing) == tk.Frame or packing == label5a:
                    packing.pack()
                elif type(packing) == tk.Label:
                    packing.pack(side=tk.LEFT)
                elif type(packing) == tk.Entry:
                    packing.pack(side=tk.RIGHT)
        if data_types[2]:
            for packing in [label5b, frame5b_1, label5b_1, entry5b_1]:
                if type(packing) == tk.Frame or packing == label5b:
                    packing.pack()
                elif type(packing) == tk.Label:
                    packing.pack(side=tk.LEFT)
                elif type(packing) == tk.Entry:
                    packing.pack(side=tk.RIGHT)
    button5.pack()


# PART 6 : DEFINING LOCATION

frame6 = tk.Frame(window)
frame6.pack()

def set_marker(coords):
    map6.delete_all_marker()
    map6.set_marker(coords[0], coords[1], text="Localisation du comptage")
    set_location(coords)

label6 = tk.Label(frame6, text="6. Cliquez sur la localisation exacte du comptage", font='Helvetica 16 bold')
map6 = tkmv.TkinterMapView(frame6, width=800, height=600)
map6.set_position(46.521934, 6.626156)  # Lausanne, Switzerland
map6.set_zoom(8)
map6.add_left_click_map_command(set_marker)

button6 = tk.Button(frame6, text="valider")
button6.bind("<Button-1>", end_input)

def pack_part6():
    frame5.pack_forget()
    label6.pack()
    map6.pack()
    button6.pack()

