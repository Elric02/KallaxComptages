import tkinter as tk

import main


window = None
root = None


# BEGIN AND END FUNCTION

# First executed function, initiates the whole process
def begin(newWindow, rootDef):
    # redefine current window and root window with the correct ones
    global window, root
    window = newWindow
    root = rootDef
    print("Starting select process...")

    # add content to the current window
    mainframe = tk.Frame(window)
    mainframe.pack()

    mainlabel = tk.Label(mainframe, text="Sélection de données", font='Helvetica 16 bold')
    templabel = tk.Label(mainframe, text="En cours d'implémentation...", font='Helvetica 12')
    analyzebutton = tk.Button(mainframe, text="Analyser", command= lambda: end_select(mainframe))

    mainlabel.pack()
    templabel.pack()
    analyzebutton.pack()

# Function to end the select process
def end_select(mainframe):
    mainframe.pack_forget()
    print("All necessary information gathered, processing to analyze...")
    main.receive_select(window, root)