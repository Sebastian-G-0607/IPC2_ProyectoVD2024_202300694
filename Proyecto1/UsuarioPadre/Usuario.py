class Usuario:
    def __init__(self, id, pwd, nombre, correo, numero):
        self.id = id
        self.password = pwd
        self.nombre = nombre
        self.correo = correo
        self.numero = numero

    def __str__(self):
            return f'ID: {self.id}\\n' \
            f'Password: {self.password}\\n' \
            f'Nombre: {self.nombre}\\n' \
            f'Correo: {self.correo}\\n'