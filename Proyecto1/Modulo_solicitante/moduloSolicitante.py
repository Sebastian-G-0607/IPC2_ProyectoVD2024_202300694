import importlib
import os
from tkinter import Button, Label, PhotoImage, Tk, Frame, filedialog, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
import xml.etree.ElementTree as et
from Artistas.Artista import Artista
from Solicitantes.Solicitante import Solicitante
from BBDD import BBDD

class Solicitante(Frame):

    def __init__(self, master=None, id=None):
        super().__init__(master, width=800, height=500)
        self.id = id
        self.master = master
        self.master.resizable(False, False)
        self.pack()
        self.create_widgets()

    def cerrarSesion(self):

        optn = messagebox.askokcancel(title="Salir", message="¿Desea cerrar sesión?")
        print(optn)
        if optn == True:
            self.master.destroy()
            LoginClass = getattr(importlib.import_module('Login.Login'), 'Login') 

            root = Tk()

            ancho_ventana = 700
            alto_ventana = 370

            x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
            y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2

            posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)

            root.geometry(posicion)

            root.wm_title("Login")

            login1 = LoginClass(root)

    def create_widgets(self):

        self.config(bg="white")

        self.CerrarSesion = Button(self, text="Cerrar sesión", font=Font(family="Roboto Cn", size=10), command=self.cerrarSesion)
        self.CerrarSesion.place(x=650, y=25, width=110, height=40)