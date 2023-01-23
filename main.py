from tkinter import *
from tkinter import colorchooser
import tkinter.filedialog
import PIL
from PIL import Image, ImageDraw
from tkinter.ttk import *
import time
import backend as bd


root = Tk()
root.title('Loading')
root.geometry('300x100')
root.iconbitmap("./assets/logo.ico")

label = Label(root, text = "Copyright © YTP Studio")
label.pack()

pb1 = Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')
pb1.pack(expand=True)

def progress():
    for i in range(5):
        root.update_idletasks()
        pb1['value'] += 20
        time.sleep(0.2)
    root.destroy()
    main()


def main():
    
    bd.Paint()
    

Button(root, text='Start Painting', command=progress).pack()

root.mainloop()
