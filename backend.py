from tkinter import *
from tkinter import colorchooser
import tkinter.filedialog
import PIL
from PIL import Image, ImageDraw

x1, y1 = None, None
actual_cursor = ''


class Paint(object):

    def __init__(self):
        # Attribut de la fenêtre
        self.window = Tk()
        self.window.geometry('600x600')
        self.window.title("Pygment")
        self.window.iconbitmap("./assets/logo.ico")
        self.window.resizable(0, 0)
        
        self.color = 'black'
        self.width_line = 1
        self.path = ""

        # Définition des boutons
        image = PhotoImage(file='./assets/crayon.gif')
        crayon_button = Button(self.window, image=image, relief=GROOVE, command=self.use_pen, cursor='hand2')

        image1 = PhotoImage(file='./assets/pinceau.gif')
        pinceau_button = Button(self.window, image=image1, relief=GROOVE, command=self.use_pen, cursor='hand2')

        image2 = PhotoImage(file='./assets/gomme.gif')
        gomme_button = Button(self.window, image=image2, relief=GROOVE, command=self.use_erase, cursor='hand2')

        image3 = PhotoImage(file='./assets/couleur.gif')
        couleur_button = Button(self.window, image=image3, borderwidth='2', cursor='hand2', command=self.color_choose)

        self.var = DoubleVar()
        scale = Scale(self.window, orient='horizontal', from_=1, to=20, resolution=1, length=200, cursor='hand2',
                      command=self.update, variable=self.var)
        self.scale = scale

        # Mettre les boutons sur la grille
        crayon_button.grid(row=0, column=0)
        pinceau_button.grid(row=0, column=1)
        gomme_button.grid(row=0, column=2)
        couleur_button.grid(row=0, column=3)
        scale.grid(row=0, column=4)

        # Définition d'un menu
        menu_bar = Menu(self.window)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command = self.save)
        file_menu.add_command(label="Save as...", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit")

        menu_bar.add_cascade(label="Fichier", menu=file_menu)

        # Canvas
        self.canvas = Canvas(self.window, bg='white', width=600,
                             height=600, cursor='crosshair')

        self.canvas.grid(row=1, columnspan=5, )

        self.image = Image.new('RGB', (600, 600), 'white')
        self.dessin = ImageDraw.Draw(self.image)
        self.canvas.bind('<1>', self.activate_paint)

        self.canvas.update_idletasks()
        self.window.config(menu=menu_bar)

        self.window.mainloop()
        
        
        
        
    def activate_paint(self, e):
        global x1, y1
        self.canvas.bind('<B1-Motion>', self.paint)
        x1, y1 = e.x, e.y

    def paint(self, e):
        global x1, y1
        x, y = e.x, e.y
        # cette fonction dessine le trait#
        self.canvas.create_line((x1, y1, x, y), fill=self.color, capstyle='round', width=self.width_line)
        self.dessin.line((x1, y1, x, y), fill=self.color, joint='curve', width=self.width_line)

        if self.width_line > 2:
            offset = (self.width_line - 1) / 2
            self.dessin.ellipse((x - offset, y - offset, x1 + offset, y1 + offset), fill=self.color)

        x1, y1 = x, y

    def use_pen(self):
        self.color = 'black'
        self.width_line = self.scale.get()

    def save_as(self):
        types = [("PNG", ".png"), ("JPG", ".jpg"), ("GIF", ".gif"), ("Autres types", ".*")]
        self.path = tkinter.filedialog.asksaveasfilename(title="Enregistrer sous ...", filetypes=types,
                                                    defaultextension=".png", initialfile="Sans nom")


        if not self.path == "":
            self.image.save(self.path)
    
    def save(self) :
        if self.path == "" :
            
            self.save_as()
     
        else :
            self.image.save(self.path)
        

    def use_erase(self):
        self.color = 'white'
        self.width_line = self.scale.get()

    def scale_get(self):
        self.scale.get()

    def update(self, var):
        if self.color == 'white':
            self.use_erase()

        else:
            self.use_pen()

    def color_choose(self):
        colorcode = colorchooser.askcolor(title="Choose color")
        self.color = colorcode[1]

    def open_file(self):
        path = tkinter.filedialog.askopenfilename(title="Ouvrir...", defaultextension=".png")

        if not path == "":
            photo = PhotoImage(file=path)
            self.canvas.create_image(300, 300, image=photo)

            for x in range(self.canvas.winfo_width()):
                for y in range(self.canvas.winfo_height()):
                    self.dessin.point([x, y], fill=photo.get(x, y))

            self.window.mainloop()
