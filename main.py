import tkinter as tk


def launch_input():
    print("AAA")
    root.withdraw()
    input_window = tk.Toplevel(root)
    import input
    input.main(input_window)

'''
class Buttons:

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.b1 = tk.Button(self.master, text="Button1", command=self.display)
        self.b2 = tk.Button(self.master, text="Button2", command=self.new_window)
        self.b1.pack()
        self.b2.pack()
        self.frame.pack()

    def display(self):
        print
        'Hello Button1'

    def new_window(self):
        self.master.withdraw()
        self.newWindow = tk.Toplevel(self.master)
        bb = Buttons1(self.newWindow)


class Buttons1():

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.b3 = tk.Button(self.master, text="Button3", command=self.display3)
        self.b3.pack()
        self.frame.pack()

    def display3(self):
        print
        'hello button3'
'''

# Tkinter execution
root = tk.Tk()
button_input = tk.Button(root, text="Importer un fichier", command=launch_input)
button_input.pack()
tk.mainloop()
