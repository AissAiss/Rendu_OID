from tkinter import *

ws = Tk()
ws.title('PythonGuides')


img = PhotoImage(file='autoSave.png')
Label(
    ws,
    image=img
).pack()

ws.mainloop()