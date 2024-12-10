import importlib
from tkinter import Button, Label, Tk, Frame, filedialog, messagebox
from tkinter.font import Font
import xml.etree.ElementTree as et

class Administrador(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=800, height=500)
        self.master = master
        self.pack()
        self.create_widgets()

    def leerArchivo(self):
        ruta = filedialog.askopenfile(title="Cargar archivo XML", filetypes=(('All files', '*.xml'),))
        return ruta

    def cargarSolicitantes(self):
        ruta = self.leerArchivo()
        if ruta == '':
            messagebox.showerror(title='Advertencia', message='Seleccione un archivo XML')
        else:
            arbol = et.parse(ruta)
            raiz = arbol.getroot()
            print(raiz)
            print(type(raiz))
            if raiz.tag != 'solicitantes':
                messagebox.showerror(title='Error', message='El formato del archivo XML no es válido')
            else:
                messagebox.showinfo(title="Bien")


    def cargarArtistas(self):
        pass

    def cerrarSesion(self):

        optn = messagebox.askokcancel(title="Salir", message="¿Desea cerrar sesión?")
        print(optn)
        if optn == True:

            self.master.destroy()
            # LoginClass = importlib.import_module('Login')
            # print(v)

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

        self.btn_cargarSolicitantes = Button(self, text="Cargar solicitantes", font=Font(family="Roboto Cn", size=12), command=self.cargarSolicitantes)
        self.btn_cargarSolicitantes.place(x=80, y=40, width=150, height=50)

        self.btn_cargarArtistas = Button(self, text="Cargar artistas", font=Font(family="Roboto Cn", size=12))
        self.btn_cargarArtistas.place(x=350, y=40, width=150, height=50)

        self.btn_verSolicitantes = Button(self, text="Ver solicitantes", font=Font(family="Roboto Cn", size=12))
        self.btn_verSolicitantes.place(x=80, y=160, width=150, height=50)

        self.btn_verArtistas = Button(self, text="Ver artistas", font=Font(family="Roboto Cn", size=12))
        self.btn_verArtistas.place(x=80, y=250, width=150, height=50)