__author__ = 'Ethan'
from tkinter import *
from tkinter import ttk
import Main

def next_scale(*args):
    Main.current_scale.append(Main.current_scale[0].get_next_scale())
    del Main.current_scale[0]
    scale_flat.set(Main.current_scale[0].display_notes_flat())
    scale_sharp.set(Main.current_scale[0].display_notes_sharp())


root = Tk()
root.title("Feet to Meters")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

feet = StringVar()
scale_flat = StringVar()
scale_sharp = StringVar()

ttk.Button(mainframe, text="Next Scale", command=next_scale).grid(column=0, row=0, sticky=W)
ttk.Label(mainframe, textvariable=scale_flat).grid(column=0, row=1, sticky=(W, E))
ttk.Label(mainframe, textvariable=scale_sharp).grid(column=0, row=2, sticky=(W, E))


for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.bind('<Return>', next_scale)

root.mainloop()