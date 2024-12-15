class Imagen:
    def __init__(self, id_logueado, id, nombre, ruta):
        self.id_logueado = id_logueado
        self.id = id
        self.nombre = nombre
        self.ruta = ruta

    def __str__(self):
        return f'ID de solicitante: {self.id_logueado}\\n' \
        f'ID de imagen: {self.id}\\n' \
        f'Nombre de la figura: {self.nombre}\\n' \
        f'Ruta de la imagen: {self.ruta}\\n' 