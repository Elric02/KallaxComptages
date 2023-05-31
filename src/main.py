# TODO : type de véhicule pour agrégés (time et speed), vider la db, commentaires, documentation dev

import tkinter as tk


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

def abort_input(input_window, root):
    root.deiconify()
    input_window.destroy()

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
    db_label = tk.Label(db_frame, text="Données ajoutées à la base de données !", font='Helvetica 16 bold')
    back_button = tk.Button(db_frame, text="Retour au menu", cursor="hand2", command=lambda: end_data(db_frame, database_window, root))
    db_label.pack()
    back_button.pack()
    import database
    database.insert_db(datadict)

def end_data(db_frame, database_window, root):
    db_frame.pack_forget()
    root.deiconify()
    database_window.destroy()


# SELECT

def launch_select():
    root.withdraw()
    select_window = tk.Toplevel(root)
    select_window.title("KallaxComptages - select")
    import select
    select.begin(select_window, root)

def receive_select(select_window, root):
    root.deiconify()
    select_window.destroy()
    start_analyze(root)


# ANALYZE

def start_analyze(root):
    root.withdraw()
    analyze_window = tk.Toplevel(root)
    analyze_window.title("KallaxComptages - analyze")
    analyze_frame = tk.Frame(analyze_window)
    analyze_frame.pack()
    analyze_label = tk.Label(analyze_frame, text="Analyse des données sélectionnées", font='Helvetica 16 bold')
    back_button = tk.Button(analyze_frame, text="Retour au menu", cursor="hand2", command=lambda: end_analyze(analyze_frame, analyze_window, root))
    analyze_label.pack()
    back_button.pack()
    import analyze
    analyze.launch()

def end_analyze(analyze_frame, analyze_window, root):
    analyze_frame.pack_forget()
    root.deiconify()
    analyze_window.destroy()


# OTHERS

def empty_database():
    print("TODO")


# MAIN

def pack_main(root):
    root_label = tk.Label(root, text="KallaxComptages", font='Helvetica 24 bold')
    root_label.pack()

    button_input = tk.Button(root, text="Importer un fichier", cursor="hand2", command=launch_input)
    button_input.pack()

    button_input = tk.Button(root, text="Sélectionner des données à analyser", cursor="hand2", command=launch_select)
    button_input.pack()

    button_empty = tk.Button(root, text="Vider la base de données", cursor="hand2", command=empty_database)
    button_empty.pack()

    button_quit = tk.Button(root, text="Quitter", cursor="hand2", command=root.destroy)
    button_quit.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("KallaxComptages - main")

    pack_main(root)

    tk.mainloop()
