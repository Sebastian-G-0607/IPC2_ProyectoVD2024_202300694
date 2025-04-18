from UsuarioPadre.Usuario import Usuario
from Artistas.listaC_artista.listaCircularArtista import ListaCircular

class Artista(Usuario):
    def __init__(self, id, pwd, nombre, correo, numero, especialidades, notas):
        super().__init__(id, pwd, nombre, correo, numero)
        self.especialidades = especialidades
        self.notas = notas
        self.imagenes_procesadas = ListaCircular()

    def __str__(self):
        return f'ID: {self.id}\\n' \
            f'Password: {self.password}\\n' \
            f'Nombre: {self.nombre}\\n' \
            f'Correo: {self.correo}\\n' \
            f'Numero: {self.numero}\\n' \
            f'Especialidades: {self.especialidades}\\n' \
            f'Notas adicionales: {self.notas}\\n'
