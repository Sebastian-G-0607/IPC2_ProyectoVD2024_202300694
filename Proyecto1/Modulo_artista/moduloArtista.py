import importlib
from tkinter import Button, Label, Tk, Frame, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
from Modulo_artista.Matriz_dispersa.Matriz_dispersa import MatrizDispersa
import xml.etree.ElementTree as et
from Imagen.Imagen import Imagen
from BBDD import BBDD

class Artista(Frame):
    info_solicitante = None

    def __init__(self, master=None):

        super().__init__(master, width=800, height=500)
        self.master = master
        self.master.resizable(False, False)
        self.pack()
        self.create_widgets()

    def cerrarSesion(self):

        optn = messagebox.askokcancel(title="Salir", message="¿Desea cerrar sesión?")
        if optn == True:

            self.master.destroy()
            BBDD.usuario_en_sesion = ''

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

    def verCola(self):
        if len(BBDD.colaSolicitudes) == 0:
            messagebox.showerror(title='Avertencia', message='No existen solicitudes en la cola')
        else:
            BBDD.colaSolicitudes.graficar()
            img = Image.open("Proyecto1/Reportes/Cola.png")
            img_ajustada = img.resize((440, 300))
            img_renderizada = ImageTk.PhotoImage(img_ajustada)
            self.label_reporte = Label(self, image=img_renderizada)
            self.label_reporte.image = img_renderizada
            self.label_reporte.place(x=290, y=170)

    def aceptarSolicitud(self):
        if len(BBDD.colaSolicitudes) == 0:
            messagebox.showerror(title="Advertencia", message="Aun no existen solicitudes en la cola")
        else:
            imagen = BBDD.colaSolicitudes.dequeue()
            id_solcitante = imagen.id_solicitante
            grafica_matriz = MatrizDispersa()
            arbol = et.parse(imagen.ruta)
            root = arbol.getroot()
            nombre_figura = ''
            for elemento in root:
                if elemento.tag == 'disenio':
                    for pixel in elemento:
                        fila = int(pixel.attrib['fila'])
                        columna = int(pixel.attrib['col'])
                        color = pixel.text
                        grafica_matriz.insertar(fila,columna,color)
                elif elemento.tag == 'nombre':
                    nombre_figura = elemento.text

            ruta = grafica_matriz.graficar(imagen.id)
            nueva_imagen = Imagen(id_solcitante, imagen.id, nombre_figura, ruta)
            BBDD.listaSolicitantes.buscar(id_solcitante).galeria.insertar(nueva_imagen)
            BBDD.listaArtistas.buscar(BBDD.usuario_en_sesion).imagenes_procesadas.insertar(nueva_imagen)
            text = ''
            if BBDD.colaSolicitudes.getPrimero() != None:
                text = f'Solicitante: {BBDD.colaSolicitudes.getPrimero().id_solicitante}\nImagen: {BBDD.colaSolicitudes.getPrimero().nombre}'
            else:
                text = "No hay solicitudes en cola"
                img = Image.open("Proyecto1/Reportes/OcultarPila.png")
                img_ajustada = img.resize((440, 300))
                img_renderizada = ImageTk.PhotoImage(img_ajustada)
                self.label_reporte = Label(self, image=img_renderizada)
                self.label_reporte.image = img_renderizada
                self.label_reporte.place(x=290, y=170)
            self.info_solicitante.config(text=text)

    def verListaCircular(self):
        if len(BBDD.listaArtistas.buscar(BBDD.usuario_en_sesion).imagenes_procesadas) == 0:
            messagebox.showerror(title='Avertencia', message='No existen imágenes procesadas')
        else:
            BBDD.listaArtistas.buscar(BBDD.usuario_en_sesion).imagenes_procesadas.graficar(BBDD.usuario_en_sesion)
            img = Image.open("Proyecto1/Reportes/Procesadas_" + BBDD.usuario_en_sesion + '.png')
            img_ajustada = img.resize((440, 300))
            img_renderizada = ImageTk.PhotoImage(img_ajustada)
            self.label_reporte = Label(self, image=img_renderizada)
            self.label_reporte.image = img_renderizada
            self.label_reporte.place(x=290, y=170)

    def create_widgets(self):

        self.config(bg="white")

        self.CerrarSesion = Button(self, text="Cerrar sesión", font=Font(family="Roboto Cn", size=10), command=self.cerrarSesion)
        self.CerrarSesion.place(x=650, y=25, width=110, height=40)

        self.aceptar_solicitud = Button(self, text="Aceptar", font=Font(family="Roboto Cn", size=12), command=self.aceptarSolicitud)
        self.aceptar_solicitud.place(x=75, y=80, width=160, height=50)

        self.ver_cola = Button(self, text="Ver cola", font=Font(family="Roboto Cn", size=12), command=self.verCola)
        self.ver_cola.place(x=75, y=250, width=160, height=50)

        self.imagenes_solicitadas = Button(self, text="Imágenes solicitadas", font=Font(family="Roboto Cn", size=12), command=self.verListaCircular)
        self.imagenes_solicitadas.place(x=75, y=340, width=160, height=50)

        text = ''
        if BBDD.colaSolicitudes.getPrimero() != None:
            text = f'Solicitante: {BBDD.colaSolicitudes.getPrimero().id_solicitante}\nImagen: {BBDD.colaSolicitudes.getPrimero().nombre}'
        else: 
            text = "No hay solicitudes en cola"
        self.info_solicitante = Label(self, text=text, font=('Gotham', 18), anchor="w", bg="white")
        self.info_solicitante.place(x=300, y=70, width=300, height=90)

        self.label_reporte = Label(self, bg="white")
        self.label_reporte.place(x=290, y=170, width=440, height=300)