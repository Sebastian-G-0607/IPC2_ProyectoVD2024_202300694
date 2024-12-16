import importlib
from tkinter import Button, Label, Tk, Frame, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
from BBDD import BBDD

class Solicitante_galeria(Frame):

    id_imagen = None
    label_imagen = None

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

    def siguiente(self):
        self.id_imagen = BBDD.listaSolicitantes.buscar(BBDD.usuario_en_sesion).galeria.obtenerSiguiente(self.id_imagen).id
        img = Image.open("Proyecto1/Reportes/Matriz_" + self.id_imagen + ".png")
        img_ajustada = img.resize((650, 300))
        img_renderizada = ImageTk.PhotoImage(img_ajustada)
        self.label_imagen.config(image=img_renderizada)
        self.label_imagen.image = img_renderizada
        self.label_imagen.place(x=80, y=155)

    def anterior(self):
        self.id_imagen = BBDD.listaSolicitantes.buscar(BBDD.usuario_en_sesion).galeria.obtenerAnterior(self.id_imagen).id
        img = Image.open("Proyecto1/Reportes/Matriz_" + self.id_imagen + ".png")
        img_ajustada = img.resize((650, 300))
        img_renderizada = ImageTk.PhotoImage(img_ajustada)
        self.label_imagen.config(image=img_renderizada)
        self.label_imagen.image = img_renderizada
        self.label_imagen.place(x=80, y=155)

    def create_widgets(self):

        self.config(bg="white")

        self.CerrarSesion = Button(self, text="Cerrar sesión", font=Font(family="Roboto Cn", size=10), command=self.cerrarSesion)
        self.CerrarSesion.place(x=650, y=25, width=90, height=30)

        self.solicitar = Button(self, text="Solicitar", font=Font(family="Roboto Cn", size=10), command=self.solicitar)
        self.solicitar.place(x=510, y=25, width=90, height=35)

        self.anterior_btn = Button(self, text="Anterior", font=Font(family="Roboto Cn", size=14), command=self.anterior)
        self.anterior_btn.place(x=70, y=85, width=100, height=40)

        self.siguiente_btn = Button(self, text="Siguiente", font=Font(family="Roboto Cn", size=14), command=self.siguiente)
        self.siguiente_btn.place(x=640, y=85, width=100, height=40)

        self.id_imagen = BBDD.listaSolicitantes.buscar(BBDD.usuario_en_sesion).galeria.getPrimero().dato.id

        img = Image.open("Proyecto1/Reportes/Matriz_" + self.id_imagen + ".png")
        img_ajustada = img.resize((650, 300))
        img_renderizada = ImageTk.PhotoImage(img_ajustada)
        self.label_imagen = Label(self, image=img_renderizada)
        self.label_imagen.image = img_renderizada
        self.label_imagen.place(x=80, y=155)
