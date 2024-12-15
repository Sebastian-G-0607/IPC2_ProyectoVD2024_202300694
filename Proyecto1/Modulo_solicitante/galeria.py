import importlib
from tkinter import Button, Label, Tk, Frame, messagebox
from tkinter.font import Font
from BBDD import BBDD

class Solicitante_galeria(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=800, height=500)
        self.master = master
        self.master.resizable(False, False)
        self.pack()
        self.create_widgets()

    def cerrarSesion(self):

        optn = messagebox.askokcancel(title="Salir", message="¿Desea cerrar sesión?")
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
        SolicitarClass = getattr(importlib.import_module('Modulo_solicitante.solicitar'), 'Solicitante_solicitar') 

        root = Tk()

        ancho_ventana = 800
        alto_ventana = 500

        x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)

        root.geometry(posicion)

        root.wm_title("Solicitante " + BBDD.usuario_en_sesion + " - Solicitar")
        app = SolicitarClass(root)

    def create_widgets(self):

        self.config(bg="white")

        self.CerrarSesion = Button(self, text="Cerrar sesión", font=Font(family="Roboto Cn", size=10), command=self.cerrarSesion)
        self.CerrarSesion.place(x=650, y=25, width=90, height=30)

        self.solicitar = Button(self, text="Solicitar", font=Font(family="Roboto Cn", size=10), command=self.solicitar)
        self.solicitar.place(x=510, y=25, width=90, height=35)

        self.anterior = Button(self, text="Anterior", font=Font(family="Roboto Cn", size=14))
        self.anterior.place(x=70, y=85, width=100, height=40)

        self.siguiente = Button(self, text="Siguiente", font=Font(family="Roboto Cn", size=14))
        self.siguiente.place(x=640, y=85, width=100, height=40)

        self.label_imagen = Label(self, bg="red")
        self.label_imagen.place(x=80, y=155, width=650 ,height=300)