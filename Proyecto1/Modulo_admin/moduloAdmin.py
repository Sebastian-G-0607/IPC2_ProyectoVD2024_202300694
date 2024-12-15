import importlib
from tkinter import Button, Label, Tk, Frame, filedialog, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
import xml.etree.ElementTree as et
from Artistas.Artista import Artista
from Solicitantes.Solicitante import Solicitante
from BBDD import BBDD

class Administrador(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=800, height=500)
        self.master = master
        self.master.resizable(False, False)
        self.pack()
        self.create_widgets()

    def leerArchivo(self):
        ruta = filedialog.askopenfile(title="Cargar archivo XML", filetypes=(('All files', '*.xml'),))
        return ruta

    def cargarArtistas(self):
        ruta = self.leerArchivo()
        if ruta == '' or ruta == None:
            messagebox.showerror(title='Advertencia', message='Seleccione un archivo XML')
        else:
            try:
                arbol = et.parse(ruta)
                raiz = arbol.getroot()

                if raiz.tag == 'Artistas':
                    for artista in raiz:
                        id = artista.attrib['id']
                        pwd = artista.attrib['pwd']
                        nombre = None
                        correo = None
                        numero = None
                        especialidades = None
                        notas = None

                        for atributo in artista:
                            match atributo.tag:
                                case 'NombreCompleto':
                                    nombre = atributo.text
                                case 'CorreoElectronico':
                                    correo = atributo.text
                                case 'NumeroTelefono':
                                    numero = atributo.text
                                case 'Especialidades':
                                    especialidades = atributo.text
                                case 'NotasAdicionales':
                                    notas = atributo.text

                        nuevoArtista = Artista(id, pwd, nombre, correo, numero, especialidades, notas)
                        BBDD.listaArtistas.insertar(nuevoArtista)

                    print("Recorriendo artistas")
                    BBDD.listaArtistas.recorrer()

                else:
                    messagebox.showerror(title='Advertencia', message='El formato del archivo no es válido')

            except:
                messagebox.showerror(title='Error', message='Ocurrió un error al leer el archivo')

    def cargarSolicitantes(self):
        ruta = self.leerArchivo()
        if ruta == '' or ruta == None:
            messagebox.showerror(title='Advertencia', message='Seleccione un archivo XML')
        else:
            try:
                arbol = et.parse(ruta)
                raiz = arbol.getroot()

                if raiz.tag == 'solicitantes':
                    for solicitante in raiz:
                        id = solicitante.attrib['id']
                        password = solicitante.attrib['pwd']
                        nombre = None
                        correo = None
                        numero = None
                        direccion = None
                        
                        for atributo in solicitante:
                            match atributo.tag:
                                case 'NombreCompleto':
                                    nombre = atributo.text
                                case 'CorreoElectronico':
                                    correo = atributo.text
                                case 'NumeroTelefono':
                                    numero = atributo.text
                                case 'Direccion':
                                    direccion = atributo.text
                        
                        nuevoSolicitante = Solicitante(id, password, nombre, correo, numero, direccion)
                        BBDD.listaSolicitantes.insertar(nuevoSolicitante)

                    print("Recorriendo solicitantes")
                    BBDD.listaSolicitantes.recorrer()

                else:
                    messagebox.showerror(title='Advertencia', message='El formato del archivo no es válido')
            except:
                messagebox.showerror(title='Error', message='Ocurrió un error al leer el archivo')

    def verSolicitantes(self):
        if len(BBDD.listaSolicitantes) == 0:
            messagebox.showerror(title='Error', message='No existen solicitantes para mostrar')
        else:
            BBDD.listaSolicitantes.graficar()
            img = Image.open("Proyecto1/Reportes/ListaSolicitantes.png")
            img_ajustada = img.resize((535, 300))
            img_renderizada = ImageTk.PhotoImage(img_ajustada)
            self.label_reporte = Label(self, image=img_renderizada)
            self.label_reporte.image = img_renderizada
            self.label_reporte.place(x=220, y=130)

    def verArtistas(self):
        if len(BBDD.listaArtistas) == 0:
            messagebox.showerror(title='Error', message='No existen artistas para mostrar')
        else:
            BBDD.listaArtistas.graficar()
            img = Image.open("Proyecto1/Reportes/ListaArtistas.png")
            img_ajustada = img.resize((535, 300))
            img_renderizada = ImageTk.PhotoImage(img_ajustada)
            self.label_reporte = Label(self, image=img_renderizada)
            self.label_reporte.image = img_renderizada
            self.label_reporte.place(x=220, y=130)

    def cerrarSesion(self):

        optn = messagebox.askokcancel(title="Salir", message="¿Desea cerrar sesión?")
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

        self.btn_cargarSolicitantes = Button(self, text="Cargar solicitantes", font=Font(family="Roboto Cn", size=12), command=self.cargarSolicitantes)
        self.btn_cargarSolicitantes.place(x=45, y=40, width=150, height=50)

        self.btn_cargarArtistas = Button(self, text="Cargar artistas", font=Font(family="Roboto Cn", size=12), command=self.cargarArtistas)
        self.btn_cargarArtistas.place(x=350, y=40, width=150, height=50)

        self.btn_verSolicitantes = Button(self, text="Ver solicitantes", font=Font(family="Roboto Cn", size=12), command=self.verSolicitantes)
        self.btn_verSolicitantes.place(x=45, y=160, width=150, height=50)

        self.btn_verArtistas = Button(self, text="Ver artistas", font=Font(family="Roboto Cn", size=12), command=self.verArtistas)
        self.btn_verArtistas.place(x=45, y=250, width=150, height=50)