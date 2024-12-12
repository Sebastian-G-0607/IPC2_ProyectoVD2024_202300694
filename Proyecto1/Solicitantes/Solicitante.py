class Solicitante:
    def __init__(self, id, pwd, nombre, correo, numero, direccion):
        self.id = id
        self.pwd = pwd
        self.nombre = nombre
        self.correo = correo
        self.numero = numero
        self.direccion = direccion
        # self.galeria

    def __str__(self):
            return f'ID: {self.id}\\n' \
            f'Password: {self.pwd}\\n' \
            f'Nombre: {self.nombre}\\n' \
            f'Correo: {self.correo}\\n' \
            f'Numero: {self.numero}\\n' \
            f'Dirección: {self.direccion}\\n'