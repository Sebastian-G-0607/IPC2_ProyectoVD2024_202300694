class Imagen:
    def __init__(self, id_solicitante, id, nombre, ruta):
        self.id_solicitante = id_solicitante
        self.id = id
        self.nombre = nombre
        self.ruta = ruta

    def __str__(self):
        return f'ID de solicitante: {self.id_solicitante}\\n' \
        f'ID de imagen: {self.id}\\n' \
        f'Nombre de la figura: {self.nombre}\\n' \
        f'Ruta de la imagen: {self.ruta}\\n' 