import tkinter as tk

def key_press(evt):
    print(evt)

root = tk.Tk()
root.bind("<Key>", key_press)
root.mainloop()