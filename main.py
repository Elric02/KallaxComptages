import tkinter as tk
import pandas as pd


# INPUT

# These variables are used in the input.py parts 5 and 6 option menus and then considered as None in database.py
optionmenu_with_other_date = 'Déjà présent dans "Date"'
optionmenu_with_other_begin = 'Déjà présent dans "Début"'
optionmenu_with_none = 'Pas de valeur'

def launch_input():
    root.withdraw()
    input_window = tk.Toplevel(root)
    input_window.title("KallaxComptages - input")
    import input
    input.begin(input_window, root)

def receive_input(datadict, input_window, root):
    root.deiconify()
    input_window.destroy()
    send_data(datadict, root)


# DATABASE

def send_data(datadict, root):
    root.withdraw()
    database_window = tk.Toplevel(root)
    database_window.title("KallaxComptages - database")
    db_frame = tk.Frame(database_window)
    db_frame.pack()
    db_label = tk.Label(db_frame, text="Envoi des données dans la base de données...", font='Helvetica 16 bold')
    db_label.pack()
    import database
    database.insert_db(datadict)


# MAIN

if __name__ == "__main__":
    root = tk.Tk()
    root.title("KallaxComptages - main")

    button_input = tk.Button(root, text="Importer un fichier", command=launch_input)
    button_input.pack()

    button_quit = tk.Button(root, text="Quitter", command=root.destroy)
    button_quit.pack()

    tk.mainloop()
