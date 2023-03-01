import tkinter as tk
from tkinter import filedialog as fd

window = tk.Tk()


# DATA SPECIFICATION

file = None
filetype = ''
working_element = ''
data_types = [False, False, False] # raw, speed-aggregated, time-aggregated
date_hour_columns = [0, 0]
speed_column = 0


# FUNCTIONS DEFINING DATA SPECIFICATIONS

# Function to open file and set file type
def choose_file(_):
    loc = fd.askopenfilename(filetypes=(("fichier XLSX ou CSV", ["*.xlsx", "*.csv"]),))
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
        print("Speed column set to :", speed_column)
    print("Proceeding to part 5")
    pack_part5()


# PART 1 : CHOOSING FILE

frame1 = tk.Frame(window)
label1 = tk.Label(frame1, text="1. Choisissez votre fichier d'entrée", font='Helvetica 16 bold')
label1.pack()
button1 = tk.Button(frame1, text="choisir")
button1.pack()
button1.bind("<Button-1>", choose_file)
frame1.pack()


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

label4a = tk.Label(frame4, text="4a. Donnez les colonnes contenant les valeurs de date et d'heure (en chiffres)", font='Helvetica 16 bold')
frame4a_1 = tk.Frame(frame4)
label4a_1 = tk.Label(frame4a_1, text="Colonne de dates : ", font='Helvetica 10')
entry4a_1 = tk.Entry(frame4a_1, bd=2)
frame4a_2 = tk.Frame(frame4)
label4a_2 = tk.Label(frame4a_2, text="Colonne d'heures : ", font='Helvetica 10')
entry4a_2 = tk.Entry(frame4a_2, bd=2)

label4b = tk.Label(frame4, text="4b. Donnez la colonne contenant les valeurs de tranches de vitesse (en chiffres)", font='Helvetica 16 bold')
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

# TODO : UI : champs pour numéro colonne V85, V50 etc, numéro colonne nombre de véhicules etc..., bouton valider (changer ces champs si données brutes)

frame5 = tk.Frame(window)
frame5.pack()

# TODO : here

def pack_part5():
    frame4.pack_forget()


# Tkinter execution

tk.mainloop()
