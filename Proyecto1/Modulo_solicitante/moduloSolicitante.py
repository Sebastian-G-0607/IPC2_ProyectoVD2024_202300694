import importlib
from tkinter import Button, Tk, Frame, messagebox
from tkinter.font import Font
from Modulo_solicitante.solicitar import Solicitante_solicitar
from BBDD import BBDD
from Modulo_solicitante.galeria import Solicitante_galeria


class Solicitante(Frame):

    def __init__(self, master=None, id=None):
        super().__init__(master, width=600, height=200)
        self.id = id
        self.master = master
        self.master.resizable(False, False)
        self.pack()
        self.create_widgets()

    def cerrarSesion(self):

        optn = messagebox.askokcancel(title="Salir", message="¿Desea cerrar sesión?")
        print(optn)
        if optn == True:
            BBDD.usuario_en_sesion = ''
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

            login = LoginClass(root)

    def solicitar(self):
        self.master.destroy()

        root = Tk()

        ancho_ventana = 800
        alto_ventana = 500

        x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)

        root.geometry(posicion)

        root.wm_title("Solicitante " + BBDD.usuario_en_sesion + " - Solicitar")
        app = Solicitante_solicitar(root)

    def ver_galeria(self):
        if len(BBDD.listaSolicitantes.buscar(BBDD.usuario_en_sesion).galeria) == 0:
            messagebox.showerror(title="Error", message="No existen imágenes en la galería, inténtelo más tarde")
        else:
            self.master.destroy()

            root = Tk()

            ancho_ventana = 800
            alto_ventana = 500

            x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
            y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2

            posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)

            root.geometry(posicion)

            root.wm_title("Solicitante " + BBDD.usuario_en_sesion + " - Ver galería")
            app = Solicitante_galeria(root)

    def create_widgets(self):

        self.config(bg="white")

        self.CerrarSesion = Button(self, text="Cerrar sesión", font=Font(family="Roboto Cn", size=10), command=self.cerrarSesion)
        self.CerrarSesion.place(x=490, y=20, width=90, height=30)

        self.solicitar = Button(self, text="Solicitar imágenes", font=Font(family="Roboto Cn", size=10), command=self.solicitar)
        self.solicitar.place(x=170, y=70, width=120, height=40)

        self.galeria = Button(self, text="Ver galería", font=Font(family="Roboto Cn", size=10), command=self.ver_galeria)
        self.galeria.place(x=320, y=70, width=110, height=40)
