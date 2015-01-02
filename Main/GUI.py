__author__ = 'Ethan'
from tkinter import *
from tkinter import ttk
import Main


root = Tk()
root.title("Feet to Meters")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()

ttk.Label(mainframe, textvariable=meters).grid(column=0, row=1, sticky=(W, E))
ttk.Button(mainframe, text="Next Scale", command=Main.next_scale()).grid(column=0, row=0, sticky=W)

ttk.Label(mainframe, text=Main.current_scale[0].display_notes_flat()).grid(column=0, row=1, sticky=N)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.bind('<Return>', Main.next_scale)

root.mainloop()