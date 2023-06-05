import tkinter as tk
import os
import shutil
import sqlite3


# INPUT

# These variables are used in the input.py parts 5 and 6 option menus and then considered as None in database.py
optionmenu_with_other_date = 'Déjà présent dans "Date"'
optionmenu_with_other_begin = 'Déjà présent dans "Début"'
optionmenu_with_none = 'Pas de valeur'

# Executed when pressing first button on main menu
def launch_input():
    # hide root window
    root.withdraw()
    # create new window for input process
    input_window = tk.Toplevel(root)
    input_window.title("KallaxComptages - input")
    # launch input process
    import input
    input.begin(input_window, root)

# Show back main menu after input process was cancelled
def abort_input(input_window, root):
    root.deiconify()
    input_window.destroy()

# Show back main menu (will be dismissed again right after) and proceed with database.py
def receive_input(datadict, input_window, root):
    root.deiconify()
    input_window.destroy()
    send_data(datadict, root)


# DATABASE

# Initiate database insert process
def send_data(datadict, root):
    # hide root window, create new window for database
    root.withdraw()
    database_window = tk.Toplevel(root)
    database_window.title("KallaxComptages - database")
    # add content which will be displayed after the completion of the database process
    db_frame = tk.Frame(database_window)
    db_frame.pack()
    db_label = tk.Label(db_frame, text="Données ajoutées à la base de données !", font='Helvetica 16 bold')
    back_button = tk.Button(db_frame, text="Retour au menu", cursor="hand2", command=lambda: end_data(db_frame, database_window, root))
    db_label.pack()
    back_button.pack()
    # launch database process
    import database
    database.insert_db(datadict)

# Show back main menu after database process is completed
def end_data(db_frame, database_window, root):
    db_frame.pack_forget()
    root.deiconify()
    database_window.destroy()


# SELECTION

# Executed when pressing second button on main menu
def launch_selection():
    # hide root window
    root.withdraw()
    # create new window for selection process
    selection_window = tk.Toplevel(root)
    selection_window.title("KallaxComptages - selection")
    # launch selection process
    import selection
    selection.begin(selection_window, root)

# Show back main menu (will be dismissed again right after) and proceed with analyze.py
def receive_selection(selection_window, root):
    root.deiconify()
    selection_window.destroy()
    start_analyze(root)


# ANALYZE

# Initiate analyze process
def start_analyze(root):
    # hide root window, create new window for analyze
    root.withdraw()
    analyze_window = tk.Toplevel(root)
    analyze_window.title("KallaxComptages - analyze")
    # add content which will be displayed after the completion of the analyze process
    analyze_frame = tk.Frame(analyze_window)
    analyze_frame.pack()
    analyze_label = tk.Label(analyze_frame, text="Analyse des données sélectionnées", font='Helvetica 16 bold')
    back_button = tk.Button(analyze_frame, text="Retour au menu", cursor="hand2", command=lambda: end_analyze(analyze_frame, analyze_window, root))
    analyze_label.pack()
    back_button.pack()
    # launch analyze process
    import analyze
    analyze.launch()

# Show back main menu after analyze process is completed
def end_analyze(analyze_frame, analyze_window, root):
    analyze_frame.pack_forget()
    root.deiconify()
    analyze_window.destroy()


# OTHERS

# Executed when pressing third button on main menu
def empty_database():
    # create confirmation window asking if user really wants to clear the db
    confirm_window = tk.Toplevel(root)
    confirm_frame = tk.Frame(confirm_window)
    confirm_frame.pack()

    # set content of the confirmation window
    label1 = tk.Label(confirm_frame, text="Confirmez-vous que vous voulez vider la base de données ? Cette opération est irréversible",
                      font='Helvetica 14 bold')
    button_yes = None
    button_no = None
    button_yes = tk.Button(confirm_frame, text="Oui, vider", cursor="hand2",
                           command=lambda: empty_database_confirmed(label1, button_yes, button_no))
    button_no = tk.Button(confirm_frame, text="Non, annuler", cursor="hand2",
                          command=lambda: confirm_window.destroy())

    label1.pack()
    button_yes.pack()
    button_no.pack()

# Actually clears the database, executed after user confirmation
def empty_database_confirmed(label1, button_yes, button_no):
    # if an additional empty database exists (should always be the case)
    if os.path.exists("db/database_empty.db"):
        # delete working database and replace it by a copy of the empty database
        os.remove("db/database.db")
        shutil.copyfile("db/database_empty.db", "db/database.db")
        # change confirmation window text to tell user that the operation was successful
        label1.config(text="Base de données vidée avec succès.")
        button_no.config(text="OK")
        button_yes.pack_forget()
        print("Database successfully cleared by replacing working file with empty file")
    # proceed differently (deleting with SQL) in case the empty database has been mistakenly deleted or moved
    else:
        # connect to working database
        con = sqlite3.connect('db/database.db')
        cur = con.cursor()
        # prepare delete statements for each table
        for table in ["Source", "Entry", "AggregatedSpeed", "AggregatedTime", "Unique"]:
            cur.execute('DELETE FROM "' + table + '";')
        # run statements
        con.commit()
        con.close()
        # change confirmation window text to tell user that the operation was successful
        label1.config(text="Base de données vidée avec succès.")
        button_no.config(text="OK")
        button_yes.pack_forget()
        print("Database successfully cleared by executing DELETE commands")


# MAIN

# display stuff on the root window (main window)
def pack_main(root):
    # main title
    root_label = tk.Label(root, text="KallaxComptages", font='Helvetica 24 bold')
    root_label.pack()

    # first button, launches input process
    button_input = tk.Button(root, text="Importer un fichier", cursor="hand2", command=launch_input)
    button_input.pack()

    # second button, launches selection process
    button_input = tk.Button(root, text="Sélectionner des données à analyser", cursor="hand2", command=launch_selection)
    button_input.pack()

    # third button, creates confirmation window to empty database
    button_empty = tk.Button(root, text="Vider la base de données", cursor="hand2", command=empty_database)
    button_empty.pack()

    # fourth button, quits the application
    button_quit = tk.Button(root, text="Quitter", cursor="hand2", command=root.destroy)
    button_quit.pack()

# What is executed when the program starts
if __name__ == "__main__":
    # create root window (main window)
    root = tk.Tk()
    root.title("KallaxComptages - main")

    pack_main(root)

    # run Tkinter
    tk.mainloop()
