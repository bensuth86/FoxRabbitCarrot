import tkinter as tk
import time

root=tk.Tk()

variable=tk.StringVar()

def update_label():
        
        i=0
        while 1:
                i=i+1
                variable.set(str(i))
                root.update()

your_label=tk.Label(root,textvariable=variable)
your_label.pack()

update_label()

root.mainloop()
