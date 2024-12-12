from tkinter import Tk, Button, Label, Entry, messagebox, Frame
from Modulo_admin.moduloAdmin import Administrador
from Modulo_solicitante.moduloSolicitante import Solicitante
from BBDD import BBDD

class Login(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=700, height=370)
        self.master = master
        self.master.resizable(False, False)
        self.pack()
        self.create_widgets()

    def iniciar_sesion(self):

        user = self.box_usuario.get()
        password = self.box_contrasenia.get()
        if user == 'AdminIPC' and password == 'ARTIPC2':
            BBDD.listaArtistas.recorrer()
            BBDD.listaSolicitantes.recorrer()
            self.master.destroy()

            root = Tk()

            ancho_ventana = 800
            alto_ventana = 500

            x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
            y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2

            posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)

            root.geometry(posicion)

            root.wm_title("Administrador")
            admin = Administrador(root)

        elif user == "0" and password == '0' :
            self.master.destroy()
            root = Tk()

            ancho_ventana = 800
            alto_ventana = 500

            x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
            y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2

            posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)

            root.geometry(posicion)

            root.wm_title("Solicitante")
            moduloSolicitante = Solicitante(root, 0)
        else:
            messagebox.showerror(message="El usuario o la contraseña son incorrectos, vuelva a intentar", title="Error")
    

    def create_widgets(self):

        self.config(bg="white")

        self.label = Label(self, text="Iniciar sesión", font=('Gotham', 24), bg="white")
        self.label.place(x=270, y=45, width=200, height=50) 

        self.label_usuario = Label(self, text="Ingrese su usuario:", font=('Gotham', 12), bg = "white")
        self.label_usuario.place(x=15, y=120, width=300, height=50)

        self.label_contrasenia = Label(self, text="Ingrese su contraseña:", font=('Gotham', 12), bg = "white")
        self.label_contrasenia.place(x=18, y=190, width=300, height=50)

        self.box_usuario = Entry(self)
        self.box_usuario.place(x=250, y=130, width=360, height=30)

        self.box_contrasenia = Entry(self)
        self.box_contrasenia.place(x=270, y=200, width=340, height=30)

        self.boton_iniciar = Button(self, text="Iniciar sesión", command=self.iniciar_sesion)
        self.boton_iniciar.place(x=305, y=275, width=110, height=35)