__author__ = 'Ethan'
from tkinter import *
from tkinter import ttk
from Main import current_scale

def next_scale(*args):
    current_scale.append(current_scale[0].get_next_scale())
    del current_scale[0]
    scale_flat.set(current_scale[0].display_notes_flat())
    scale_sharp.set(current_scale[0].display_notes_sharp())
    string_ints = map(str, current_scale[0].intervals)
    ints.set('  '.join(string_ints))


root = Tk()
root.title("Feet to Meters")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

scale_flat = StringVar()
scale_sharp = StringVar()
ints = StringVar()

ttk.Button(mainframe, text="Next Scale", command=next_scale).grid(column=0, row=0, sticky=W)
ttk.Label(mainframe, textvariable=scale_flat).grid(column=0, row=1, sticky=(W, E))
ttk.Label(mainframe, textvariable=scale_sharp).grid(column=0, row=2, sticky=(W, E))
ttk.Label(mainframe, text="Intervals:").grid(column=0, row=3, sticky=(S))
ttk.Label(mainframe, textvariable=ints).grid(column=0, row=4, sticky=(W, E))


for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.bind('<Return>', next_scale)

root.mainloop()