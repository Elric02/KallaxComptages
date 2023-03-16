import tkinter as tk

# INPUT

def launch_input():
    root.withdraw()
    input_window = tk.Toplevel(root)
    input_window.title("KallaxComptages - input")
    import input
    input.begin(input_window, root)

def receive_input(datadict, input_window, root):
    root.deiconify()
    print(datadict)
    input_window.destroy()


# MAIN

if __name__ == "__main__":
    root = tk.Tk()
    root.title("KallaxComptages - main")

    button_input = tk.Button(root, text="Importer un fichier", command=launch_input)
    button_input.pack()

    button_quit = tk.Button(root, text="Quitter", command=root.destroy)
    button_quit.pack()

    tk.mainloop()
