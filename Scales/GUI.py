__author__ = 'Ethan'
from tkinter import *
from tkinter import ttk


def next_scale(*args):
    current_scale = current_scale.g
    return current_scale


root = Tk()
root.title("Feet to Meters")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()

ttk.Label(mainframe, textvariable=meters).grid(column=0, row=1, sticky=(W, E))
ttk.Button(mainframe, text="Next Scale", command=next_scale).grid(column=0, row=0, sticky=W)

ttk.Label(mainframe, text="Scale notes").grid(column=0, row=1, sticky=N)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.bind('<Return>', next_scale)

root.mainloop()