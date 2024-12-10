from tkinter import Tk
from Login.Login import Login

root = Tk()

ancho_ventana = 700
alto_ventana = 370

x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2

posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)

root.geometry(posicion)

root.wm_title("Login")
app = Login(root)
app.mainloop()