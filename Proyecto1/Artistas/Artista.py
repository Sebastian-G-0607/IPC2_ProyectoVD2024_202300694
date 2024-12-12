class Artista:
    def __init__(self, id, pwd, nombre, correo, numero, especialidades, notas):
        self.id = id
        self.pwd = pwd
        self.nombre = nombre
        self.correo = correo
        self.numero = numero
        self.especialidades = especialidades
        self.notas = notas

    def __str__(self):
        return f'ID: {self.id}\\n' \
            f'Password: {self.pwd}\\n' \
            f'Nombre: {self.nombre}\\n' \
            f'Correo: {self.correo}\\n' \
            f'Numero: {self.numero}\\n' \
            f'Especialidades: {self.especialidades}\\n' \
            f'Notas adicionales: {self.notas}\\n'
