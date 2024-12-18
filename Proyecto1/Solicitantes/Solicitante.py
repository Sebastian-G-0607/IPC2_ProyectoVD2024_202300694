from UsuarioPadre.Usuario import Usuario
from Solicitantes.pila.pila_solicitante import pila_solicitante
from Solicitantes.lista_doble_circular.listaC_doble_solicitante import Lista_doble_circular

class Solicitante(Usuario):
    def __init__(self, id, pwd, nombre, correo, numero, direccion):
        super().__init__(id, pwd, nombre, correo, numero)
        self.direccion = direccion
        self.pilaUsuario = pila_solicitante()
        self.galeria = Lista_doble_circular()

    def __str__(self):
            return (f'ID: {self.id}\\n' \
            f'Password: {self.password}\\n' \
            f'Nombre: {self.nombre}\\n' \
            f'Correo: {self.correo}\\n' \
            f'Numero: {self.numero}\\n' \
            f'Dirección: {self.direccion}\\n')
