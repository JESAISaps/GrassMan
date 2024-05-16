#!/usr/bin/env python3

from tkinter import *
from tkscrolledframe import ScrolledFrame

# Create a root window
root = Tk()

# Create a ScrolledFrame widget
sf = ScrolledFrame(root, width=640, height=480)
sf.pack(side="top", expand=1, fill="both")

# Create a frame within the ScrolledFrame
inner_frame = sf.display_widget(Frame)

Button(inner_frame, text="fdddd").pack()


# Start Tk's event loop
root.mainloop()