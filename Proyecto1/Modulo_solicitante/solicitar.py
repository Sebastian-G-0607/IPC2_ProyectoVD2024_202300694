import importlib
from tkinter import Button, Label, Tk, Frame, filedialog, messagebox
from tkinter.font import Font
import xml.etree.ElementTree as et
import io
from PIL import Image, ImageTk
from Imagen.Imagen import Imagen
from BBDD import BBDD

class Solicitante_solicitar(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=800, height=500)
        self.master = master
        self.master.resizable(False, False)
        self.pack()
        self.create_widgets()
    
    def leerArchivo(self):
        ruta = filedialog.askopenfile(title="Cargar archivo XML", filetypes=(('All files', '*.xml'),))
        return ruta

    def cargar_figura(self):
        ruta = self.leerArchivo()
        if ruta == '' or ruta == None:
            messagebox.showerror(title='Advertencia', message='Seleccione un archivo XML')
        else:
            try:
                arbol = et.parse(ruta)
                raiz = arbol.getroot()
                print(raiz.tag)
                id = None
                nombre = None
                if raiz.tag == 'figura': 
                    for etiqueta in raiz:
                        if etiqueta.tag == 'nombre':
                            id = etiqueta.attrib['id']
                            nombre = etiqueta.text
                            break
                    nuevaImagen = Imagen(BBDD.usuario_en_sesion, id, nombre, ruta.name)
                    BBDD.listaSolicitantes.buscar(BBDD.usuario_en_sesion).pilaUsuario.push(nuevaImagen)
            except:
                messagebox.showerror(title="Error", message="Ocurrió un error al cargar el archivo")

    def ver_pila(self):
        if len(BBDD.listaSolicitantes.buscar(BBDD.usuario_en_sesion).pilaUsuario) == 0:
            messagebox.showerror(title='Error', message='No existen solicitudes para mostrar')
        else:
            BBDD.listaSolicitantes.buscar(BBDD.usuario_en_sesion).pilaUsuario.graficar(BBDD.usuario_en_sesion)
            img = Image.open("Proyecto1/Reportes/Pila_" + BBDD.usuario_en_sesion + ".png")
            img_ajustada = img.resize((535, 300))
            img_renderizada = ImageTk.PhotoImage(img_ajustada)
            label_reporte.config(image=img_renderizada)
            label_reporte.image = img_renderizada
            label_reporte.place(x=220, y=130)
    
    def solicitar(self):
        cantidadPila = len(BBDD.listaSolicitantes.buscar(BBDD.usuario_en_sesion).pilaUsuario)
        for i in range(cantidadPila):
            nuevoSolicitud = BBDD.listaSolicitantes.buscar(BBDD.usuario_en_sesion).pilaUsuario.pop()
            BBDD.colaSolicitudes.enqueue(nuevoSolicitud)

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
    
    def ver_galeria(self):
        self.master.destroy()
        GaleriaClass = getattr(importlib.import_module('Modulo_solicitante.galeria'), 'Solicitante_galeria') 

        root = Tk()

        ancho_ventana = 800
        alto_ventana = 500

        x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)

        root.geometry(posicion)

        root.wm_title("Solicitante " + BBDD.usuario_en_sesion + " - Ver galería")
        app = GaleriaClass(root)

    def create_widgets(self):

        self.config(bg="white")

        self.CerrarSesion = Button(self, text="Cerrar sesión", font=Font(family="Roboto Cn", size=10), command=self.cerrarSesion)
        self.CerrarSesion.place(x=650, y=25, width=110, height=40)

        self.ver_galeria = Button(self, text="Ver galeria", font=Font(family="Roboto Cn", size=10), command=self.ver_galeria)
        self.ver_galeria.place(x=500, y=25, width=110, height=40)

        self.label_solicitar = Label(self, text="Solicitar", font=('Gotham', 24), bg="white")
        self.label_solicitar.place(x=45, y=50, height=50, width=170)

        self.cargar_figura = Button(self, text="Cargar figura", font=Font(family="Roboto Cn", size=12), command=self.cargar_figura)
        self.cargar_figura.place(x=70, y=120, width=110, height=40)

        self.solicitar = Button(self, text="Solicitar", font=Font(family="Roboto Cn", size=12), command=self.solicitar)
        self.solicitar.place(x=70, y=200, width=110, height=40)

        self.ver_pila = Button(self, text="Ver pila", font=Font(family="Roboto Cn", size=12), command=self.ver_pila)
        self.ver_pila.place(x=70, y=300, width=110, height=40)

        self.ver_lista = Button(self, text="Ver lista", font=Font(family="Roboto Cn", size=12))
        self.ver_lista.place(x=70, y=370, width=110, height=40)

        global label_reporte
        label_reporte = Label(self, bg="white")
        label_reporte.place(x=220, y=130, width=530, height=300)